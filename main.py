# ============================================================================
# main.py - Точка входа в приложение
# ============================================================================
import tkinter as tk
from domain.finite_automaton import MooreAutomaton
from services.automaton_service import AutomatonService
from services.state_manager import StateManager
from ui.main_window import MainWindow


def main():
    """Главная функция приложения"""
    # Создаём корневое окно
    root = tk.Tk()
    
    # Создаём слои приложения (Dependency Injection)
    automaton = MooreAutomaton()               # Domain Layer
    service = AutomatonService(automaton)      # Service Layer
    state_manager = StateManager(automaton)    # State Management
    
    # Создаём UI и передаём зависимости
    app = MainWindow(root, state_manager, service)
    
    # Запускаем главный цикл
    root.mainloop()


if __name__ == "__main__":
    main()

# ============================================================================
# СТРУКТУРА ПРОЕКТА (создайте эти файлы):
# ============================================================================
"""
project_avt/
│
├── main.py                          # ← Этот файл
│
├── domain/                          # Бизнес-логика (Domain Layer)
│   ├── __init__.py
│   ├── finite_automaton.py         # Класс MooreAutomaton
│   └── transition.py               # Класс Transition
│
├── services/                        # Сервисный слой (Application Layer)
│   ├── __init__.py
│   ├── automaton_service.py        # Бизнес-операции
│   └── state_manager.py            # Управление состоянием (Observer)
│
├── ui/                              # Представление (Presentation Layer)
│   ├── __init__.py
│   ├── main_window.py              # Главное окно
│   ├── graph_drawing.py            # GraphCanvas (без изменений)
│   │
│   └── panels/                     # Панели UI
│       ├── __init__.py
│       ├── base_panel.py           # Базовый класс панелей
│       ├── edge_panel.py           # Панель управления рёбрами
│       ├── analysis_panel.py       # Панель анализа
│       └── visualization_panel.py  # Панель визуализации
│
└── utils/                           # Утилиты (опционально)
    ├── __init__.py
    └── validators.py               # Валидаторы (для будущего)
"""
