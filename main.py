from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'Times New Roman'  # 指定默认的字体为Arial

# 获取脚本目录下的所有.wav文件
wav_files = [f for f in os.listdir() if f.endswith(".wav")]

# 显示文件编号和文件名
for i, file in enumerate(wav_files, 1):
    print(f"{i}: {file}")

# 获取用户选择的文件编号
while True:
    choosefile = input("请输入你选择的文件的编号：")
    try:
        file_index = int(choosefile) - 1
        if 0 <= file_index < len(wav_files):
            filename = wav_files[file_index]
            break
        else:
            print("选择无效，请重新输入。")
    except ValueError:
        print("输入不是有效的数字，请重新输入。")

# 获取用户输入的标题
title = input("请输入图表标题：")

# 获取用户选择的预设编号
print("\n预设0：自行输入\n")
print("预设1：\n 傅里叶变换数据点数：16384\n 重叠样本数：12000\n")
print("预设2：\n 傅里叶变换数据点数：25600\n 重叠样本数：21600\n")


while True:
    choose = input("请输入你选择的预设的编号：")
    if choose == "0":
        while True:
            try:
                NFFT = int(float(input("请输入傅里叶变换数据点数：")))
                noverlap = int(float(input("请输入重叠样本数：")))
                if NFFT >= noverlap:
                    break
                else:
                    print("重叠样本数不能大于等于傅里叶变换数据点数，请重新输入。")
            except ValueError:
                print("输入不是有效的整数，请重新输入。")
        break
    elif choose == "1":
        NFFT = 16384
        noverlap = 12000
        break
    elif choose == "2":
        NFFT = 25600
        noverlap = 21600
        break
    else:
        print("选择无效，请重新输入。")

def check_sample_rate(filename):
    try:
        _, y = read(filename)
        sample_rate = _

        print(f"{filename}的采样率为: {sample_rate} Hz")

        return sample_rate, y

    except IOError as e:
        print(f"Error reading {filename}: {e}")
        return None, None

sample_rate, y = check_sample_rate(filename)

def plot_fft_freq_chart(filename, NFFT, noverlap, plot=True, max_display_frequency=10000):
    try:
        freqs, bins, Pxx = signal.spectrogram(y, sample_rate, nperseg=NFFT, noverlap=noverlap)

        print("Frequency array:", freqs)

        if len(freqs) == 0:
            print("Error: Empty frequency array.")
            return -1

        # 仅显示频率范围在 0 Hz 和 max_display_frequency 之间的数据
        display_mask = (freqs >= 0) & (freqs <= max_display_frequency)
        freqs_display = freqs[display_mask]
        Pxx_display = Pxx[display_mask]

        # 确保最大值的索引不超过数组的大小
        max_freq_index = np.argmax(Pxx_display)
        if max_freq_index >= len(freqs_display):
            max_freq_index = len(freqs_display) - 1
        max_freq_value = freqs_display[max_freq_index]

        print(f"Maximum amplitude frequency found at {max_freq_value} Hz")

        if plot:
            # 对数变换
            plt.figure(figsize=(12, 9), dpi=369)  # 调整图像大小和分辨
            log_spec = 10 * np.log10(Pxx_display)
            plt.ylim(2350, 2850)
            plt.xlim(12400, 13300)
            plt.imshow(log_spec, cmap='binary', aspect='auto', origin='lower', interpolation='lanczos',vmin=32,vmax=45)
            plt.title(title)
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.colorbar(label='Amplitude (dB)')
            plt.savefig('Fig1.png', dpi=369)  # 在保存时指定更高的dpi
            plt.show()

        return max_freq_value

    except IOError as e:
        print("IOError:", e)
        return -1
    except ValueError as e:
        print("ValueError:", e)
        return -1

# 绘制图表
plot_fft_freq_chart(filename, NFFT, noverlap, True, max_display_frequency=10000)
