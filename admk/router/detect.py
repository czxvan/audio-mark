import os
import shutil

from fastapi import APIRouter, UploadFile, File, Request
from pydub import AudioSegment

from admk.config import UPLOAD
from admk.utils.utils import load_audio, get_figure_base64, get_audio_base64, tensor_to_string
from admk.utils.detector import detect_wateramrk, get_pink_noised_audio, get_lowpass_filtered_audio

router = APIRouter()


"""
    upload potential watermarked audio and store its path into session
"""

@router.post('/api/detect/upload')
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

    request.session['watermarked_audio_path'] = audio_path
    return {
        "status": "success",
        "audio_path": audio_path
    }


"""
    return figure, detect result and message
"""

@router.get('/api/detect/audio')
def detect_audio(request: Request):
    if not request.session.get('watermarked_audio_path'):
        return "please upload watermarked_audio first"
    audio_path = request.session['watermarked_audio_path']
    audio, sr = load_audio(audio_path)

    result, message = detect_wateramrk(audio, sr)
    message_s = tensor_to_string(message)

    figure_base64 = get_figure_base64(audio, sr, title='Potential Watermarked Audio')
    audio_base64 = get_audio_base64(audio, sr)

    return {
        'figure': figure_base64,
        'audio': audio_base64,
        'result': result,
        'message_s': message_s,
        'message': message.squeeze().tolist()
    }

@router.get('/api/detect/pink-noised-audio')
def detect_pink_noised_audio(request: Request):
    if not request.session.get('watermarked_audio_path'):
        return "please upload watermarked_audio first"
    audio_path = request.session['watermarked_audio_path']
    audio, sr = load_audio(audio_path)

    pink_noised_audio = get_pink_noised_audio(audio)
    result, message = detect_wateramrk(pink_noised_audio, sr)
    message_s = tensor_to_string(message)
    
    figure_base64 = get_figure_base64(pink_noised_audio, sr, title='Pink Noised Audio')
    audio_base64 = get_audio_base64(pink_noised_audio, sr)

    return {
        'figure': figure_base64,
        'audio': audio_base64,
        'result': result,
        'message_s': message_s,
        'message': message.squeeze().tolist()
    }

@router.get('/api/detect/lowpass-filtered-audio')
def detect_lowpass_filtered_audio(request: Request):
    if not request.session.get('watermarked_audio_path'):
        return "please upload watermarked_audio first"
    audio_path = request.session['watermarked_audio_path']
    audio, sr = load_audio(audio_path)

    lowpass_filtered_audio = get_lowpass_filtered_audio(audio)
    result, message = detect_wateramrk(lowpass_filtered_audio, sr)
    message_s = tensor_to_string(message)

    figure_base64 = get_figure_base64(lowpass_filtered_audio, sr, title='Losspass Filtered Audio')
    audio_base64 = get_audio_base64(lowpass_filtered_audio, sr)

    return {
        'figure': figure_base64,
        'audio': audio_base64,
        'result': result,
        'message_s': message_s,
        'message': message.squeeze().tolist()
    }