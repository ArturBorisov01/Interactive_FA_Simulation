# ============================================================================
# ui/panels/base_panel.py - Базовый класс для панелей
# ============================================================================
import tkinter as tk

class BasePanel(tk.Frame):
    """Базовый класс для всех панелей (Template Method pattern)"""
    
    def __init__(self, parent, state_manager, service, **kwargs):
        super().__init__(parent, **kwargs)
        self.state_manager = state_manager
        self.service = service
        
        # Подписываемся на изменения состояния
        self.state_manager.subscribe(self)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Шаблонный метод - переопределяется в подклассах"""
        raise NotImplementedError
    
    def on_state_changed(self, event_type: str, data=None):
        """Обработчик изменения состояния - переопределяется в подклассах"""
        pass

