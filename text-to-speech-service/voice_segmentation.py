from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import whisper
import librosa
import numpy as np
import soundfile as sf
import tempfile
import os

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173"])

# model = whisper.load_model("tiny")  

# STATIC_AUDIO_PATH = "D:/clip_0009.wav"

# def preprocess_audio(path, target_sr=16000):
#     """
#     Normalisation + trim du silence
#     """
#     y, sr = librosa.load(path, sr=target_sr, mono=True)

#     # éviter division par zéro
#     max_val = np.max(np.abs(y)) + 1e-9
#     y = y / max_val

#     # enlever silence mais PAS trop agressif
#     y, _ = librosa.effects.trim(y, top_db=40)

#     return y, target_sr


# def save_chunk(y, sr):
#     tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
#     sf.write(tmp_file.name, y, sr)
#     return tmp_file.name


# def transcribe_audio(path, chunk_duration=30):
#     y, sr = preprocess_audio(path)
#     samples_per_chunk = chunk_duration * sr

#     segments_all = []
#     text_all = ""

#     chunk_index = 0

#     for i in range(0, len(y), samples_per_chunk):
#         chunk = y[i:i + samples_per_chunk]

#         # ✅ éviter chunk vide
#         if chunk.size == 0:
#             print(f"Chunk {chunk_index} vide → ignoré")
#             chunk_index += 1
#             continue

#         # ✅ éviter chunk trop court (< 0.3s)
#         if len(chunk) < int(sr * 0.3):
#             print(f"Chunk {chunk_index} trop court ({len(chunk)/sr:.2f}s) → ignoré")
#             chunk_index += 1
#             continue

#         # ✅ Sauvegarde temporaire
#         tmp_path = save_chunk(chunk, sr)

#         try:
#             result = model.transcribe(tmp_path, verbose=False)

#             text_all += result.get("text", "") + " "

#             if "segments" in result:
#                 # Ajouter l’offset global au timestamp
#                 for seg in result["segments"]:
#                     seg["start"] += i / sr
#                     seg["end"] += i / sr
#                 segments_all.extend(result["segments"])

#         except Exception as e:
#             print(f"Erreur transcription chunk {chunk_index}: {e}")

#         finally:
#             os.remove(tmp_path)

#         chunk_index += 1

#     return text_all.strip(), segments_all



# def transcribe():
#     try:
#         text, segments = transcribe_audio(STATIC_AUDIO_PATH)
#         return {"text": text, "segments": segments}
#     except Exception as e:
#         print(f"Erreur globale: {e}")
#         return {"error": str(e), "text": "", "segments": []}

# @app.route("/transcribe", methods=["POST"])
# def transcribeSegmentation():
#     segments=transcribe()
#     return jsonify({"segements":segments})

# @app.route("/audio", methods=["GET"])
# def serve_audio():
#     return send_file(STATIC_AUDIO_PATH, mimetype="audio/wav")


# if __name__ == "__main__":
#     app.run(debug=True)






from flask import Flask, jsonify, send_file
import whisper

app = Flask(__name__)

# Charger le modèle (CPU par exemple)
model = whisper.load_model("tiny")
STATIC_AUDIO_PATH = "D:/stories/new stories/thatsnothow.wav"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    # Transcrire l'audio statique
    result = model.transcribe(STATIC_AUDIO_PATH)
    
    # Générer segments avec timestamps
    segments = [
        {"start": s["start"], "end": s["end"], "text": s["text"]}
        for s in result.get("segments", [])
    ]

    # Retourner la transcription + lien vers le fichier audio
    return jsonify({
        "text": result["text"],
        "segments": segments,
         # endpoint statique
    })

# Endpoint pour servir l'audio
@app.route("/audio")
def serve_audio():
    return send_file("D:/stories/new stories/thatsnothow.wav", mimetype="audio/wav")

if __name__ == "__main__":
    app.run(debug=True)
