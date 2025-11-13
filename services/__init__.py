# ============================================================================
# services/__init__.py
# ============================================================================

"""
Сервисный слой (Application Layer)
Содержит бизнес-логику и управление состоянием приложения
"""

from .automaton_service import AutomatonService
from .state_manager import StateManager

__all__ = ['AutomatonService', 'StateManager']
