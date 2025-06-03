import streamlit as st
import numpy as np
import plotly.graph_objects as go


def generate_signal(amplitude, frequency, phase, x):
    return amplitude * np.sin(frequency * x + phase)


def filter(signal, window_size):
    signal: np.ndarray
    window_size: int
    filtered = np.zeros_like(signal)
    half_window = window_size // 2
    for i in range(len(signal)):
        start = max(0, i - half_window)
        end = min(len(signal), i + half_window + 1)
        window_values = signal[start:end]
        filtered[i] = sum(window_values) / len(window_values)
    return filtered


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
    window = st.slider("Вікно фільтра", 1, 50, 10)

    show_noise = st.checkbox("Показати шум", value=True)
    show_filtered = st.checkbox("Показати фільтрований", value=True)

x = np.linspace(0, 2 * np.pi, 1000)
pure = generate_signal(amp, freq, phase, x)

if "noise_state" not in st.session_state or st.session_state.noise_params != (mean, var):
    st.session_state.noise_state = np.random.normal(mean, np.sqrt(var), 1000)
    st.session_state.noise_params = (mean, var)

noisy = pure + st.session_state.noise_state if show_noise else pure
filtered = filter(noisy, window) if show_filtered else None

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=pure, name="Чистий графік"))
fig.add_trace(go.Scatter(x=x, y=noisy, name="З шумом"))
if show_filtered:
    fig.add_trace(go.Scatter(x=x, y=filtered, name="Фільтрований"))

fig.update_layout(title="Сигнали")
st.plotly_chart(fig, use_container_width=True)