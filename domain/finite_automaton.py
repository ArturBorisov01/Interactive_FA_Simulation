# Класс конечного автомата (Мура)
"""
Модуль: finite_automaton.py
Назначение: Определяет класс MooreAutomaton (конечный автомат Мура)
"""

from .transition import Transition

class MooreAutomaton:
    """
    Простейшая модель автомата Мура.
    Содержит состояния, переходы и выходные значения.
    """

    def __init__(self):
        self.states = []          # Список состояний
        self.transitions = []     # Список переходов (Transition)
        self.current_state = None
        self.initial_state = None 
        self.outputs = {}         # Выходы (state -> value)

    def add_state(self, name, output=None):
        """Добавляет новое состояние (ИСПРАВЛЕНО)"""
        if name not in self.states:
            self.states.append(name)
        
        # Всегда обновляем выход, если он предоставлен
        if output is not None:
            self.outputs[name] = output

    def add_transition(self, from_state, to_state, symbol):
        """Добавляет переход между состояниями"""
        if from_state in self.states and to_state in self.states:
            self.transitions.append(Transition(from_state, to_state, symbol))
        else:
            raise ValueError("Переход содержит неизвестное состояние")

    def get_transitions(self):
        """Возвращает список всех переходов"""
        return [(t.from_state, t.symbol, t.to_state) for t in self.transitions]

    def get_states(self):
        """Возвращает список всех состояний"""
        return list(self.states)

    def get_outputs(self):
        """Возвращает словарь выходных значений"""
        return dict(self.outputs)

    def set_start_state(self, state_name):
        """Устанавливает начальное состояние"""
        if state_name in self.states:
            self.current_state = state_name
        else:
            raise ValueError(f"Состояние {state_name} не найдено")

    def process_symbol(self, symbol):
        """Обрабатывает входной символ и выполняет переход"""
        for t in self.transitions:
            if t.from_state == self.current_state and t.symbol == symbol:
                self.current_state = t.to_state
                return self.outputs.get(self.current_state, None)
        return None

    def reset(self):
        """Сбрасывает автомат в начальное состояние"""
        self.current_state = self.states[0] if self.states else None

    def __repr__(self):
        return f"<MooreAutomaton states={len(self.states)} transitions={len(self.transitions)}>"

    def find_transition(self, from_state, symbol):
        """(ДОБАВЛЕНО) Ищет переход по состоянию и символу"""
        for t in self.transitions:
            if t.from_state == from_state and t.symbol == symbol:
                return t
        return None

    def remove_transition(self, index):
        """(ДОБАВЛЕНО) Удаляет переход по индексу"""
        if 0 <= index < len(self.transitions):
            return self.transitions.pop(index)
        return None

    def clear_transitions(self):
        """(ДОБАВЛЕНО) Очищает все переходы и состояния"""
        self.states = []
        self.transitions = []
        self.outputs = {}
        self.initial_state = None

    def get_input_alphabet(self):
        """(ДОБАВЛЕНО) Возвращает входной алфавит"""
        return sorted(list(set(t.symbol for t in self.transitions)))

    def get_output_alphabet(self):
        """(ДОБАВЛЕНО) Возвращает выходной алфавит"""
        return sorted(list(set(self.outputs.values())))

    def get_initial_state(self):
        return self.initial_state

    def is_deterministic(self):
        """(ДОБАВЛЕНО-ЗАГЛУШКА) Проверяет детерминированность"""
        seen = set()
        for t in self.transitions:
            key = (t.from_state, t.symbol)
            if key in seen:
                return False
            seen.add(key)
        return True

    def is_complete(self):
        """(ДОБАВЛЕНО-ЗАГЛУШКА) Проверяет полноту"""
        # Упрощенная проверка
        if not self.states or not self.get_input_alphabet():
            return True # Пустой граф считаем полным
            
        input_alphabet = self.get_input_alphabet()
        for state in self.states:
            for symbol in input_alphabet:
                if self.find_transition(state, symbol) is None:
                    return False
        return True

    def get_available_inputs_for_state(self, state):
        """(ДОБАВЛЕНО) Получить доступные входы для состояния"""
        if state not in self.states:
            return []
        symbols = {t.symbol for t in self.transitions if t.from_state == state}
        return sorted(list(symbols))

    def set_initial_state(self, state):
        """(служебно) Установить только вершину начального состояния q0"""
        if state not in self.states:
            raise ValueError(f"Состояние {state} отсутствует в автомате")
        
        self.initial_state = state
        self.current_state = state

    def remove_state(self, state):
        """Удаляет состояние и все связанные с ним переходы."""
        if state not in self.states:
            return False
        self.states.remove(state)
        self.outputs.pop(state, None)
        self.transitions = [
            t for t in self.transitions
            if t.from_state != state and t.to_state != state
        ]
        if self.initial_state == state:
            self.initial_state = None
        if self.current_state == state:
            self.current_state = None
        return True
