from flask import Flask, jsonify

app = Flask(__name__)

@app.get('/login')
def login():
    return jsonify({"status": "Success", "message": "You are logged in!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)