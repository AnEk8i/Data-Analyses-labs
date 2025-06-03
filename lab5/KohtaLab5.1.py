import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_show_noise = True
init_filter_cutoff = 2.0
init_show_filtered = True

x = np.linspace(0, 2 * np.pi, 1000)
current_noise = None
noise_changed = False


def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    global current_noise
    global noise_changed
    y_clean = amplitude * np.sin(frequency * x + phase)
    if current_noise is None or noise_changed:
        current_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), size=x.shape)
        noise_changed = False
    return y_clean + current_noise if show_noise else y_clean, y_clean


def filter(data, cutoff, fs=1000, order=4):
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    b, a = butter(order, norm_cutoff, btype='low', analog=False)
    y_filtered = filtfilt(b, a, data)
    return y_filtered


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.55)
y_noisy, y_clean = harmonic_with_noise(init_amplitude, init_frequency, init_phase,
                                       init_noise_mean, init_noise_cov, init_show_noise)

line_noisy, = ax.plot(x, y_noisy, label="Гармоніка з шумом")
line_clean, = ax.plot(x, y_clean, label="Чиста гармоніка", linestyle="--", alpha=0.5)
line_filtered, = ax.plot(x, filter(y_noisy, init_filter_cutoff), label="Фільтрована", color='green')

ax.set_ylim(-3, 3)
ax.legend(loc="upper right")
ax.set_title("Гармоніка з шумом, чиста та фільтрована")

axamp = plt.axes([0.25, 0.45, 0.65, 0.03])
axfreq = plt.axes([0.25, 0.40, 0.65, 0.03])
axphase = plt.axes([0.25, 0.35, 0.65, 0.03])
axnmean = plt.axes([0.25, 0.30, 0.65, 0.03])
axncov = plt.axes([0.25, 0.25, 0.65, 0.03])
axcutoff = plt.axes([0.25, 0.20, 0.65, 0.03])

samp = Slider(axamp, 'Амплітуда', 0.1, 5.0, valinit=init_amplitude)
sfreq = Slider(axfreq, 'Частота', 0.1, 5.0, valinit=init_frequency)
sphase = Slider(axphase, 'Фаза', -np.pi, np.pi, valinit=init_phase)
snmean = Slider(axnmean, 'Середнє шуму', -1.0, 1.0, valinit=init_noise_mean)
sncov = Slider(axncov, 'Дисперсія шуму', 0.01, 1.0, valinit=init_noise_cov)
scutoff = Slider(axcutoff, 'Частота зрізу', 0.1, 10.0, valinit=init_filter_cutoff)

check_ax = plt.axes([0.025, 0.5, 0.15, 0.15])
check = CheckButtons(check_ax, ['Шум', 'Фільтр'], [init_show_noise, init_show_filtered])

reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(reset_ax, 'Reset', color='lightgoldenrodyellow')


def update(val):
    show_noise, show_filtered = check.get_status()
    y_noisy, y_clean = harmonic_with_noise(samp.val, sfreq.val, sphase.val,
                                           snmean.val, sncov.val, show_noise)
    line_noisy.set_ydata(y_noisy)
    line_clean.set_ydata(y_clean)
    if show_filtered:
        line_filtered.set_ydata(filter(y_noisy, scutoff.val))
        line_filtered.set_visible(True)
    else:
        line_filtered.set_visible(False)
    fig.canvas.draw_idle()


samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
scutoff.on_changed(update)


def on_noise_change(val):
    global noise_changed
    noise_changed = True
    update(val)


snmean.on_changed(on_noise_change)
sncov.on_changed(on_noise_change)

check.on_clicked(update)


def reset(event):
    samp.reset()
    sfreq.reset()
    sphase.reset()
    snmean.reset()
    sncov.reset()
    scutoff.reset()

    global current_noise
    global noise_changed
    current_noise = None
    noise_changed = True

    if not check.get_status()[0]: check.set_active(0)
    if not check.get_status()[1]: check.set_active(1)

    update(None)


button.on_clicked(reset)

plt.show()
