# ============================================================================
# services/state_manager.py
# ============================================================================
"""State management layer for the Moore automaton."""

from typing import Any
from domain.finite_automaton import MooreAutomaton
from services.live_edit_processor import LiveEditProcessor


class StateManager:
    """Keeps the automaton and the UI in sync (Observer pattern)."""

    def __init__(self, automaton: MooreAutomaton):
        self.automaton = automaton
        self._observers: list[Any] = []
        self.live_processor = LiveEditProcessor(automaton)
        self._undo_stack: list[dict] = []
        self._redo_stack: list[dict] = []
        self._history_limit = 50
        self._history_suspended = False
        self._notify_history()

    # ---------------------------------------------------------------------
    # Observer helpers
    # ---------------------------------------------------------------------
    def subscribe(self, observer: Any) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: Any) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: str, data: Any = None) -> None:
        for observer in self._observers:
            if hasattr(observer, "on_state_changed"):
                try:
                    observer.on_state_changed(event_type, data)
                except Exception as exc:
                    print(f"Observer error for {observer}: {exc}")

    # ---------------------------------------------------------------------
    # History helpers
    # ---------------------------------------------------------------------
    def _history_status(self) -> dict:
        return {
            "can_undo": bool(self._undo_stack),
            "can_redo": bool(self._redo_stack),
        }

    def _notify_history(self) -> None:
        self.notify("history_changed", self._history_status())

    def _push_history_snapshot(self) -> None:
        if self._history_suspended:
            return
        self._undo_stack.append(self.get_state_snapshot())
        if len(self._undo_stack) > self._history_limit:
            self._undo_stack.pop(0)
        self._redo_stack.clear()
        self._notify_history()

    def _reset_history(self) -> None:
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._notify_history()

    # ---------------------------------------------------------------------
    # Automaton mutations
    # ---------------------------------------------------------------------
    def add_transition(self, from_state: str, input_symbol: str,
                       output_symbol: str, to_state: str) -> None:
        self._push_history_snapshot()
        self.automaton.add_state(from_state)
        self.automaton.add_state(to_state, output=output_symbol)
        try:
            self.automaton.add_transition(from_state, to_state, input_symbol)
        except ValueError as exc:
            print(f"Cannot add transition: {exc}")
            return
        self.notify("transition_added", {
            "from_state": from_state,
            "input_symbol": input_symbol,
            "output_symbol": output_symbol,
            "to_state": to_state,
        })

    def remove_transition(self, index: int):
        if index < 0 or index >= len(self.automaton.transitions):
            return None
        self._push_history_snapshot()
        removed = self.automaton.remove_transition(index)
        if removed:
            self.notify("transition_removed", {"index": index, "transition": removed})
        return removed

    def remove_state(self, state: str) -> bool:
        if state not in self.automaton.get_states():
            return False
        self._push_history_snapshot()
        removed = self.automaton.remove_state(state)
        if removed:
            self.notify("state_removed", state)
        return removed

    def clear_all(self) -> None:
        if not self.automaton.get_states() and not self.automaton.get_transitions():
            self.live_processor.reset()
            return
        self._push_history_snapshot()
        self.automaton.clear_transitions()
        self.live_processor.reset()
        self.notify("cleared")

    def set_initial_state(self, state: str) -> None:
        current = self.automaton.get_initial_state()
        if current == state:
            return
        self._push_history_snapshot()
        self.automaton.set_initial_state(state)
        self.notify("initial_state_changed", state)

    # ---------------------------------------------------------------------
    # Snapshots
    # ---------------------------------------------------------------------
    def _capture_snapshot(self) -> dict:
        outputs = self.automaton.get_outputs()
        transitions = []
        for from_state, symbol, to_state in self.automaton.get_transitions():
            transitions.append({
                "from_state": from_state,
                "input_symbol": symbol,
                "to_state": to_state,
            })
        return {
            "states": list(self.automaton.get_states()),
            "outputs": outputs,
            "transitions": transitions,
            "initial_state": self.automaton.get_initial_state(),
        }

    def get_state_snapshot(self) -> dict:
        return self._capture_snapshot()

    def restore_state_snapshot(self, snapshot: dict) -> None:
        if not snapshot:
            return
        self._history_suspended = True
        try:
            self.automaton.clear_transitions()
            outputs = snapshot.get("outputs", {})
            for state in snapshot.get("states", []):
                self.automaton.add_state(state, output=outputs.get(state))
            for item in snapshot.get("transitions", []):
                from_state = item.get("from_state")
                to_state = item.get("to_state")
                symbol = item.get("input_symbol")
                if from_state is None or to_state is None or symbol is None:
                    continue
                try:
                    self.automaton.add_transition(from_state, to_state, symbol)
                except ValueError:
                    pass
            initial_state = snapshot.get("initial_state")
            if initial_state:
                try:
                    self.automaton.set_initial_state(initial_state)
                except ValueError:
                    pass
            else:
                self.automaton.initial_state = None
                self.automaton.current_state = None
            self.live_processor.reset()
        finally:
            self._history_suspended = False
        self.notify("state_restored", snapshot)
        self.notify("live_edit_reset")

    # ---------------------------------------------------------------------
    # Bootstrapping
    # ---------------------------------------------------------------------
    def create_default_graph(self) -> None:
        if self.automaton.get_transitions():
            return
        previous = self._history_suspended
        self._history_suspended = True
        default_edges = [
            ("1", "1", "1", "1"),
            ("1", "0", "1", "2"),
            ("2", "1", "1", "3"),
            ("2", "0", "1", "2"),
            ("3", "1", "1", "1"),
            ("3", "0", "1", "3"),
        ]
        try:
            for from_state, input_sym, output_sym, to_state in default_edges:
                self.add_transition(from_state, input_sym, output_sym, to_state)
            try:
                self.set_initial_state("1")
            except ValueError:
                pass
        finally:
            self._history_suspended = previous
        self._reset_history()

    # ---------------------------------------------------------------------
    # Live edit controls
    # ---------------------------------------------------------------------
    def start_live_edit(self, word: str) -> dict:
        status = self.live_processor.start(word)
        self.notify("live_edit_started", status)
        return status

    def advance_live_edit(self) -> dict:
        status = self.live_processor.step()
        self.notify("live_edit_step", status)
        return status

    def reset_live_edit(self) -> None:
        self.live_processor.reset()
        self.notify("live_edit_reset")

    # ---------------------------------------------------------------------
    # Undo / Redo API
    # ---------------------------------------------------------------------
    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        snapshot = self._undo_stack.pop()
        self._redo_stack.append(self.get_state_snapshot())
        if len(self._redo_stack) > self._history_limit:
            self._redo_stack.pop(0)
        self.restore_state_snapshot(snapshot)
        self._notify_history()
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        snapshot = self._redo_stack.pop()
        self._undo_stack.append(self.get_state_snapshot())
        if len(self._undo_stack) > self._history_limit:
            self._undo_stack.pop(0)
        self.restore_state_snapshot(snapshot)
        self._notify_history()
        return True

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def get_history_status(self) -> dict:
        return self._history_status()
