import json
import os

from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions

from django.apps import apps

from django.conf import settings


def process_image(path):
    model = VGG16()

    undetermined = 0.30
    # print(model.summary())

    image = load_img(path, target_size=(224, 224))
    image = img_to_array(image)  # output Numpy-array

    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    image = preprocess_input(image)
    yhat = model.predict(image)

    label = decode_predictions(yhat)
    first_label = label[0][0]
    labels = [first_label]
    if first_label[2] < undetermined:
        labels.append(label[0][1])

    print(labels)
    categories = []
    for label in labels:
        categories.append(get_categorie(label[1]))

    categories = sorted(set(categories))

    categorie_str = ""

    for categorie in categories:
        categorie_str += categorie
        categorie_str += "#"
    return categorie_str[:-1]


def get_categorie(ml_class):
    file_dir = os.getcwd()
    print(file_dir)
    with open(file_dir + '\\home\\classes.json') as json_file:
        dictionary = json.load(json_file)

    def getpath(nested_dict, prepath=()):
        for key, value in nested_dict.items():
            path = prepath + (key,)
            if ml_class in value:  # if found
                return path
            elif type(value) is dict:  # check if dict
                temp_path = getpath(value, path)  # dig further
                if temp_path is not None:
                    return temp_path  # if path return it

    path = getpath(dictionary)

    tag_string = "#"
    for tag in path:
        tag_string += tag
        tag_string += "#"

    return tag_string[:-1]


if __name__ == '__main__':
    process_image("C:\\Users\\ItayK\\Pictures\\nsfw.png")
    pass
