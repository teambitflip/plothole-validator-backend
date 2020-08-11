
################# INSTRUCTIONS ##########################
#########################################################

# it returns output as a tuple containing two elements (integers).
# first element - if 0 then it doesn't contain a pothole.
#                 if 1 then it contains a pothole.

# second element - if 1 then the severity is low.
#                  if 2 then the severity is medium.
#                  if 3 then the severity is high.

#########################################################
#########################################################


import numpy as np
from PIL import Image
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import keras.backend as K

class Pothole:
    
    def __init__(self, model0_path, weights0_path, model1_path, weights1_path, model2_path, weights2_path, model3_path, weights3_path):
        
        self.loaded_models_dict = {}
        self.models_and_weights_path_list = [[model0_path, weights0_path, "for_first_filter"], [model1_path, weights1_path, "for_road"], [model2_path, weights2_path, "for_pothole"], [model3_path, weights3_path, "severity"]]

        for model_and_weight in self.models_and_weights_path_list:
            json_file = open(model_and_weight[0], 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            loaded_model.load_weights(model_and_weight[1])
            self.loaded_models_dict[model_and_weight[2]] = loaded_model



    def img_preprocessing(self, img):
        img = img.resize((480, 640))
        img = np.asarray(img)
        img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
        img = (img * 1.) / 255
        return img
    

    def for_first_filter_prediction(self, img):
        # print(np.max(self.loaded_models_dict["for_first_filter"].predict(img))* 100)
        if np.max(self.loaded_models_dict["for_first_filter"].predict(img)) * 100 > 28:
            return 1
        return 0


    def for_road_prediction(self, img):
        if np.max(self.loaded_models_dict["for_road"].predict(img)) * 100 > 75:
            return 1
        return 0

    
    def for_pothole_prediction(self, img):
        # print(self.loaded_models_dict["for_pothole"].predict(img))
        if np.max(self.loaded_models_dict["for_pothole"].predict(img)) * 100 > 58:
            return 1
        return 0

    
    def for_severity_prediction(self, img):
        return np.argmax(self.loaded_models_dict["severity"].predict(img)) + 1



    def prediction(self, img):
        img = self.img_preprocessing(img)
        first_filter_result = self.for_first_filter_prediction(img)
        is_road = self.for_road_prediction(img)
        is_pothole = self.for_pothole_prediction(img)
        severity = self.for_severity_prediction(img)   
        # print(is_road)
        # print(is_pothole)

        if first_filter_result and is_road and is_pothole:
            K.clear_session()
            return (1, severity)
                
        else:
            K.clear_session()
            return (0, 0)