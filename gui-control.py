from jpype import *

JRE_PATH = r'C:\Java\jre1.8.0_111\bin\server\jvm.dll'
SIKULI_PATH = r'D:\projects\AutoPoker\sikulixapi.jar'

startJVM(JRE_PATH, '-XX:MaxHeapSize=512m', '-Djava.class.path=%s' % SIKULI_PATH)

Screen = JClass('org.sikuli.script.Screen')

g_screen = Screen()

class Rect:
    def __init__(x, y, w, h, self):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def find_in_screen(image_filename):
    global g_screen
    try:
        match = g_screen.find(image_filename)
        return Rect(match.getX(), match.getY(), match.getW(), match.getH())
    except FindFailed:
        logging.error("Can't find % on screen." % image_filename)
        return None

def find_in_rect(image_filename, rect):
    global g_screen
    try:
        
    return None

def click_rect(rect):
    return None

def get_string_from_rect(rect):
    return None
