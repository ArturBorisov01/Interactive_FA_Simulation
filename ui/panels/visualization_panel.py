# ============================================================================
# ui/panels/visualization_panel.py - Панель визуализации
# ============================================================================
import tkinter as tk
from ui.graph_drawing import GraphCanvas
from ui.panels.base_panel import BasePanel

class VisualizationPanel(BasePanel):
    """Панель для визуализации графа"""
    
    def create_widgets(self):
        self.configure(bg='white')
        
        # Заголовок
        title_frame = tk.LabelFrame(
            self,
            text="Визуализация Диаграммы Мура",
            font=("Arial", 10, "bold"),
            bg='white',
            padx=5,
            pady=5
        )
        title_frame.pack(fill="both", expand=True)
        
        # Холст
        self.canvas = tk.Canvas(
            title_frame,
            bg='white',
            width=500,
            height=500
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Объект для рисования
        self.graph_canvas = GraphCanvas(self.canvas, 500, 500)
        
        # Обработчик изменения размера
        self.canvas.bind('<Configure>', self._on_resize)
        
        # Начальная отрисовка
        self._refresh_graph()
    
    def _on_resize(self, event):
        """Обработчик изменения размера"""
        self.graph_canvas.width = event.width
        self.graph_canvas.height = event.height
        self._refresh_graph()
    
    def on_state_changed(self, event_type: str, data=None):
        """Перерисовать граф при изменении состояния"""
        self._refresh_graph()
    
    def _refresh_graph(self):
        """Обновить визуализацию (ИСПРАВЛЕНО)"""
        automaton = self.state_manager.automaton
        
        # Получаем данные
        transitions = automaton.get_transitions() # [(from, in, to), ...]
        nodes = list(automaton.get_states())
        initial_state = automaton.get_initial_state()
        outputs = automaton.get_outputs()         # {state: output, ...}

        # (ДОБАВЛЕНО) Собираем 4-элементные кортежи, которые ждет graph_drawing
        # (from, input, output, to)
        edges_for_drawing = []
        for from_state, input_sym, to_state in transitions:
            # Берем выход {B} из КОНЕЧНОГО состояния (по нашей логике Мура)
            output_sym = outputs.get(to_state, '?') 
            edges_for_drawing.append((from_state, input_sym, output_sym, to_state))
        
        # (ИЗМЕНЕНО) Передаем 'edges_for_drawing'
        self.graph_canvas.draw_graph(edges_for_drawing, nodes, initial_state)