import numpy as np
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import keras.backend as K



class Pothole:

    def __init__(self, model_path, weights_path):
        self.model_path = model_path
        self.weights_path = weights_path

        json_file = open(self.model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(self.weights_path)
        self.model = loaded_model

    #returns a tuple -  first index containing the probability 
    #                   second index containing the severity class from 1-3, 3 being most severe and 1 being least severe
    def prediction(self, img):
        img = img.resize((480, 640))
        # img = load_img(img, target_size= (640, 480))
        img = img_to_array(img)
        img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
        img = (img * 1.) / 255

        result = np.max(self.model.predict(img))
        severity =  3 if (0.98 <= result <= 1) else 2 if (0.90 <= result < 0.98) else 1 if (0.74 <= result < 0.90) else -1
        K.clear_session()
        return (result, severity)


######## Sample code to predict ###########################################


# detector = Pothole('changed_model_vgg16.json', 'first_try_25epochs.h5')
# result = detector.prediction("sample_test_img/n47.jpg")
# print(result)

###########################################################################
    


