import pandas as pd

new_dataset_path = 'resume_seek_repeat_intent_dataset.csv'
old_dataset_path = 'Updated_Dataset_with_Feedback.csv'

df_old = pd.read_csv(old_dataset_path)
df_new = pd.read_csv(new_dataset_path)

df_final = pd.concat([df_old, df_new], ignore_index= True)

df_final.to_csv("Final_Dataset.csv", index = False)