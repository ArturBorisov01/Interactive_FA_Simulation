# ============================================================================
# ui/panels/edge_panel.py - Панель управления рёбрами
# ============================================================================
import tkinter as tk
from tkinter import messagebox
from ui.panels.base_panel import BasePanel

class EdgePanel(BasePanel):
    """Панель для добавления и управления рёбрами (переходами)"""
    
    def create_widgets(self):
        self.configure(bg='#f0f0f0', width=275)
        self.pack_propagate(False)
        
        # Заголовок
        title = tk.Label(
            self, 
            text="Управление графом",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'
        )
        title.pack(pady=10)

        # Undo/Redo перед формой добавления
        self._create_history_controls(self)
        
        # Форма ввода
        self._create_input_form()
        
        # Список рёбер
        self._create_edge_list()
        
        # Кнопки управления
        self._create_control_buttons()
        
        # Счётчик
        self.counter_label = tk.Label(
            self,
            text="Рёбер: 0 | Узлов: 0",
            font=("Arial", 9),
            bg='#f0f0f0'
        )
        self.counter_label.pack(pady=5)
        self._update_history_buttons()
    
    def _create_input_form(self):
        """Создать форму для ввода ребра"""
        input_frame = tk.LabelFrame(
            self,
            text="Добавить ребро",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        input_frame.pack(padx=10, pady=10, fill="x")
        
        # Поля ввода
        fields = [
            ("q(t)", "entry_q_t"),
            ("A", "entry_A"),
            ("B", "entry_B"),
            ("q(t+1)", "entry_q_t_plus_1")
        ]
        
        for col, (label_text, attr_name) in enumerate(fields):
            tk.Label(
                input_frame, 
                text=label_text, 
                bg='#f0f0f0',
                font=("Arial", 9)
            ).grid(row=0, column=col, pady=5)
            
            entry = tk.Entry(input_frame, width=6, font=("Arial", 10))
            entry.grid(row=1, column=col, padx=5, pady=5)
            setattr(self, attr_name, entry)
        
        
        # Кнопка добавления
        add_button = tk.Button(
            input_frame,
            text="➕ Добавить",
            command=self._add_edge,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=15,
            pady=5
        )
        add_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def _create_edge_list(self):
        """Создать список рёбер с прокруткой"""
        list_frame = tk.LabelFrame(
            self,
            text="Список рёбер",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        # list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        list_frame.pack(padx=10, pady=10, fill="x")

        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
       
       


        self.listbox = tk.Listbox(
            list_frame,
            font=("Courier", 10),
            height=10,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )


        self.listbox.pack(fill="x")  # было fill="both", expand=True
        scrollbar.config(command=self.listbox.yview)
    
    def _create_control_buttons(self):
        """Создать кнопки управления"""
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(pady=10, fill="x")
        
        # блок кнопок удаления и очистки
        buttons_row = tk.Frame(button_frame, bg='#f0f0f0')
        buttons_row.pack(fill="x")
        
        tk.Button(
            buttons_row,
            text="🗑️ Удалить ребро",
            command=self._delete_selected,
            bg='#f44336',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=5
        ).pack(side="left", expand=True, fill="x", padx=5)
        
        tk.Button(
            buttons_row,
            text="Очистить всё!",
            command=self._clear_all,
            bg='#FF9800',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=5
        ).pack(side="left", expand=True, fill="x", padx=5)

        remove_state_frame = tk.Frame(button_frame, bg='#f0f0f0')
        remove_state_frame.pack(fill="x", pady=(10, 0))

       # --- новая рамка для удаления вершины ---
        remove_state_frame = tk.LabelFrame(
            button_frame,
            text="Удаление вершины",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        remove_state_frame.pack(fill="x", padx=10, pady=(10, 0)) 

        row = tk.Frame(remove_state_frame, bg='#f0f0f0')
        row.pack(fill="x")

        tk.Label(
            row,
            text="q:",
            bg='#f0f0f0',
            font=("Arial", 9)
        ).grid(row=0, column=0, sticky="w")

        self.state_remove_entry = tk.Entry(row, width=6, font=("Arial", 10))
        self.state_remove_entry.grid(row=0, column=1, padx=5)

        tk.Button(
            row,
            text="Удалить q",
            command=lambda: self._remove_state(self.state_remove_entry.get().strip()),
            bg='#9C27B0',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=3
        ).grid(row=0, column=2, padx=5)

    def _create_history_controls(self, parent):
        history_row = tk.Frame(parent, bg='#f0f0f0')
        history_row.pack(fill="x", pady=(0, 10))

        self.undo_button = tk.Button(
            history_row,
            text="Отменить",
            command=self._handle_undo,
            bg="#455A64",
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.undo_button.pack(side="left", expand=True, fill="x", padx=5)

        self.redo_button = tk.Button(
            history_row,
            text="Вернуть",
            command=self._handle_redo,
            bg='#455A64',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.redo_button.pack(side="left", expand=True, fill="x", padx=5)


    
    # === ОБРАБОТЧИКИ СОБЫТИЙ ===
    
    def _add_edge(self):
        """Добавить ребро"""
        from_state = self.entry_q_t.get().strip()
        input_sym = self.entry_A.get().strip()
        output_sym = self.entry_B.get().strip()
        to_state = self.entry_q_t_plus_1.get().strip()
        
        # Валидация через сервис
        is_valid, error = self.service.validate_transition(
            from_state, input_sym, output_sym, to_state
        )
        
        if not is_valid:
            messagebox.showwarning("Ошибка валидации", error)
            return
        
        # Добавляем через state manager (с уведомлением)
        self.state_manager.add_transition(from_state, input_sym, output_sym, to_state)
        
        # Очищаем поля
        for entry in [self.entry_q_t, self.entry_A, self.entry_B, self.entry_q_t_plus_1]:
            entry.delete(0, tk.END)
    
    def _delete_selected(self):
        """Удалить выбранное ребро"""
        selection = self.listbox.curselection()
        
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите ребро для удаления!")
            return
        
        index = selection[0]
        self.state_manager.remove_transition(index)
    
    def _clear_all(self):
        """Очистить все рёбра"""
        result = messagebox.askyesno(
            "Подтверждение",
            "Вы уверены, что хотите удалить все рёбра?"
        )
        
        if result:
            self.state_manager.clear_all()
    
    def on_state_changed(self, event_type: str, data=None):
        """Обновить отображение при изменении состояния"""
        self._refresh_list()
        self._update_history_buttons()
    
    def _refresh_list(self):

        """Обновить список рёбер (ИСПРАВЛЕНО)"""
        self.listbox.delete(0, tk.END)
        
        automaton = self.state_manager.automaton
        transitions = automaton.get_transitions() # Это [(from, in, to), ...]
        outputs = automaton.get_outputs()         # Это {state: output, ...}
        
        for i, t in enumerate(transitions):
            from_state, input_sym, to_state = t
            
            # Получаем выходной символ {B} для КОНЕЧНОГО состояния (логика Мура)
            output_sym = outputs.get(to_state, '?') # '?' если выход не найден
            
            # Собираем строку в нужном формате
            formatted_str = f"{i}. {from_state} --({input_sym} / {output_sym})--> {to_state}"
            self.listbox.insert(tk.END, formatted_str)
        
        # Обновляем счётчик
        info = self.service.get_automaton_info()
        self.counter_label.config(
            text=f"Рёбер: {info['transitions_count']} | Узлов: {len(info['states'])}"
        )   

    def _remove_state(self, state: str):
        if not state:
            messagebox.showwarning("Ошибка", "Укажите состояние для удаления.")
            return
        if not self.state_manager.remove_state(state):
            messagebox.showwarning("Ошибка", f"Состояние {state} не найдено.")
            return
        self.state_remove_entry.delete(0, tk.END)

    def _handle_undo(self):
        if self.state_manager.undo():
            self._refresh_list()
        self._update_history_buttons()

    def _handle_redo(self):
        if self.state_manager.redo():
            self._refresh_list()
        self._update_history_buttons()

    def _update_history_buttons(self):
        status = self.state_manager.get_history_status()
        can_undo = bool(status.get('can_undo'))
        can_redo = bool(status.get('can_redo'))
        if hasattr(self, 'undo_button'):
            self.undo_button.config(state=tk.NORMAL if can_undo else tk.DISABLED)
        if hasattr(self, 'redo_button'):
            self.redo_button.config(state=tk.NORMAL if can_redo else tk.DISABLED)
