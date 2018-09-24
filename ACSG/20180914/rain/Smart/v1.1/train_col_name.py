from nltk.stem import PorterStemmer
import train_neural_net as net
import numpy as np
import json, sys
from nltk.corpus import wordnet

def classify(sentence,condition=True,show_details=False):
	training_data = []
	training_data.append({"class":"SPEC_NUMBER", "sentence":"SPEC.NO"})
	training_data.append({"class":"SPEC_NUMBER", "sentence":"SPECN"})
	training_data.append({"class":"SPEC_NUMBER", "sentence":"SPEC NO."})
	training_data.append({"class":"SPEC_NUMBER", "sentence":"SPECIFICATION NO"})
	training_data.append({"class":"SPEC_NUMBER", "sentence":"SPECN . NO."})
	training_data.append({"class":"SPEC_NUMBER", "sentence":"SPECN NUMBER"})
	training_data.append({"class":"SPEC_NUMBER", "sentence":"SPECEFICATION NUMBER"})

	training_data.append({"class":"SPEC_ATTACHED", "sentence":"SPEC ATTACHED"})
	training_data.append({"class":"SPEC_ATTACHED", "sentence":"SPECN ATTACHED"})
	training_data.append({"class":"SPEC_ATTACHED", "sentence":"SPEC ATT"})
	training_data.append({"class":"SPEC_ATTACHED", "sentence":"SPECIFICATION ATTACHED"})
	training_data.append({"class":"SPEC_ATTACHED", "sentence":"SPECN . ATTACH"})

	training_data.append({"class":"SK_NUMBER", "sentence":"SK NO"})
	training_data.append({"class":"SK_NUMBER", "sentence":"SK. NO."})
	training_data.append({"class":"SK_NUMBER", "sentence":"SKETCH NO"})
	training_data.append({"class":"SK_NUMBER", "sentence":"SKETCH"})
	training_data.append({"class":"SK_NUMBER", "sentence":"SKETCH NUMBER"})
	syns = wordnet.synsets("sketch")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"SK_NUMBER", "sentence":m_word})

	training_data.append({"class":"AMENDMENT_NO","sentence":"AMD,AMENDMENT"})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMENDMENT NO"})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMENDMENT NO."})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMD."})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMENDMENT NUMBER"})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMD NO"})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMD.NO."})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMD NO."})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMD. NUMBER"})
	training_data.append({"class":"AMENDMENT_NO","sentence":"AMD NUMBER"})
	syns = wordnet.synsets("amendment")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"AMENDMENT_NO", "sentence":m_word})

	training_data.append({"class":"DRG._NUMBER", "sentence":"DRG.NO."})
	training_data.append({"class":"DRG._NUMBER", "sentence":"DRG,DRG."})
	training_data.append({"class":"DRG._NUMBER", "sentence":"DRG NO."})
	training_data.append({"class":"DRG._NUMBER", "sentence":"DRG NO"})
	training_data.append({"class":"DRG._NUMBER", "sentence":"DRG NO."})
	training_data.append({"class":"DRG._NUMBER", "sentence":"DRAWING NUMBER"})
	training_data.append({"class":"DRG._NUMBER", "sentence":"DRAWING NO"})
	training_data.append({"class":"DRG._NUMBER", "sentence":"DRAWING NO."})

	training_data.append({"class":"QUANTITY", "sentence":"QTY"})
	training_data.append({"class":"QUANTITY", "sentence":"QUANTITY"})
	training_data.append({"class":"QUANTITY", "sentence":"AMOUMT"})
	syns = wordnet.synsets("quantity")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"QUANTITY", "sentence":m_word})

	training_data.append({"class":"ITEM_NUMBER", "sentence":"ITEM"})
	training_data.append({"class":"ITEM_NUMBER", "sentence":"ITMNO"})
	training_data.append({"class":"ITEM_NUMBER", "sentence":"ITEM NO"})
	training_data.append({"class":"ITEM_NUMBER", "sentence":"ITEM NO."})
	training_data.append({"class":"ITEM_NUMBER", "sentence":"ITEM NUMBER"})
	training_data.append({"class":"ITEM_NUMBER", "sentence":"ITM NO"})
	syns = wordnet.synsets("item")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"ITEM_NUMBER", "sentence":m_word})

	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT"})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT NO."})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT NO"})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT NUMBER"})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT.NO."})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALTNO"})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT NO."})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT."})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALTERATION NO."})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALTERATION_NO."})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT."})
	training_data.append({"class":"ALT_NUMBER", "sentence":"ALT."})
	syns = wordnet.synsets("alteration")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"ALT_NUMBER", "sentence":m_word})

	training_data.append({"class":"REV_NUMBER", "sentence":"REV"})
	training_data.append({"class":"REV_NUMBER", "sentence":"REV NO"})
	training_data.append({"class":"REV_NUMBER", "sentence":"REV NUMBER"})
	training_data.append({"class":"REV_NUMBER", "sentence":"REV. NO."})
	training_data.append({"class":"REV_NUMBER", "sentence":"REV.NO."})

	training_data.append({"class":"DRAWING_ATTACHED", "sentence":"DRAW"})
	training_data.append({"class":"DRAWING_ATTACHED", "sentence":"DRAWING"})
	training_data.append({"class":"DRAWING_ATTACHED", "sentence":"DRW"})
	training_data.append({"class":"DRAWING_ATTACHED", "sentence":"DRAW ATTACHED"})
	training_data.append({"class":"DRAWING_ATTACHED", "sentence":"DRAWING ATTACHED"})
	training_data.append({"class":"DRAWING_ATTACHED", "sentence":"DRAW ATT"})
	syns = wordnet.synsets("drawing")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"DRAWING_ATTACHED", "sentence":m_word})

	training_data.append({"class":"OTHER_SPECIFICATION", "sentence":"OTH SPEC"})
	training_data.append({"class":"OTHER_SPECIFICATION", "sentence":"OTHER SPECIFICATION"})
	training_data.append({"class":"OTHER_SPECIFICATION", "sentence":"OTHER SPEC"})
	training_data.append({"class":"OTHER_SPECIFICATION", "sentence":"REST SPECIFICATION"})
	training_data.append({"class":"OTHER_SPECIFICATION", "sentence":"SPEC"})

	training_data.append({"class":"REST_DATA", "sentence":"REST DATA"})
	training_data.append({"class":"REST_DATA", "sentence":"LEFT"})
	training_data.append({"class":"REST_DATA", "sentence":"UNPROCESSED"})
	training_data.append({"class":"REST_DATA", "sentence":"UNCATAGORISE"})
	training_data.append({"class":"REST_DATA", "sentence":"JUNK"})
	training_data.append({"class":"REST_DATA", "sentence":"REJECTED"})
	syns = wordnet.synsets("unprocessed")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"REST_DATA", "sentence":m_word})
	syns = wordnet.synsets("uncatagorise")
	for i in range(len(syns)):
		m_word = str(syns[i].lemmas()[0].name())
		training_data.append({"class":"REST_DATA", "sentence":m_word})

	##print ("%s Sentences in training data" % len(training_data))

	words = []
	classes = []
	documents = []
	ignore_words = ['?']
	# loop through each sentence in our training data
	for pattern in training_data:
		# tokenize each word in the sentence
		w = pattern['sentence'].split(' ')
		# add to our words list
		words.extend(w)
		# add to documents in our corpus
		documents.append((w, pattern['class']))
		# add to our classes list
		if pattern['class'] not in classes:
			classes.append(pattern['class'])

	# stem and lower each word and remove duplicates
	ps = PorterStemmer()
	words = [ps.stem(w.lower()) for w in words if w not in ignore_words]
	words = list(set(words))

	# remove duplicates
	classes = list(set(classes))

	# create our training data
	training = []
	output = []
	# create an empty array for our output
	output_empty = [0] * len(classes)

	# training set, bag of words for each sentence
	for doc in documents:
		# initialize our bag of words
		bag = []
		# list of tokenized words for the pattern
		pattern_words = doc[0]
		# stem each word
		pattern_words = [ps.stem(word.lower()) for word in pattern_words]
		# create our bag of words array
		for w in words:
			bag.append(1) if w in pattern_words else bag.append(0)

		training.append(bag)
		# output is a '0' for each tag and '1' for current tag
		output_row = list(output_empty)
		output_row[classes.index(doc[1])] = 1
		output.append(output_row)

	X = np.array(training)
	y = np.array(output)

	synapse_0 = 0
	synapse_1 = 0
	ERROR_THRESHOLD = 0.2

	if condition == True:
		net.train(X, y, classes, words, hidden_neurons=20, alpha=0.1, epochs=100000, dropout=False, dropout_percent=0.2)
		print 'Training Done!'
	else:
		print 'Picking trained model!'
		#try:
			# probability threshold
			
			# load our calculated synapse values
	synapse_file = 'Trained_data.json' 
	try:
		with open(synapse_file) as data_file: 
			synapse = json.load(data_file)
			synapse_0 = np.asarray(synapse['synapse0'])
			synapse_1 = np.asarray(synapse['synapse1'])
	except IOError:
		print 'Trained file not found...'
		print "Call function wit condition True\n"
		sys.exit()
	results = net.think(sentence, words, synapse_0, synapse_1, show_details)
	results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ]
	results.sort(key=lambda x: x[1], reverse=True)
	return_results =[[classes[r[0]],r[1]] for r in results]
	print ("%s \nclassification: %s" % (sentence, return_results))
	return return_results

#var = classify("data left")

