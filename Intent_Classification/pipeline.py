import os
from dotenv import load_dotenv
import spotify
import intent_classification
import pandas as pd

load_dotenv()

def prediction_to_function_call(prediction):
    
    """
    So, the prediction will be a 9 element vector (as 9 intents so far), with either 0 or 1. 
    
    Since we know what value corresponds to what category using one hot encoder's categories_ attribute on kaggle,
    
    We can accordingly call the desired function from spotify itself.
    
    So if output is say [1, 0, 0, 0, 0, 0, 0, 0, 0]
    
    And we know the third element corresponds to the intent "pause_music_spotify"
    
    Then directly we can call the pause music function on spotify.
    
    Hence, making a pipelined program taking the predictions from IC model, and calling the spotify function from spotify program
    """
    
    categories = ['Pause_Music_Spotify', 'Play_Music_Spotify',
       'Repeat_Track_Spotify', 'Resume_Playing_Spotify',
       'Seek_Song_Spotify', 'Skip_Music_Spotify',
       'Toggle_Shuffle_Spotify', 'Volume_Decrease_Spotify',
       'Volume_Increase_Spotify']  #categories from the kaggle notebook
    
    
    """
    Categories to add:- Resume playing, seek song, repeat track
    Also, need to enhance the dataset and add more commands
    Maybe do a feature where I enter a command, it makes the prediction and then asks me if i was correct
    if yes, add it to dataset with command and intent and later retrain model
    if not, ask which intent it was to further train.
    basically incorporating feedback
    """
    
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    token = spotify.refresh_token(client_id,client_secret) #to get access token
    
    
    #function_map is a dictionary which for every index contains the function name in spotify program,
    #this can be then used to retrieve function name using prediction and index of '1' and accordingly call the correct function
    # function_map = {
    #     0: spotify.pause,
    #     1: spotify.play_song,
    #     2: spotify.skip
    #     3: spotify.toggle_shuffle,
    #     4: spotify.volume_up_down,
    #     5: spotify.volume_up_down
    # }
    
    print(prediction)
    
    
    
    calling_index = list(prediction).index(1)
    
    print(categories[calling_index])  #printing the predicted intent
    
    #since diff functions have diff parameters, its best to just use if else like switch case 
    
    if calling_index == 0:
        spotify.pause(token)
    elif calling_index == 1:
        spotify.play_song(token, None)
    elif calling_index == 2:
        spotify.repeat_track(token)
    elif calling_index == 3:
        spotify.resume(token)
    elif calling_index == 4:
        spotify.seek_song(token)
    elif calling_index == 5:
        spotify.skip_song(token)
    elif calling_index == 6:
        spotify.toggle_shuffle(token)
    elif calling_index == 7:
        spotify.volume_up_down(token, "down")
    elif calling_index == 8:
        spotify.volume_up_down(token, "up")
        

def pipeline(command, encoder, tf_model):
    
    prediction = intent_classification.predict(command, encoder, tf_model)
    
    prediction_to_function_call(prediction)
    
    return prediction
    
def main():
    
    """
    So, by calling the function and getting instance of universal sentence encoder, 
    if we put all our commands in while loop the encoder is already initialised so it wont have to be called everytime
    reducing computation time. Also, we then pass this as argument in the functions to make sure this instance is used 
    everytime and new one is not created.
    """
    encoder = intent_classification.load_sent_encoder() #getting instance of encoder so that the tensorflow is not called everytime, reducing computation time
    tf_model = intent_classification.load_tensorflow_model() #to avoid the model being initialised everytime leading to inefficiency as mentioned by tensorflow warnings
    
    updated_dataset_path = 'Updated_Dataset_with_Feedback.csv'
    
    if os.path.exists(updated_dataset_path):
        df = pd.read_csv(updated_dataset_path)  #so that later on when program is called updated dataset file is read but first time og dataset is read
    else:
        df = pd.read_csv("Final_Dataset.csv")
        
    
    print(df.head())
    
    final_categories = ['Pause_Music_Spotify', 'Play_Music_Spotify',
       'Repeat_Track_Spotify', 'Resume_Playing_Spotify',
       'Seek_Song_Spotify', 'Skip_Music_Spotify',
       'Toggle_Shuffle_Spotify', 'Volume_Decrease_Spotify',
       'Volume_Increase_Spotify']
    
    while True:
        ip = input('Command: ')
        if ip == 'quit':
            break
        prediction = pipeline(ip, encoder, tf_model)
        
        #adding feedback loop
        
        feedback = input('Was the intent correct for given command? [y/n]: ')
        
        if feedback.lower() == "y":
            
            categories = final_categories
            
            cat_ind = list(prediction).index(1)  #finding the index of the category of predicted intent
            
            new_row = {'Command' : ip, 'Intent' : categories[cat_ind]}
            new_df = pd.DataFrame([new_row])
            
            df = pd.concat([df, new_df], ignore_index= True)
        elif feedback.lower() == "n":
            categories = final_categories  #displaying categories and asking user which is the correct intent to be added
            
            print("Please choose the correct intent")
            
            for i in range(len(categories)):
                print(f"{i+1} : {categories[i]}")
            
            correct = int(input("Which category is the correct intent? Please enter the corresponding number: "))
            
            new_row = {'Command' : ip, 'Intent' : categories[correct-1]}  #indexing is from 0 while displaying is from 1
            new_df = pd.DataFrame([new_row])
            
            df = pd.concat([df, new_df], ignore_index= True)
            
    
    df.to_csv(updated_dataset_path, index = False)  #once the loop is exited, only then write to csv to avoid redundant saving to csv
            
    
if __name__ == '__main__':
    main()
    
    
    
    