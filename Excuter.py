from PIL import ImageGrab
import cv2
import keyboard
import mouse
import numpy as np
from tensorflow import keras
import tensorflow as tf

from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import matplotlib.pyplot as plt

def load_image(img_path, show=False):

    img = load_img(img_path, target_size=(75, 75))
    img_tensor = img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]

    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor

def set_roi():
    global ROI_SET, x1, y1, x2, y2
    ROI_SET = False
    print("Select your ROI using mouse drag.")
    while(mouse.is_pressed() == False):
        x1, y1 = mouse.get_position()
        while(mouse.is_pressed() == True):
            x2, y2 = mouse.get_position()
            while(mouse.is_pressed() == False):
                print("Your ROI : {0}, {1}, {2}, {3}".format(x1, y1, x2, y2))
                ROI_SET = True
                return

print()
print("------- 인테리어 분류기 -------");print()
print("ctrl+1을 누르면 캡쳐가 시작됩니다.")

keyboard.add_hotkey("ctrl+1", lambda: set_roi())
ROI_SET = False
x1, y1, x2, y2 = 0, 0, 0, 0

while True:
    if ROI_SET == True:
        image = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)
        cv2.imshow("image", image)
        
        key = cv2.waitKey(100)
        if key == ord("q"):
            cv2.imwrite('./real_test/my_img.png', image)
            print("image is saved.")
            break
cv2.destroyAllWindows()

img_path = './real_test/my_img.png'
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) #cv2.IMREAD_COLOR : 컬러 이미지

cv2.imshow("User's Image",img)
print("사진이 입력되었습니다.");print()

furniture = input("원하는 가구를 말씀해주세요 : ")

print()
print("사용자가 입력한 사진을 딥러닝 모델이 분류합니다...");print()
print("Style 분류를 시작합니다.");print()

cv2.destroyAllWindows()

# load model
model = load_model("./saved_model/style_model")

# image path
img_path = './real_test/my_img.png'

# load a single image
new_image = load_image(img_path)

# check prediction
with tf.device('/gpu:0'):
    pred = model.predict(new_image)

list_tmp = pred[0][0][0]
tmp = max(list_tmp)
tmp2 = np.where(tmp == list_tmp)
index = tmp2[0][0]
categories_style = ["casual", "classic", "modern", "natural"]
print()
print("Probability : ")
print(list_tmp);print()

style = categories_style[index]

print(f"입력한 사진은 {style} Style 입니다.");print()

print("Factor 분류를 시작합니다.");print()

model2 = load_model("./saved_model/factor_model")

with tf.device('/gpu:0'):
    pred = model2.predict(new_image)

print(pred)

list_tmp = pred[0][0][0]
tmp = max(list_tmp)
tmp2 = np.where(tmp == list_tmp)
index = tmp2[0][0]
categories_factor = ["cold", "neutral", "warm"]
print()
print("Probability : ")
print(list_tmp);print()

factor = categories_factor[index]

print(f"입력한 사진은 {factor} factor 입니다.");print()

search_word = style + "하고, " + factor + "한 " + furniture
search_word2 = style + "한 " + furniture

print(f"입력한 사진은 {style} style 이고, {factor} factor의 인테리어 입니다.")
print(f"추천 검색어1 은 [{style}하고, {factor}에 가까운 {furniture}] 입니다.")
print(f"추천 검색어2 는 [{style}한 {furniture}] 입니다.");print()



# 사이트 자동 검색 기능
print("'오늘의 집' 사이트에서 추천 검색어를 검색합니다.");print()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path='chromedriver')
driver.maximize_window()

url = "https://www.google.com" # Google
url2 = "https://ohou.se/" # 오늘의 집

driver.get(url2)

time.sleep(0.5) ## 0.5초

element = driver.find_element_by_class_name("css-16px0cl")
element.send_keys(search_word2)

element.send_keys(Keys.RETURN)

while(True):
    pass