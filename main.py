import time
import lichessCommunication as LC
import client
# Down below, I commented 2 lines with registration because it is rudimentary
# for you, but for me, it is the only chance to analyse the games. That's why
# I added it.

# from personalData import login, password
# LC.registration(login, password)

# Connection to connector.txt file and launch of a game.
file_path = client.get_connector_path()
LC.start_playing_with_people()
color = LC.detect_color()
client.load_to_file(file_path, color)

# Some variables that are necessary for future infinite loop.
prev_move = ''
move_color = 'white'

# An infinite loop
while True:
    # Checking the last move
    cur_move = LC.last_move(color)[:4]
    # If it is castling, changes the notation
    # (there are a couple of them by some reason)
    if (cur_move == 'e1h1' and prev_move == 'e1g1')\
            or (cur_move == 'e8h8' and prev_move == 'e8g8')\
            or (cur_move == 'e1a1' and prev_move == 'e1c1')\
            or (cur_move == 'e8a8' and prev_move == 'e8c8'):
        cur_move = prev_move
    # if it is our move, connection to the engine and waiting for the answer.
    if move_color == color:
        move = ''
        while move == '':
            move = client.read_from_file(file_path)
            move = move.replace(' ', '')
        LC.make_move(move, color)
        prev_move = move
        move_color = 'black' if move_color == 'white' else 'white'
    # if an opponent did a move
    else:
        if prev_move != cur_move:
            client.load_to_file(file_path, cur_move)
            prev_move = cur_move
            move_color = 'black' if move_color == 'white' else 'white'
    # not to make moves instantly
    time.sleep(0.1)

