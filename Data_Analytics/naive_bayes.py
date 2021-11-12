import numpy as np 
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import recall_score, precision_score, f1_score 

file = "dataset.json"
data = pd.read_json(file)
# print(data.tail())
# print(data.shape)
data.sort_index(inplace = True)
# print(data.tail())


vectorizer = CountVectorizer(stop_words='english', strip_accents='unicode')
all_features = vectorizer.fit_transform(data.tweets)
# print(all_features.shape)
# print(vectorizer.vocabulary_)
# print(all_features)
x_train, x_test, y_train, y_test = train_test_split(all_features, data.topic, test_size=0.3, random_state=88)

print(x_train.shape)
print(x_test.shape)

classifier = MultinomialNB()
classifier.fit(x_train,y_train)

num_correct = (y_test == classifier.predict(x_test)).sum()
num_incorrect = y_test.size -num_correct

# fraction = classifier.score(x_test, y_test) 
accuracy = num_incorrect/ (num_incorrect + num_correct)

recall = recall_score(y_test, classifier.predict(x_test),  average='macro')
precision = precision_score(y_test, classifier.predict(x_test),  average='macro')
f1_score = f1_score(y_test, classifier.predict(x_test),  average='macro')

print(f'{num_correct} classified correctly')
print(f'{num_incorrect} classified incorrectly')
print(f'The (testing) accuracy of the model is {1-accuracy:.2%}')
# print(f'The (testing) inaccuracy of the model is {fraction}')

print(f'Recall Score: {recall}')
print(f'Precision Score: {precision}')
print(f'f1 Score:  {f1_score}')

sample = ["The University of East has announced suspension.","Corrupted politicians are not hero",
	"Be sure to vote on the upcomming election", "Signal number 3 sa Bicol", "sd;oosfskfj", 
	"The Student Council has an important announcement to make this week", 
	"The UE Journalism has an important integrity to uphold",

	"university of the east is close for holiday.",
	"Ester Garcia nag announce ng walang pasok sa buong linggo",
	"manny paquiao for president!",
	"urgent just in advisory breaking news"
]
matrix = vectorizer.transform(sample)
print(classifier.predict(matrix))