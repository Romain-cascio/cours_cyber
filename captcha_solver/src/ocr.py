import pytesseract
import cv2
import config

pytesseract.pytesseract.tesseract_cmd = config.OCR_ENGINE_PATH

def extract_text_from_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    text = pytesseract.image_to_string(img)
    return text.strip()