import tkinter as tk

class VentanaScrollable:
    def __init__(self, titulo, ancho, alto):
        self.ventanas_activas = {}
        
        self.ventana = self._create_window(titulo, ancho, alto)
        
        self.canvas = tk.Canvas(self.ventana)
        self.scrollbar = tk.Scrollbar(self.ventana, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y") # Cambiado a 'right' para consistencia
        
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _create_window(self, titulo, ancho, alto):
        ventana = tk.Tk()
        ventana.title(titulo)
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = (screen_width / 2) - (ancho / 2)
        y = (screen_height / 2) - (alto / 2)
        ventana.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")
        return ventana
    
    def _on_canvas_resize(self, event):
        canvas_width = event.width
        self.canvas.itemconfigure(self.frame_id, width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def get_frame(self):
        return self.scrollable_frame
    
    def run(self):
        self.ventana.mainloop()

    def destruir(self):
        self.ventana.destroy()

    def crear_caja_entidad(self, parent_frame):
        caja = tk.Frame(
            parent_frame,
            relief=tk.RIDGE,      # Estilo de borde: RIDGE (levantado) o GROOVE (hundido)
            borderwidth=2,        # Grosor del borde en píxeles
            padx=10,              # Padding interno horizontal
            pady=10,              # Padding interno vertical
        )
        return caja