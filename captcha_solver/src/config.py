import os

# Configuration des chemins et paramètres généraux
DATASET_PATH = "data/Large_Captcha_Dataset/"
MODEL_PATH = "models/captcha_model.h5"
OCR_ENGINE_PATH = "/usr/bin/tesseract"
CAPTCHA_IMAGE_SIZE = (100, 40)  # Ajuster en fonction du dataset
CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
CHAR_TO_INDEX = {char: i for i, char in enumerate(CHARACTERS)}
INDEX_TO_CHAR = {i: char for i, char in enumerate(CHARACTERS)}
