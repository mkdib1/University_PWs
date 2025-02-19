import pandas as pd
from xgboost import XGBClassifier
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Concatenate

from scipy.signal import find_peaks, spectrogram, stft
from scipy.fft import rfft, rfftfreq
from librosa import zero_crossings

def peaks_properties(signal_raw):
    peaks, _ = find_peaks(signal_raw)
    num_peaks = np.float64(len(peaks))
    p2p_amplitude = np.ptp(signal_raw)*1.0
    
    return num_peaks, p2p_amplitude

def energy(signal_raw):
    e = np.sum(signal_raw**2)*1.0
    return e

def power(signal_raw):
    pow_ = np.mean(signal_raw**2)*1.0
    return pow_

def zcr(signal_raw):
    zcr_mask = zero_crossings(np.asarray(signal_raw) * 1.0, pad=False)
    zcr_sum = np.sum(zcr_mask)*1.0
    return zcr_sum

def mean_val(signal_raw):
    return np.mean(signal_raw)*1.0

def std_val(signal_raw):
    return np.std(signal_raw)*1.0


def dominant_freq(signal_raw, sampling_rate=173.61):

    fft_result = rfft(signal_raw)
    frequencies = rfftfreq(len(signal_raw), d=1/sampling_rate)
    amplitudes = np.abs(fft_result)
    idx_max = np.argmax(amplitudes)
    dom_freq = frequencies[idx_max]

    return dom_freq, fft_result, frequencies

def feats_spectrogram(signal_raw, rate=173.61):
    f, _, spec = spectrogram(signal_raw, fs=rate)
    mask = f <= 20
    spec_filtered = spec[mask, :]
    return spec_filtered.flatten()

def compute_spectrogram_from_stft(signal_raw, flat=False, filt=False, fs=173.61, nperseg=512, noverlap=64):
    f, t, Zxx = stft(signal_raw, fs=fs, nperseg=nperseg, noverlap=noverlap)
    spec = np.abs(Zxx)
    if filt:
        idx = np.where(f <= 20)[0]
        spec= spec[idx, :]
        f = f[idx]
        # t = t[idx]
    if flat:
        return spec.flatten()
    return f,t, spec

def handcr_feat_descriptor(signal_raw):
    num_peaks, p2p_amplitude  = peaks_properties(signal_raw)
    e = energy(signal_raw)
    pow_ = power(signal_raw)  
    zcr_ = zcr(signal_raw)
    mean_val_ = mean_val(signal_raw)
    std_val_ = std_val(signal_raw)
    dom_freq_,_,_ = dominant_freq(signal_raw)
    spec_ = compute_spectrogram_from_stft(signal_raw, flat=True, filt=True)
    
    return [num_peaks, p2p_amplitude, 
            e, pow_, zcr_, mean_val_, 
            std_val_, dom_freq_, *spec_]


def load_handcr_descr(signals: pd.DataFrame):
    handcr_descriptor = signals.apply(lambda row: handcr_feat_descriptor(row), axis=1, result_type='expand')
    return handcr_descriptor

def concat_lstm_handcr_feat_descriptor(signals, handcrafted_descr):
    input_neural_feat = Input(shape=(signals.shape[1], 1))
    neural_feat = LSTM(64, return_sequences=True, recurrent_dropout=0.2)(input_neural_feat)
    neural_feat = Dropout(0.2)(neural_feat)
    neural_feat = LSTM(32, return_sequences=False, recurrent_dropout=0.2)(neural_feat)
    neural_feat = Dense(64, activation='relu')(neural_feat)
    neural_feat = Dropout(0.5)(neural_feat)  
    inputs_handcrafted = Input(shape=(handcrafted_descr.shape[1],)) 
    concatenated = Concatenate()([neural_feat, inputs_handcrafted]) 
    
    feature_extractor_model = Model(inputs=[input_neural_feat, inputs_handcrafted], 
                                    outputs=concatenated)
    neural_feat_reshaped = signals.values.reshape((signals.shape[0], 
                                                       signals.shape[1],
                                                       1))
    concat_feat_descriptor = feature_extractor_model.predict([neural_feat_reshaped, 
                                                        handcrafted_descr])

    return concat_feat_descriptor

def load_mod(path: str):
    xgb_model = None
    xgb_model = XGBClassifier()
    xgb_model.load_model(path)
    return xgb_model

def extract_descriptor(signals, scaler):
    hand_descr = load_handcr_descr(signals)
    hand_descr = scaler.transform(hand_descr)
    concat_descr = concat_lstm_handcr_feat_descriptor(signals, hand_descr)
    return concat_descr 

def dict_pred(prediction):
    mapping = {
        0: "Healthy_subject_eyes_open",
        1: "Healthy_subject_eyes_closed",
        2: "Patient_opposite_hyppocampus",
        3: "Patient_epilept_zone",
        4: "Seizure"
    }
    return mapping.get(prediction, "Unknown")

def plot_eeg(file):
    try:
        df = pd.read_csv(file.name, sep=";", header=None)
        signal = df.iloc[0, :].values
        first_1000_values = signal[:1000]
        time = np.linspace(0, 23.6, 1000)
        fig, ax = plt.subplots(figsize=(18, 5))
        ax.plot(time, first_1000_values, color='b')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        
        plt.tight_layout()
        
        return fig
    except Exception as e:
        print(f"Errore durante il plotting: {str(e)}")
        return None