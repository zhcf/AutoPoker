from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

image = Image.open(r'D:\AutoPoker\tmp\sikuliximage-1541336518715.png')

config = r'--oem 0 -c tessedit_char_whitelist=0123456789'

print(pytesseract.image_to_string(image, config=config))
