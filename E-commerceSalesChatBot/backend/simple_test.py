from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:5174'])

@app.route('/')
def hello():
    return jsonify({'message': 'Backend server is running!', 'status': 'success'})

@app.route('/api/test')
def test():
    return jsonify({'message': 'API is working!', 'status': 'success'})

if __name__ == '__main__':
    print("Starting simple Flask server...")
    print("Server will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
