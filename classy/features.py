# features.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import numpy as np
import util
import samples

DIGIT_DATUM_WIDTH=28
DIGIT_DATUM_HEIGHT=28

def basicFeatureExtractor(datum):
    """
    Returns a binarized and flattened version of the image datum.

    Args:
        datum: 2-dimensional numpy.array representing a single image.

    Returns:
        A 1-dimensional numpy.array of features indicating whether each pixel
            in the provided datum is white (0) or gray/black (1).
    """
    features = np.zeros_like(datum, dtype=int)
    features[datum > 0] = 1
    return features.flatten()

def enhancedFeatureExtractor(datum):
    """
    Returns a feature vector of the image datum.

    Args:
        datum: 2-dimensional numpy.array representing a single image.

    Returns:
        A 1-dimensional numpy.array of features designed by you. The features
            can have any length.

    ## DESCRIBE YOUR ENHANCED FEATURES HERE...

    ##
    """
    features = basicFeatureExtractor(datum)
     
    # visited nodes
    visited = []
    # unique # of contiguous whitespace
    unique = 0    

    for x in range(DIGIT_DATUM_HEIGHT):
        for y in range(DIGIT_DATUM_WIDTH):
	    if datum[x][y] == 0:
		# if coordinates not visited yet and is whitespace, it's new
		if (x, y) not in visited:
		    unique += 1
		    # add nodes to visited based on explore function
		    visited += explore(datum, visited, x, y)	    

    # represents how many unique contiguous whitespace components (bools)
    enhancedFeatures = [0, 0, 0]
    if unique == 1:
	enhancedFeatures[0] = 1
    elif unique == 2:
	enhancedFeatures[1] = 1
    elif unique > 2:
	enhancedFeatures[2] = 1

    # concatenate the flattened features (basic) with my new features
    return np.concatenate((features, np.array(enhancedFeatures)))

# used to explore all contiguous whitespace of a pixel
def explore(datum, visited, x, y):
    # explore nodes w/ dfs, since we know it has a limited depth
    stack = util.Stack()
    stack.push((x, y))
    # list to keep track of what's been explored
    explored = []

    while not stack.isEmpty():
	i, j = stack.pop()
	# if the node hasn't been visited (prior run)
	# or explored (this run), then add it, then explore it.
	if (i, j) not in visited and (i, j) not in explored:
	    explored.append((i, j))
		    
	    # find the neighbors of current location
	    neighbors = []
	    if i >= 1 and datum[i-1][j] == 0:
		neighbors.append((i-1, j))
	    if i < DIGIT_DATUM_WIDTH - 1 and datum[i+1][j] == 0:
		neighbors.append((i+1, j))
	    if j >= 1 and datum[i][j-1] == 0:
		neighbors.append((i, j-1))
	    if j < DIGIT_DATUM_HEIGHT - 1 and datum[i][j+1] == 0:
		neighbors.append((i, j+1))

	    # push neighbors onto stack
	    for neighbor in neighbors:
		stack.push(neighbor)
    return explored

def analysis(model, trainData, trainLabels, trainPredictions, valData, valLabels, validationPredictions):
    """
    This function is called after learning.
    Include any code that you want here to help you analyze your results.

    Use the print_digit(numpy array representing a training example) function
    to the digit

    An example of use has been given to you.

    - model is the trained model
    - trainData is a numpy array where each row is a training example
    - trainLabel is a list of training labels
    - trainPredictions is a list of training predictions
    - valData is a numpy array where each row is a validation example
    - valLabels is the list of validation labels
    - valPredictions is a list of validation predictions

    This code won't be evaluated. It is for your own optional use
    (and you can modify the signature if you want).
    """

    # Put any code here...
    # Example of use:
    #for i in range(len(trainPredictions)):
    #    prediction = trainPredictions[i]
    #    truth = trainLabels[i]
    #    if (prediction != truth):
    #        print "==================================="
    #        print "Mistake on example %d" % i
    #        print "Predicted %d; truth is %d" % (prediction, truth)
    #        print "Image: "
    #        print_digit(trainData[i,:])


## =====================
## You don't have to modify any code below.
## =====================

def print_features(features):
    str = ''
    width = DIGIT_DATUM_WIDTH
    height = DIGIT_DATUM_HEIGHT
    for i in range(width):
        for j in range(height):
            feature = i*height + j
            if feature in features:
                str += '#'
            else:
                str += ' '
        str += '\n'
    print(str)

def print_digit(pixels):
    width = DIGIT_DATUM_WIDTH
    height = DIGIT_DATUM_HEIGHT
    pixels = pixels[:width*height]
    image = pixels.reshape((width, height))
    datum = samples.Datum(samples.convertToTrinary(image),width,height)
    print(datum)

def _test():
    import datasets
    train_data = datasets.tinyMnistDataset()[0]
    for i, datum in enumerate(train_data):
        print_digit(datum)

if __name__ == "__main__":
    _test()
