Link to the available QazLip dataset: https://doi.org/10.7910/DVN/VIP1J8

·      Video_Cutter.py  This script automates the process ofextracting and saving individual word clips from a 
full-length video: it first uses Vosk to transcribe the audio into time-aligned word segments, then for each recognized 
Kazakh word in a predefined list it cuts out the corresponding video fragment with MoviePy and saves it into a folder 
named after that word. In doing so, it organizes the output into subdirectories by word, producing a dataset of short 
video clips for each target vocabulary item.

·       Rename_Videos.py  This script standardizes the naming of video files and their containing folders in two 
QazLip dataset directories (train and test). For each Kazakh-script subfolder, it renames every video to a
Latin-transliteration prefix plus a sequential index (e.g. men_1.mp4,men_2.mp4, …), then renames the folder 
itself to use that same transliterated prefix. This ensures a consistent, machine-friendly naming convention across the dataset.
