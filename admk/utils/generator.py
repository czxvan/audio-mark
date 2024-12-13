from audioseal import AudioSeal
from torch import Tensor
import torch

model = AudioSeal.load_generator("audioseal_wm_16bits")

def get_watermark(audio: Tensor, sr, message: Tensor):
    audios = audio.unsqueeze(0)
    torch.manual_seed(0)
    watermark = model.get_watermark(audios, sample_rate=sr, message=message)
    return watermark.squeeze(0)

def get_watermarked_audio(audio: Tensor, sr, message: Tensor):
    watermark = get_watermark(audio, sr, message)
    watermarked_audio = audio + watermark
    return watermarked_audio
