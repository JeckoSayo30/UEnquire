from sklearn.feature_extraction.text import CountVectorizer 
import numpy as np
import pandas as pd


training_data = "final_train.json"
data = pd.read_json(training_data)

print(data.tail())
print(data.shape)
vectorizer = CountVectorizer(stop_words = "english")

all_features = vectorizer.fit_transform(data.tweets)
print(all_features.shape)