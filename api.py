import atexit
import base64
import getopt
import os
import signal
import sys
from datetime import datetime

import torch
from faster_whisper import WhisperModel
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' # Set the upload folder
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16 MB max file size

SUPPORTED_LANGUAGES = [
    "Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian",
    "Bulgarian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch",
    "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek",
    "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian",
    "Japanese", "Kannada", "Kazakh", "Korean", "Latvian", "Lithuanian",
    "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", "Persian",
    "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak",
    "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai",
    "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh"
]
# ISO 639-1 Code
LANGUAGE_CODES = {
    "Afrikaans" : "af",
    "Arabic": "ar", 
    "Armenian": "hy", 
    "Azerbaijani": "az", 
    "Belarusian": "be", 
    "Bosnian": "bs",
    "Bulgarian": "bg", 
    "Catalan": "ca", 
    "Chinese": "zh", 
    "Croatian": "co", 
    "Czech": "cs", 
    "Danish": "da", 
    "Dutch": "nl",
    "English": "en", 
    "Estonian": "et", 
    "Finnish": "fi", 
    "French": "fr", 
    "Galician": "gl", 
    "German" : "de", 
    "Greek": "el",
    "Hebrew": "he", 
    "Hindi": "hi", 
    "Hungarian": "hu", 
    "Icelandic": "is", 
    "Indonesian": "id", 
    "Italian": "it",
    "Japanese": "ja", 
    "Kannada": "kn", 
    "Kazakh": "kk", 
    "Korean": "ko", 
    "Latvian": "lv", 
    "Lithuanian": "lt",
    "Macedonian": "mk", 
    "Malay": "ms", 
    "Marathi": "mr", 
    "Maori": "mi", 
    "Nepali": "ne", 
    "Norwegian": "nn", 
    "Persian": "fa",
    "Polish": "pl", 
    "Portuguese": "pt", 
    "Romanian": "rm", 
    "Russian": "ru", 
    "Serbian": "sr", 
    "Slovak": "sk",
    "Slovenian": "sl", 
    "Spanish": "es", 
    "Swahili": "sw", 
    "Swedish": "sv", 
    "Tagalog": "tl", 
    "Tamil": "ta", 
    "Thai": "th",
    "Turkish": "tr", 
    "Ukrainian": "uk", 
    "Urdu": "ur", 
    "Vietnamese": "vi", 
    "Welsh": "cy"
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Translation Service API!",
        "endpoints": {
            "/translate": "POST endpoint to translate an audio file. Optionally provide 'from_language'.",
            "/transcribe": "POST endpoint to transcribe an audio file. Optionally provide 'from_language'.",
            "/supportedLanguages": "GET endpoint to list supported languages or check if a specific language is supported."
        }
    })

def ensure_upload_folder_exists():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/transcribe', methods=['POST'])
def transcribe():
    from_language = request.args.get('from_language', 'English') # Default to English if not provided

    if from_language not in SUPPORTED_LANGUAGES:
        return jsonify({"error": "Invalid language"}), 400
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(audio_path)

        # Transcribe
        result = model.transcribe(
            audio_path,beam_size=5,
        )
        # Optionally remove the file after transcription
        os.remove(audio_path)

        return jsonify({"text": result["text"]})

    else:
        return jsonify({"error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'wav'}


@app.route('/translate', methods=['POST'])
def translate():
    print(request)
    from_language = request.args.get('from_language', 'English')  # Default to English if not provided

    if from_language not in SUPPORTED_LANGUAGES:
        return jsonify({"error": "Invalid language"}), 400

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(audio_path)

        # Translate
        result, info = model.transcribe(
            audio_path,beam_size=5,
            task="translate",
            without_timestamps=True,
       )

        # Optionally remove the file after translation
        os.remove(audio_path)
        #Iterate over the result and append all the result.text to a text
        text = " ".join(segment.text for segment in result)
        print(text)
        
        return jsonify({"text": text})

    else:
        return jsonify({"error": "Invalid file type"}), 400


@app.route('/supportedLanguages', methods=['GET'])
def supported_languages():
    language = request.args.get('language')
    if language:
        return jsonify({"supported": language in SUPPORTED_LANGUAGES})
    else:
        return jsonify({"languages": SUPPORTED_LANGUAGES})

# Decodes base64 string to mp3 file and saves it to the disk
def decode_audio(data: str) -> str:
    audio_data = base64.b64decode(data)
    file_path = "audio-cache/audio" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp3"
    with open(file_path, 'wb') as file:
        file.write(audio_data)
    return file_path


def handle_exit(*args):
    # TODO: cleanup audio-cache
    print("Shutting down")
    sys.exit(0)

def get_model_version(argv):
    model = 'large-v3'
    opts, args = getopt.getopt(argv,"hm:",["model="])
    for opt, arg in opts:
        if opt == '-h':
            print ('api.py -m [tiny|small|medium|large|large-v2|large-v3]')
            sys.exit()
        elif opt in ("-m", "--model"):
            model = arg
    return model

model = None
if __name__ == '__main__':
    model_v = get_model_version(sys.argv[1:])
    ensure_upload_folder_exists()  # Ensure the uploads folder exists
    
    # Add exit handler to clear audio-cache on shutdown
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    
    # Load model
    on_gpu = torch.cuda.is_available()
    print("Is CUDA available?", on_gpu, 
          "\nIf CUDA is not available, check installation instructions in README")
    model = WhisperModel(model_v, device="cuda", compute_type="auto")
    
    # Run the app
    app.run(host='0.0.0.0', debug = False)
