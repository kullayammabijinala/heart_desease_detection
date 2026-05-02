from flask import Flask, render_template, request
import mysql.connector
import pickle
import numpy as np
import os

app = Flask(__name__)

# --- Safe Model Loading ---
# This looks for the model.pkl file in the same folder as this script
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'model.pkl')

model = None
if os.path.exists(model_path):
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print("Model loaded successfully!")
    except EOFError:
        print("Error: model.pkl is empty. Run train_model.py again.")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print("Warning: model.pkl not found. Please run train_model.py first.")

# --- Database Configuration ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # XAMPP default is empty
    'database': 'heart_disease_db'
}

def save_to_mysql(data_tuple):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """INSERT INTO predictions 
                   (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, prediction_result) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, data_tuple)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return "Error: Machine Learning Model (model.pkl) is missing or corrupted. Run train_model.py first."

    try:
        # 1. Define the exact order expected by the model
        feature_names = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]
        
        # 2. Extract values and check for None/Empty
        features_list = []
        for name in feature_names:
            val = request.form.get(name)
            if val is None or val.strip() == "":
                return render_template('index.html', prediction_text=f"Error: Missing value for {name}")
            features_list.append(float(val))
        
        # 3. Convert to Numpy Array for Prediction
        final_features = np.array([features_list])
        
        # 4. Perform Prediction
        prediction = model.predict(final_features)
        result = "Positive (Risk Detected)" if prediction[0] == 1 else "Negative (No Risk)"
        
        # 5. Save data to Database
        # data_tuple needs the 13 inputs + the result string
        save_to_mysql(tuple(features_list) + (result,))
        
        return render_template('index.html', prediction_text=result)

    except ValueError:
        return render_template('index.html', prediction_text="Error: Please enter valid numbers in all fields.")
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)