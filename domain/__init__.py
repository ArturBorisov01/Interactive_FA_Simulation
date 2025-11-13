# ============================================================================
# domain/__init__.py
# ============================================================================
"""
Domain Layer (Бизнес-логика)
Содержит модели и логику конечного автомата
"""

from .transition import Transition
from .finite_automaton import MooreAutomaton

__all__ = ['Transition', 'MooreAutomaton']
