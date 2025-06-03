import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons

init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_show_noise = True

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
    return y_clean + current_noise if show_noise else y_clean


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.45)
l, = ax.plot(x, harmonic_with_noise(init_amplitude, init_frequency, init_phase,
                                    init_noise_mean, init_noise_cov, init_show_noise))
ax.set_title("Гармоніка з шумом")
ax.set_ylim(-3, 3)

axamp = plt.axes([0.25, 0.35, 0.65, 0.03])
axfreq = plt.axes([0.25, 0.30, 0.65, 0.03])
axphase = plt.axes([0.25, 0.25, 0.65, 0.03])
axnmean = plt.axes([0.25, 0.20, 0.65, 0.03])
axncov = plt.axes([0.25, 0.15, 0.65, 0.03])

samp = Slider(axamp, 'Амплітуда', 0.1, 5.0, valinit=init_amplitude)
sfreq = Slider(axfreq, 'Частота', 0.1, 5.0, valinit=init_frequency)
sphase = Slider(axphase, 'Фаза', -np.pi, np.pi, valinit=init_phase)
snmean = Slider(axnmean, 'Середнє шуму', -1.0, 1.0, valinit=init_noise_mean)
sncov = Slider(axncov, 'Дисперсія шуму', 0.01, 1.0, valinit=init_noise_cov)

check_ax = plt.axes([0.025, 0.5, 0.15, 0.15])
check = CheckButtons(check_ax, ['Шум'], [init_show_noise])

reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(reset_ax, 'Reset', color='lightgoldenrodyellow')


def update(val):
    y = harmonic_with_noise(samp.val, sfreq.val, sphase.val,
                            snmean.val, sncov.val, check.get_status()[0])
    l.set_ydata(y)
    fig.canvas.draw_idle()


def on_noise_change(val):
    global noise_changed
    noise_changed = True
    update(val)


samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
snmean.on_changed(on_noise_change)
sncov.on_changed(on_noise_change)


def on_check(label):
    update(None)


check.on_clicked(on_check)


def reset(event):
    samp.reset()
    sfreq.reset()
    sphase.reset()
    snmean.reset()
    sncov.reset()
    check.set_active(0) if not check.get_status()[0] else None
    global current_noise
    global noise_changed
    current_noise = None
    noise_changed = True
    update(None)


button.on_clicked(reset)

plt.show()
