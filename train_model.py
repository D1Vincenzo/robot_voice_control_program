from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import os

# Suppose commands is a list of strings with the commands for your robot
commands = ["righthand", "lefthand", "move forward", "turn left", "pick up the object", "stop", 
                  "turn right", "backward", "go right", "go left", 
                  "go straight", "go", "move", "back"]

# Tokenize and preprocess the commands
sentences = [simple_preprocess(command) for command in commands]

model_filename = "word2vec_model"

# Check if the model file exists
if os.path.exists(model_filename):
    # Load the model from the file
    model = Word2Vec.load(model_filename)
else:
    # Train the Word2Vec model
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    # Save the model to a file
    model.save(model_filename)
    