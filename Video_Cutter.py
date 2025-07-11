import wave
import json
import os
import re  # To clean folder names from invalid characters
from vosk import Model, KaldiRecognizer
from moviepy.editor import VideoFileClip

def transcribe_with_vosk(audio_path, model_path):
    wf = wave.open(audio_path, "rb")
    
    # Check that the WAV is indeed 16-bit, mono, uncompressed
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio must be 16-bit WAV with one channel (mono), uncompressed.")

    # Load the model
    model = Model(model_path)
    
    # Initialize the recognizer
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    # Final result
    final_result = json.loads(rec.FinalResult())
    results.append(final_result)

    # Extract intervals (start, end, word_text) for each word
    word_segments = []
    for res in results:
        if "result" in res:
            for w in res["result"]:
                start = w["start"]
                end = w["end"]
                text = w["word"]
                word_segments.append((start, end, text))

    return word_segments

def split_video_by_words(video_path, word_segments, output_folder):
    """
    Splits the original video into fragments by intervals (start, end),
    corresponding to each word, and saves them in subfolders named by the word.
    Only those segments are saved where the word is included in the list of allowed ones.
    """
    # List of allowed words
    allowed_words = {
        "мен", "сен", "ол", "адам", "бала", "ата", "апа", "әке", "ана", "дос",
        "мұғалім", "оқушы", "көрші", "әріптес", "қонақ", "жүргізуші", "сатушы",
        "дәрігер", "әнші", "спортшы", "жазушы", "үй", "бөлме", "үстел", "орындық",
        "есік", "терезе", "теледидар", "компьютер", "телефон", "жарық", "мектеп",
        "кітап", "дәптер", "қалам", "қарындаш", "сызғыш", "тақта", "сабақ", "баға",
        "сұрақ", "күн", "аспан", "бұлт", "жел", "жаңбыр", "қар", "өзен", "орман",
        "көлік", "автобус", "пойыз", "ұшақ", "жол", "көпір", "аялдама", "қала",
        "ауыл", "дүкен", "сөз", "тіл", "әуен", "ойын", "жұмыс", "ақша", "хат",
        "жаңалық", "сурет", "өмір", "бақыт", "білім", "арман", "сезім", "жауап",
        "көмек", "мақсат", "еркіндік", "ақпарат", "деректер", "бағдарлама", "желі",
        "қауіпсіздік", "құрылғы", "қолданба", "дерекқор", "нұсқаулық", "жоба", "стартап",
        "тамыр", "асхана", "ірімшік", "жылқы", "жұмыртқа", "жүрек", "жүйке", "жастық",
        "шаш", "шатыр", "шынаяқ", "махаббат", "мемлекет", "ғаламтор", "өңір", "қолтаңба",
        "жатыр", "жалап", "аңшы", "бүлкең", "желп", "жүйені", "жүргізушінің", "күбір",
        "орысша", "ояз", "пояс", "сезем", "сұрау", "үсті", "қарандаш", "шынайы", "о"
    }
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = VideoFileClip(video_path)

    for idx, (start, end, word_text) in enumerate(word_segments, start=44000):
        # Convert the word to lowercase for comparison
        lower_word = word_text.lower()
        if lower_word not in allowed_words:
            continue  

        # Clear the word name from invalid characters 
        safe_word = re.sub(r'[\\/*?:"<>|]', '_', lower_word)
        
        # Create a folder for the word if it doesn't exist yet
        word_folder = os.path.join(output_folder, safe_word)
        os.makedirs(word_folder, exist_ok=True)

        # Form the name of the output file, for example: "men_4300.mp4"
        output_filename = os.path.join(word_folder, f"{safe_word}_{idx}.mp4")
        
        # Cut out a fragment with precise boundaries (without expansion)
        word_clip = video.subclip(start, end)
        word_clip.write_videofile(output_filename, codec="libx264")

def main():
    # Path to the original video (MP4 or MOV)
    video_path = r"D:\PATH_TO_YOUR_DIRECTORY\EXAMPLE_OF_FULL_VIDEO.mp4"
    
    # Path to already converted WAV (16-bit, mono, 16 kHz)
    audio_path = r"D:\PATH_TO_YOUR_DIRECTORY\EXAMPLE_OF_FULL_VIDEO.wav"
    
    # Folder with Vosk model (for example, model for Kazakh language)
    model_path = r"D:\PATH_TO_YOUR_DIRECTORY\vosk-model-kz-0.15"
    
    # Folder where to save the final video fragments
    output_folder = r"D:\PATH_TO_YOUR_DIRECTORY"

    # 1. Recognize speech and get a list (start, end, word_text) for each word
    word_segments = transcribe_with_vosk(audio_path, model_path)
    print(f"Words found: {len(word_segments)}")

    # 2. Divide the original video into fragments and save them in subfolders by words (only allowed words)
    split_video_by_words(video_path, word_segments, output_folder)
    print("Done! Individual videos are saved in subfolders of the directory:", output_folder)

if __name__ == "__main__":
    main()
