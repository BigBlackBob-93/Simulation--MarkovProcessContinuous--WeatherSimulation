from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
)
from base_object import Object
from constants import weather, Q, LEFT

obj: Object = Object()

window: QMainWindow = obj.set_obj(
    object=QMainWindow(),
    title="Simulation: Weather Simulation"
)

table: QTableWidget = obj.set_obj(
    object=QTableWidget(),
    columns=20,
    title='Weather prediction',
)
table.resizeColumnsToContents()

for index, item in weather.items():
    obj.set_obj(
        object=QLabel(window),
        title=item,
        case=0,
        above=obj.indent
    )
    left = LEFT * 4
    for i in range(len(weather)):
        if i != index:
            obj.add_obj(
                obj.set_obj(
                    object=QDoubleSpinBox(window),
                    left=left,
                    above=obj.indent + 7,
                    step=0.1,
                    value=Q[index][i],
                ),
                key='spinbox'
            )
            left += LEFT * 4
    obj.increase_indent()

obj.increase_indent()
obj.set_obj(
    object=QLabel(window),
    title='Days: ',
    case=0,
    above=obj.indent,
)
obj.add_obj(
    obj.set_obj(
        object=QSpinBox(window),
        left=100,
        above=obj.indent + 7,
        step=1,
        span=[1, 100],
    ),
    key='spinbox'
)

obj.increase_indent()
obj.set_obj(
    object=QLabel(window),
    title='Sample: ',
    case=0,
    above=obj.indent,
)
obj.add_obj(
    obj.set_obj(
        object=QSpinBox(window),
        left=100,
        above=obj.indent + 7,
        step=1000,
        span=[100, 10000000],
        value=10000,
    ),
    key='spinbox'
)

obj.increase_indent(3)
obj.add_obj(
    obj.set_obj(
        object=QPushButton(window),
        title='Predict',
        above=obj.indent,
        left=LEFT * 6
    ),
    key='button'
)
window.show()
table.show()
