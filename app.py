from flask import Flask, request
import numpy as np
import os
import random, string
from i_love_ai import make_model
from segment import segmenter_list_foods
from PIL import Image

class_names = ['Drink_Bottle_PokkaGreenTea', 'Drink_Bottle_PokkaIcePeachTea', 'Drink_Bottle_Sencha', 'Drink_Can_100PlusActive', 'Drink_Can_100PlusOriginal', 'Drink_Can_FuzeteaJasmine', 'Drink_Can_FuzeteaLemon', 'Drink_Can_FuzeteaLychee', 'Drink_Can_Houjicha', 'Drink_Can_Sencha', 'Drink_Carton_MarigoldHLMilk', 'Drink_Carton_YeosCoconutWater']
os.makedirs('/tmp/csaiproj', exist_ok=True)
FILENAMES = string.ascii_letters + string.digits
def random_filename(n):
    return '/tmp/csaiproj/' + ''.join([random.choice(FILENAMES) for _ in range(n)])


app = Flask('__name__')
# model = make_model("./Weights/weights_1")

@app.route('/ai_orz', methods=['POST'])
def ai_orz():
    print("======= INFO =======", request.files)
    file = request.files['file']
    img = Image.open(file)
    np_img = np.array(img)
    print(np_img.shape)
    return class_names[np.argmax(model.predict(np.expand_dims(np_img, axis=0)))]

@app.route("/segment", methods=['POST'])
def segment():
    print("======= INFO =======", request.files)
    file = request.files['file']
    img = Image.open(file)
    np_img = np.array(img)
    return segmenter_list_foods(np_img)

if __name__ == '__main__':
    app.run(debug=True)
