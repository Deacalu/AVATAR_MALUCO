from flask import Flask, render_template, request, jsonify
import vosk
import torch
from transformers import pipeline
from gtts import gTTS
import os
import io

app = Flask(__name__)

# Atualize o caminho para o modelo baixado e extraído
model_path = "C:/projeto_avatar/models/vosk-model"
model = vosk.Model(model_path)

# Carrega o modelo de linguagem (LLM - GPT-Neo ou LLaMA)
llm = pipeline('text-generation', model="EleutherAI/gpt-neo-2.7B")


@app.route('/')
def index():
    return render_template('index.html')  # Arquivo HTML renderizado


@app.route('/api/process_audio', methods=['POST'])
def process_audio():
    audio = request.data
    rec = vosk.KaldiRecognizer(model, 16000)

    # Aceita o áudio para reconhecimento
    if rec.AcceptWaveform(audio):
        result = rec.Result()
        user_input = result['text']
    else:
        return jsonify({'error': 'Não foi possível reconhecer a fala'}), 400

    # Gera resposta com IA
    response = llm(user_input, max_length=50)[0]['generated_text']

    # Converte resposta em áudio usando gTTS
    tts = gTTS(text=response, lang='pt')
    audio_file_path = 'response.mp3'
    tts.save(audio_file_path)

    # Lê o arquivo de áudio e envia como resposta
    with open(audio_file_path, 'rb') as f:
        audio_data = f.read()

    # Remove o arquivo após o uso (opcional)
    os.remove(audio_file_path)

    return jsonify({'response': response, 'audio': audio_data.decode('latin1')})


if __name__ == '__main__':
    app.run(debug=True)
