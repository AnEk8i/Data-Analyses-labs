import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import butter, filtfilt


def generate_signal(amplitude, frequency, phase, x):
    return amplitude * np.sin(frequency * x + phase)


def filter(signal, cutoff_freq, fs=1000, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, signal)


st.set_page_config("Графік з шумом", layout="wide")

with st.sidebar:
    st.header("Сигнал")
    amp = st.slider("Амплітуда", 0.1, 5.0, 1.0)
    freq = st.slider("Частота", 0.1, 5.0, 1.0)
    phase = st.slider("Фаза", -np.pi, np.pi, 0.0, step=0.1)

    st.header("Шум")
    mean = st.slider("Середнє", -1.0, 1.0, 0.0)
    var = st.slider("Дисперсія", 0.01, 1.0, 0.1)

    st.header("Фільтр")
    cutoff = st.slider("Частота зрізу (Гц)", 0.01, 2.5, 0.5)
    order = st.slider("Порядок фільтра", 1, 10, 4)

    show_noise = st.checkbox("Показати шум", value=True)
    show_filtered = st.checkbox("Показати фільтрований", value=True)

x = np.linspace(0, 2 * np.pi, 1000)
pure = generate_signal(amp, freq, phase, x)

if "noise_state" not in st.session_state or st.session_state.noise_params != (mean, var):
    st.session_state.noise_state = np.random.normal(mean, np.sqrt(var), size=x.shape)
    st.session_state.noise_params = (mean, var)

noisy = pure + st.session_state.noise_state if show_noise else pure
filtered = filter(noisy, cutoff) if show_filtered else None

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=pure, name="Чистий графік"))
fig.add_trace(go.Scatter(x=x, y=noisy, name="З шумом"))
if show_filtered:
    fig.add_trace(go.Scatter(x=x, y=filtered, name="Фільтрований"))

fig.update_layout(title="Сигнали")
st.plotly_chart(fig, use_container_width=True)