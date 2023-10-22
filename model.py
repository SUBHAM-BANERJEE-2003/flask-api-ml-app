import pickle 
import warnings
warnings.filterwarnings('ignore')

class RealEstateModel:
    def __init__(self, model_path='realestate.pkl'):
        with open(model_path, 'rb') as file:
            self.loaded_model = pickle.load(file)

    def predict(self, input_data):
        result = self.loaded_model.predict(input_data)
        return result
