from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from domain.finite_automaton import MooreAutomaton

@dataclass
class LiveStep:
    step_number: int
    current_state: str
    input_symbol: str
    next_state: str
    output_symbol: Optional[str]

class LiveEditProcessor:
    def __init__(self, automaton: MooreAutomaton) -> None:
        self.automaton = automaton
        self._word: str = ""
        self._pointer: int = 0
        self._active: bool = False
        self._history: List[LiveStep] = []
        self._current_state: Optional[str] = None

    def start(self, word: str) -> dict:
        if not word:
            raise ValueError("Введите слово для live-режима.")
        initial_state = self.automaton.get_initial_state()
        if initial_state is None:
            raise ValueError("Сначала задайте начальное состояние.")
        alphabet = set(self.automaton.get_input_alphabet())
        if any(ch not in alphabet for ch in word):
            raise ValueError("Слово содержит символы вне входного алфавита.")
        self._word = word
        self._pointer = 0
        self._history.clear()
        self._current_state = initial_state
        self.automaton.current_state = initial_state
        self._active = True
        return self._build_status()

    def step(self) -> dict:
        if not self._active:
            raise ValueError("Live-режим не запущен.")
        if self._pointer >= len(self._word):
            self._active = False
            return self._build_status(finished=True)

        symbol = self._word[self._pointer]
        if self._current_state not in self.automaton.get_states():
            self._active = False
            raise ValueError("Текущее состояние было удалено из автомата.")

        transition = self.automaton.find_transition(self._current_state, symbol)
        if transition is None:
            self._active = False
            raise ValueError(f"Не найден переход δ({self._current_state}, {symbol}).")

        output_symbol = self.automaton.outputs.get(transition.to_state)
        step_info = LiveStep(
            step_number=self._pointer + 1,
            current_state=self._current_state,
            input_symbol=symbol,
            next_state=transition.to_state,
            output_symbol=output_symbol
        )
        self._history.append(step_info)

        self._pointer += 1
        self._current_state = transition.to_state
        self.automaton.current_state = self._current_state
        finished = self._pointer >= len(self._word)
        if finished:
            self._active = False
        return self._build_status(last_step=step_info, finished=finished)

    def reset(self) -> None:
        self._word = ""
        self._pointer = 0
        self._history.clear()
        self._current_state = None
        self._active = False

    def _build_status(self, last_step: Optional[LiveStep] = None, finished: bool = False) -> dict:
        return {
            "word": self._word,
            "pointer": self._pointer,
            "current_state": self._current_state,
            "finished": finished,
            "last_step": last_step,
            "history": list(self._history)
        }
