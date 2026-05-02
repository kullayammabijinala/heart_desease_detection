import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1. Load your dataset
try:
    df = pd.read_csv('heart.csv') # Ensure your filename matches exactly
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: heart.csv not found. Please place the dataset in this folder.")
    exit()

# 2. Split data into Features (X) and Target (y)
# Assuming 'target' is the column name for the result (0 or 1)
X = df.drop('target', axis=1)
y = df['target']

# 3. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model
print("Training the model... please wait.")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 5. Save the model to a file
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Success! 'model.pkl' has been created.")