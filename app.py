from flask import Flask, request
import numpy as np
import os
import random, string, base64
from io import BytesIO
from segment import segmenter_list_foods
from PIL import Image
import tensorflow as tf

class_names = ['Drink_Bottle_FruitTreeApple', 'Drink_Bottle_H2ONonCarbonated', 'Drink_Bottle_H2OOriginal', 'Drink_Bottle_PinkDolphinPeach', 'Drink_Bottle_PokkaGreenTea', 'Drink_Bottle_PokkaIcePeachTea', 'Drink_Bottle_PokkaSparklinFujiApple', 'Drink_Bottle_Sencha', 'Drink_Bottle_YeosLemonBarley', 'Drink_Can_100PlusActive', 'Drink_Can_100PlusOriginal', 'Drink_Can_FuzeteaJasmine', 'Drink_Can_FuzeteaLemon', 'Drink_Can_FuzeteaLychee', 'Drink_Can_Houjicha', 'Drink_Can_Sencha', 'Drink_Carton_MarigoldHLChocolate', 'Drink_Carton_MarigoldHLStrawberry', 'Drink_Carton_NutrisoyOatsAndQuinoa', 'Drink_Carton_NutrisoyOriginal', 'Drink_Carton_NutrisoyReducedSugar', 'Drink_Carton_YeosCoconutWater']

os.makedirs('/tmp/csaiproj', exist_ok=True)
FILENAMES = string.ascii_letters + string.digits
def random_filename(n):
    return '/tmp/csaiproj/' + ''.join([random.choice(FILENAMES) for _ in range(n)])


app = Flask('__name__')
drink_model = tf.keras.models.load_model('drink_model.keras')

@app.route('/ai_orz', methods=['POST'])
def ai_orz():
    print("======= INFO =======", request.form['b64img'][:200])
    image_data = base64.b64decode(request.form['b64img'])
    img = Image.open(BytesIO(image_data))
    # file = request.files['file']
    # img = Image.open(file)
    np_img = np.array(img)
    print(np_img.shape)
    return class_names[np.argmax(drink_model.predict(np.expand_dims(np_img, axis=0)))]

@app.route("/segment", methods=['POST'])
def segment():
    print("======= INFO =======", request.form['b64img'][:200])
    image_data = base64.b64decode(request.form['b64img'])
    img = Image.open(BytesIO(image_data))
    # file = request.files['file']
    # img = Image.open(file)
    np_img = np.array(img)
    return segmenter_list_foods(np_img)

if __name__ == '__main__':
    app.run(port=8000)
