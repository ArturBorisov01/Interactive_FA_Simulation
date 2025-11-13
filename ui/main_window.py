# ============================================================================
# ui/main_window.py - Главное окно (минимальная логика)
# ============================================================================

import tkinter as tk
from ui.panels.edge_panel import EdgePanel
from ui.panels.analysis_panel import AnalysisPanel
from ui.panels.visualization_panel import VisualizationPanel


class MainWindow:
    """Главное окно приложения"""
    
    def __init__(self, root, state_manager, service):
        self.root = root
        self.state_manager = state_manager
        self.service = service
        
        self._setup_window()
        self._create_layout()
    
    def _setup_window(self):
        """Настроить окно"""
        self.root.title("Визуализация графа - Автомат Мура")
        self.root.geometry("1400x700")
        self.root.configure(bg='#f0f0f0')
    
    def _create_layout(self):
        """Создать раскладку из панелей"""
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Левая панель - управление рёбрами
        self.edge_panel = EdgePanel(
            main_container, 
            self.state_manager, 
            self.service
        )
        self.edge_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Центральная панель - визуализация
        self.viz_panel = VisualizationPanel(
            main_container,
            self.state_manager,
            self.service
        )
        self.viz_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Правая панель - анализ
        self.analysis_panel = AnalysisPanel(
            main_container,
            self.state_manager,
            self.service
        )
        self.analysis_panel.pack(side="right", fill="y")
