from jpype import *
from PIL import Image
from functools import reduce
import operator
import logging
import pytesseract
import math

# JRE_PATH = r'C:\Java\jre1.8.0_111\bin\server\jvm.dll'
# SIKULI_PATH = r'D:\projects\AutoPoker\sikulixapi.jar'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
JRE_PATH = r'C:\Program Files\Java\jre1.8.0_191\bin\server\jvm.dll'
SIKULI_PATH = r'D:\AutoPoker\sikulixapi.jar'

startJVM(JRE_PATH, '-XX:MaxHeapSize=512m', '-Djava.class.path=%s' % SIKULI_PATH)

Screen = JClass('org.sikuli.script.Screen')
Region = JClass('org.sikuli.script.Region')
FindFailed = JException(JClass('org.sikuli.script.FindFailed'))

g_screen = Screen()

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_string(self):
        return ("[%d, %d, %d, %d]" % (self.x, self.y, self.w, self.h))


def find_in_screen(image_filename):
    global g_screen
    try:
        match = g_screen.find(image_filename)
        return Rect(match.getX(), match.getY(), match.getW(), match.getH())
    except FindFailed:
        logging.error("Can't find %s on screen." % image_filename)
        return None

def find_in_rect(image_filename, rect):
    global g_screen
    MARGIN = 20
    try:
        region = Region(rect.x - MARGIN,
            rect.y - MARGIN,
            rect.w + MARGIN * 2,
            rect.h + MARGIN *2)
        region.initScreen(g_screen)
        match = region.find(image_filename)
        return Rect(match.getX(), match.getY(), match.getW(), match.getH())
    except FindFailed:
        logging.error("Can't find %s on %s." % (image_filename, rect.to_string()))
        return None

def find_all_in_rect(image_filename, rect):
    global g_screen
    MARGIN = 20
    try:
        region = Region(rect.x - MARGIN,
            rect.y - MARGIN,
            rect.w + MARGIN * 2,
            rect.h + MARGIN *2)
        region.initScreen(g_screen)
        match_iter = region.findAll(image_filename)
        result = []
        while match_iter.hasNext():
            match = match_iter.next()
            result.append(Rect(match.getX(), match.getY(), match.getW(), match.getH()))
        return result
    except FindFailed:
        logging.error("Can't find %s on %s." % (image_filename, rect.to_string()))
        return []

def get_string_from_rect(rect):
    global g_screen
    region = Region(rect.x, rect.y, rect.w, rect.h)
    region.initScreen(g_screen)
    image_file = g_screen.capture(region).getFile()
    # The OCR min height is 30
    MIN_OCR_HEIGHT = 27
    if rect.h < MIN_OCR_HEIGHT:
        image = Image.open(image_file)
        image = image.convert('L')
        rate = float(MIN_OCR_HEIGHT) / float(rect.h)
        width = int(float(rect.w) * rate)
        image = image.resize((width, MIN_OCR_HEIGHT), Image.ANTIALIAS)
        image.save(image_file)
    result = pytesseract.image_to_string(image_file)
    return result

def compare_rect(rect, image_file):
    global g_screen
    region = Region(rect.x, rect.y, rect.w, rect.h)
    region.initScreen(g_screen)
    rect_image_file = g_screen.capture(region).getFile()
    image1 = Image.open(rect_image_file)
    image2 = Image.open(image_file)
    h1 = image1.histogram()
    h2 = image2.histogram()
    result = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1))
    logging.debug("Compare Result: %f" % result)
    if result <= 0.0001:
        return True
    else:
        return False

def click_rect(rect):
    return None
