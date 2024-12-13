from functools import cache
import torchaudio

import torch
from torch import Tensor
import matplotlib.pyplot as plt


@cache
def load_audio(audio_path: str):
    if audio_path.endswith('.mp3'):
        audio, sr = torchaudio.load(audio_path, backend='sox')
    elif audio_path.endswith('.wav'):
        audio, sr = torchaudio.load(audio_path)
    else:
        raise Exception()
    return audio, sr


def string_to_tensor(input_string):
    # 将字符串转换为字节
    byte_array = input_string.encode('utf-8')
    
    # 将每个字节转换为二进制字符串并拼接
    binary_string = ''.join(f'{byte:08b}' for byte in byte_array)

    # 确保总长度为16，如果不足则补零，多余的部分截断
    if len(binary_string) < 16:
        binary_string = binary_string.ljust(16, '0')  # 在末尾补零
    elif len(binary_string) > 16:
        binary_string = binary_string[:16]  # 截断到16位

    # 将二进制字符串转换为 Tensor
    tensor = torch.tensor([[int(bit) for bit in binary_string]], dtype=torch.int32)

    return tensor

def tensor_to_string(tensor: Tensor):
    # 确保输入是长度为 16 的 Tensor
    tensor = tensor.squeeze(0)
    if tensor.size(0) != 16:
        raise ValueError("Input tensor must have a length of 16.")
    
    # 将 Tensor 转换为字符串
    binary_string = ''.join(str(bit.item()) for bit in tensor)

    # 分割为字节（每 8 位一个字节）
    bytes_array = [binary_string[i:i+8] for i in range(0, 16, 8)]

    # 将每个字节转换为字符
    characters = [chr(int(byte, 2)) for byte in bytes_array]

    # 拼接回字符串
    result_string = ''.join(characters)

    return result_string



def plot_waveform_and_specgram(waveform, sample_rate, title):
    waveform = waveform.squeeze().detach().cpu().numpy()

    num_frames = waveform.shape[-1]
    time_axis = torch.arange(0, num_frames) / sample_rate

    plt.figure(figsize=(20, 6))
    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(time_axis, waveform, linewidth=1)
    ax1.grid(True)
    ax2.specgram(waveform, Fs=sample_rate)

    figure.suptitle(f"{title} - Waveform and specgram")
    return figure