import pandas as pd
import random

# Function to generate sentence variations
def generate_simple_variations(variations, count):
    sentences = []
    for _ in range(count):
        variation = random.choice(variations)
        sentences.append(variation)
    return sentences

# Variations for each command
resume_variations = [
    "Resume the music", "Continue playing", "Play the music", "Resume playback", "Resume the song", 
    "Start playing again", "Continue the song", "Resume audio", "Play again", "Continue the track", 
    "Restart the music", "Resume the tunes", "Resume the playlist", "Unpause the music", 
    "Play the track", "Continue the playlist", "Play the song again", "Unpause playback", 
    "Resume my music", "Continue audio", "Resume this", "Restart playback", "Resume play", 
    "Continue the music", "Resume track", "Unpause song", "Resume Spotify", "Start playing the music", 
    "Play from where it left off", "Resume the tunes now", "Continue Spotify", "Resume the sound", 
    "Play the audio", "Play from before", "Pick up the music", "Restart the song", "Resume the jam", 
    "Play my music again", "Play from the point it stopped", "Start playing", "Resume now", 
    "Resume this song", "Continue from where we stopped", "Pick up the track", "Resume streaming", 
    "Resume the beat", "Play it again", "Continue playing from the break", "Play from pause", 
    "Pick up the playback"
]

seek_variations = [
    "Go back to previous track", "Skip back", "Go to previous song", "Rewind to previous track", 
    "Rewind song", "Back to the last track", "Play the previous track", "Seek previous song", 
    "Go to the last song", "Return to the previous track", "Seek back", "Play the last song", 
    "Rewind the track", "Play previous song", "Go back a track", "Play the earlier track", 
    "Go to previous music", "Previous track please", "Rewind to the last track", "Go back one track", 
    "Rewind one song", "Seek the previous track", "Go back to last song", "Seek last track", 
    "Rewind the previous song", "Go back to the last song", "Back to earlier music", 
    "Skip to previous music", "Rewind to the previous song", "Rewind to the earlier track", 
    "Go to previous playlist song", "Backtrack to the last song", "Go back one", 
    "Play the last music", "Seek the last track", "Go back to earlier track", "Play from previous song", 
    "Rewind this playlist", "Go back in music", "Previous track", "Skip to last song", 
    "Play the older track", "Go to older track", "Rewind one track", "Rewind to last song", 
    "Rewind one music", "Go back to old song", "Skip backward", "Seek older track", "Back one song"
]

repeat_variations = [
    "Repeat this song", "Loop the track", "Repeat the music", "Play the song again", "Loop this song", 
    "Repeat the track", "Play the song on repeat", "Play again", "Repeat this track", 
    "Play this on loop", "Repeat song", "Repeat that track", "Loop again", "Repeat the song", 
    "Repeat this music", "Replay the song", "Play that again", "Play the track again", "Loop music", 
    "Loop that song", "Repeat the playlist", "Replay the track", "Replay the music", "Loop song", 
    "Play music again", "Repeat it", "Play the track on loop", "Loop this again", "Repeat audio", 
    "Replay the song again", "Play it on repeat", "Repeat this audio", "Replay that music", 
    "Put the song on repeat", "Repeat tunes", "Loop that track", "Repeat again", "Loop this", 
    "Play this song repeatedly", "Play on loop", "Loop it", "Put this track on repeat", 
    "Replay this track", "Loop the song again", "Replay the tunes", "Put the music on repeat", 
    "Loop track", "Repeat the audio", "Replay this again", "Put it on repeat"
]

# Generating 50 variations for each command
resume_sentences = generate_simple_variations(resume_variations, 50)
seek_sentences = generate_simple_variations(seek_variations, 50)
repeat_sentences = generate_simple_variations(repeat_variations, 50)

# Combine all sentences and intents
all_commands = resume_sentences + seek_sentences + repeat_sentences
all_intents = (
    ["Resume_Playing_Spotify"] * 50 +
    ["Seek_Song_Spotify"] * 50 +
    ["Repeat_Track_Spotify"] * 50
)

# Create DataFrame and save to CSV
df = pd.DataFrame({"Command": all_commands, "Intent": all_intents})
df.to_csv("resume_seek_repeat_intent_dataset.csv", index=False)

print("Dataset saved as resume_seek_repeat_intent_dataset.csv")
