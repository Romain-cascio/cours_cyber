from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def solve_captcha_automatically(url, solver):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)  # Laisser le temps de charger la page
    captcha_img = driver.find_element("id", "captcha-image").screenshot_as_png
    captcha_text = solver.predict(captcha_img)
    input_field = driver.find_element("id", "captcha-input")
    input_field.send_keys(captcha_text)
    input_field.send_keys(Keys.RETURN)
    time.sleep(2)
    driver.quit()