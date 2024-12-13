from fastapi import APIRouter
from admk.utils.utils import load_audio, get_figure_base64, get_audio_base64

router = APIRouter()

@router.get('/api/test-figure')
def test_figure():
    audio_path = 'upload/test.wav'
    audio, sr = load_audio(audio_path)

    figure_base64 = get_figure_base64(audio, sr, title='Original audio')

    return {'figure': figure_base64}


@router.get('/api/test-audio')
def test_audio():
    audio_path = 'upload/test.wav'
    audio, sr = load_audio(audio_path)

    audio_base64 = get_audio_base64(audio, sr)

    return {'audio':  audio_base64}