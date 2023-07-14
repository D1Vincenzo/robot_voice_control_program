from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import numpy as np

# Ignore the non-existing word
def vectorize_command(command, model):
    vectorized_words = [model.wv[word] for word in simple_preprocess(command) if word in model.wv]
    if vectorized_words:
        return np.mean(vectorized_words, axis=0)
    else:
        return None
'''
# Give commands
def get_user_command():
    return input("Please give a command: ")
'''
def find_the_most_similar_command(new_commands):
    # Load the model from the file
    model = Word2Vec.load("word2vec_model")

    known_commands = ["move forward", "left", "pick", "stop", 
                    "right", "back", "backward", "go straight"]

    known_command_vectors = [vectorize_command(command, model) for command in known_commands]

    # Check if the whole commands is empty
    if not new_commands.strip():
        return []

    split_commands = new_commands.split("and")

    most_similar_commands = []
    for new_command in split_commands:

        # Ignore the first command if it is empty ('and go and pick')
        if not new_command:
            continue

        new_command_vector = vectorize_command(new_command, model)
        
        # Ignore the command if it is empty ('hello')
        if new_command_vector is None:
            continue

        # Calculate cosine similarities
        similarities = [np.dot(new_command_vector, vec)/(np.linalg.norm(new_command_vector)* np.linalg.norm(vec)) for vec in known_command_vectors]

        # Find the most similar command
        most_similar_command = known_commands[np.argmax(similarities)]
        most_similar_commands.append(most_similar_command)
    
    return most_similar_commands
