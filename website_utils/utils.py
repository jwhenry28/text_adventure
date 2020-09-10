import queue
import threading


class HistoryNode:
    def __init__(self, node_type, message):
        self.node_type = node_type
        self.message = message


class ServerContext:
    def __init__(self):
        self.current_loc = 'Cornfield South'  # Set up beginning
        self.history = []
        self.moves = 0
        self.score = 0
        self.mode = ''  # Mode will always be manually specified by command line arg
        self.pipeline = queue.Queue(maxsize=10)
        self.html_barrier = threading.Barrier(2)

    def get_message(self):
        value = self.pipeline.get()
        return value

    def set_message(self, value):
        self.pipeline.put(value)

    def set_mode(self, mode):
        self.mode = mode

    def print(self):
        print("LOCATION    : " + self.current_loc)
        print("MOVES       :", self.moves)
        print("SCORE       :", self.score)
        for item in self.history:
            print("NODE_TYPE: " + item.node_type)
            print("MESSAGE  : " + item.message)

    def append_to_history(self, node_type, message):
        new_node = HistoryNode(node_type, message)
        self.history.append(new_node)


server_context = ServerContext()


# Takes output from game and puts it into a history node
def server_print(node_type, *strings):
    complete_msg = ""
    for string in strings:
        complete_msg += string + " "

    server_context.append_to_history(node_type, complete_msg)


# Prints to either console or webpage depending on what mode is run
def my_print(node_type, *argv):
    # Append full string
    complete_msg = ''
    for item in argv:
        complete_msg += str(item) + ' '

    logs = ["crit", "err", "log"]
    log_tags = {'crit': '[CRITICAL]', 'err': '[ERROR]   ', 'log': '[INFO]    '}

    # Console if local
    if server_context.mode == 'local':
        if node_type in logs:
            log_tag = log_tags[node_type]
            print("- {} ----- {}".format(log_tag, complete_msg))
        else:
            print(complete_msg)

    # Webpage if server - also print logs (only for server)
    elif server_context.mode == 'server':
        if node_type in logs:
            log_tag = log_tags[node_type]
            print("- {} ----- {}".format(log_tag, complete_msg))
        else:
            server_print(node_type, complete_msg)


def my_input(msg):
    if server_context.mode == 'local':
        command = input(msg)
        return command

    else:
        # Only print if it's a clarification message; "> " is included in the html
        if msg != "> ":
            my_print("des", msg)
            server_context.html_barrier.wait()
        command = server_context.get_message()
        return command
