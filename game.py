import time, sys
from classes.parser import regex_imperative
from classes.handlers import route_imperative
from classes.context import gen_context
from website_utils.utils import my_print, my_input, server_context


context = gen_context(sys.argv[1])


# Meant for playing on console - really just to easily design & debug
def local_game():
    context.map[context.current_loc].print_surroundings()

    # Game loop
    while True:
        # Gather input from player
        command = input("> ")
        imp = regex_imperative(context, command)

        # Route imperative if something was given
        if imp:
            route_imperative(imp, context)
            print('')
        else:
            my_print("des", "I beg your pardon?")
            print('')


# Game for the webserver
def server_game():
    context.map[context.current_loc].print_surroundings()

    # Game loop
    while True:
        # Gather input from server
        my_print("des", "")  # one newline
        command = my_input("> ")
        imp = regex_imperative(context, command)

        # Route imperative if something was given
        if imp:
            route_imperative(imp, context)

            # Update server context metainfo
            server_context.current_loc = context.map[context.current_loc].brief
            server_context.moves += 1
        else:
            my_print("des", "I beg your pardon?")

        # Break the barrier so the html file can be rendered properly
        server_context.html_barrier.wait()
