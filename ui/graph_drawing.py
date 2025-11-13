import tkinter as tk
import math
import random

class GraphCanvas:
    """Класс для визуализации графа (Диаграмма Мура/Мили)"""
    
    def __init__(self, canvas, width=500, height=400):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.node_positions = {}
        self.node_radius = 25
    

    def clear(self):
        """Очистить холст"""
        self.canvas.delete("all")
    
    def calculate_positions(self, nodes):
        """Рассчитать позиции узлов по кругу"""
        self.node_positions = {}
        n = len(nodes)
        
        if n == 0:
            return
        
        # Центр холста
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Радиус круга для размещения узлов
        radius = min(self.width, self.height) * 0.35
        
        if n == 1:
            # Один узел в центре
            self.node_positions[nodes[0]] = (center_x, center_y)
        else:
            # Размещаем узлы по кругу
            for i, node in enumerate(nodes):
                angle = 2 * math.pi * i / n - math.pi / 2  # Начинаем сверху
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.node_positions[node] = (x, y)
    
    def draw_edge(self, node1, node2, phi, psi):
        """Нарисовать ребро с меткой (phi/psi) между узлами"""
        if node1 not in self.node_positions or node2 not in self.node_positions:
            return
        
        x1, y1 = self.node_positions[node1]
        x2, y2 = self.node_positions[node2]
        r = self.node_radius
        
        label_text = f"{phi}, {psi}"

        if node1 == node2:
            # === СПЕЦИАЛЬНАЯ ОБРАБОТКА ПЕТЛИ (A -> A) в запрошенном стиле ===
            loop_r = self.node_radius * 1.5
            
            # Координаты центра узла
            x, y = x1, y1 
            
            # Определяем центр Bounding Box, смещенный ВВЕРХ
            x_center_bbox = x1
            y_center_bbox = y1 - loop_r # Смещаем центр на 1.5R вверх

            # Координаты для bounding box 
            bbox = (x_center_bbox - loop_r, y_center_bbox - loop_r, 
                    x_center_bbox + loop_r, y_center_bbox + loop_r)
            
            # Рисуем дугу: от 225 градусов до 315 градусов, чтобы создать петлю над узлом
            start_angle_deg = 225
            extent_deg = -270 # Дуга на 270 градусов против часовой стрелки

            # Рисуем дугу (ПЕТЛЮ). Здесь нельзя использовать опцию 'arrow'.
            self.canvas.create_arc(
                bbox,
                start=start_angle_deg, 
                extent=extent_deg,
                style=tk.ARC,
                outline="#FF9800", # Оранжевый цвет для петли
                width=2,
                tags="edge"
            )

            # --- ДОБАВЛЕНИЕ СТРЕЛКИ (ВРУЧНУЮ) ---
            # Стрелка должна быть в точке входа на узел (примерно 135 градусов)
            
            # Угол входа на окружность узла (135 градусов)
            entry_angle_rad = 135 * math.pi / 180 
            entry_x = x1 + r * math.cos(entry_angle_rad)
            entry_y = y1 + r * math.sin(entry_angle_rad)

            # Угол для точки на дуге, предшествующей входу (например, 140 градусов относительно центра BBox)
            arc_point_angle_rad = 140 * math.pi / 180 
            arc_x = x_center_bbox + loop_r * math.cos(arc_point_angle_rad)
            arc_y = y_center_bbox + loop_r * math.sin(arc_point_angle_rad)
            
            # Рисуем линию со стрелкой от точки на дуге к точке на узле
            self.canvas.create_line(
                arc_x, arc_y,
                entry_x, entry_y,
                fill="#FF9800",
                width=2,
                arrow=tk.LAST,
                arrowshape=(12, 15, 5),
                tags="edge_arrow"
            )


            # --- Расположение метки ---
            # Метка справа от петли, на уровне ее "вершины"
            label_x = x1 + loop_r * 1.5
            label_y = y1 - r * 1.5
            
            self.canvas.create_text(
                label_x, label_y,
                text=f"({label_text})", # Оборачиваем метку в скобки
                font=("Arial", 9, "bold"),
                fill="#FF9800",
                tags="edge_label"
            )

        else:
            # === ОБЫЧНОЕ НАПРАВЛЕННОЕ РЕБРО (A -> B) ===
            
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx*dx + dy*dy)

            # Нормализация вектора
            if dist == 0: return 
            
            # Точка старта, смещенная от центра узла 1
            x_start = x1 + dx * r / dist
            y_start = y1 + dy * r / dist
            
            # Точка конца, смещенная к центру узла 2
            x_end = x2 - dx * r / dist
            y_end = y2 - dy * r / dist
            
            # Рисуем линию (Здесь опция 'arrow' РАБОТАЕТ)
            self.canvas.create_line(
                x_start, y_start, x_end, y_end,
                fill="#2196F3",
                width=2,
                arrow=tk.LAST,
                arrowshape=(12, 15, 5),
                tags="edge"
            )
            
            # === ДОБАВЛЕНИЕ МЕТКИ (Phi / Psi) ===
            
            # Координаты середины ребра
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Рассчитываем угол линии для смещения метки
            angle = math.atan2(y2 - y1, x2 - x1)
            
            # Небольшое смещение метки перпендикулярно линии для лучшей видимости
            offset = 15
            label_x = mid_x + offset * math.sin(angle)
            label_y = mid_y - offset * math.cos(angle)

            # Рисуем текст метки
            self.canvas.create_text(
                label_x, label_y,
                text=f"({label_text})", # Оборачиваем метку в скобки
                font=("Arial", 9, "bold"),
                fill="#1E88E5",
                tags="edge_label"
            )
    
    def draw_node(self, node, is_initial=False):
        """Нарисовать узел"""
        if node not in self.node_positions:
            return
        
        x, y = self.node_positions[node]
        r = self.node_radius
        
        # Если это начальная вершина, рисуем двойной круг
        if is_initial:
            # Внешний круг (больший радиус)
            self.canvas.create_oval(
                x - r - 4, y - r - 4, x + r + 4, y + r + 4,
                fill="#FFD54F",  # Золотистый цвет для начальной вершины
                outline="#F57C00",  # Оранжевая граница
                width=3,
                tags="node_outer"
            )
            
            # Внутренний круг
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="#FFF176",  # Светло-желтый
                outline="#F57C00",
                width=2,
                tags="node"
            )
        else:
            # Обычный узел
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="#4CAF50",
                outline="#2E7D32",
                width=3,
                tags="node"
            )
        
        # Рисуем текст
        text_color = "#333" if is_initial else "white"
        self.canvas.create_text(
            x, y,
            text=str(node),
            font=("Arial", 12, "bold"),
            fill=text_color,
            tags="node_text"
        )
    
    def draw_graph(self, edges, nodes, initial_state=None):
        """Нарисовать весь граф"""
        self.clear()
        
        if not nodes:
            # Рисуем сообщение если граф пустой
            self.canvas.create_text(
                self.width / 2,
                self.height / 2,
                text="Граф пуст\nДобавьте пары для отображения",
                font=("Arial", 14),
                fill="#999",
                justify=tk.CENTER
            )
            return
        
        # Рассчитываем позиции узлов
        self.calculate_positions(nodes)
        
        # Рисуем сначала все рёбра (чтобы они были под узлами)
        for state_a, phi, psi, state_b in edges: 
            self.draw_edge(state_a, state_b, phi, psi)
        
        # Получаем начальную вершину из кортежа (вершина, символ)
        if isinstance(initial_state, tuple):
            initial_vertex = initial_state[0]
        else:
            initial_vertex = initial_state
            
        # Затем рисуем узлы поверх рёбер
        for node in nodes:
            is_initial = (node == initial_vertex)
            self.draw_node(node, is_initial)