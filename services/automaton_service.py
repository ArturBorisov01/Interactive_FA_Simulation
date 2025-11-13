# ============================================================================
# services/automaton_service.py
# ============================================================================
"""
Сервис для работы с автоматом
Содержит валидацию, форматирование и бизнес-операции
"""

from typing import Tuple
from domain.finite_automaton import MooreAutomaton


class AutomatonService:
    """Сервис для бизнес-логики работы с автоматом"""
    
    def __init__(self, automaton: MooreAutomaton):
        """
        Args:
            automaton: Экземпляр конечного автомата
        """
        self.automaton = automaton
    
    def validate_transition(self, from_state: str, input_symbol: str, 
                          output_symbol: str, to_state: str) -> Tuple[bool, str]:
        """
        Валидация перехода перед добавлением
        
        Args:
            from_state: Начальное состояние
            input_symbol: Входной символ
            output_symbol: Выходной символ
            to_state: Конечное состояние
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        # Проверка на пустые поля
        if not all([from_state, input_symbol, output_symbol, to_state]):
            return False, "Все поля должны быть заполнены"
        
        # Проверка на дубликаты (для детерминированности)
        existing = self.automaton.find_transition(from_state, input_symbol)
        if existing:
            return False, f"Переход из '{from_state}' по символу '{input_symbol}' уже существует"
        
        return True, ""
    
    def get_automaton_info(self) -> dict:
        """
        Получить полную информацию об автомате
        
        Returns:
            dict: Словарь с информацией о состояниях, алфавитах и свойствах автомата
        """
        return {
            'states': sorted(self.automaton.get_states()),
            'input_alphabet': sorted(self.automaton.get_input_alphabet()),
            'output_alphabet': sorted(self.automaton.get_output_alphabet()),
            'transitions_count': len(self.automaton.get_transitions()),
            'is_deterministic': self.automaton.is_deterministic(),
            'is_complete': self.automaton.is_complete(),
            'has_initial_state': self.automaton.get_initial_state() is not None
        }
    
    def format_process_result(self, result: dict) -> str:
        """
        Форматировать результат обработки слова для отображения
        
        Args:
            result: Результат обработки слова из automaton.process_word()
            
        Returns:
            str: Отформатированная строка для отображения пользователю
        """
        if not result['success']:
            # Форматирование ошибки
            output = f"❌ ОШИБКА: {result['error']}\n"
            output += "=" * 40 + "\n\n"
            
            if result['steps']:
                output += "Выполненные шаги:\n"
                for step in result['steps']:
                    output += f"Шаг {step['step_number']}: "
                    output += f"q={step['current_state']}, вход={step['input_symbol']} "
                    output += f"→ выход={step['output_symbol']}, "
                    output += f"q'={step['next_state']}\n"
                output += f"\nЧастичный результат: {result['output_word']}\n"
            return output
        
        # Форматирование успешного результата
        output = "✅ УСПЕШНАЯ ОБРАБОТКА\n"
        output += "=" * 40 + "\n\n"
        output += "Пошаговая обработка:\n"
        
        for step in result['steps']:
            output += f"Шаг {step['step_number']}: "
            output += f"q={step['current_state']}, вход={step['input_symbol']} "
            output += f"→ выход={step['output_symbol']}, "
            output += f"q'={step['next_state']}\n"
        
        output += "\n" + "=" * 40 + "\n"
        output += f"Выходное слово: {result['output_word']}\n"
        output += f"Конечное состояние: {result['final_state']}\n"
        
        return output
    
    def get_statistics(self) -> dict:
        """
        Получить статистику по автомату
        
        Returns:
            dict: Статистические данные
        """
        info = self.get_automaton_info()
        
        return {
            'total_states': len(info['states']),
            'total_transitions': info['transitions_count'],
            'input_alphabet_size': len(info['input_alphabet']),
            'output_alphabet_size': len(info['output_alphabet']),
            'is_deterministic': info['is_deterministic'],
            'is_complete': info['is_complete'],
            'completeness_percentage': self._calculate_completeness()
        }
    
    def _calculate_completeness(self) -> float:
        """
        Рассчитать процент полноты автомата
        
        Returns:
            float: Процент полноты (0.0 - 100.0)
        """
        states = self.automaton.get_states()
        alphabet = self.automaton.get_input_alphabet()
        
        if not states or not alphabet:
            return 0.0
        
        total_needed = len(states) * len(alphabet)
        existing = 0
        
        for state in states:
            for symbol in alphabet:
                if self.automaton.find_transition(state, symbol):
                    existing += 1
        
        return (existing / total_needed) * 100 if total_needed > 0 else 0.0

