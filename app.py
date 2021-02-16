# app.py
import chess_core
import chess
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/nextmove/', methods=['POST'])
def post_something():
    param = request.form.get('fen')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "move": chess_core.minimax_input(chess.Board(param),4)
        })
    else:
        return jsonify({
            "ERROR": "no fen found"
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server!!</h1>\nYou can get the next move at /nextmove"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=443)