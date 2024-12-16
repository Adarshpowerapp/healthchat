from flask import Flask, request, jsonify, render_template, redirect, flash, url_for, session
import pandas as pd

# Load the dataset
file_path = 'medquad.csv'  # Replace with the correct path if necessary
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found. Make sure the path is correct.")
    exit()

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# In-memory "database" for user credentials
users = {}

# Function to get the chatbot response
def get_response_from_data(user_input):
    try:
        # Perform exact or case-insensitive matching in 'question' column
        matched_row = data[data['question'].str.lower() == user_input.lower()]
        if not matched_row.empty:
            return matched_row.iloc[0]['answer']
        else:
            return "Sorry, I don't know the answer to that question."
    except Exception as e:
        return f"Error: {e}"

# Redirect to login by default
@app.route('/')
def default():
    return redirect('/login')

# Sign Up Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        if username in users:
            flash("Username already exists! Please choose another one.", "error")
            return redirect('/signup')
        
        # Add new user to the "database"
        users[username] = password
        flash("Sign-up successful! You can now log in.", "success")
        return redirect('/login')
    
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists and the password matches
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            flash("Login successful!", "success")
            return redirect('/home')  # Redirect to home page after login
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect('/login')
    
    return render_template('login.html')

# Home Route (after login)
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    flash("You need to log in first!", "error")
    return redirect('/login')

# Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear session data to logout
    flash("You have been logged out.", "success")
    return redirect('/login')

# Chat Route for chatbot functionality
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message')
    if user_message:
        print(f"Received message: {user_message}")  # Debugging log
        chatbot_response = get_response_from_data(user_message)
        print(f"Generated response: {chatbot_response}")  # Debugging log
        return jsonify({'response': chatbot_response})
    return jsonify({'response': 'Please type a message!'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

