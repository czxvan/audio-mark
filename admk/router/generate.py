import os
import shutil

from fastapi import APIRouter, UploadFile, File, Request
from pydub import AudioSegment

from admk.config import UPLOAD, DEFAULT_MARK
from admk.utils.utils import load_audio, get_figure_base64, get_audio_base64, \
                             string_to_tensor, tensor_to_string
from admk.utils.generator import get_watermark, get_watermarked_audio

router = APIRouter()


"""
    upload original audio and store its path into session['audio_path']
"""

@router.post('/api/generate/upload')
def upload(request: Request, file: UploadFile = File(...)):
    # 保存上传文件
    original_path = os.path.join(UPLOAD, file.filename)
    with open(original_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    # 检查文件格式并转换
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext != '.wav':
        # 构建新的wav文件路径
        wav_filename = os.path.splitext(file.filename)[0] + '.wav'
        wav_path = os.path.join(UPLOAD, wav_filename)

        # 转换为wav格式
        audio = AudioSegment.from_file(original_path)
        audio.export(wav_path, format='wav')

        # 删除原始文件
        os.remove(original_path)

        # 更新路径
        audio_path = wav_path
    else:
        audio_path = original_path

    request.session['audio_path'] = audio_path
    return {
        "status": "success",
        "audio_path": audio_path
    }


"""
    return figure
"""

@router.get('/api/generate/audio')
def generate_audio(request: Request):
    if not request.session.get('audio_path'):
        return "please upload audio first"
    audio_path = request.session['audio_path']
    audio, sr = load_audio(audio_path)

    figure_base64 = get_figure_base64(audio, sr, title='Original Audio')
    audio_base64 = get_audio_base64(audio, sr)
    return {
        'figure': figure_base64,
        'audio': audio_base64
    }


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

    figure_base64 = get_figure_base64(watermark, sr, title='Watermark')
    audio_base64 = get_audio_base64(watermark, sr)
    return {
        'figure': figure_base64,
        'audio': audio_base64,
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

    figure_base64 = get_figure_base64(watermarker_audio, sr, title='Watermarked Audio')
    audio_base64 = get_audio_base64(watermarker_audio, sr)

    return {
        'figure': figure_base64,
        'audio': audio_base64,
        'message_s': message_s,
        'message': message.squeeze().tolist()
    }