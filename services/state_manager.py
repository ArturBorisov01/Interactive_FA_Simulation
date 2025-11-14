# ============================================================================
# services/state_manager.py
# ============================================================================
"""
Менеджер состояния приложения
Реализует паттерн Observer для уведомления UI об изменениях
"""

from typing import Any, Callable
from domain.finite_automaton import MooreAutomaton
from services.live_edit_processor import LiveEditProcessor


class StateManager:
    """
    Управление состоянием приложения (Observer pattern)
    Уведомляет подписчиков об изменениях в автомате
    """
    
    def __init__(self, automaton: MooreAutomaton):
        """
        Args:
            automaton: Экземпляр конечного автомата
        """
        self.automaton = automaton
        self._observers = []
        self.live_processor = LiveEditProcessor(automaton)
    
    def subscribe(self, observer: Any) -> None:
        """
        Подписать наблюдателя на изменения
        
        Args:
            observer: Объект с методом on_state_changed(event_type, data)
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: Any) -> None:
        """
        Отписать наблюдателя
        
        Args:
            observer: Объект для отписки
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: Any = None) -> None:
        """
        Уведомить всех наблюдателей об изменении
        
        Args:
            event_type: Тип события ('transition_added', 'cleared', и т.д.)
            data: Дополнительные данные о событии
        """
        for observer in self._observers:
            if hasattr(observer, 'on_state_changed'):
                try:
                    observer.on_state_changed(event_type, data)
                except Exception as e:
                    print(f"Ошибка в наблюдателе {observer}: {e}")
    
    # === Методы-обёртки с уведомлениями ===
    
    def add_transition(self, from_state: str, input_symbol: str, 
                      output_symbol: str, to_state: str) -> None:
        """
        Добавить переход с уведомлением (ИСПРАВЛЕНО)
        """
        
        # 1. Добавляем состояния (узлы). 
        # Логика Мура: выход (output_symbol) привязывается к состоянию.
        # Судя по вашему коду process_symbol, выход генерирует КОНЕЧНОЕ состояние.
        # Поэтому 'B' (output_symbol) мы присваиваем 'q(t+1)' (to_state).
        self.automaton.add_state(from_state) # Добавляем q(t)
        self.automaton.add_state(to_state, output=output_symbol) # Добавляем q(t+1) с выходом B
        
        # 2. Добавляем сам переход (3 аргумента)
        try:
            self.automaton.add_transition(from_state, to_state, input_symbol)
        except ValueError as e:
            print(f"Ошибка при добавлении перехода: {e}")
            return # Не уведомлять, если переход не удался
        
        # 3. Уведомляем
        self.notify('transition_added', {
            'from_state': from_state,
            'input_symbol': input_symbol,
            'output_symbol': output_symbol,
            'to_state': to_state
        })
    
    def remove_transition(self, index: int) -> Any:
        """
        Удалить переход с уведомлением
        
        Args:
            index: Индекс перехода для удаления
            
        Returns:
            Удалённый переход или None
        """
        removed = self.automaton.remove_transition(index)
        if removed:
            self.notify('transition_removed', {'index': index, 'transition': removed})
        return removed
    
    def remove_state(self, state: str) -> bool:
        """
        Удаляет состояние вместе со связанными переходами и сбрасывает live-режим.
        Returns:
            bool: True, если состояние существовало и было удалено.
        """
        removed = self.automaton.remove_state(state)
        if removed:
            self.live_processor.reset()
            self.notify('state_removed', state)
        return removed

    
    def clear_all(self) -> None:
        """Очистить всё с уведомлением"""
        self.automaton.clear_transitions()
        self.live_processor.reset()
        self.notify('cleared')
    
    def set_initial_state(self, state: str) -> None:
        """
        Устанавливает вершину, которая считается начальной.

        Args:
            state: имя вершины для q0

        Raises:
            ValueError: если вершины нет в автомате
        """
        self.automaton.set_initial_state(state)
        self.notify('initial_state_changed', state)

    def get_state_snapshot(self) -> dict:
        """
        Получить снимок текущего состояния автомата
        
        Returns:
            dict: Полное состояние автомата для сохранения/восстановления
        """
        transitions = [t.to_tuple() for t in self.automaton.get_transitions()]
        initial_state = self.automaton.get_initial_state()
        
        return {
            'transitions': transitions,
            'initial_state': initial_state
        }
    
    def restore_state_snapshot(self, snapshot: dict) -> None:
        """
        Восстановить состояние автомата из снимка
        
        Args:
            snapshot: Снимок состояния из get_state_snapshot()
        """
        self.automaton.clear_transitions()
        
        for from_state, input_sym, output_sym, to_state in snapshot.get('transitions', []):
            self.automaton.add_transition(from_state, input_sym, output_sym, to_state)
        
        initial_state = snapshot.get('initial_state')
        if initial_state:
            state, symbol = initial_state
            try:
                self.automaton.set_initial_state(state, symbol)
            except ValueError:
                pass  # Игнорируем если состояние невалидно
        
        self.notify('state_restored', snapshot)

    # services/state_manager.py:118
    def create_default_graph(self) -> None:
        """Автозаполнение автомата базовым графом при запуске."""
        if self.automaton.get_transitions():
            return
        default_edges = [
            ("1", "1", "1", "1"),
            ("1", "0", "1", "2"),
            ("2", "1", "1", "3"),
            ("2", "0", "1", "2"),
            ("3", "1", "1", "1"),
            ("3", "0", "1", "3")
        ]
        for from_state, input_sym, output_sym, to_state in default_edges:
            self.add_transition(from_state, input_sym, output_sym, to_state)
        try:
            self.set_initial_state("1")
        except ValueError:
            pass

    def start_live_edit(self, word: str) -> dict:
        status = self.live_processor.start(word)
        self.notify('live_edit_started', status)
        return status

    def advance_live_edit(self) -> dict:
        status = self.live_processor.step()
        self.notify('live_edit_step', status)
        return status

    def reset_live_edit(self) -> None:
        self.live_processor.reset()
        self.notify('live_edit_reset')
