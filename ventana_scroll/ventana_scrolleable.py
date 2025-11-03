import tkinter as tk

class VentanaScrollable:
    def __init__(self, titulo, ancho, alto):
        self.ventanas_activas = {}
        
        # Crear ventana principal
        self.ventana = self._create_window(titulo, ancho, alto)
        
        # Configurar componentes scrollables
        self.canvas = tk.Canvas(self.ventana)
        self.scrollbar = tk.Scrollbar(self.ventana, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # Configurar el sistema de scroll
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Creamos la ventana dentro del canvas y guardamos su ID
        self.frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Ajustamos el ancho del frame para centrar contenido
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
        # Empaquetar componentes
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configurar rueda del mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _create_window(self, titulo, ancho, alto):
        """Método para crear ventanas"""
        ventana = tk.Tk()
        ventana.title(titulo)
        
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = (screen_width / 2) - (ancho / 2)
        y = (screen_height / 2) - (alto / 2)
        ventana.geometry(f"{ancho}x{alto}+{int(x)}+{int(y)}")
        return ventana
    
    def _on_canvas_resize(self, event):
        """Ajustar el ancho del scrollable_frame al ancho del Canvas."""
        canvas_width = event.width
        # Aseguramos que el frame interno tome el ancho del canvas para centrar
        self.canvas.itemconfigure(self.frame_id, width=canvas_width) 
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Manejar el evento de la rueda del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def get_frame(self):
        """Obtener el frame scrollable para agregar widgets"""
        return self.scrollable_frame
    
    def destruir(self):
        """Destruir la ventana"""
        self.ventana.destroy()

    def crear_caja_entidad(self, parent_frame):
        """
        Crea y retorna un tk.Frame pre-configurado para actuar como una 'caja' de entidad,
        con un borde estético.
        """
        caja = tk.Frame(
            parent_frame,
            relief=tk.RIDGE,      # Estilo de borde: RIDGE (levantado) o GROOVE (hundido)
            borderwidth=2,        # Grosor del borde en píxeles
            padx=10,              # Padding interno horizontal
            pady=10,              # Padding interno vertical
        )
        return caja
