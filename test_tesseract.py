from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

image = Image.open(r'C:\Users\tutu\AppData\Local\Temp\Sikulix_1959764601\sikuliximage-1542294319383.png')

config = r'--oem 0'

print(pytesseract.image_to_string(image, config=config).upper())
