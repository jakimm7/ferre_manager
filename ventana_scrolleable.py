import tkinter as tk

class VentanaScrollable:
    def __init__(self, titulo, ancho, alto):
        self.ventanas_activas = {}
        # self.contador_ventanas = 0
        
        # Crear ventana principal
        self.ventana = self._create_window(titulo, ancho, alto)
        
        # Configurar componentes scrollables
        self.canvas = tk.Canvas(self.ventana)
        self.scrollbar = tk.Scrollbar(self.ventana, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # Configurar el sistema de scroll
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Empaquetar componentes
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="left", fill="y")
        
        # Configurar rueda del mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _create_window(self, titulo, ancho, alto):
        """Método para crear ventanas (originalmente en GestorVentanas)"""
        ventana = tk.Tk()
        ventana.title(titulo)
        ventana.geometry(f"{ancho}x{alto}")
        return ventana
    
    def _on_mousewheel(self, event):
        """Manejar el evento de la rueda del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def get_frame(self):
        """Obtener el frame scrollable para agregar widgets"""
        return self.scrollable_frame
    
    def run(self):
        """Iniciar el mainloop de la ventana"""
        self.ventana.mainloop()

    def destruir(self):
        self.ventana.destroy()