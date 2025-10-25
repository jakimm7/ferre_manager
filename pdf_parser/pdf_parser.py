import pdfplumber
import re
import csv
import os
import random

RUTA = "/home/jakim7/Documentos/Archivos Santi/stock_ferre/bdd/pedido"
RUTA_CLIENTES = "/home/jakim7/Documentos/Archivos Santi/stock_ferre/bdd/pedidos_totales.csv"
EXTENSION_CSV = ".csv"
AUX = "/home/jakim7/Documentos/Archivos Santi/stock_ferre/bdd/auxiliar.csv"
AUX2 = "/home/jakim7/Documentos/Archivos Santi/stock_ferre/bdd/auxiliar2.csv"

MODO_LECTURA = "r"
MODO_ESCRITURA = "w"
MODO_APPEND = "a"
MODO_LECTURA_ESCRITURA = "r+"

CODIGO = 0
PRODUCTO = 1
CANTIDAD = 2

NRO_ORDEN = 1

def extraer_numero_orden(texto):
    patrones = [
        r'N[º°]\s*(\d+)',           # Nº 17624 o N° 17624
        r'N[º°]\s*0*(\d+)',         # Nº 0017624 (elimina ceros a la izquierda)
        r'ORDEN\s+DE\s+COMPRA\s+N[º°]\s*(\d+)',  # Más específico
    ]
    
    for patron in patrones:
        coincidencia = re.search(patron, texto, re.IGNORECASE)
        if coincidencia:
            numero = coincidencia.group(1)
            print(f"✅ Número de orden extraído: {numero}")
            return numero
    
    print(f"❌ No se encontró número de orden en: {texto}")
    return None

def es_linea_producto(linea):
    patron_numeros = r'\d+\s+[\d.,]+\s+[\d.,]+'
    return bool(re.search(patron_numeros, linea))

def dividir_linea_producto(linea):
    patron_numeros = r'(\d+)\s+([\d.,]+)\s+([\d.,]+)$'
    coincidencia = re.search(patron_numeros, linea)
    
    if coincidencia:
        parte_texto = linea[:coincidencia.start()].strip()
        partes = parte_texto.split(' ', 1)
        
        if len(partes) == 2:
            codigo = partes[0]
            descripcion = partes[1]
            cantidad, precio, total = coincidencia.groups()
            
            return [codigo, descripcion, cantidad, precio, total]
    
    return None

def pedido_en_bdd(orden):
    with open(RUTA_CLIENTES, MODO_LECTURA_ESCRITURA) as pedidos_pendientes:
        pedidos_pendientes_reader = csv.reader(pedidos_pendientes, delimiter=',')
        for pedido in pedidos_pendientes_reader:
            if pedido[NRO_ORDEN] == orden:
                print("Pedido ya cargado")
                return True
        
        return False

def agregar_pedido_bbdd(razon_social, orden):
    with open(RUTA_CLIENTES, MODO_APPEND) as pedidos_pendientes:
        p_pendientes_writer = csv.writer(pedidos_pendientes, delimiter=',', lineterminator='\n')
        p_pendientes_writer.writerow([razon_social, orden])

def parser_pdf(ruta_pdf, clientes):
    razon_social, orden = None, None
    with pdfplumber.open(ruta_pdf) as pdf:
        with open(AUX, MODO_ESCRITURA) as pedido_analizado_file:
            pedido_writer = csv.writer(pedido_analizado_file, delimiter=',')

            for page in range(len(pdf.pages)):
                pagina = pdf.pages[page]
                texto = pagina.extract_text()
                lineas_pdf = texto.splitlines()

                linea_razon_social = False
                for linea in lineas_pdf:
                    if linea_razon_social:
                        razon_social = linea
                        linea_razon_social = False
                        continue

                    if "VENDEDOR" in linea.upper() and razon_social == None:
                        linea_razon_social = True

                    if "ORDEN" in linea.upper():
                        orden = extraer_numero_orden(linea)
                        continue

                    if es_linea_producto(linea):
                        linea_res = dividir_linea_producto(linea)
                        codigo = linea_res[CODIGO]
                        producto = linea_res[PRODUCTO]
                        cantidad = linea_res[CANTIDAD]
                        pedido_writer.writerow([codigo, producto, cantidad])
                        
            if orden == None:
                orden = random.randint(100000, 999999)
            clientes.append((razon_social, orden))

        if not pedido_en_bdd(orden):
            agregar_pedido_bbdd(razon_social, orden)
        else:
            os.remove(AUX)
            return

        os.rename(AUX, f"{RUTA}_{razon_social}_{orden}{EXTENSION_CSV}")
        return True