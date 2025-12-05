import os
FLASK_PORT_NUMBER = 5004

MONGODB_URL ="mongodb://localhost:27017"

MONGO_DB_NAME = "med_ins_project_db"

MODEL_FILE_PATH = os.path.join("artifacts", "Linear_reg_model.pkl")
LABEL_ENCODED_DATA = os.path.join("artifacts", "label_encoded_data.json")