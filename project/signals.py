from PyQt6.QtWidgets import (
    QPushButton,
    QTableWidgetItem,
)
import matplotlib.pyplot as plt
from random import random
from math import log as ln
from constants import weather
from objects import (
    table,
    obj,
)

button: QPushButton = obj.objects.get('button')[0]


def start():
    clear_table()

    state: int = 0
    frequencies = [0 for k in range(len(weather))]

    days: int = obj.objects.get('spinbox')[-2].value()
    sample: int = obj.objects.get('spinbox')[-1].value()

    infinitesimal_matrix: list[list] = get_infinitesimal_matrix()
    sorted_probs: list[dict] = get_sorted_index_probs(get_probs(infinitesimal_matrix))

    for i in range(days):
        prediction: list[list] = day_predict(state, sorted_probs, infinitesimal_matrix[state][state])
        state = prediction[0][-1]
        upd_table(prediction=prediction, day=i)

    for k in range(sample):
        state = day_predict(state, sorted_probs, infinitesimal_matrix[state][state])[0][-1]
        frequencies[state] += 1

    draw_bar(frequencies=get_freq(frequencies=frequencies, sample=sample))


def get_infinitesimal_matrix() -> list[list[float]]:
    infinitesimal_matrix: list[list] = []

    count = 0
    for i in range(len(weather)):
        row: list = []
        for j in range(len(weather)):
            if i == j:
                row.append(0)
            else:
                row.append(obj.objects.get('spinbox')[count].value())
                count += 1
        row = [sum(row) * -1 if item == 0 else item for item in row]
        infinitesimal_matrix.append(row)

    return infinitesimal_matrix


def day_predict(state: int, probs: list[dict], q: float) -> list[list]:
    time: list[float] = []
    states: list[int] = []

    t: float = get_step(q)
    while t < 24:
        time.append(t)
        state = get_state(probs[state])
        states.append(state)
        t += get_step(q)

    return [states, time]


def generator() -> float:
    return random()


def get_sorted_index_probs(probs: list[list]) -> list[dict]:
    d_probs: list = []
    for i in range(len(probs)):
        d = {item[0]: item[1] for item in enumerate(probs[i])}
        d_probs.append(d)

    sorted_probs: list = []
    for i in range(len(weather)):
        sorted_probs.append(dict(sorted(d_probs[i].items(), key=lambda x: x[1])))

    return sorted_probs


def get_probs(infinitesimal_matrix: list[list]) -> list[list]:
    probs: list[list] = []

    for i in range(len(weather)):
        prob = [0 for k in range(len(weather))]
        probs.append(prob)

    for i in range(len(probs)):
        diag_el: float = infinitesimal_matrix[i][i]
        for q in enumerate(infinitesimal_matrix[i]):
            if q[0] != i:
                probs[i][q[0]] = -q[1] / diag_el

    return probs


def get_state(probs: dict) -> int:
    betta: float = generator()
    for index, prob in probs.items():
        if betta <= prob:
            return index

    return len(probs) - 1


def get_step(q: float) -> float:
    return ln(generator()) / q


def upd_table(prediction: list[list], day: int) -> None:
    count = 0
    if day != 0:
        count = day*2

    table.insertRow(count)
    table.setItem(count, 0, QTableWidgetItem('Day-' + str(day+1)))

    for index, item in enumerate(prediction[0]):
        table.setItem(count, index + 1, QTableWidgetItem(weather.get(item)))

    table.insertRow(count + 1)
    table.setItem(count + 1, 0, QTableWidgetItem('Time'))

    for index, item in enumerate(prediction[1]):
        table.setItem(count + 1, index + 1, QTableWidgetItem(str(round(item, 2))))


def clear_table() -> None:
    table.setRowCount(0)


def get_freq(frequencies: list[int], sample: int) -> list[float]:
    freq = [item / sample for item in frequencies]
    return freq


def draw_bar(frequencies: list[float]) -> None:
    names: list[str] = []
    for val in weather.values():
        names.append(val)

    width: list[int] = [1 for k in range(len(frequencies))]
    plt.bar(names, frequencies, width=width, edgecolor="k")
    plt.xlabel("Weather")
    plt.ylabel("Frequencies")
    plt.show()


button.clicked.connect(start)
