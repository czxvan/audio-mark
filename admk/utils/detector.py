from audioseal import AudioSeal
import torch
from torch import Tensor
from admk.utils.attacks import AudioEffects as af

detector = AudioSeal.load_detector("audioseal_detector_16bits")

def detect_wateramrk(audio: Tensor, sr):
    audios = audio.unsqueeze(0)
    torch.manual_seed(0)
    result, message = detector.detect_watermark(
        audios, sample_rate=sr,
        message_threshold=0.5
    )
    return result, message

def get_pink_noised_audio(audio: Tensor):
    audios = audio.unsqueeze(0)
    pink_noised_audio = af.pink_noise(audios, noise_std=0.2)
    return pink_noised_audio.squeeze(0)

def get_lowpass_filtered_audio(audio: Tensor, sr=16000):
    audios = audio.unsqueeze(0)
    lowpass_filtered_audio = af.lowpass_filter(audios, cutoff_freq=5000, sample_rate=sr)
    return lowpass_filtered_audio.squeeze(0)





    