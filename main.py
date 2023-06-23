import time
import lichessCommunication as LC
import client

file_path = client.get_connector_path()
LC.start_playing()
color = LC.detect_color()

client.load_to_file(file_path, color)

prev_move = ''
move_color = 'white'

while True:
    cur_move = LC.last_move()
    if move_color == color:
        move = ''
        while move == '':
            move = client.read_from_file(file_path)
            move = move.replace(' ', '')
        LC.make_move(move, color)
        prev_move = move
        move_color = 'black' if move_color == 'white' else 'white'
    else:
        if prev_move != cur_move:
            client.load_to_file(file_path, cur_move)
            prev_move = cur_move
            move_color = 'black' if move_color == 'white' else 'white'
    time.sleep(0.1)

