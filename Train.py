import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('dataset.csv')
df1 = pd.read_csv('Symptom-severity.csv')

# Data preprocessing
# Replace missing values
df = df.fillna(0)

# Replace symptoms with their severity weights
vals = df.values
symptoms = df1['Symptom'].unique()

for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = df1[df1['Symptom'] == symptoms[i]]['weight'].values[0]

d = pd.DataFrame(vals, columns=df.columns)
d = d.replace('dischromic _patches', 0)
d = d.replace('spotting_ urination', 0)
df = d.replace('foul_smell_of urine', 0)

# Split the data into features and labels
data = df.iloc[:, 1:].values
labels = df['Disease'].values

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
train_accuracy = accuracy_score(y_train, model.predict(X_train))
test_accuracy = accuracy_score(y_test, model.predict(X_test))

print('Accuracy on Training data:', train_accuracy)
print('Accuracy on Test data:', test_accuracy)

# Export the trained model
import joblib

joblib.dump(model, 'trained_model.pkl')
print("Model saved successfully.")
