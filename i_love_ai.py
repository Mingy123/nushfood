import tensorflow as tf
from keras import layers
import keras
import matplotlib.pyplot as plt
print(tf.__version__)
print(keras.__version__)

class_names = ['Drink_Bottle_PokkaGreenTea', 'Drink_Bottle_PokkaIcePeachTea', 'Drink_Bottle_Sencha', 'Drink_Can_100PlusActive', 'Drink_Can_100PlusOriginal', 'Drink_Can_FuzeteaJasmine', 'Drink_Can_FuzeteaLemon', 'Drink_Can_FuzeteaLychee', 'Drink_Can_Houjicha', 'Drink_Can_Sencha', 'Drink_Carton_MarigoldHLMilk', 'Drink_Carton_YeosCoconutWater']

def make_model(path_name):
    base_model = keras.applications.Xception(
        weights='imagenet',  # Load weights pre-trained on ImageNet.
        input_shape=(299, 299, 3),
        include_top=False)  # Do not include the ImageNet classifier at the top.

    base_model.trainable = False

    # Augmentation layers
    data_augmentation = tf.keras.Sequential([
      layers.RandomFlip("horizontal_and_vertical"),
      layers.RandomRotation(0.2),
      layers.RandomBrightness(0.2),
      layers.RandomContrast(0.2),
    ])

    inputs = keras.Input(shape=(None, None, 3))

    # Resize data for easy predicts
    x = layers.Resizing(299, 299)(inputs)
    # Augment data
    x = data_augmentation(x)
    # Preprocess input
    x = keras.applications.xception.preprocess_input(x)
    # We make sure that the base_model is running in inference mode here, by passing `training=False`.
    x = base_model(x, training=False)
    # Convert features of shape `base_model.output_shape[1:]` to vectors
    x = keras.layers.GlobalAveragePooling2D()(x)

    outputs = keras.layers.Dense(len(class_names))(x)

    model = keras.Model(inputs, outputs)

    model.compile(optimizer=keras.optimizers.AdamW(),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=["accuracy"])
    model.summary()
    model.load_weights(path_name)
    return model
