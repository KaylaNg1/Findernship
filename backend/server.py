from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from jobScraper import *

app = Flask(__name__, static_folder = '../frontend/public')
CORS(app)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/getData', methods=['GET'])
def upload_file():
    print("in GET endpoint")
    data = jobScraper()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host = 'localhost', port = 8000) # run on part 3000