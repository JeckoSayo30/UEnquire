import re
import string
import json
import nltk
from nltk import word_tokenize

nltk.download('stopwords')
from nltk.corpus import stopwords
# ==============================================================
def text_cleaning(data):
	# Disregarding Unicode character
	data = data.encode("ascii", "ignore")
	data = data.decode()

	# removing  links 
	data = data.split(" ")
	for word in data:
		pattern = r"https://"
		if re.match(pattern, word):
			print("TRUE")
			data.remove(word) 
	data = ' '.join(data)
	remove_punctuation = [char for char in data if char not in string.punctuation]
	remove_punctuation = ''.join(remove_punctuation)
	return [word for word in remove_punctuation.split() if word.lower() not in stopwords.words('english')]

with open("dataset.json", 'r') as data_file:
	dataset = json.load(data_file)

clean_data = []
for i in range(len(dataset["data"])):
	print(i, "===================================")
	sample = text_cleaning(dataset["data"][i])
	print(sample)
	clean_data.append(sample)

# Slicing data 70 by 30 trainig and testing data 
train = clean_data[0:735]
test = clean_data[735:1050]

print("train: ", len(train))
print("train: ", len(test))

training_data = {"data": train}
testing_data = {"data": test}

with open("training_data.json", 'w') as data_file:
	json.dump(training_data, data_file, indent=4)

with open("testing_data.json", 'w') as data_file:
	json.dump(testing_data, data_file, indent=4)
