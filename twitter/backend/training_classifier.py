import numpy as np 
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import recall_score, precision_score, f1_score 


# In order to run the naive bayes traing model, the file must have the required format for the system.
def naive_bayes(file, t_size, state, averaging):
	data = pd.read_json(file)
	data.sort_index(inplace = True)

	tail = data.tail()
	shape = data.shape


	vectorizer = CountVectorizer(stop_words='english', strip_accents='unicode')
	all_features = vectorizer.fit_transform(data.tweets)
	
	feature_shape = all_features.shape
	vector_vocab = vectorizer.vocabulary_
	feature = all_features
	

	x_train, x_test, y_train, y_test = train_test_split(all_features, data.topic, test_size= float(t_size), random_state= int(state))

	train_shape = [x_train.shape, y_train.shape]
	test_shape = [x_test.shape, y_test.shape]

	# TRAINING OF THE MODEL
	classifier = MultinomialNB()
	classifier.fit(x_train,y_train)

	num_correct = (y_test == classifier.predict(x_test)).sum()
	num_incorrect = y_test.size -num_correct

	# fraction = classifier.score(x_test, y_test) 
	accuracy = str(round(num_correct/ (num_incorrect + num_correct)*100,4))+ ' %'
	recall = str(round((recall_score(y_test, classifier.predict(x_test),  average=averaging))* 100, 4)) + ' %'
	precision = str(round((precision_score(y_test, classifier.predict(x_test),  average=averaging))* 100, 4)) + ' %'
	f1 = str(round((f1_score(y_test, classifier.predict(x_test),  average=averaging))* 100, 4)) + ' %'
	
	# precision = precision_score(y_test, classifier.predict(x_test),  average=averaging)
	# f1 = f1_score(y_test, classifier.predict(x_test),  average=averaging )

	# print(f'{num_correct} classified correctly')
	# print(f'{num_incorrect} classified incorrectly')
	# print(f'The (testing) accuracy of the model is {1-accuracy:.2%}')
	# # print(f'The (testing) inaccuracy of the model is {fraction}')

	# print(f'Recall Score: {recall}')
	# print(f'Precision Score: {precision}')
	# print(f'f1 Score:  {f1}')

	scores = {
		'correct': num_correct,
		'incorrect': num_incorrect,
		'accuracy': accuracy,
		'recall': recall,
		'precision': precision,
		'f1_score': f1
	}
	# data_detail = {


	# }
	return classifier, scores, vectorizer

	
