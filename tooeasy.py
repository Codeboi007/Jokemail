from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    url = "https://v2.jokeapi.dev/joke/Programming"
    response = requests.get(url)
    data = response.json()
    
    if data["type"] == "single":
        joke = data["joke"]
    else:
        joke = f"{data['setup']} - {data['delivery']}"
    
    return joke

if __name__ == "__main__":
    app.run(debug=True)
