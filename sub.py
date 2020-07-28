import pandas as pd

training_data = pd.read_csv('test.csv')

print(training_data.head())

for ind, row in training_data.iterrows():
    training_data.loc[ind, "ball x rev"] = 800 - row['ball x'] 

print(training_data.head())

y = training_data[' right paddle']
X = training_data.drop(columns = [" right paddle", "ball x"])

print(X.head())
print(y.head())