from gui_element import *
from gui_control import *
from game_table import *
from play_engine import *
from pokers.junior import Junior
from pokers.calculator import Calculator
import time
import sys
import logging
import argparse
import os
from multiprocessing import Process, Queue


log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_filename = os.path.join(log_dir, 'auto_poker_%s.log' % time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time())))
logging.basicConfig(level = logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%a, %d %b %Y %H:%M:%S',
    filename = log_filename,
    filemode = 'w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def start_play_engine(queue, engine_code, max_players, window_rect, table_rect, poker_code):
    table = GameTable(max_players, table_rect, queue)
    if poker_code == 'junior':
        poker = Junior()
    elif poker_code == 'calculator':
        poker = Calculator()
    engine = PlayEngine(engine_code, window_rect, table, poker, log_dir)
    engine.play()

def main(max_players, poker):
    game_processes = []
    queue = Queue()
    window_rects = find_all_in_screen(WINDOW_TOP_LEFT)
    for window_rect in window_rects:
        window_rect.h = WINDOW_HEIGHT
        window_rect.w = WINDOW_WIDTH
        logging.info("Game window found: %s" % window_rect.to_string())
        engine_code = '%dX%d' % (window_rect.x, window_rect.y)

        table_rect = find_in_rect(TABLE_TOP_LEFT, window_rect)
        if table_rect is None:
            logging.warn("There is no game table in window.")
            continue
        table_rect.h = TABLE_HEIGHT
        table_rect.w = TABLE_WIDTH
        logging.info("Game table found in window: %s" % table_rect.to_string())
        process = Process(target=start_play_engine, args=(queue, engine_code, max_players, window_rect, table_rect, poker))
        process.start()
        game_processes.append(process)
    # Get action from queue
    while True:
        try:
            gui_action = queue.get(timeout=2)
            if gui_action[0] == 'click':
                click_in_rect(gui_action[1], gui_action[2])
                time.sleep(0.5)
            else:
                logging.error("Invalid GUI action: %s" % gui_action[0])
        except:
            continue

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_players', required=True, type=int, help='The max number of players in one table: 6 or 9')
    parser.add_argument('--poker', required=True, help='The AI poker: junior, calculator.')
    args = parser.parse_args()
    main(args.max_players, args.poker)
