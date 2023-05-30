from typing import Any
from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget
)
from constants import (
    LEFT,
    ABOVE,
    WIDTH,
    HEIGHT
)


class Object:
    """Class for setting form objects and keeping some important of them.

    Fields: objects: dict | functions: dict | indent: int.
    Methods: __init__() | add_obj(obj: Any, key: str) -> None | set_obj(**kwargs) -> Any |
    increase_indent(index: int = 1) -> None | get_objects() -> dict
    """

    def __init__(self):
        self.objects: dict = {
            'spinbox': [],
            'button': [],
            'label': [],
        }
        self.functions: dict = {
            QMainWindow: set_form,
            QLabel: set_label,
            QPushButton: set_button,
            QDoubleSpinBox: set_spinbox,
            QSpinBox: set_spinbox,
            QTableWidget: set_table,
        }
        self.indent: int = ABOVE

    def add_obj(self, obj: Any, key: str) -> None:
        """Add object to the objects dict"""
        self.objects.get(key).append(obj)

    def set_obj(self, **kwargs) -> Any:
        """Set form object.

        Keyword arguments:
        object  -- setting object |
        title -- visible part |
        left -- vertical indent between form objects (default XX.LEFT) |
        above -- horizontal indent between form objects (default XX.ABOVE) |
        step -- numerical value (step for QSpinBox, QDoubleSpinBox) |
        span -- list of two numerical values (range for QSpinBox, QDoubleSpinBox) |
        value -- visible part, default numerical value (for QSpinBox, QDoubleSpinBox)
        case: Any -- text stile indicator for QLable setter (None - italic, Any - bold).

        :return: object: QMainWindow | QLabel | QPushButton | QSpinBox | QDoubleSpinBox
        """
        self.functions.get(type(kwargs.get('object')))(**kwargs)
        return kwargs.get('object')

    def increase_indent(self, index: int = 1) -> None:
        """Increase vertical indent between form objects"""
        self.indent = self.indent + ABOVE * index

    def get_objects(self) -> dict:
        """Return dict of the objects"""
        return self.objects


# --------- setters ---------
def set_form(**kwargs) -> None:
    form = kwargs.get('object')
    form.setWindowTitle(kwargs.get('title'))
    form.setGeometry(350, 300, WIDTH, HEIGHT)


def set_spinbox(**kwargs) -> None:
    spin_box = kwargs.get('object')
    left = kwargs.get('left') if kwargs.get('left') is not None else LEFT
    above = kwargs.get('above') if kwargs.get('above') is not None else ABOVE
    step = kwargs.get('step') if kwargs.get('step') is not None else 1
    value = kwargs.get('value') if kwargs.get('value') is not None else 0
    span = kwargs.get('span') if kwargs.get('span') is not None else [0, 100]

    spin_box.setValue(value)
    spin_box.setFixedSize(60, 20)
    spin_box.setRange(span[0], span[1])
    spin_box.setSingleStep(step)
    spin_box.move(left, above)


def set_label(**kwargs) -> None:
    label = kwargs.get('object')
    title = kwargs.get('title')
    left = kwargs.get('left') if kwargs.get('left') is not None else LEFT
    above = kwargs.get('above') if kwargs.get('above') is not None else ABOVE

    font = label.font()
    font.setPointSize(10)
    label.setFont(font)
    label.setFixedWidth(WIDTH)

    if kwargs.get('case') is None:
        label.setText(title.upper())
    else:
        font.setItalic(True)
        label.setFont(font)
        label.setText(title)
    label.move(left, above)


def set_button(**kwargs) -> None:
    button = kwargs.get('object')
    title = kwargs.get('title')
    left = kwargs.get('left') if kwargs.get('left') is not None else LEFT
    above = kwargs.get('above') if kwargs.get('above') is not None else ABOVE

    button.setText(title.upper())
    button.move(left, above)


def set_table(**kwargs) -> None:
    table: QTableWidget = kwargs.get('object')
    columns: int = kwargs.get('columns') if kwargs.get('columns') is not None else 2
    h_headers: list[str] = kwargs.get('h_headers') if kwargs.get('h_headers') is not None else []

    table.setWindowTitle(kwargs.get('title'))
    table.setGeometry(650, 300, WIDTH*3, HEIGHT)
    table.setColumnCount(columns)
    table.setHorizontalHeaderLabels(h_headers)
