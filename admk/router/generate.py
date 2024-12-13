import os
import shutil

from fastapi import APIRouter, UploadFile, File, Request
import torchaudio

from admk.config import UPLOAD, DEFAULT_MARK
from admk.utils.utils import load_audio, plot_waveform_and_specgram, string_to_tensor, tensor_to_string
from admk.utils.generator import get_watermark, get_watermarked_audio

router = APIRouter()


"""
    upload original audio and store its path into session['audio_path']
"""

@router.post('/api/generate/upload')
def upload(request: Request, file: UploadFile = File(...)):
    audio_path = os.path.join(UPLOAD, file.filename)
    with open(os.path.join(UPLOAD, file.filename), 'wb') as f:
        shutil.copyfileobj(file.file, f)

    request.session['audio_path'] = audio_path

    return {"audio_path": audio_path}


"""
    return figure
"""

@router.get('/api/generate/audio')
def generate_audio(request: Request):
    if not request.session.get('audio_path'):
        return "please upload audio first"
    audio_path = request.session['audio_path']
    audio, sr = load_audio(audio_path)

    figure = plot_waveform_and_specgram(audio, sr, title='Original audio')
    figure.savefig('result/original-audio.png')
    return {'figure': "original-audio.png"}


@router.get('/api/generate/watermark/{message_s:path}')
def generate_watermark(request: Request, message_s):
    if not request.session.get('audio_path'):
        return "please upload audio first"
    if not message_s:
        message_s=DEFAULT_MARK

    audio_path = request.session['audio_path']
    audio, sr = load_audio(audio_path)

    message = string_to_tensor(message_s)
    watermark = get_watermark(audio, sr, message)

    figure = plot_waveform_and_specgram(watermark, sr, title='watermark')
    figure.savefig('result/watermark.png')
    return {
        'figure': "watermark.png",
        'message_s': message_s,
        'message': message.squeeze().tolist()
    }


@router.get('/api/generate/watermarked-audio/{message_s:path}')
def generate_watermarked_audio(request: Request, message_s):
    if not request.session.get('audio_path'):
        return "please upload audio first"
    if not message_s:
        message_s=DEFAULT_MARK

    audio_path = request.session['audio_path']
    audio, sr = load_audio(audio_path)

    message = string_to_tensor(message_s)
    watermarker_audio = get_watermarked_audio(audio, sr, message)

    figure = plot_waveform_and_specgram(watermarker_audio, sr, title='Watermarked audio')
    figure.savefig('result/watermarked-audio.png')
    
    watermarker_audio_path = 'upload/watermarked-audio.wav'
    torchaudio.save(watermarker_audio_path, watermarker_audio, sr)

    return {
        'figure': "watermarked-audio.png",
        'watermarked-audio':  watermarker_audio_path,
        'message_s': message_s,
        'message': message.squeeze().tolist()
    }