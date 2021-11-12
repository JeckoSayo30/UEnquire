import json 

with open("compiled_training.json", 'r') as data_file:
	topic_data = json.load(data_file)

topics = []
for i in range(0, len(topic_data["data"]), 2):
	topics.append(topic_data["data"][i])
# ==============================================================================
with open("training_data.json", 'r') as data_file:
	data = json.load(data_file)

print("LENGTH: ",len(data["data"]))
tweets_col = {}
topic_col = {}

for i in range(len(data["data"])):
	tweets_col[i] = data["data"][i]
	topic_col[i] = topics[i]

new_data = {
	"tweets": tweets_col, "topic":topic_col
}	



with open("final_train.json", 'w') as data_file:
	json.dump(new_data, data_file, indent=4)
