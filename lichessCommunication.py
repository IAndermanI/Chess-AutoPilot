from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


def click_on_button(xpath):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    button.click()

def start_playing():
    driver.get("https://lichess.org/")
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
                    "/group[@class='radio']/div[5]/label")

    click_on_button("//main[@class='lobby']"
                    "/div[@class='lobby__table']"
                    "/div[@id='modal-overlay']"
                    "/div[@id='modal-wrap']"
                    "/div/div[@class='setup-content']"
                    "/div[@class='color-submits']"
                    "/button[@class='button button-metal color-submits__button random']/i")


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


def last_move():
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



def make_move(move, color):
    source = move[:2]
    target = move[2:]
    promotion = ''
    if len(target) > 2:
        target = target[:2]
        promotion = target[2:]
    source_square = coordinates_of_a_square(source, color)
    target_square = coordinates_of_a_square(target, color)
    action_chains = ActionChains(driver)
    action_chains.move_by_offset(source_square[0], source_square[1]).click().perform()
    action_chains.move_by_offset(-source_square[0], -source_square[1]).perform()
    action_chains.move_by_offset(target_square[0], target_square[1]).click().perform()
    action_chains.move_by_offset(-target_square[0], -target_square[1]).perform()
