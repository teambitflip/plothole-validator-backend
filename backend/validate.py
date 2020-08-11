from model.v2.script import Pothole
from PIL import Image
import urllib.request, json

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("backend/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://bitflip-potholedetector.firebaseio.com/'
})


class Validator:
    def __init__(self, uid, sub_id):
        self.uid = uid
        self.sub_id = sub_id
    
        # model and weights path
        self.filter_model_path = "model/v2/filter_model/model.json"
        self.filter_model_weights_path = "model/v2/filter_model/weights.h5"

        self.road_model_path = "model/v2/road_model/model.json"
        self.road_model_weights_path = "model/v2/road_model/weights.h5"

        self.pothole_model_path = "model/v2/pothole_model/model.json"
        self.pothole_model_weights_path = "model/v2/pothole_model/weights.h5"

        self.severity_model_path = "model/v2/severity_model/model.json"
        self.severity_model_weights_path = "model/v2/severity_model/weights.h5"



    # returns a tuple => (validity, severity) of the image passed        
    def validate(self):
        detector = Pothole(
            self.filter_model_path, self.filter_model_weights_path,
            self.road_model_path, self.road_model_weights_path,
            self.pothole_model_path, self.pothole_model_weights_path,
            self.severity_model_path, self.severity_model_weights_path
        )
        result = detector.prediction(self.get_submission_image())

        return result

    # download the image from the link self.get_image_link() will return
    def get_submission_image(self):
        URL = urllib.request.urlretrieve(self.get_image_link())
        img = Image.open(URL[0])
        
        return img
    
    # get image_link attirbute of the submission at uid/sub_id
    def get_image_link(self):
        submissionRef = db.reference("submissions/{}/{}".format(self.uid, self.sub_id))
        submissions = submissionRef.get()
        print(submissions)
        return submissions["image_link"]


    # uploads the result to firebase as per the the decided schema
    def upload_result(self, result):
        submission = db.reference("submissions/{}/{}".format(self.uid, self.sub_id)).get()

        db.reference("submissions/{}/{}".format(self.uid, self.sub_id)).update({
            "processed":"true"
        })

        resultsRef = db.reference("results/")
        result_id = resultsRef.push()
        
        payload = {
            'uid': self.uid,
            'gps_coordinates': submission['gps_coordinates'],
            'validity': float(result[0] * 100),
            'severity': int(result[1]),
            'action_taken': "false",
            'issue_fixed': "false",
            'img_link': self.get_image_link()
        }

		
        print("Uploaded Payload")
        print(payload)
        
        result_id.set(payload)



