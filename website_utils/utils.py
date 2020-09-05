class HistoryNode:
    def __init__(self, orig_text, message):
        self.orig_text = orig_text
        self.message = message


# Take text, input it into program, then create node with the output
def add_node(text):
    return