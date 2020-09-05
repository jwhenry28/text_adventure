class HistoryNode:
    def __init__(self, command, description):
        self.command = command
        self.description = description


def create_node(command):
    if command == 'barn':
        node = HistoryNode(command, "An old barn")
    elif command == 'field':
        node = HistoryNode(command, "An old field")
    elif command == 'house':
        node = HistoryNode(command, "A beautiful house")
    else:
        node = HistoryNode(command, "I don't know")

    return node