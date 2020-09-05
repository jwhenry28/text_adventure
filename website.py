from flask import Flask, request, render_template
from website_utils.utils import HistoryNode, create_node

app = Flask(__name__)
history = []


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)