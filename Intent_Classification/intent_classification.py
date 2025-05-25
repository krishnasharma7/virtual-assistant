import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow_hub as hub
from nltk.stem import WordNetLemmatizer  #importing lemmatizer
from nltk.corpus import stopwords     #importing nltk corpus of stopwords

def load_rfc():
    rfc_path = 'C:\\Users\\krish\\OneDrive\\Desktop\\Projects\\Project 1 Virtual Assistant\\Intent_Classification\\Models\\rfc_model.pkl'
    
    # Load the saved model
    rfc_model = joblib.load(rfc_path)
    
    #scikit issue, locally train model tbf if conda and pyenv doesnt work
    
    return rfc_model


def load_tensorflow_model():
    tf_model_path = './Models/saved_intent_tensorflow_model.keras'
    
    tf_model = load_model(tf_model_path)
    
    return tf_model
    

def load_sent_encoder(local_path='./Models/universal-sentence-encoder'):
    # Load the Universal Sentence Encoder model from the local path
    sent_encoder = hub.load(local_path)
    
    return sent_encoder

def process_text(command):
    stopword_set = set(stopwords.words('english'))
    lm = WordNetLemmatizer()     #creating an object of the lemmatizer to call it later on
    command = command.lower()   #convert to lowercase
    words = command.split()      #split to words
    tokens = [lm.lemmatize(token) for token in words if token not in stopword_set]   #if the word is not a stopword, lemmatize it and add it to a list
    command_tokenized = (' '.join(str(x) for x in tokens))    #join all the lemmatized word to form the lemmatized command
    return command_tokenized

def encode_command(command, encoder):
    encoder = encoder
    
    if isinstance(command, str):
        command = [command]  # Wrap in a list
    
    encoded_command = encoder(command)
    
    return encoded_command

def predict(command, encoder, tf_model):
    processed_command = process_text(command)
    # print(processed_command)
    encoded_command = encode_command(processed_command, encoder)
    
    rfc_model = load_rfc()
    
    tf_model = tf_model
    
    model = tf_model
    
    if model == tf_model:
        encoded_command = np.reshape(encoded_command, (1, 1, -1))  #batch size, LSTM timestep, 512 dimension vector so even prediction input needs batch size 1
        
        prediction = tf_model.predict(encoded_command)
        
        prediction = prediction[0]
        
        max_ind = np.argmax(prediction)
        
        prediction = np.zeros(9)
        
        prediction[max_ind] = 1
        
        return prediction  #converting the probability values to max prob having 1 and rest 0 same as rfc
    
    elif model == rfc_model:
        prediction = rfc_model.predict(encoded_command)
        
        return prediction[0]  #as prediciction by default is a 2d array like [[0,1,0,0,0,0]]


def prediction_to_function_call(prediction):
    
    """
    So, the prediction will be a 9 element vector (as 9 intents so far), with either 0 or 1. 
    
    Since we know what value corresponds to what category using one hot encoder's categories_ attribute on kaggle,
    
    We can accordingly call the desired function from spotify itself.
    
    So if output is say [1, 0, 0, 0, 0, 0, 0, 0, 0]
    
    And we know the third element corresponds to the intent "pause_music_spotify"
    
    Then directly we can call the increase volume function on spotify.
    
    For this, its best to make a pipelined python file which takes the prediction from this program, and
    accordingly calls the desired function from the spotify program.
    """
    
    categories = ['Pause_Music_Spotify', 'Play_Music_Spotify',
       'Repeat_Track_Spotify', 'Resume_Playing_Spotify',
       'Seek_Song_Spotify', 'Skip_Music_Spotify',
       'Toggle_Shuffle_Spotify', 'Volume_Decrease_Spotify',
       'Volume_Increase_Spotify']
    
    return prediction, categories

def main():
    res = predict("Increase the volume")
    
    print(res)
    
    
if __name__ == '__main__':
    main()
