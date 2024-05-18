from numpy.fft import fft
import numpy as np

def fresp(x, N, fs):
    window = np.hanning(N)
    win_data = x * window
    spectrum = 2*fft(win_data / sum(window))
    psd = 10 * np.log10(np.abs(spectrum ** 2))

    f = np.arange(0, N/2, 1) * fs / N
    X = psd[:N/2]

    return (f, X)