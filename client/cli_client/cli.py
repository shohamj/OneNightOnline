import socketio
import time

DELAY = 0.1

sio = socketio.Client()

room_id = None
last_input = ""
should_reprint = False


def input_with_save(input_message):
    global last_input, should_reprint
    last_input = input_message
    should_reprint = True
    user_input = input(input_message)
    should_reprint = False
    return user_input


def print_keep_input(*args):
    global last_input
    if should_reprint:
        print('\r', end='')
        print(*args)
        print(last_input, end='')
    else:
        print(*args)


@sio.event
def message(data):
    print_keep_input(data["message"])


@sio.event
def error(data):
    print_keep_input('ERROR:', data)


@sio.event
def player_created(data):
    print_keep_input('Player', data["name"], 'created')


@sio.event
def room_created(data):
    global room_id
    print_keep_input('Room Created!', data)
    room_id = data["room_id"]


@sio.event
def player_joined(data):
    print_keep_input("Player", data["name"], "has joined the room")


@sio.event
def player_left(data):
    print_keep_input("Player", data["name"], "has left the room")


@sio.event
def game_started(data):
    print_keep_input("The game has started!")


def connect():
    print("Connecting to server")
    sio.connect('http://localhost:8080')
    time.sleep(DELAY)


def create_player():
    print("Creating player")
    selected_name = input_with_save("Choose name: ")
    sio.emit("create_player", {"name": selected_name})
    time.sleep(DELAY)


def choose_room():
    print("1: Create new room\n2: Join room")
    room_choice = input_with_save("Your choice: ")
    if room_choice == "1":
        add_room()
        start_game()
    else:
        join_room()


def join_room():
    id = input_with_save("Room ID: ")
    sio.emit("join_room", {"room_id": id})
    time.sleep(DELAY)


def add_room():
    print("Adding room")
    sio.emit("add_room", {"cards": ["alien"] * 5})
    time.sleep(DELAY)


def start_game():
    input_with_save("Press Enter to start: ")
    sio.emit("start_game", {})


def main():
    connect()
    create_player()
    choose_room()
