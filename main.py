# Import necessary libraries
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib

# Create a Flask app
app = Flask(__name__)

# Load the symptom data
symptom_data = pd.read_csv('Symptom-severity.csv')

# Load the trained model
model = joblib.load('trained_model.pkl')

# Load disease descriptions
def load_disease_descriptions(file_path):
    descriptions = {}
    with open(file_path, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                disease = parts[0].strip()
                description = parts[1].strip()
                descriptions[disease] = description
    return descriptions

descriptions_file = 'symptom_Description.csv'
disease_descriptions = load_disease_descriptions(descriptions_file)

# Define the home route
@app.route('/')
def index():
    # Retrieve search query from GET parameters
    search_query = request.args.get('search')

    # Filter symptom data based on the search query
    if search_query:
        symptom_data_filtered = symptom_data[symptom_data['Symptom'].str.contains(search_query, case=False)]
    else:
        symptom_data_filtered = symptom_data.sort_values(by='Symptom', ascending=True)

    return render_template('index.html', symptom_data=symptom_data_filtered)


# Define the submit route for form submission
@app.route('/submit', methods=['POST'])
def submit():
    selected_symptoms = []
    max_symptoms = 17

    # Retrieve selected symptoms and their weights from the form
    for i in range(max_symptoms):
        symptom_weight = request.form.get(f"symptom_{i}")
        if symptom_weight:
            selected_symptoms.append(float(symptom_weight))

    # Pad the selected symptoms if necessary
    num_selected_symptoms = len(selected_symptoms)
    if num_selected_symptoms < max_symptoms:
        selected_symptoms.extend([0.0] * (max_symptoms - num_selected_symptoms))

    # Convert selected symptoms to numpy array
    input_data = np.array(selected_symptoms).reshape(1, -1)

    # Make predictions using the model
    prediction = model.predict(input_data)[0]
    predicted_disease = prediction  # Assuming prediction is the disease name

    # Get description for predicted disease
    if predicted_disease in disease_descriptions:
        predicted_description = disease_descriptions[predicted_disease]
    else:
        predicted_description = "Description not available."

    return render_template('result.html', prediction=predicted_disease, description=predicted_description)


# Run the app if the script is executed
if __name__ == "__main__":
    app.run(debug=True)
