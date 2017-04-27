'''
A module of static methods that act on a completed graph model's embedding and similarity arrays.similarity
The vector operations can map directly to word sequences 

The cosine similarity formula is adapted from: 
https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/word2vec/word2vec_basic.py

'''

import numpy as np
from tensor_synth.exceptions import *


def get_knn_of_target(graph, target, top_k=8):  # TODO unit tests/error check on for I/O
    ''' 
    helper function that generates a list of nearest neighbors for a given input
    target is a word string that gets converted
    size is number of neighbors
    '''
    if not graph.model_trained:
        raise tsGeneratorException()

    target_word_key = graph.word_key_dict[target]  # gets key from input string - word_key instance var # TODO check for key error
    nearest = (-graph.final_cos_similarity[target_word_key,:].argsort()[1:top_k + 1])   # key word instance var
    knn = np.array([graph.key_word_dict[-nearest[k]] for k in range(top_k)])
    return knn


def generate_word_sequence(graph, num_output_words, knn_size): # TODO unit tests/error check for I/O
    ''' 
    generates a simple word sequence of size n using cosine similarity from each previous word
    num_ouput_words is the length of the output sequence
    '''

    if not graph.model_trained:
        raise tsGeneratorException()

    word_seq = [] # the string values
    for i in range(0,num_output_words):
        if i == 0:
            word_seq.append(graph.key_word_dict[np.random.choice(list(graph.key_word_dict.keys()))])
            continue
        knn = get_knn_of_target(graph,word_seq[i-1])
        word_seq.append(graph.key_word_dict[graph.word_key_dict[np.random.choice(knn)]])
        
    return word_seq