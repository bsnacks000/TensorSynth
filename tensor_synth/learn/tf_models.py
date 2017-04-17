import pandas as pd
import json
import os


from tensor_synth.exceptions import *


class SkipGramTF(object):
    '''
    class for tensorflow SkipGram training 
    takes a word series as input and trains a skip gram on a sequence
    
    after successful training, sets the final_embeddings and final_cos_similarity parameters for the model
    
    ::params:: 
    word_series = pd.Series of encoded string data
    span = an integer value 2 or 4; size of SkipGram window

    '''

    def __init__(self, word_series_input, span=2):
        self.model_trained = False

        # intialize vars
        self.word_series_input = word_series_input #TODO error handling here 
        self.span = span # TODO can only handle 2 or 4 span window for now...
        self.span = steps # TODO error check

        # initialize data structures
        self.targets, self.target_index_map_df, self.unique_words_df = _prepare_batch(word_series)

        self.key_word_dict = self._make_key_word_dict()
        self.word_key_dict = self._make_word_key_dict()

        self.batch,self.labels = self._generate_batch_labels(self.targets, self.span)

        # model values initialized 
        self.graph = None
        self.init = None

        self.final_embeddings = None
        self.final_cos_similarity = None

        
    def _prepare_batch(self, word_series):
        
        word_series.name = None
        sentence_df = pd.DataFrame(word_series,columns=['words'])
        sentence_df['word_counts'] = sentence_df.groupby('words')['words'].transform('count')

        unique_words_df = pd.DataFrame(word_series.unique(),columns=['words']).reset_index(drop=True)
        sentence_df['word_counts'] = sentence_df.groupby('words')['words'].transform('count')

        unique_words_df = pd.merge( unique_words_df, sentence_df, 
            how='inner',on=['words']).drop_duplicates() \
            .sort_values('word_counts',ascending=False).reset_index(drop=True).reset_index()
    
        unique_words_sub = unique_words_df[['index','words']]
        seq_to_integer = pd.merge(sentence_df,unique_words_sub,how='left',on='words').drop('word_counts', axis=1)

        word_ints = np.array(seq_to_integer['index']) # TODO check each output is properly formatted 
        
        return word_ints, seq_to_integer, unique_words_df


    def _make_key_word_dict(self):
        ''' returns dict of unique words in the vocabulary: { index: 'word_val'}'''
        return self.unique_words_df['words'].to_dict() 


    def _make_word_key_dict(self):
        '''returns a reversed version of the vocabulary: { 'word_val': index }'''
        return dict(zip(self.key_word_dict.values(),self.key_word_dict.keys()))


    def _generate_batch_labels(self, targets, span=2):
        ''' 
        generates tuples of context words given a target
        span is the size of the target tuple: 
        ex: span = 2
        [anarchism, originated, as] --> originated, (anarchism,as)
        
        '''    
        batch = np.repeat(targets[span//2:-span//2],span)  # TODO  targets should already be correctly formatted if handled correctly in __init__
        labels = []
        
        if span == 2:
            for i in range(0, len(targets)-span):  
                labels.append(targets[i])           # grabs i
                labels.append(targets[i+span])      # skips over target and grabs that span

        if span == 4:
            for i in range(0, len(targets)-span):
                labels.append(targets[i])
                labels.append(targets[i+1])
                labels.append(targets[i+span-1])
                labels.append(targets[i+span])
                
        labels = np.array(labels).reshape(len(labels),1) # need to add a dimension for nce loss
            #TODO error checking batch and labels here before passing out of function
        return batch, labels


    # PUBLIC METHODS
    def make_graph(self):
        '''
        user initializes and builds the graph -- future builds might include options here

        The code in this method is adapted from: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/word2vec/word2vec_basic.py  
        '''

        batch_size = len(self.batch)   # these all become class variabes
        embedding_size = len(self.batch)
        vocabulary_size = len(self.unique_words_df)
        num_sampled = 24  # for nce negative sampling


        self.graph = tf.Graph()
        with self.graph.as_default():

            train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
            train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
            valid_inputs = tf.constant(self.batch, dtype=tf.int32) # for computing cosine similarity 

            with tf.device("/cpu:0"):
                embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
                embed = tf.nn.embedding_lookup(embeddings, train_inputs)

                nce_weights = tf.Variable(tf.truncated_normal([vocabulary_size, embedding_size], stddev=1.0 / (embedding_size**0.5)))
                nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

                loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights, biases=nce_biases,
                                 labels=train_labels,inputs=embed,num_sampled=num_sampled,
                                 num_classes=vocabulary_size
                                 ))
                # SGD.optimizer
                optimizer = tf.train.GradientDescentOptimizer(2.0).minimize(loss)
                
                # placeholders for                 
                norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
                normalized_embeddings = embeddings / norm
                valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_inputs)
                similarity = tf.matmul(valid_embeddings, tf.transpose(normalized_embeddings))
                
                self.init = tf.global_variables_initializer()


    def run_model(self, steps):
        '''
        initializes a run of the training model -- user specifies number of steps
        sets: final_cosine_similarity 
        sets: final_embeddings
        sets: model.trained = True on success
        '''
        if self.graph = None:

        with tf.Session(graph=self.graph) as session:
            self.init.run()
            print('tf.session initialized')
    
            average_loss = 0
            for step in range(steps):
                _, loss_val = session.run([optimizer,loss],feed_dict={train_inputs:batch, train_labels:labels})
            
                average_loss += loss_val  # this code tracks the loss and training progress
                if step%200 == 0:
                    if step > 0:
                        average_loss /= 100
                    print('Average loss at step ', step,": ",average_loss)
                    average_loss = 0
    
            self.final_embeddings = normalized_embeddings.eval()
            self.final_cos_similarity = similarity.eval()

        print('model successfully trained')
        self.model_trained = True
    
    
    def save_graph(self):
        #TODO implement save_graph (via tensorflow save feature)

        pass

    
    def save_embeddings(self):
        #TODO implement save_embeddings (via pickle)

        pass