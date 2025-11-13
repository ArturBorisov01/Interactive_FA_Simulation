# Класс для переходов
"""
Модуль: transition.py
Назначение: Описывает переход между состояниями автомата
"""

class Transition:
    def __init__(self, from_state, to_state, symbol):
        self.from_state = from_state
        self.to_state = to_state
        self.symbol = symbol

    def __repr__(self):
        return f"{self.from_state} --{self.symbol}--> {self.to_state}"
