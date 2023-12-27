import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains

# Creating driver instance and launch lichess.org website.
# preparing 'wait' variable for clicking on buttons.
# It will be used later for waiting until objects starts to be clickable.
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("https://lichess.org/")

'''Clicks on button depending on XPATH'''
def click_on_button(xpath):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    button.click()

'''Finds an element in which data can be entered by XPATH and input the data on it.'''
def input_data(xpath, data):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    button.send_keys(data)

'''Registration on lichess.org'''
def registration(login, password):
    click_on_button("//header[@id='top']/div[@class='site-buttons']/a[@class='signin button button-empty']")
    time.sleep(0.5)
    input_data("//div[@id='main-wrap']/main[@class='auth auth-login box box-pad']/form[@class='form3']/div[@class='one-factor']/div[@class='form-group'][1]/input[@id='form3-username']", login)
    time.sleep(0.5)
    input_data("//div[@id='main-wrap']/main[@class='auth auth-login box box-pad']/form[@class='form3']/div[@class='one-factor']/div[@class='form-group'][2]/input[@id='form3-password']", password)
    time.sleep(0.5)
    click_on_button("//div[@id='main-wrap']/main[@class='auth auth-login box box-pad']/form[@class='form3']/div[@class='one-factor']/button[@class='submit button']")

# difficulty of an engine (5 is the best competitor)
engine_level = 5
'''Pushes some different buttons to start a game with computer'''
def start_playing_with_computer():
    click_on_button("//div[@id='main-wrap']"
                    "/main[@class='lobby']"
                    "/div[@class='lobby__table']"
                    "/div[@class='lobby__start']"
                    "/button[@class='button button-metal config_ai']")

    click_on_button("//div[@id='main-wrap']"
                    "/main[@class='lobby']"
                    "/div[@class='lobby__table']"
                    "/div[@id='modal-overlay']"
                    "/div[@id='modal-wrap']"
                    "/div/div[@class='setup-content']"
                    "/div[@class='level buttons']"
                    "/div[@class='config_level']"
                    "/group[@class='radio']/div[4]/label")

    click_on_button("//main[@class='lobby']"
                    "/div[@class='lobby__table']"
                    "/div[@id='modal-overlay']"
                    "/div[@id='modal-wrap']"
                    "/div/div[@class='setup-content']"
                    "/div[@class='color-submits']"
                    "/button[@class='button button-metal color-submits__button random']/i")


'''Pushes some different buttons to start a game with real people
 (you can be banned due to the rules of Lichess, do not use it without necessity)'''
def start_playing_with_people():
    click_on_button("//div[@id='main-wrap']/main[@class='lobby']/div[@class='lobby__app lobby__app-pools']/div[@class='lobby__app__content lpools']/div[7]/div[@class='clock']")

'''Detects your color (black or white)'''
def detect_color():
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main-wrap']"
                                                         "/main[@class='round']"
                                                         "/div[@class='round__app variant-standard']"
                                                         "/div[@class='round__app__board main-board']"
                                                         "/div[@class='cg-wrap orientation-white manipulable']"
                                                         "/cg-container/cg-board")))
        return 'white'

    except TimeoutException:
        return 'black'

'''Returns last move on the board'''
def last_move(color):
    html = requests.get(driver.current_url).text
    soup = bs(html, 'html.parser')
    cg_board = soup.find('cg-board')
    last_move_squares = cg_board.findAll(class_='last-move')
    last = ''
    for square in last_move_squares:
        x, y = square['style'].replace('top:', '').replace('left:', '').replace('%', '').split(sep=';')
        x, y = float(x) / 12.5, float(y) / 12.5
        x = 7 - x
        from_num_to_file = 'abcdefgh'
        last += from_num_to_file[int(y)] + str(int(x + 1))
    return last

'''Returns coordinates of a square on browser depending on algebraic notation (e.g. e2e4, f7f8Q)'''
def coordinates_of_a_square(square, color):
    alphabet = 'abcdefgh'
    board_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='main-wrap']"
                                                                     "/main[@class='round']"
                                                                     "/div[@class='round__app variant-standard']"
                                                                     "/div[@class='round__app__board main-board']"
                                                                     "/div[@class='cg-wrap orientation-" + color + " manipulable']"
                                                                                                                   "/cg-container/cg-board")))
    square_size, x0, y0 = board_element.size['height'] / 8, board_element.location['x'], board_element.location['y']
    rank, file = 7 - (int(square[1]) - 1),  alphabet.find(square[0])
    if color == 'black':
        rank, file = 7-rank, 7 - file
    return x0 + square_size * (file + 0.5), y0 + square_size * (rank + 0.5)


'''Moving a piece on a browser. Also supports promotions and castlings'''
def make_move(move, color):
    source = move[:2]
    target = move[2:4]
    promotion = move[4:]
    source_square = coordinates_of_a_square(source, color)
    target_square = coordinates_of_a_square(target, color)
    action_chains = ActionChains(driver)
    action_chains.move_by_offset(source_square[0], source_square[1]).click().perform()
    action_chains.move_by_offset(-source_square[0], -source_square[1]).perform()
    action_chains.move_by_offset(target_square[0], target_square[1]).click().perform()
    action_chains.move_by_offset(-target_square[0], -target_square[1]).perform()
    promotion_coord = ''
    if promotion == 'q' or promotion == 'Q':
        promotion_coord = target
    elif promotion == 'n' or promotion == 'N':
        promotion_coord = target[0] + ('7' if color == 'white' else '2')
    elif promotion == 'r' or promotion == 'R':
        promotion_coord = target[0] + ('6' if color == 'white' else '3')
    elif promotion == 'b' or promotion == 'B':
        promotion_coord = target[0] + ('5' if color == 'white' else '4')
    if len(promotion_coord) > 0:
        promotion_square = coordinates_of_a_square(promotion_coord, color)
        action_chains.move_by_offset(promotion_square[0], promotion_square[1]).click().perform()
        action_chains.move_by_offset(-promotion_square[0], -promotion_square[1]).perform()
