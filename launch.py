import sys
from flask import Flask, request, render_template
from website_utils.utils import server_context, server_print
from game import local_game, server_game
import threading

app = Flask(__name__)


if len(sys.argv) != 2:
    print("For the time being, you must specify a debug mode or not.")
    sys.exit(1)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST' and request.form:
        server_context.append_to_history('input', request.form['input'])
        server_context.set_message(request.form['input'])

        # Make sure the server history is completely up to date
        server_context.html_barrier.wait()
    return render_template('game.html', context=server_context)


server_context.set_mode(sys.argv[1])
if sys.argv[1] == 'local':
    local_game()
elif sys.argv[1] == 'server':
    if __name__ == '__main__':
        application_thread = threading.Thread(target=server_game)
        application_thread.start()

        app.run(debug=True)
else:
    print("I didn't understand that mode. Mode must be local or server.")
    sys.exit(-1)
