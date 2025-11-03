import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if not getattr(sys, 'frozen', False) else sys._MEIPASS
BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))

BDD_DIR_ACTIVOS = os.path.join(BASE_DIR, "bdd/pedidos_activos")
BDD_DIR_FIN = os.path.join(BASE_DIR, "bdd/pedidos_finalizados")

NOM_GENERICO_ACT = os.path.join(BDD_DIR_ACTIVOS, "pedido")
NOM_GENERICO_FIN = os.path.join(BDD_DIR_FIN, "pedido")
RUTA_TOTALES = os.path.join(BDD_DIR_ACTIVOS, "pedidos_totales.csv")
RUTA_FINALIZADOS = os.path.join(BDD_DIR_FIN, "pedidos_finalizados.csv")
AUX = os.path.join(BDD_DIR_ACTIVOS, "aux.csv")
AUX2 = os.path.join(BDD_DIR_FIN, "aux.csv")
MODIFICADO = os.path.join(BDD_DIR_ACTIVOS, "modificado.csv")

EXTENSION = ".csv"
MODO_LECTURA = "r"
MODO_ESCRITURA = "w"
MODO_APPEND = "a"

CODIGO = 0
PRODUCTO = 1
CANT_PEDIDA = 2
RAZON = 3

RAZON_SOCIAL = 0
ORDEN = 1

def leer_faltantes(razon_social, numero_orden):
    nombre_a_orden = f"{NOM_GENERICO_ACT}_{razon_social}_{numero_orden}{EXTENSION}"
    with open(nombre_a_orden, MODO_LECTURA) as pedido_file:    
        faltante_productos = {}
        nombre_por_codigo = {}
        pedido_reader = csv.reader(pedido_file, delimiter=",")
        for pedido in pedido_reader:
            if len(pedido) == 0:
                continue
            codigo = int(pedido[CODIGO])
            nombre = pedido[PRODUCTO]
            cant_pedida = pedido[CANT_PEDIDA]

            faltante_productos[codigo] = cant_pedida
            if codigo not in nombre_por_codigo.keys():
                nombre_por_codigo[codigo] = nombre

        pedido_file.close()
        return faltante_productos, nombre_por_codigo

def administrar_faltantes(codigo_producto, unidades_faltantes, razon_social, numero_orden):
    nombre_a_orden = f"{NOM_GENERICO_ACT}_{razon_social}_{numero_orden}{EXTENSION}"
    with open(nombre_a_orden, MODO_LECTURA) as pedido_file:
        with open(MODIFICADO, MODO_ESCRITURA) as pedido_mod_file:
            pedido_reader = csv.reader(pedido_file, delimiter=",")
            modificado_writer = csv.writer(pedido_mod_file, delimiter=",")
            producto_encontrado = False

            for pedido in pedido_reader:
                if len(pedido) == 0:
                    continue
                codigo = int(pedido[CODIGO])
                producto = pedido[PRODUCTO]
                stock = int(pedido[CANT_PEDIDA])

                if codigo == codigo_producto:
                    stock = unidades_faltantes
                    producto_encontrado = True
            
                modificado_writer.writerow([codigo, producto, stock])

    if not producto_encontrado:
        print("ERROR: Producto no encontrado en la base de datos del pedido")
        os.remove(MODIFICADO)
        return

    os.replace(MODIFICADO, nombre_a_orden)
    print("Pedido Modificado")
    return

def eliminar_ordenes(razon_social, nro_orden):
    orden_encontrada = False
    with open(RUTA_TOTALES, MODO_LECTURA) as totales_file:
        with open(AUX, MODO_ESCRITURA) as aux_file:
            with open(AUX2, MODO_APPEND) as aux2_file:
                totales_reader = csv.reader(totales_file, delimiter=',')
                aux_writer = csv.writer(aux_file, delimiter=',', lineterminator='\n')
                aux2_writer = csv.writer(aux2_file, delimiter=',', lineterminator='\n')
                for pedido in totales_reader:
                    if len(pedido) == 0:
                        continue

                    razon_actual = pedido[RAZON_SOCIAL]
                    orden_actual = pedido[ORDEN]

                    if razon_actual == razon_social and int(orden_actual) == int(nro_orden):
                        orden_encontrada = True
                        aux2_writer.writerow([razon_actual, orden_actual])
                        continue

                    aux_writer.writerow([razon_actual, orden_actual])

    if not orden_encontrada:
        print("ERROR: La órden a eliminar no fue encontrada")
        return
    
    nombre_src = f"{NOM_GENERICO_ACT}_{razon_social}_{nro_orden}{EXTENSION}"
    nombre_dst = f"{NOM_GENERICO_FIN}_{razon_social}_{nro_orden}{EXTENSION}"
    os.rename(nombre_src, nombre_dst)
    os.replace(AUX, RUTA_TOTALES)
    os.replace(AUX2, RUTA_FINALIZADOS)       

def cargar_ordenes(clientes):
    with open(RUTA_TOTALES, MODO_LECTURA) as totales_file:
        totales_file_reader = csv.reader(totales_file, delimiter=',')
        for pedido in totales_file_reader:
            if len(pedido) == 0:
                continue
            cliente = pedido[RAZON_SOCIAL]
            orden = pedido[ORDEN]
            clientes.append((cliente, orden))
