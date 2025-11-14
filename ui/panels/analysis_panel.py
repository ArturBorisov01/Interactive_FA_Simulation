# ============================================================================
# ui/panels/analysis_panel.py - Панель анализа автомата
# ============================================================================
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ui.panels.base_panel import BasePanel

class AnalysisPanel(BasePanel):
    """Панель для анализа автомата и обработки слов"""
    
    def create_widgets(self):
        self.configure(bg='#f0f0f0', width=350)
        self.pack_propagate(False)
        
        # Заголовок
        title = tk.Label(
            self, 
            text="Анализ автомата",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'
        )
        title.pack(pady=10)
        
        # Секции
        self._create_initial_state_section()
        self._create_alphabets_section()
        self._create_word_processing_section()
    
    def _create_initial_state_section(self):
        """Секция начального состояния"""
        frame = tk.LabelFrame(
            self,
            text="Начальное состояние",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        frame.pack(padx=10, pady=5, fill="x")
        
        # Выбор вершины
        state_frame = tk.Frame(frame, bg='#f0f0f0')
        state_frame.pack(pady=5)
        
        tk.Label(state_frame, text="Вершина:", bg='#f0f0f0', font=("Arial", 9)).pack(side="left", padx=5)
        
        self.state_combo = ttk.Combobox(
            state_frame, 
            width=8, 
            font=("Arial", 10),
            state='readonly'
        )
        self.state_combo.pack(side="left", padx=5)
        
    
        # Кнопка установки
        tk.Button(
            state_frame,
            text="Установить",
            command=self._set_initial_state,
            bg='#2196F3',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=3
        ).pack(side="left", padx=5) 
        
        self.current_label = tk.Label(
            frame,
            text="Текущее: не установлено",
            bg='#f0f0f0',
            font=("Arial", 9),
            fg='#666'
        )

    
    def _create_alphabets_section(self):
        """Секция алфавитов"""
        frame = tk.LabelFrame(
            self,
            text="Алфавиты автомата",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        frame.pack(padx=10, pady=5, fill="x")
        
        # Входной алфавит
        tk.Label(frame, text="Входной алфавит (A):", bg='#f0f0f0', 
                font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 2))
        
        self.input_alphabet_label = tk.Label(
            frame, text="{ }", bg='#f0f0f0', font=("Arial", 9),
            anchor="w", padx=5, pady=5
        )
        self.input_alphabet_label.pack(fill="x", pady=(0, 10))
        
        # Выходной алфавит
        tk.Label(frame, text="Выходной алфавит (B):", bg='#f0f0f0',
                font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 2))
        
        self.output_alphabet_label = tk.Label(
            frame, text="{ }", bg='#f0f0f0', font=("Arial", 9),
            anchor="w", padx=5, pady=5
        )
        self.output_alphabet_label.pack(fill="x")
    
    def _create_word_processing_section(self):
        """Секция обработки слов"""
        frame = tk.LabelFrame(
            self,
            text="Обработка входного слова",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        tk.Label(frame, text="Входное слово:", bg='#f0f0f0',
                font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 2))
        
        self.word_entry = tk.Entry(frame, font=("Arial", 10))
        self.word_entry.pack(fill="x", pady=(0, 10))
        
        tk.Button(
            frame,
            text="▶ Обработать",
            command=self._process_word,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=20,
            pady=5
        ).pack(pady=5)
        
        tk.Label(frame, text="Результат:", bg='#f0f0f0',
                font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 2))
        
        self.result_text = tk.Text(
            frame,
            height=1,
            font=self.word_entry.cget("font"),
            wrap=tk.NONE,
            state='disabled',
            borderwidth=self.word_entry.cget("borderwidth"),
            relief=self.word_entry.cget("relief"),
            highlightthickness=self.word_entry.cget("highlightthickness")
        )
        self.result_text.pack(fill="x")
        
        live_frame = tk.LabelFrame(
            frame,
            text="Live-Edit режим",
            font=("Arial", 9, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=5
        )
        live_frame.pack(fill="x", pady=(10,0))

        tk.Button(
            live_frame,
            text="Старт Live-Edit",
            command=self._start_live_edit,
            bg='#3F51B5',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=3
        ).pack(fill="x", pady=2)

        tk.Button(
            live_frame,
            text="Следующий символ",
            command=self._live_step,
            bg='#009688',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=3
        ).pack(fill="x", pady=2)

        tk.Button(
            live_frame,
            text="Сбросить Live-Edit",
            command=self._reset_live,
            bg='#795548',
            fg='white',
            font=("Arial", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=3
        ).pack(fill="x", pady=2)

        self.live_status_label = tk.Label(
            live_frame,
            text="Live-Edit: ожидание запуска",
            bg='#f0f0f0',
            font=("Arial", 9),
            anchor="w"
        )
        self.live_status_label.pack(fill="x", pady=(5,0))


    
    # === ОБРАБОТЧИКИ СОБЫТИЙ ===
    
    def _on_vertex_selected(self, event=None):
        """Обновить доступные входные символы при выборе вершины"""
        selected = self.state_combo.get()
        if not selected:
            self.symbol_combo['values'] = []
            return
        
        symbols = self.state_manager.automaton.get_available_inputs_for_state(selected)
        self.symbol_combo['values'] = sorted(symbols)
        
        if symbols and not self.symbol_combo.get():
            self.symbol_combo.current(0)
    
    def _set_initial_state(self):
        """Установить начальное состояние только по вершине"""
        state = self.state_combo.get().strip()

        if not state:
            messagebox.showwarning("Ошибка", "Выберите вершину!")
            return

        try:
            self.state_manager.set_initial_state(state)
            # всплывающее окно отключено для лучшего UX
            # messagebox.showinfo("Успех", f"Начальное состояние: q0={state}")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def _process_word(self):
        """Обработать входное слово"""
        word = self.word_entry.get().strip()
        
        if not word:
            messagebox.showwarning("Ошибка", "Введите входное слово!")
            return
        
        # NEW: make sure the automaton is deterministic before processing
        if not self.state_manager.automaton.is_complete():
            messagebox.showerror(
                "Недетерминированный автомат",
                "Нельзя обработать слово: автомат не является полным!"
            )
            return
        
        if not self.state_manager.automaton.get_initial_state():
            messagebox.showwarning("Ошибка", "Сначала установите начальное состояние!")
            return
        
        # Обрабатываем через автомат
        result = self.state_manager.automaton.process_word(word)
        
        # Форматируем через сервис
        formatted = self.service.format_process_result(result)
        
        # Отображаем результат
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, formatted)
        self.result_text.config(state='disabled')
    
    def _start_live_edit(self):
        word = self.word_entry.get().strip()
        try:
            status = self.state_manager.start_live_edit(word)
        except ValueError as exc:
            messagebox.showerror("Live-Edit", str(exc))
            return
        self._render_live_status(status)

    def _live_step(self):
        try:
            status = self.state_manager.advance_live_edit()
        except ValueError as exc:
            messagebox.showerror("Live-Edit", str(exc))
            return
        self._render_live_status(status)
        if status['finished']:
            messagebox.showinfo("Live-Edit", "Слово полностью обработано.")

    def _reset_live(self):
        self.state_manager.reset_live_edit()
        self.live_status_label.config(text="Live-Edit: ожидание запуска")

    def _render_live_status(self, status: dict):
        history = status.get('history', [])
        pointer = status.get('pointer', 0)
        length = len(status.get('word', ""))
        current_state = status.get('current_state', '∅')
        last = status.get('last_step')
        extra = ""
        if last:
            extra = f" | δ({last.current_state}, {last.input_symbol}) = {last.next_state} / {last.output_symbol}"
        self.live_status_label.config(
            text=f"w[{pointer}/{length}], q={current_state}{extra}"
        )


    def on_state_changed(self, event_type: str, data=None):
        """Обновить отображение при изменении состояния"""
        # Обновляем комбобоксы состояний
        info = self.service.get_automaton_info()
        self.state_combo['values'] = info['states']
        
        # Обновляем алфавиты
        input_str = "{ " + ", ".join(info['input_alphabet']) + " }" if info['input_alphabet'] else "{ }"
        output_str = "{ " + ", ".join(info['output_alphabet']) + " }" if info['output_alphabet'] else "{ }"
        
        self.input_alphabet_label.config(text=input_str)
        self.output_alphabet_label.config(text=output_str)
        
        # Обновляем метку начального состояния
        if event_type == 'initial_state_changed' and data:
            self.current_label.config(text=f"Текущее: q0 = {data}")
        elif event_type == 'cleared':
            self.current_label.config(text="Текущее: q0 не задано")

