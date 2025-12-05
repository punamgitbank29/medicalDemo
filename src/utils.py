import config
import pickle
import json
import numpy as np
import pandas as pd

class MedicalInsurance():

    def __init__(self):
        pass
        
    def load_model(self):
        """
            This method will be used to load Linear Regresion Model
        """
        with open(config.MODEL_FILE_PATH, "rb") as f:
            self.model = pickle.load(f)
        return self.model

    def load_json_data(self):
        """
        Docstring for load_json_data
        
        :param self: Description
        """
        with open(config.LABEL_ENCODED_DATA, "r") as f:
            self.column_encoded_data = json.load(f)

        return self.column_encoded_data

    def create_test_df(self):
        self.load_model()
        self.load_json_data()

        test_array = np.zeros((1,self.model.n_features_in_))
        
        test_array[0,0] = self.data['age']
        test_array[0,1] = self.column_encoded_data['gender'][self.data['gender']]
        test_array[0,2] = self.data['bmi']
        test_array[0,3] = self.data['children']
        test_array[0,4] = self.column_encoded_data['smoker'][self.data['smoker']]

        region = f"region_{self.data['region']}"

        region_index = np.where(self.model.feature_names_in_ == region)[0]
        test_array[0,region_index] = 1
        print("test_array", test_array)
        self.test_df = pd.DataFrame(test_array, columns=self.model.feature_names_in_)

    def predict_charges(self, user_input_data):
        self.data = user_input_data
        self.create_test_df()

        prediction = self.model.predict(self.test_df)[0]
        print("Predicted Price is :",prediction )
        return np.around(prediction,4)