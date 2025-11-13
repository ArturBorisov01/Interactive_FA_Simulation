# ============================================================================
# ui/__init__.py
# ============================================================================
"""
UI Layer (Presentation Layer)
Содержит все компоненты пользовательского интерфейса
"""

from .main_window import MainWindow
from .graph_drawing import GraphCanvas

# Импортируем панели
from .panels import (
    BasePanel,
    EdgePanel,
    AnalysisPanel,
    VisualizationPanel
)

__all__ = [
    'MainWindow',
    'GraphCanvas',
    'BasePanel',
    'EdgePanel',
    'AnalysisPanel',
    'VisualizationPanel'
]

