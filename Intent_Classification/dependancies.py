# import nltk
# # nltk.download('stopwords')
# nltk.download('wordnet')

#also use this to download and load models maybe?

import tensorflow_hub as hub
import os
import tensorflow as tf

def download_use_model(local_path='models/universal-sentence-encoder'):
    # Check if the local path exists; if not, download the model
    if not os.path.exists(local_path):
        os.makedirs(local_path)
        # Download the Universal Sentence Encoder from TensorFlow Hub
        sent_encoder = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        # Save the model using TensorFlow's SavedModel format
        tf.saved_model.save(sent_encoder, local_path)
    else:
        print(f"Model already exists at {local_path}")

download_use_model()
