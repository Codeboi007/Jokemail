from flask import Flask, jsonify
import requests
import schedule
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Email Configuration
FROM_EMAIL = "sender_email"
TO_EMAIL = "receipient_email"
EMAIL_PASSWORD = "App-specific password"  
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Fetch a joke from the API
def get_joke():
    url = "https://v2.jokeapi.dev/joke/Dark"
    response = requests.get(url)
    data = response.json()
    
    if data["type"] == "single":
        joke = data["joke"]
    else:
        joke = f"{data['setup']} - {data['delivery']}"
    
    return joke

# Function to send an email
def send_email():
    joke = get_joke()
    
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = "Your Daily Joke"
    
    body = f"Here's your daily joke:\n\n{joke}"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"


@app.route("/send-email")
def trigger_email():
    response = send_email()
    return jsonify({"message": response})

# Function to run the scheduler in the background
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check the schedule every minute

# Schedule the email to be sent at 8:00 AM daily
schedule.every().day.at("08:00").do(send_email)

# Seperate thread to allow flask and mail to run at the same time
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Flask Route to Show the Latest Joke
@app.route("/")
def home():
    joke = get_joke()
    return joke

if __name__ == "__main__":
    app.run(debug=True)
