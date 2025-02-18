from tensorflow.keras.models import load_model # type: ignore
import cv2
import numpy as np
from src import config

class CaptchaSolver:
    def __init__(self, model_path=config.MODEL_PATH):
        self.model = load_model(model_path)
    
    def preprocess_image(self, img):
        img = cv2.resize(img, config.CAPTCHA_IMAGE_SIZE)
        img = img / 255.0  # Normalisation
        return np.expand_dims(img, axis=0)
    
    def predict(self, img):
        img = self.preprocess_image(img)
        prediction = self.model.predict(img)
        return self.decode_prediction(prediction)
    
    def decode_prediction(self, prediction):
        return "".join([config.CHARACTERS[np.argmax(char)] for char in prediction])