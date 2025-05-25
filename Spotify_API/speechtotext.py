import speech_recognition as sr

def speechrecog():
    r= sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        print("Please speak the command:")
        
        audio = r.listen(source,5,5)
        
        try:
            print("Sentence recognised:\n"+ r.recognize_google(audio))
            ip = str(r.recognize_google(audio))
            return ip
        except Exception as e:
            print(f"Error: {str(e)}")



# if __name__ == "__speechrecog__":
#     test=speechrecog()
#     print(f"\n{test}")