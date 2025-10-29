import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_parser.pdf_parser import *
from ventana_scrolleable import *
from admin_pedido.admin_pedido import *

def descontar_faltante(entrada, codigo, razon_social, nro_orden, faltantes_producto, etiqueta, widgets):
    stock = entrada.get()
    total_pedido = faltantes_producto[codigo]

    if stock == "":
        messagebox.showwarning("Advertencia", "No pusiste el stock del producto")
        return

    if int(stock) > int(total_pedido):
        messagebox.showwarning("Advertencia", "El valor ingresado es mayor al stock solicitado o ya no necesitas mas unidades del producto")
        return

    faltante = int(total_pedido) - int(stock)
    etiqueta.config(text=f"FALTAN {faltante} UNIDADE(S)")
    faltantes_producto[codigo] = faltante
    entrada.delete(0, tk.END)
    administrar_faltantes(codigo, faltante, razon_social, nro_orden)

    if faltante <= 0:
        messagebox.showinfo("Exito!", "Ya tenemos el stock del producto!")
        for w in widgets:
            w.destroy()
        return

    return

def entregar_orden(razon_social, nro_orden, widgets):
    eliminar_ordenes(razon_social, nro_orden)
    lista_widgets = widgets[(razon_social, nro_orden)]
    for widget in lista_widgets:
        widget.destroy()
    return

def mostrar_producto(frame, codigo, razon_social, nro_orden, nombre_por_codigo, faltante_productos, client_widgets):
    producto, faltante = nombre_por_codigo[codigo], faltante_productos[codigo]
    widgets = []

    e_producto = tk.Label(frame, text=f"PRODUCTO: {producto}", font=("Arial", 10))
    e_producto.pack(pady=10)
    client_widgets.append(e_producto)

    e_stock = tk.Label(frame, text=f"FALTAN {faltante} UNIDADE(S)", font=("Arial", 10))
    e_stock.pack(pady=10)
    client_widgets.append(e_stock)

    if int(faltante) > 0:
        entrada_stock = tk.Entry(frame, width=5)
        entrada_stock.pack(pady=5)
        client_widgets.append(entrada_stock)
        widgets.append(entrada_stock)

        submit_button = tk.Button(frame, text="Descontar", command=lambda entrada=entrada_stock, codigo=codigo,razon_social=razon_social, 
                                            nro_orden=nro_orden, faltantes_producto=faltante_productos, etiqueta=e_stock: 
                                            descontar_faltante(entrada, codigo, razon_social, nro_orden, faltantes_producto, etiqueta, widgets))
        widgets.append(submit_button)
        submit_button.pack(pady=5)
        client_widgets.append(submit_button)


def mostrar_clientes(clientes, frame, ventana_scroll, widgets):
    for cliente in clientes:
        razon_social, nro_orden = cliente[RAZON_SOCIAL], cliente[NRO_ORDEN]
        faltante_productos, nombre_por_codigo = leer_faltantes(razon_social, nro_orden)
        client_widgets = []

        cliente_frame = ventana_scroll.crear_caja_entidad(frame)
        cliente_frame.pack(fill='x', pady=10, padx=20)
        
        client_widgets.append(cliente_frame) 

        btn_entregar = tk.Button(cliente_frame, text="Entregar Pedido", command=lambda razon_social=razon_social,widgets=widgets,
                                    nro_orden=nro_orden: entregar_orden(razon_social, nro_orden, widgets))
        btn_entregar.pack(pady=5)
        client_widgets.append(btn_entregar)

        e_razon = tk.Label(cliente_frame, text=razon_social, font=("Arial", 18, "bold"))
        e_razon.pack()
        client_widgets.append(e_razon)

        e_nro_orden = tk.Label(cliente_frame, text=F"Número de órden: {nro_orden}" ,font=("Arial", 14, "bold"))
        e_nro_orden.pack()
        client_widgets.append(e_nro_orden)

        for codigo in faltante_productos.keys():
            mostrar_producto(cliente_frame, codigo, razon_social, nro_orden, nombre_por_codigo, faltante_productos, client_widgets)
            widgets[(razon_social, nro_orden)] = client_widgets

def volver_menu_principal(frame, ventana):
    frame.destroy()
    ventana.destruir()
    menu_principal()

def handler_ordenes(clientes):
    ventana_scroll = VentanaScrollable("Pedidos Totales", 500, 600)
    scrollable_frame = ventana_scroll.get_frame()

    e_instrucciones = tk.Label(scrollable_frame, text="Ingresa en la caja la cantidad de unidades en stock de c/producto\n", wraplength=400, font=("Arial", 15, "italic"))
    e_instrucciones.pack()
    widgets = {}

    mostrar_clientes(clientes, scrollable_frame, ventana_scroll, widgets)

    volver_button = tk.Button(scrollable_frame, text="Volver", command=lambda frame=scrollable_frame, ventana=ventana_scroll: 
                              volver_menu_principal(frame, ventana_scroll))
    volver_button.pack(pady=5)

    return ventana_scroll

def adjuntar_archivo(archivos_seleccionados):
    archivo = filedialog.askopenfilenames(multiple=True)
    if archivo:
        lista_archivos = list(archivo)
        for archivo in lista_archivos: 
            archivos_seleccionados.append(archivo)
            print("Archivo adjuntado con éxito")

        print(f"Han sido seleccionados {len(archivos_seleccionados)} archivo(s)")

def handler_procesos(archivos, manager, window, carga_archivos):
    pedidos = []
    cargar_ordenes(pedidos)

    if carga_archivos:
        if len(archivos) == 0:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados")
            return
        
        for archivo in archivos:
            print(f"Procesando el archivo {archivo}")
            parser_pdf(archivo, pedidos)
        
        print(f"Han sido procesados {len(archivos)}")
    else:
        if len(pedidos) == 0:
            messagebox.showwarning("Advertencia", "No hay pedidos cargados en el sistema")
            return

        print(f"Han sido procesados {len(pedidos)} pedido(s)")

    window.destroy()
    manager.destruir()
    handler_ordenes(pedidos)

def menu_principal():    
    archivos_seleccionados = []
    manager = VentanaScrollable("Inicio", 600, 500)
    main_window = manager.get_frame()

    main_text = tk.Label(main_window, text="Seleccione la(s) proforma(s) a analizar")
    main_text.pack(pady=20)

    important_text = tk.Label(main_window, text="Antes de subir la NP, asegurate de que tenga un número de órden en la misma.", wraplength=300, justify="center")
    important_text.pack(pady=20)

    btn_select = tk.Button(main_window, text="Seleccionar Archivo(s)", command=lambda: adjuntar_archivo(archivos_seleccionados))
    btn_select.pack(pady=20)

    btn_process = tk.Button(main_window, text="Procesar Archivo(s)", command=lambda: handler_procesos(archivos_seleccionados, manager, main_window, True))
    btn_process.pack(pady=10)

    btn_cargar_pendientes = tk.Button(main_window, text="Cargar Pendiente(s)", command=lambda: handler_procesos(archivos_seleccionados, manager, main_window, False))
    btn_cargar_pendientes.pack(pady=10)

    main_window.mainloop()

def main():
    menu_principal()

if __name__ == "__main__":
    main()