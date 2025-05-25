import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Intent_Classification import intent_classification
from Spotify_API import spotify

def prediction_to_function_call(prediction):
    
    """
    So, the prediction will be a 6 element vector (as 6 intents so far), with either 0 or 1. 
    
    Since we know what value corresponds to what category using one hot encoder's categories_ attribute on kaggle,
    
    We can accordingly call the desired function from spotify itself.
    
    So if output is say [0, 0, 1, 0, 0, 0]
    
    And we know the third element corresponds to the intent "increase_volume"
    
    Then directly we can call the increase volume function on spotify.
    
    Hence, making a pipelined program taking the predictions from IC model, and calling the spotify function from spotify program
    """
    
    categories = ['Pause_Music_Spotify', 'Play_Music_Spotify', 'Skip_Music_Spotify',
       'Toggle_Shuffle_Spotify', 'Volume_Decrease_Spotify',
       'Volume_Increase_Spotify']  #categories from the kaggle notebook
    
    
    token = spotify.get_token() #to get access token
    
    
    #function_map is a dictionary which for every index contains the function name in spotify program,
    #this can be then used to retrieve function name using prediction and index of '1' and accordingly call the correct function
    # function_map = {
    #     0: spotify.pause,
    #     1: spotify.play_song,
    #     2: spotify.toggle_shuffle,
    #     3: spotify.volume_up_down,
    #     4: spotify.volume_up_down
    # }
    
    print(prediction)
    
    calling_index = prediction.index(1)
    
    #since diff functions have diff parameters, its best to just use if else like switch case 
    
    if calling_index == 0:
        spotify.pause(token)
    elif calling_index == 1:
        spotify.play_song(token, None)
    elif calling_index == 2:
        spotify.toggle_shuffle(token)
    elif calling_index == 3:
        spotify.volume_up_down(token, "down")
    elif calling_index == 4:
        spotify.volume_up_down(token, "up")
        

def pipeline(command):
    
    prediction = intent_classification.predict(command)
    
    prediction_to_function_call(prediction)
    
def main():
    pipeline("Pause the music")
    
if __name__ == '__main__':
    main()
    
    
    
    