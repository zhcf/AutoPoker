import sys; print('Python %s on %s' % (sys.version, sys.platform))
#sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])
import org.sikuli.script.SikulixForJython
import logging
from sikuli import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

WINDOW_TOP_LEFT = 'images/window_top_left.png'
WINDOW_WIDTH = 792
WINDOW_HEIGHT = 577
TABLE_TOP_LEFT = 'images/table_top_left.png'
TABLE_WIDTH = 792
TABLE_HEIGHT = 547
MARGIN = 20
ACTION_RAISE_TO = 'images/action_raise_to.png'
ACTION_HEIGHT = 41

Settings.OcrTextSearch = True
Settings.OcrTextRead = True

screen = Screen()

try:
    match = screen.find(WINDOW_TOP_LEFT)
    logging.debug(match)
    window_region = Region(x = match.getX() - MARGIN,
        y = match.getY() - MARGIN,
        w = WINDOW_WIDTH + MARGIN * 2,
        h = WINDOW_HEIGHT + MARGIN * 2)
    window_region.initScreen(screen)
    logging.info("Find PokerStars Window")
except FindFailed:
    logging.error("Can't find PokerStars window")
    sys.exit(99)

try:
    match = window_region.find(TABLE_TOP_LEFT)
    logging.debug(match)
    table_region = Region(x = match.getX() - MARGIN,
        y = match.getY() - MARGIN,
        w = TABLE_WIDTH + MARGIN * 2,
        h = TABLE_HEIGHT + MARGIN * 2)
    table_region.initScreen(screen)
    logging.info("Find PokerStars Game Table")
except FindFailed:
    logging.error("Can't find game table")
    sys.exit(99)

try:
    match = table_region.find(ACTION_RAISE_TO)
    logging.debug(match)
    amount_region = Region(x = match.getX(),
        y = match.getY() + match.getH(),
        w = match.getW(),
        h = ACTION_HEIGHT - match.getH())
    amount_region.initScreen(screen)
    amount = amount_region.collectWords()
    print amount
except FindFailed:
    logging.error("Can't find raise-to action")
    sys.exit(99)
