# 🎵 Spotify Virtual Assistant

A voice-enabled virtual assistant that listens to your commands, understands your intent, and controls Spotify to play your favorite music, manage playlists, and more.

---

## 🧠 Features

- 🎤 **Voice Input**: Converts your spoken commands into text.  
- 🧾 **Intent Classification**: Uses an ensemble of Random Forest Classifier (RFC) and LSTM models to accurately detect the user’s intent.  
- 🔍 **Text Encoding**: Employs Google’s Universal Sentence Encoder to transform text commands into embeddings for effective intent recognition.  
- 🎶 **Spotify Integration**: Executes commands on Spotify via API calls based on classified intent and extracted parameters.

---

## 🚀 How It Works

1. User speaks a command (e.g., "Play Shape of You by Ed Sheeran").  
2. The command is converted from speech to text.  
3. The text is encoded using the Universal Sentence Encoder to get meaningful sentence embeddings.  
4. The embeddings are fed into an ensemble of RFC and LSTM models for robust intent classification.  
5. Based on the predicted intent and extracted entities (song, artist, playlist), the assistant makes corresponding Spotify API calls to execute the command.
