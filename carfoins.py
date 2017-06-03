#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

# carfoin$(c) 2015, Jesús Cuerda Villanueva
# Ver README.txt y LICENSE.txt
# Visita la web del proyecto http://carfoins.esy.es/

# Módulos y métodos importados
# from ast import literal_eval        # Para convertir string en lista
from datetime import datetime       # Para el cálculo de tae
#from datetime import date, datetime

from os import remove               # Para eliminar archivo
from socket import timeout          # Para controlar el tiempo de carga
import csv
import sqlite3
import shutil
import sys
import os.path
try:                                # GUI (Interfaces gráficas de usuario)
    from tkinter import *
    from tkinter import scrolledtext
    from tkinter import messagebox
    from tkinter import ttk
    from tkinter import filedialog
except ImportError:
    print("Se requiere el módulo tkinter. Más información en el archivo"
    " adjunto 'README.txt'")
    exit()
# import time                       # ¿?
from urllib.error import URLError   # Para controlar la URL
from urllib.request import urlopen  # Para abrir web
import webbrowser                   # Para abrir navegador


#### CENTRO DE OPERACIONES
def operaciones(base_datos):

    ## Crear tabla si no existe
    if os.path.isfile(base_datos):
        pass
    else:
        db = sqlite3.connect(base_datos)
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE CARTERA1
            (isin text unique, nombre text)
            ''')
        db.commit()
        db.close()

    fondos_isin = []
    fondos_nombre = []
    db = sqlite3.connect(base_datos)
    cursor = db.cursor()
    cursor.execute("SELECT * from CARTERA1")
    total_cartera = cursor.fetchall()
    for cart in total_cartera:
        fondos_isin.append(cart[0])
        fondos_nombre.append(cart[1])
    db.close()

    # Ventana de Operaciones
    cartera_win = Tk()
    cartera_win.title('Carfoin$')
    cartera_win.resizable(width=False, height=False)

    sw = cartera_win.winfo_screenwidth()    # tamaño y posicion
    sh = cartera_win.winfo_screenheight()

    sd = (sw - sh)
    cartera_win.geometry("%dx%d+0+0" % (sw, sh))  #Posicion
    cuerpo = int(sh*0.85)
    pie = int(sh-cuerpo)

    # Enlaces de salida
    def ir_bienvenida():
        cartera_win.destroy()
        bienvenida()

    # Enlaces desde Menú
    def ir_actualizar():
        activa_actualizar(fondos_nombre)
    def ir_consultar():
        activa_consultar(fondos_nombre)
    def ir_borrar():
        activa_borrar(fondos_nombre)
    def ir_nuevo():
        activa_nuevo()
    def ir_eliminar():
        activa_eliminar()
    def ir_bienvenida():
        cartera_win.destroy()
        bienvenida()
    def ir_info():
        cartera_win.destroy()
        bienvenida(tab=2)
    def ir_legal():
        cartera_win.destroy()
        bienvenida(tab=3)
    def ir_creditos():
        cartera_win.destroy()
        bienvenida(tab=4)

    # Menu
    menu = Menu(cartera_win)
    cartera_win.config(menu=menu)
    cartera_win.option_add('*tearOff', FALSE)

    carfoins_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Carfoin$", menu=carfoins_menu, underline=3)
    carfoins_menu.add_command(label="Inicio", command=ir_bienvenida, accelerator="Alt+I")
    carfoins_menu.add_separator()
    carfoins_menu.add_command(label="Salir", command=sys.exit, accelerator="Ctrl+Q")

    cartera_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Mi Cartera", menu=cartera_menu, underline=3)
    cartera_menu.add_command(label="Actualizar", command=ir_actualizar)
    cartera_menu.add_command(label="Consultar", command=ir_consultar)
    cartera_menu.add_command(label="Borrar", command=ir_borrar)

    mercado_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Mercado", menu=mercado_menu, underline=0)
    mercado_menu.add_command(label="Nuevo Fondo", command=ir_nuevo, accelerator="Ctrl+N")
    mercado_menu.add_command(label="Eliminar Fondo", command=ir_eliminar)

    ayuda_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Ayuda", menu=ayuda_menu, underline=0)
    ayuda_menu.add_command(label="Información", command=ir_info, accelerator="F1")
    ayuda_menu.add_command(label="Licencia", command=ir_legal)
    ayuda_menu.add_command(label="Créditos", command=ir_creditos)
    #ayuda_menu.add_command(label="Acerca de", command=ir_info)

    #Actualización de menú
    db = sqlite3.connect(base_datos)
    cursor = db.cursor()
    cursor.execute("SELECT * from CARTERA1")
    tabla_vacia = cursor.fetchall()
    db.close()
    if len(tabla_vacia) == 0:
        cartera_menu.entryconfig(0, state=DISABLED)
        cartera_menu.entryconfig(1, state=DISABLED)
        cartera_menu.entryconfig(2, state=DISABLED)
        mercado_menu.entryconfig(1, state=DISABLED)
    else:
        cartera_menu.entryconfig(0, state=NORMAL)
        cartera_menu.entryconfig(1, state=NORMAL)
        cartera_menu.entryconfig(2, state=NORMAL)
        mercado_menu.entryconfig(1, state=NORMAL)

    ################# FUNCIONES DE ACCIÓN

    ## COMPROBAR QUE HAY FONDOS
    def comprobar_cartera():
        db = sqlite3.connect(base_datos)
        cursor = db.cursor()
        cursor.execute("SELECT * from CARTERA1")
        #tabla_vacia = cursor.fetchone() #if tabla_vacia is None:
        tabla_vacia = cursor.fetchall()
        db.close()
        if len(tabla_vacia) == 0:
            comprobar_cartera = Toplevel()
            comprobar_cartera.title('Cartera vacía')
            comprobar_cartera.resizable(width=False, height=False)

            comprobar_cartera.grab_set()   # grab_release() # to return to normal
            # esta se posiciona siempre sobre la ventana principal
            comprobar_cartera.transient(cartera_win)

            sw = comprobar_cartera.winfo_screenwidth()       # posicion
            sh = comprobar_cartera.winfo_screenheight()
            sd = (sw - sh)
            comprobar_cartera.geometry('770x200+%d+%d' % (sd/2, sd/6))

            img_comprobar = PhotoImage(file="img/nopasar.gif")
            logo_comprobar = Label(comprobar_cartera, image=img_comprobar)
            logo_comprobar.image = img_comprobar
            logo_comprobar.pack(side="left", padx=10)

            frame_com = Frame(comprobar_cartera)
            msg_comprobar = "¿Qué quieres hacer?: Tu Cartera está " \
                "vacía.\n\nPuedes añadir " \
                "Fondos a tu Cartera con el botón 'Nuevo'."
            texto_comprobar = Label(frame_com, text=msg_comprobar,
                justify="left", wraplength=600, font=(12))
            texto_comprobar.config(font=(None, '12'))
            texto_comprobar.pack(side="left")
            frame_com.pack(fill=X, padx=10, pady=20)

            boton = Button(comprobar_cartera, text="Continuar",
                command=lambda: comprobar_cartera.destroy(),
                cursor="hand1", bd=3, activebackground="#ACD1E9",
                activeforeground="#FFFFFF")
            boton.bind('<Return>', lambda e:comprobar_cartera.destroy())
            boton.focus()
            boton.pack(side="left", expand=1, pady=10)
            comprobar_cartera.bind('<Escape>', lambda e:comprobar_cartera.destroy())
            comprobar_cartera.mainloop()
            return False
        else:
            return True

    ## ACTUALIZAR
    def activa_actualizar(fondos_nombre):

        def actualizar():
            #fondo_actualizar = listbox_fondos.get(listbox_fondos.curselection())
            #if fondo_actualizar != None:       # Se hace clic en OK
            fondos_para_actualizar = {}
            #nombres_actualizar = []
            #isin_actualizar = []
            db = sqlite3.connect(base_datos)
            cursor = db.cursor()
            for cada_fondo in fondos_actualizar:
                cursor.execute("SELECT * from CARTERA1 WHERE nombre = ?", (cada_fondo,))
                for cada_uno in cursor:
                    #isin_actualizar.append(cada_uno[0])
                    #nombres_actualizar.append(cada_uno[1])
                    fondos_para_actualizar[cada_uno[0]]=cada_uno[1]
            db.close()

            actualizado_texto = open("actualizado.txt", "w", encoding='utf-8')
            actualizado_texto.close()

            ### Inicio de actualización para cada fondo
            for isin, nombre in fondos_para_actualizar.items():
                error = False
                nombre_fondo = nombre
                tabla_fondo = isin
                web = "http://www.quefondos.com/m/es/fondos/ficha/index.html?isin=" + tabla_fondo
                pagina_fondo = "http://www.quefondos.com/m/es/fondos/ficha/index.html?isin=" + tabla_fondo

                # Abre la web
                try:                    # Para comprobar que carga la web
                    web = urlopen(web, timeout=5)   # Default = 5
                except URLError:        # Mensaje de error si no reconoce la URL
                    msg_error = "{}\nERROR: URL no encontrada. El fondo " \
                        "no ha sido actualizado.\nHa sido imposible conectar con " \
                        "la página web de ese fondo.\nComprueba tu conexión " \
                        "a internet.\nQuizá esa web no está disponible en " \
                        "este momento. Inténtalo más tarde.\n\n".format(nombre_fondo)
                    with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                        contenido = fichero.read()
                        fichero.write(msg_error)
                    error = True
                except timeout:
                    msg_time = "{}\nERROR: Tiempo de conexión excedido.\nEl fondo " \
                        "no ha sido actualizado.\nHa sido imposible conectar con " \
                        "la página web de ese fondo.\nComprueba tu conexión " \
                        "a internet.\nQuizá esa web no está disponible en " \
                        "este momento. Inténtalo más tarde.\n\n".format(nombre_fondo)
                    with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                        contenido = fichero.read()
                        fichero.write(msg_time)
                    error = True
                if error == False:
                    #La web carga sin errores y se llama a la función
                    #fondo(nombre_fondo, pagina_fondo, tabla_fondo)

                    # ACTUALIZAR 2: Función que obtiene los datos vía internet y los guarda
                    # Recorre el texto de la web abierta
                    check_web = 0           # Sistema de control de web
                    for line in web:
                        linea = str(line)   # Convierte el texto en una cadena
                        # Busca las líneas con los datos coincidentes y las limpia
                        if "Valor liquidativo:" in linea or "Fecha:" in linea:
                            linea = linea.strip(
                                "b<span class=\"floatleft\">""</span>\\n'")
                            linea = linea.replace(
                                "</span><span class=\"floatright\">", "")
                            check_web = check_web + 1
                        if "Valor liquidativo:" in linea:
                            linea_valor = linea
                            check_web = check_web + 1
                        if "Fecha:" in linea:
                            linea_fecha = linea
                            check_web = check_web + 1

                    if check_web != 4:      # Sistema de control de web: 4
                        msg_datos = "{}\nERROR: Datos corruptos.\nLo siento, pero " \
                            "ha habido un error al consultar los datos " \
                            "del Fondo.\nQuizá la web no está disponible " \
                            "en este momento o ha cambiado su formato.\n" \
                            "Prueba más tarde. Si el error continúa, " \
                            "puedes contactar con el autor para que lo " \
                            "resuelva (visita 'Acerca de').\n\n".format(nombre_fondo)
                        with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                            contenido = fichero.read()
                            fichero.write(msg_datos)
                    else:
                        web.close()    # Cierra la página web

                        fecha_nueva = linea_fecha.replace("Fecha: ", "")
                        valor_nuevo = linea_valor.strip("Valor liquidativo: "" EUR")
                        #valor_nuevo = int(valor_nuevo)

                        ## Convertir string en float desde el principio
                        #valor_nuevo = valor_nuevo.replace(".", "").replace(",", ".")
                        #valor_nuevo = float(valor_nuevo)

                        # ABRE LA TABLA DEL FONDO
                        #db = sqlite3.connect(base_datos)
                        #cursor = db.cursor()
                        #cursor.execute("SELECT fecha from {} WHERE fecha = ?".format(tabla_fondo), (fecha_nueva,))
                        #duplicada = cursor.fetchone()
                        #db.close()

                        #if duplicada is not None:  # Si la fecha ya existe
                            #msg_duple = "{}\nEl fondo no necesita " \
                                #"actualización.\nLa última cotización guardada " \
                                #"corresponde a esta fecha: {}.\n\n".format(nombre_fondo, fecha_nueva)
                            #with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                                #contenido = fichero.read()
                                #fichero.write(msg_duple)

                        #else:           # Si no existe: Incorpora los datos

                        #try:
                        #capital_existe = "NO"
                        db = sqlite3.connect(base_datos)
                        cursor = db.cursor()
                        #cursor.execute("SELECT * from {} where capital != ''".format(isin_consultar[0]))
                        cursor.execute("SELECT * from {}".format(tabla_fondo))
                        fieldnames=[f[0] for f in cursor.description]
                        db.close()

                        #if ((inversion is None) or (len(inversion) == 2)):
                            #capital_existe = "NO"
                        #except:
                            #capital_existe = "SI"
                            #pass
                        if len(fieldnames) > 2:
                            capital_existe = "SI"
                        else:
                            capital_existe = "NO"

                        #if ((inversion is None) or (len(inversion) == 2)):
                            #capital_existe = "NO"

                        #if len(inversion) == 2:
                            #capital_existe = "NO"

                        #else:
                            #capital_existe = "SI"

                        #try:

                        if capital_existe == "NO":
                            try:
                                fecha_nueva = datetime.strptime(fecha_nueva, '%d/%m/%Y')
                                db = sqlite3.connect(base_datos)
                                cursor = db.cursor()
                                cursor.execute("INSERT INTO {} VALUES(?, ?)".format(tabla_fondo), (fecha_nueva, valor_nuevo))
                                db.commit()
                                db.close()

                                linea_total = linea_valor + linea_fecha
                                #msg_nuevo = "\n" + linea_total
                                msg_nuevo = linea_valor + "\n" + linea_fecha

                                msg_nuevo = "{}\nFondo actualizado.\n{}.\n\n".format(nombre_fondo, msg_nuevo)
                                with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                                    contenido = fichero.read()
                                    fichero.write(msg_nuevo)

                            except:

                                fechas = []
                                db = sqlite3.connect(base_datos)
                                cursor = db.cursor()
                                cursor.execute("SELECT * from {} ORDER BY fecha".format(tabla_fondo))
                                historico = cursor.fetchall()
                                db.close()
                                for fecha in historico:
                                    fechas.append(fecha[0])
                                fecha_ul = fechas[-1]

                                #fecha_ul = fecha_ul[0:10]
                                fecha_or = str(fecha_ul[0])
                                fecha_Y = fecha_ul[0:4]
                                fecha_m = fecha_ul[5:7]
                                fecha_d = fecha_ul[8:10]
                                fecha_t = fecha_d + "/" + fecha_m + "/" + fecha_Y

                                msg_duple = "{}\nEl fondo no necesita " \
                                    "actualización.\nLa última cotización guardada " \
                                    "corresponde a esta fecha: {}.\n\n".format(nombre_fondo, fecha_t)
                                with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                                    contenido = fichero.read()
                                    fichero.write(msg_duple)
                                pass

                        else:
                            try:
                                fecha_nueva = datetime.strptime(fecha_nueva, '%d/%m/%Y')
                                db = sqlite3.connect(base_datos)
                                cursor = db.cursor()
                                cursor.execute("INSERT INTO {} VALUES(?, ?, ?)".format(tabla_fondo), (fecha_nueva, valor_nuevo, ''))
                                db.commit()
                                db.close()

                                linea_total = linea_valor + linea_fecha
                                #msg_nuevo = "\n" + linea_total
                                msg_nuevo = linea_valor + "\n" + linea_fecha

                                msg_nuevo = "{}\nFondo actualizado.\n{}.\n\n".format(nombre_fondo, msg_nuevo)
                                with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                                    contenido = fichero.read()
                                    fichero.write(msg_nuevo)

                            except:
                                fechas = []
                                db = sqlite3.connect(base_datos)
                                cursor = db.cursor()
                                cursor.execute("SELECT * from {} ORDER BY fecha".format(tabla_fondo))
                                historico = cursor.fetchall()
                                db.close()
                                for fecha in historico:
                                    fechas.append(fecha[0])
                                fecha_ul = fechas[-1]

                                #fecha_ul = fecha_ul[0:10]
                                fecha_or = str(fecha_ul[0])
                                fecha_Y = fecha_ul[0:4]
                                fecha_m = fecha_ul[5:7]
                                fecha_d = fecha_ul[8:10]
                                fecha_t = fecha_d + "/" + fecha_m + "/" + fecha_Y

                                msg_duple = "{}\nEl fondo no necesita " \
                                    "actualización.\nLa última cotización guardada " \
                                    "corresponde a esta fecha: {}.\n\n".format(nombre_fondo, fecha_t)
                                with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                                    contenido = fichero.read()
                                    fichero.write(msg_duple)
                                pass
            ### Fin actualización

            progreso_win.destroy()

            def volver():
                actualizado_win.destroy()
                cartera_win.destroy()
                operaciones(base_datos)

            actualizado_win = Toplevel()
            actualizado_win.title('Actualización terminada')
            actualizado_win.resizable(width=False, height=False)

            actualizado_win.grab_set()
            actualizado_win.transient(cartera_win)

            sh = actualizado_win.winfo_screenheight()       # position
            sw = actualizado_win.winfo_screenwidth()
            h = sh * 0.7
            sd = (sw - sh)
            actualizado_win.geometry('770x%d+%d+%d' % (h, sd/2, sd/6))

            frame1_act = Frame(actualizado_win)

            img = PhotoImage(file="img/actualiza.gif")
            logo = Label(frame1_act, image=img)
            logo.image = img
            logo.pack(side="left", padx=10)

            frame_txt = Frame(frame1_act)
            msg_actualizado = "Resultado del proceso de actualización."
            texto_act = Label(frame_txt, text=msg_actualizado, justify="left",
                wraplength=600, font=(11))
            texto_act.config(font=(NONE, '11'))
            texto_act.pack(side="left")
            frame_txt.pack(fill=X, padx=10, pady=20)

            frame_bot = Frame(frame1_act)
            boton = Button(frame_bot, text='Continuar', cursor="hand1", bd=3,
                activebackground="#ACD1E9", activeforeground="#FFFFFF",
                command=volver)
            boton.bind('<Return>', lambda e:volver())
            boton.focus()
            boton.pack(side="left", padx=10)
            frame_bot.pack(pady=10)

            frame1_act.pack(fill=X, padx=10, pady=5)

            frame2_act = Frame(actualizado_win)
            with open("actualizado.txt", "r", encoding='utf-8') as fichero:
                contenido = fichero.read()
            text = scrolledtext.ScrolledText(frame2_act, wrap="word")
            text.configure(state=NORMAL)
            text.insert(END, contenido)
            text.configure(state=DISABLED, padx=5)
            text.pack(fill=BOTH, expand=1)
            frame2_act.pack(fill=BOTH, expand=1)

            actualizado_win.bind('<Escape>', lambda e:volver())
            actualizado_win.mainloop()

        if comprobar_cartera():     # SI existen fondos
            fondos_isin = []
            fondos_nombre = []
            db = sqlite3.connect(base_datos)
            cursor = db.cursor()
            cursor.execute("SELECT * from CARTERA1")
            total_cartera = cursor.fetchall()
            for cart in total_cartera:
                fondos_isin.append(cart[0])
                fondos_nombre.append(cart[1])
            db.close()

            indice = listbox_fondos.curselection()
            fondos_actualizar = [listbox_fondos.get(idx) for idx in listbox_fondos.curselection()]

            def volver_actualizar():
                mensaje_win.destroy()
                cartera_win.grab_set()

            if len(fondos_actualizar) == 0:     # SI no hay selección
                mensaje_win = Toplevel()
                mensaje_win.title('Cartera: Error de Selección')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(cartera_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/noselect.gif")
                logo = Label(mensaje_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje_win)
                msg = "No ha seleccionado ningún Fondo para actualizar."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje_win, text="Volver", command=volver_actualizar,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:volver_actualizar())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje_win.bind('<Escape>', lambda e:volver_actualizar())
                mensaje_win.mainloop()

            else:       # SI hay selección

                ### BARRA DE PROGRESO
                progreso_win = Toplevel()
                progreso_win.title('ACTUALIZANDO')
                progreso_win.resizable(width=False, height=False)

                progreso_win.grab_set()
                progreso_win.transient(cartera_win)

                sh = progreso_win.winfo_screenheight()       # position
                sw = progreso_win.winfo_screenwidth()
                sd = (sw - sh)
                progreso_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img_espera = PhotoImage(file="img/reloj.gif")
                logo_espera = Label(progreso_win, image=img_espera)
                logo_espera.image = img_espera
                logo_espera.pack(side="left", padx=10)

                frame_p1 = Frame (progreso_win)
                msg_espera = "\nACTUALIZANDO..."
                texto_bp = Label(frame_p1, text=msg_espera, justify="left",
                    wraplength=600, font=(12))
                texto_bp.config(font=(None, '12', 'bold'))
                texto_bp.pack(fill=X)
                bp = ttk.Progressbar(frame_p1, orient=HORIZONTAL,
                    length=200, mode='indeterminate')
                bp.start()
                bp.pack(pady=10)
                msg2_espera = "El tiempo de este proceso depende del número " \
                    "de fondos a actualizar.\nPor favor, espera hasta " \
                    "que aparezca el informe de actualización."
                texto2_bp = Label(frame_p1, text=msg2_espera, justify="left",
                    wraplength=600, font=(11))
                texto2_bp.config(font=(None, '11'))
                texto2_bp.pack(fill=X)
                frame_p1.pack(fill=X, pady=10)

                progreso_win.after(2500, lambda: actualizar())
                progreso_win.mainloop()


    ## CONSULTAR
    def activa_consultar(fondos_nombre):

        def inicia_consultar(fondo_consultar):

            def seguir():
                consultar2_win.destroy()
                #cartera_win.grab_set()
                cartera_win.eval('::ttk::CancelRepeat')
                cartera_win.destroy()
                operaciones(base_datos)

            def exportar():

                db = sqlite3.connect(base_datos)
                cursor = db.cursor()
                cursor.execute("SELECT * from {} ORDER BY fecha".format(isin_consultar[0]))
                copia_fichero = cursor.fetchall()
                db.close()

                copia_csv = isin_consultar[0] + ".csv"
                destino = "backup/" + copia_csv

                try:
                    with open(destino, 'w') as csvfile:
                        #writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
                        writer = csv.writer(csvfile)
                        for linea in copia_fichero:
                            fecha = linea[0]
                            fecha = fecha[0:10]
                            valor = linea[1]
                            writer.writerow([fecha, valor])
                    pass

                except:
                    #Ventana de error
                    mensaje_win = Toplevel()
                    mensaje_win.title('Error de Exportación')
                    mensaje_win.resizable(width=False, height=False)

                    mensaje_win.grab_set()
                    mensaje_win.transient(consultar2_win)

                    sw = mensaje_win.winfo_screenwidth()       # posicion
                    sh = mensaje_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/error.gif")
                    logo = Label(mensaje_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt = Frame(mensaje_win)
                    msg = "Se ha producido un error durante la exportación" \
                        "de la tabla.\n\nComprueba que " \
                        "existe la carpeta carfoins/backup.\n"
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600)
                    texto.config(font=(None, '12'))
                    texto.pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    boton = Button(mensaje_win, text="Volver",
                        command=lambda: mensaje_win.destroy(),
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:mensaje_win.destroy())
                    boton.focus()
                    boton.pack(side="left", expand=1, pady=10)
                    mensaje_win.bind('<Escape>', lambda e:mensaje_win.destroy())
                    mensaje_win.mainloop()

                #Ventana de confirmación de exportación
                mensaje_win = Toplevel()
                mensaje_win.title('Exportación realizada')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(consultar2_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje_win.geometry('770x300+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/check.gif")
                logo = Label(mensaje_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje_win)
                msg = "Tabla exportada con éxito en carfoins/backup.\n\n" \
                    "El archivo {} contine el histórico de valores.\n" \
                    "Lo puedes abrir con una hoja de cálculo " \
                    "(LibreOffice, Excel,...).\n\nPara asegurarte la máxima " \
                    "compatibilidad:\n- Utiliza caracteres Unicode (UTF-8).\n" \
                    "- Selecciona 'Coma' como separador de columnas.\n" \
                    "- Selecciona 'Dobles comillas' como delimitador de " \
                    "texto.".format(copia_csv)
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje_win, text="Volver",
                    command=lambda: mensaje_win.destroy(),
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:mensaje_win.destroy())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje_win.bind('<Escape>', lambda e:mensaje_win.destroy())
                mensaje_win.mainloop()


            def invertir():

                def volver_invertir():
                    invertir_win.destroy()
                    consultar2_win.grab_set()
                    #cartera_win.eval('::ttk::CancelRepeat')

                def control_invertir():

                    def reinvertir():
                        error_win.destroy()
                        invertir_win.grab_set()
                    def no_reinvertir():
                        error_win.destroy()
                        invertir_win.destroy()
                        consultar2_win.grab_set()

                    inv_capital = capital_inv.get()

                    caracter_val = ["0", "1", "2", "3", "4", "5", "6",
                        "7", "8", "9", "."]
                    control_car = True
                    for caracter in inv_capital:
                        if caracter not in caracter_val:
                            control_car = False
                    puntos = inv_capital.count('.')

                    if ((control_car == False) or (puntos > 1) or
                        (inv_capital == "")):

                        error_win = Toplevel()
                        error_win.title('ERROR FORMATO CAPITAL')
                        error_win.resizable(width=False, height=False)

                        error_win.grab_set()
                        error_win.transient(invertir_win)

                        sw = error_win.winfo_screenwidth()       # posicion
                        sh = error_win.winfo_screenheight()
                        sd = (sw - sh)
                        error_win.geometry('770x250+%d+%d' % (sd/2, sd/6))

                        img = PhotoImage(file="img/error.gif")
                        logo = Label(error_win, image=img)
                        logo.image = img
                        logo.pack(side="left", padx=10)
                        frame_txt = Frame(error_win)
                        msg = "Eso no parece correcto:\nEl capital sólo debe " \
                            "contener números y separar los decimales con " \
                            "un punto.\nEjemplos: 23.453980 ó 2145.42 " \
                            "ó 45.\n\nCopiar y pegar puede añadir elementos no " \
                            "visibles que producen error.\nInténtalo otra vez."
                        texto = Label(frame_txt, text=msg, justify="left",
                            font=(12), wraplength=600).pack(side="left")
                        frame_txt.pack(fill=X, padx=10, pady=20)
                        frame1 = Frame (error_win)
                        boton1 = Button(frame1, text="Reintentar", command=reinvertir,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton1.bind('<Return>', lambda e:reinvertir())
                        boton1.focus()
                        boton1.pack(side="left", padx=10)
                        boton2 = Button(frame1, text="Cancelar", command=no_reinvertir,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton2.bind('<Return>', lambda e:no_reinvertir())
                        boton2.pack(side="left", padx=10)
                        frame1.pack(pady=10)
                        error_win.bind('<Escape>', lambda e:no_reinvertir())
                        error_win.mainloop()

                    else:

                        # ¿TRY?
                        inv_capital = float(inv_capital)
                        inv_capital = round(inv_capital, 2)
                        #inv_capital = format(inv_capital, '.2f')

                        fecha_inv = combox_fechas.get()
                        fecha_inv = datetime.strptime(fecha_inv, "%d/%m/%Y")
                        #fecha_inv = datetime.strftime(fecha_inv, "%d/%m/%Y")

                        db = sqlite3.connect(base_datos)
                        cursor = db.cursor()
                        try:
                            cursor.execute("ALTER TABLE {} ADD COLUMN 'capital' real".format(isin_consultar[0]))
                            db.commit()
                            pass
                        except:
                            cursor.execute("UPDATE {} SET capital = ? WHERE capital IS NOT NULL".format(isin_consultar[0]), ('',))
                            db.commit()
                            pass
                        #cursor.execute("INSERT INTO {} (capital) VALUES(?) WHERE fecha = ?".format(isin_consultar[0]), (inv_capital, fecha_inv))
                        cursor.execute("UPDATE {} SET capital = ? WHERE fecha = ?".format(isin_consultar[0]), (inv_capital, fecha_inv))

                        db.commit()
                        db.close()

                        invertir_win.destroy()
                        consultar2_win.destroy()
                        cartera_win.grab_set()
                        inicia_consultar(fondo_consultar)

                invertir_win = Toplevel()
                invertir_win.title('Invertir Capital')
                invertir_win.resizable(width=False, height=False)

                invertir_win.grab_set()
                invertir_win.transient(consultar2_win)
                invertir_win.update()

                sh = invertir_win.winfo_screenheight()       # position
                sw = invertir_win.winfo_screenwidth()
                sd = (sw - sh)
                invertir_win.geometry('770x300+%d+%d' % (sd/2, sd/6))

                frame1 = Frame (invertir_win)
                img1 = PhotoImage(file="img/capital.gif")
                logo1 = Label(frame1, image=img1)
                logo1.image = img1
                logo1.pack(side="left", padx=10)
                msg1 = "Selecciona una fecha e introduce el capital " \
                    "invertido.\n\nSepara los decimales con un punto " \
                    "(12524.43).\n\n" \
                    "Si ya existe una inversión realizada, el nuevo capital " \
                    "introducido sustituirá al anterior."
                texto1 = Label(frame1, text=msg1, justify="left",
                    wraplength=600, font=(12)).pack(fill=X)

                #entrada1 = Frame(frame1)
                #Label(entrada1, text="Fecha:", bd=10, font=(12), width=8).pack(side="left")
                #fecha_inv = Entry(entrada1, text="Fecha:",font=(12), width=16)
                #fecha_inv.pack(side="left")
                #fecha_inv.focus_set()
                #limpiar_fecha = Button(entrada1, text="⌫", command=lambda: fecha_inv.delete(0, 'end'))
                #limpiar_fecha.bind('<Return>', lambda e:fecha_inv.delete(0, 'end'))
                #limpiar_fecha.pack(side="left")
                #entrada1.pack()

                entrada1 = Frame(frame1)

                Label(entrada1, text="Fecha:", bd=10, font=(12), width=8).pack(side="left")
                fechas = []
                db = sqlite3.connect(base_datos)
                cursor = db.cursor()
                cursor.execute("SELECT * from {} ORDER BY fecha".format(isin_consultar[0]))
                total_fechas = cursor.fetchall()
                for fec in total_fechas:
                    fech = str(fec[0])
                    #fech = fech[0:10]
                    fech_Y = fech[0:4]
                    fech_m = fech[5:7]
                    fech_d = fech[8:10]
                    fech_tot = fech_d + "/" + fech_m + "/" + fech_Y
                    fechas.append(fech_tot)
                db.close()

                combox_fechas = ttk.Combobox(entrada1, values=fechas,
                    state='readonly', exportselection=0, width=10)
                combox_fechas.current(0)
                #combox_fechas.bind('<<ComboboxSelected>>', volver_invertir)
                combox_fechas.config(font=(NONE, '10', 'bold'), height=7) # height=7
                #combox_fechas.focus()
                combox_fechas.pack(side="left")

                entrada1.pack(fill=X, padx=60)

                entrada2 = Frame(frame1)
                Label(entrada2, text="Capital:", bd=10, font=(12), width=8).pack(side="left")
                capital_inv = Entry(entrada2, font=(12), width=10)
                capital_inv.pack(side="left")
                limpiar_capital = Button(entrada2, text="⌫", command=lambda: capital_inv.delete(0, 'end'))
                limpiar_capital.bind('<Return>', lambda e:capital_inv.delete(0, 'end'))
                limpiar_capital.pack(side="left")
                entrada2.pack(fill=X, padx=60)

                frame1.pack(fill=X, padx=10, pady=10)

                frame2 = Frame(invertir_win)
                boton_ok = Button(frame2, text="OK", cursor="hand1",
                    bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=control_invertir)
                boton_ok.bind('<Return>', lambda e:control_invertir())
                boton_ok.pack(side="left", padx=10)
                boton_cancel = Button(frame2, text="Volver", cursor="hand1",
                    bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=volver_invertir)
                boton_cancel.bind('<Return>', lambda e:volver_invertir())
                boton_cancel.pack(side="left", padx=10)
                frame2.pack(pady=10)

                invertir_win.bind('<Escape>', lambda e:volver_invertir())
                invertir_win.mainloop()


            def editar():
                fecha_in = ""
                valor_in = ""

                def refrescar():
                    editar_win.destroy()
                    consultar2_win.destroy()
                    #consultar2_win.destroy()
                    activa_consultar(fondo_consultar)
                def volver_editar():
                    editar_win.destroy()
                    consultar2_win.grab_set()

                def control_editar():

                    def reeditar():
                        error_win.destroy()
                        editar_win.grab_set()
                    def no_reeditar():
                        error_win.destroy()
                        editar_win.destroy()
                        consultar2_win.grab_set()
                    def reeditar2():
                        error2_win.destroy()
                        editar_win.grab_set()
                    def no_reeditar2():
                        error2_win.destroy()
                        editar_win.destroy()
                        consultar2_win.grab_set()

                    fecha_in = fecha_edit.get()
                    valor_in = valor_edit.get()

                    caracter_val = ["0", "1", "2", "3", "4", "5", "6",
                        "7", "8", "9", "."]
                    control_car = True
                    for caracter in valor_in:
                        if caracter not in caracter_val:
                            control_car = False
                    puntos = valor_in.count('.')

                    """
                    if ((fecha_in == "") or (valor_in == "") or
                        (control_car == False) or (puntos > 1) or
                        (float(valor_in) == 0.0)):
                        # or (fecha_in[2] != "/") or (fecha_in[5] != "/")

                    else:
                    """
                    try:
                        fecha_in = datetime.strptime(fecha_in, "%d/%m/%Y")
                        fecha_in = datetime.strftime(fecha_in, "%d/%m/%Y")
                        #valor_in = float(valor_in)
                        #valor_in = round(valor_in, 6)
                        #valor_in = format(valor_in, '.6f')
                        pass

                    except:
                        error2_win = Toplevel()
                        error2_win.title('ERROR FORMATO FECHA')
                        error2_win.resizable(width=False, height=False)

                        error2_win.grab_set()
                        error2_win.transient(editar_win)

                        sw = error2_win.winfo_screenwidth()       # posicion
                        sh = error2_win.winfo_screenheight()
                        sd = (sw - sh)
                        error2_win.geometry('770x250+%d+%d' % (sd/2, sd/6))

                        img = PhotoImage(file="img/error.gif")
                        logo = Label(error2_win, image=img)
                        logo.image = img
                        logo.pack(side="left", padx=10)
                        frame_txt = Frame(error2_win)
                        msg = "Eso no parece correcto:\nLa fecha debe " \
                            "seguir el siguiente formato: dd/mm/aaaa.\n" \
                            "Por ejemplo: 07/12/2004.\n\n" \
                            "Copiar y pegar puede añadir elementos no " \
                            "visibles que producen error.\nInténtalo otra vez."
                        texto = Label(frame_txt, text=msg, justify="left",
                            font=(12), wraplength=600).pack(side="left")
                        frame_txt.pack(fill=X, padx=10, pady=20)
                        frame1 = Frame (error2_win)
                        boton1 = Button(frame1, text="Reintentar", command=reeditar2,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton1.bind('<Return>', lambda e:reeditar2())
                        boton1.focus()
                        boton1.pack(side="left", padx=10)
                        boton2 = Button(frame1, text="Cancelar", command=no_reeditar2,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton2.bind('<Return>', lambda e:no_reeditar2())
                        boton2.pack(side="left", padx=10)
                        frame1.pack(pady=10)
                        error2_win.bind('<Escape>', lambda e:no_reeditar2())
                        error2_win.mainloop()

                    if valor_in == "":      #borra la fecha

                        fecha_in = datetime.strptime(fecha_in, '%d/%m/%Y')

                        db = sqlite3.connect(base_datos)
                        cursor = db.cursor()
                        cursor.execute("DELETE FROM {} WHERE fecha = ?".format(isin_consultar[0]), (fecha_in,))
                        db.commit()
                        db.close()

                        editar_win.destroy()
                        consultar2_win.destroy()
                        cartera_win.grab_set()
                        inicia_consultar(fondo_consultar)

                    elif ((control_car == False) or (puntos > 1) or
                        (float(valor_in) == 0.0)):
                        # o len(fecha > 10)

                        error_win = Toplevel()
                        error_win.title('ERROR FORMATO VALOR')
                        error_win.resizable(width=False, height=False)

                        error_win.grab_set()
                        error_win.transient(editar_win)

                        sw = error_win.winfo_screenwidth()       # posicion
                        sh = error_win.winfo_screenheight()
                        sd = (sw - sh)
                        error_win.geometry('770x250+%d+%d' % (sd/2, sd/6))

                        img = PhotoImage(file="img/error.gif")
                        logo = Label(error_win, image=img)
                        logo.image = img
                        logo.pack(side="left", padx=10)
                        frame_txt = Frame(error_win)
                        msg = "Eso no parece correcto:\nEl valor sólo debe " \
                            "contener números y separar los decimales con " \
                            "un punto.\nEjemplos: 23.453980 ó 2145.42 " \
                            "ó 45.\n\nCopiar y pegar puede añadir elementos no " \
                            "visibles que producen error.\nInténtalo otra vez."
                        texto = Label(frame_txt, text=msg, justify="left",
                            font=(12), wraplength=600).pack(side="left")
                        frame_txt.pack(fill=X, padx=10, pady=20)
                        frame1 = Frame (error_win)
                        boton1 = Button(frame1, text="Reintentar", command=reeditar,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton1.bind('<Return>', lambda e:reeditar())
                        boton1.focus()
                        boton1.pack(side="left", padx=10)
                        boton2 = Button(frame1, text="Cancelar", command=no_reeditar,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton2.bind('<Return>', lambda e:no_reeditar())
                        boton2.pack(side="left", padx=10)
                        frame1.pack(pady=10)
                        error_win.bind('<Escape>', lambda e:no_reeditar())
                        error_win.mainloop()

                    else:
                        # ¿TRY?
                        valor_in = float(valor_in)
                        valor_in = round(valor_in, 6)
                        valor_in = format(valor_in, '.6f')

                        valor_in = str(valor_in)
                        valor_in = valor_in.replace(".", ",")
                        if len(valor_in) > 10:
                            valor_in = valor_in.replace(valor_in[:-10], valor_in[:-10] + ",", 1)

                        # Si la fecha EXISTE: UPDATE. Si NO EXISTE: INSERT
                        fecha_in = datetime.strptime(fecha_in, '%d/%m/%Y')

                        """
                        # ABRE LA TABLA DEL FONDO
                        db = sqlite3.connect(base_datos)
                        cursor = db.cursor()
                        cursor.execute("SELECT fecha from {} WHERE fecha = ?".format(isin_consultar[0]), (fecha_in,))
                        duplicada = cursor.fetchone()
                        db.close()

                        if duplicada is not None:  # Si la fecha ya existe
                            #msg_duple = "{}\nEl fondo no necesita " \
                                #"actualización.\nLa última cotización guardada " \
                                #"corresponde a esta fecha: {}.\n\n".format(nombre_fondo, fecha_nueva)
                            #with open("actualizado.txt", "r+", encoding='utf-8') as fichero:
                                #contenido = fichero.read()
                                #fichero.write(msg_duple)
                        """

                        try:
                            if capital_existe == "NO":
                                db = sqlite3.connect(base_datos)
                                cursor = db.cursor()
                                cursor.execute("INSERT INTO {} VALUES(?, ?)".format(isin_consultar[0]), (fecha_in, valor_in))
                                db.commit()
                                db.close()
                                #pass
                            else:
                                db = sqlite3.connect(base_datos)
                                cursor = db.cursor()
                                cursor.execute("INSERT INTO {} VALUES(?, ?, ?)".format(isin_consultar[0]), (fecha_in, valor_in, ''))
                                db.commit()
                                db.close()
                                #pass

                        except:
                            db = sqlite3.connect(base_datos)
                            cursor = db.cursor()
                            cursor.execute("UPDATE {} SET valor = ? WHERE fecha = ?".format(isin_consultar[0]), (valor_in, fecha_in))
                            db.commit()
                            db.close()
                            pass

                        editar_win.destroy()
                        consultar2_win.destroy()
                        cartera_win.grab_set()
                        inicia_consultar(fondo_consultar)

                editar_win = Toplevel()
                editar_win.title('Editar Valores')
                editar_win.resizable(width=False, height=False)

                editar_win.grab_set()
                editar_win.transient(consultar2_win)
                editar_win.update()

                sh = editar_win.winfo_screenheight()       # position
                sw = editar_win.winfo_screenwidth()
                sd = (sw - sh)
                editar_win.geometry('770x300+%d+%d' % (sd/2, sd/6))

                frame1 = Frame (editar_win)
                img1 = PhotoImage(file="img/nuevo.gif")
                logo1 = Label(frame1, image=img1)
                logo1.image = img1
                logo1.pack(side="left", padx=10)
                msg1 = "Introduce los datos según estos formatos:\n" \
                    "Fecha: dd/mm/aaaa (07/12/2004).\n" \
                    "Valor: Separa decimales con un punto " \
                    "(2524.430656).\n\n" \
                    "Si la fecha ya existe, el nuevo valor introducido " \
                    "sustituirá al anterior.\nAl dejar en blanco el valor, " \
                    "se elimina el registro de esa fecha."
                texto1 = Label(frame1, text=msg1, justify="left",
                    wraplength=600, font=(12)).pack(fill=X)

                entrada1 = Frame(frame1)
                Label(entrada1, text="Fecha:", bd=10, font=(12), width=8).pack(side="left")
                fecha_edit = Entry(entrada1, font=(12), width=16)
                fecha_edit.pack(side="left")
                fecha_edit.focus_set()
                limpiar_fecha = Button(entrada1, text="⌫", command=lambda: fecha_edit.delete(0, 'end'))
                limpiar_fecha.bind('<Return>', lambda e:fecha_edit.delete(0, 'end'))
                limpiar_fecha.pack(side="left")
                entrada1.pack(fill=X, padx=60)

                entrada2 = Frame(frame1)
                Label(entrada2, text="Valor:", bd=10, font=(12), width=8).pack(side="left")
                valor_edit = Entry(entrada2, font=(12), width=16)
                valor_edit.pack(side="left")
                limpiar_valor = Button(entrada2, text="⌫", command=lambda: valor_edit.delete(0, 'end'))
                limpiar_valor.bind('<Return>', lambda e:valor_edit.delete(0, 'end'))
                limpiar_valor.pack(side="left")
                entrada2.pack(fill=X, padx=60)

                frame1.pack(fill=X, padx=10, pady=10)

                frame2 = Frame(editar_win)
                boton_ok = Button(frame2, text="OK", cursor="hand1",
                    bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=control_editar)
                boton_ok.bind('<Return>', lambda e:control_editar())
                boton_ok.pack(side="left", padx=10)
                boton_cancel = Button(frame2, text="Volver", cursor="hand1",
                    bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=volver_editar)
                boton_cancel.bind('<Return>', lambda e:volver_editar())
                boton_cancel.pack(side="left", padx=10)
                frame2.pack(pady=10)

                editar_win.bind('<Escape>', lambda e:volver_editar())
                editar_win.mainloop()

            def volver_consultar2():
                mensaje2_win.destroy()
                cartera_win.grab_set()

            db = sqlite3.connect(base_datos)
            cursor = db.cursor()
            cursor.execute("SELECT isin from CARTERA1 WHERE nombre = ?", (fondo_consultar,))
            isin_consultar = cursor.fetchone()
            cursor.execute("SELECT * from {}".format(isin_consultar[0]))
            fondo_vacio = cursor.fetchone()
            db.close()

            if fondo_vacio is None:
                mensaje2_win = Toplevel()
                mensaje2_win.title('Cartera: Archivo vacío')
                mensaje2_win.resizable(width=False, height=False)

                mensaje2_win.grab_set()
                mensaje2_win.transient(cartera_win)

                sw = mensaje2_win.winfo_screenwidth()       # posicion
                sh = mensaje2_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje2_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/vacio.gif")
                logo = Label(mensaje2_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje2_win)
                msg = "El archivo del fondo {} está vacío. \n\nActualiza " \
                    "el fondo para añadir un valor al archivo.".format(fondo_consultar)
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje2_win, text="Volver",
                    command=volver_consultar2, cursor="hand1", bd=3,
                    activebackground="#ACD1E9", activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:volver_consultar2())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje2_win.bind('<Escape>', lambda e:volver_consultar2())
                mensaje2_win.mainloop()

            else:
                # Calcula índices de rentabilidad
                fechas_consultar = []
                valores_consultar = []
                #capital_existe = "NO"

                db = sqlite3.connect(base_datos)
                cursor = db.cursor()
                cursor.execute("SELECT * from {} ORDER BY fecha".format(isin_consultar[0]))
                historico = cursor.fetchall()
                for valor_h in historico:
                    fechas_consultar.append(valor_h[0])
                    valores_consultar.append(valor_h[1])
                db.close()
                
                db = sqlite3.connect(base_datos)
                cursor = db.cursor()
                cursor.execute("SELECT * from {}".format(isin_consultar[0]))
                fieldnames=[f[0] for f in cursor.description]
                #inversion = cursor.fetchone()                       
                db.close()
                if len(fieldnames) > 2:
                    capital_existe = "SI"                    
                    try:
                        db = sqlite3.connect(base_datos)
                        cursor = db.cursor()                    
                        cursor.execute("SELECT * from {} where capital != ''".format(isin_consultar[0]))
                        #cursor.execute("SELECT * from {}".format(isin_consultar[0]))
                        inversion = cursor.fetchone()
                        db.close()
                        fecha_inv = inversion[0]
                        valor_inv = inversion[1]
                        inversion = inversion[2]
                    except:
                        db = sqlite3.connect(base_datos)
                        cursor = db.cursor()                                            
                        cursor.execute("SELECT * from {}".format(isin_consultar[0]))
                        inversion = cursor.fetchone()
                        db.close()
                        fecha_inv = inversion[0]
                        valor_inv = inversion[1]
                        inversion = 0
                        pass
                        
                else:
                    capital_existe = "NO"
                    db = sqlite3.connect(base_datos)
                    cursor = db.cursor()
                    cursor.execute("SELECT * from {}".format(isin_consultar[0]))                    
                    inversion = cursor.fetchone()                    
                    db.close()                    
                    fecha_inv = inversion[0]
                    valor_inv = inversion[1]

                """
                try:
                    db = sqlite3.connect(base_datos)
                    cursor = db.cursor()
                    cursor.execute("SELECT * from {} where capital != ''".format(isin_consultar[0]))
                    #cursor.execute("SELECT * from {} where capital != ''".format(isin_consultar[0]))
                    inversion = cursor.fetchone()
                    if len(inversion) == 2:
                        capital_existe = "NO"
                        fecha_inv = inversion[0]
                        valor_inv = inversion[1]
                    db.close()
                except:
                    db = sqlite3.connect(base_datos)
                    cursor = db.cursor()
                    #cursor.execute("SELECT * from {} where capital != ''".format(isin_consultar[0]))
                    cursor.execute("SELECT * from {}".format(isin_consultar[0]))
                    inversion = cursor.fetchone()
                    db.close()
                    pass
                """

                if fondo_vacio is None:

                    mensaje2_win = Toplevel()
                    mensaje2_win.title('Cartera: Archivo vacío')
                    mensaje2_win.resizable(width=False, height=False)

                    mensaje2_win.grab_set()
                    mensaje2_win.transient(cartera_win)

                    sw = mensaje2_win.winfo_screenwidth()       # posicion
                    sh = mensaje2_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje2_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/vacio.gif")
                    logo = Label(mensaje2_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt = Frame(mensaje2_win)
                    msg = "El archivo del fondo {} está vacío. \n\nActualiza " \
                        "el fondo para añadir un valor al archivo.".format(fondo_consultar)
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600)
                    texto.config(font=(None, '12'))
                    texto.pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    boton = Button(mensaje2_win, text="Volver",
                        command=volver_consultar2, cursor="hand1", bd=3,
                        activebackground="#ACD1E9", activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:volver_consultar2())
                    boton.focus()
                    boton.pack(side="left", expand=1, pady=10)
                    mensaje2_win.bind('<Escape>', lambda e:volver_consultar2())
                    mensaje2_win.mainloop()

                """
                elif len(inversion) == 2:
                    capital_existe = "NO"
                    fecha_inv = inversion[0]
                    valor_inv = inversion[1]
                else:
                    capital_existe = "SI"
                    fecha_inv = inversion[0]
                    valor_inv = inversion[1]
                    inversion = inversion[2]
                """

                if len(fechas_consultar) > 1:
                    fecha_ini = fechas_consultar[0]
                    fecha_fin = fechas_consultar[-1]

                    fecha_ini = fecha_ini[0:10]
                    fecha_fin = fecha_fin[0:10]
                    fecha_ini = datetime.strptime(fecha_ini, "%Y-%m-%d")
                    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

                    #fecha_ini = datetime.strptime(fecha_ini, "%d/%m/%Y")
                    #fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")

                    delta = (fecha_fin - fecha_ini).days
                    delta = int(delta)

                    suma_valores = 0
                    for cada_valor in valores_consultar:
                        cada_valor = cada_valor.replace(".", "").replace(",", ".")
                        cada_valor = float(cada_valor)
                        suma_valores += cada_valor

                    media = suma_valores / len(valores_consultar)

                    sumatorio = 0
                    for cada_valor in valores_consultar:
                        cada_valor = cada_valor.replace(".", "").replace(",", ".")
                        cada_valor = float(cada_valor)
                        sumatorio += (cada_valor - media) ** 2
                    desviacion = (sumatorio / len(valores_consultar)) ** 0.5

                    #valores_cambio = []
                    #for cada_valor in valores_consultar:
                        #cada_valor = cada_valor.replace(".", "").replace(",", ".")
                        #cada_valor = float(cada_valor)
                        #valores_cambio.append(cada_valor)

                    valor_ini = valores_consultar[0]
                    valor_fin = valores_consultar[-1]
                    valor_ini = valor_ini.replace(".", "").replace(",", ".")
                    valor_fin = valor_fin.replace(".", "").replace(",", ".")
                    valor_ini = float(valor_ini)
                    valor_fin = float(valor_fin)

                    diferencia = (valor_fin - valor_ini)
                    ratio = valor_fin / valor_ini
                    desviacion = (format(desviacion, '.4f'))
                    rentabilidad = ((valor_fin - valor_ini) / valor_ini) * 100
                    tae = (((valor_fin/valor_ini) ** (365/delta))-1) * 100
                    diferencia = (format(diferencia, '+.6f'))
                    ratio = (format(ratio, '.4f'))
                    rentabilidad = (format(rentabilidad, '+.2f'))
                    tae = (format(tae, '+.2f'))

                    if capital_existe == "SI":
                        valor_inv = valor_inv.replace(".", "").replace(",", ".")
                        valor_inv = float(valor_inv)
                        reembolso = (inversion * valor_fin) / valor_inv

                        if reembolso >= inversion:
                            valia = "Plusvalía"
                        elif reembolso < inversion:
                            valia = "Minusvalía"
                        plus = reembolso - inversion

                        #fecha_inv = fecha_inv[0:10]
                        #fecha_inv = datetime.strptime(fecha_inv, "%Y-%m-%d")
                        fecha_inv = str(fecha_inv)
                        fe1_Y = fecha_inv[0:4]
                        fe1_m = fecha_inv[5:7]
                        fe1_d = fecha_inv[8:10]
                        fe1 = fe1_d + "/" + fe1_m + "/" + fe1_Y

                        fecha_inv2 = str(fecha_fin)
                        fe2_Y = fecha_inv2[0:4]
                        fe2_m = fecha_inv2[5:7]
                        fe2_d = fecha_inv2[8:10]
                        fe2 = fe2_d + "/" + fe2_m + "/" + fe2_Y

                        valor_inv = (format(valor_inv, '.2f'))
                        #inversion = (format(inversion, '.2f'))
                        #reembolso = (format(reembolso, '.2f'))
                        #plus = (format(plus, '+.2f'))


                        #valor_in = float(valor_in)
                        #valor_in = round(valor_in, 6)
                        #valor_in = format(valor_in, '.6f')
                        #valor_in = str(valor_in)
                        #valor_in = valor_in.replace(".", ",")
                        #if len(valor_in) > 10:
                            #valor_in = valor_in.replace(valor_in[:-10], valor_in[:-10] + ",", 1)

                        inversion = round(inversion, 2)
                        inversion = (format(inversion, '.2f'))
                        inversion = str(inversion)
                        inversion = inversion.replace(".", ",")
                        if len(inversion) > 6:
                            inversion = inversion.replace(inversion[:-6], inversion[:-6] + ".", 1)

                        reembolso = round(reembolso, 2)
                        reembolso = (format(reembolso, '.2f'))
                        reembolso = str(reembolso)
                        reembolso = reembolso.replace(".", ",")
                        if len(reembolso) > 6:
                            reembolso = reembolso.replace(reembolso[:-6], reembolso[:-6] + ".", 1)

                        plus = round(plus, 2)
                        plus = (format(plus, '+.2f'))
                        plus = str(plus)
                        plus = plus.replace(".", ",")
                        if len(plus) > 7:
                            plus = plus.replace(plus[:-7], plus[:-7] + ".", 1)

                # Muestra el archivo
                consultar2_win = Toplevel()
                consultar2_win.title('Cartera: HISTÓRICO DE VALORES')
                #msg_info = leeme
                #texto_info = Label(info_win, text=msg_info,
                    #wraplength=600, justify="left", bd=5).pack(fill=X)
                consultar2_win.resizable(width=False, height=False)

                consultar2_win.grab_set()
                consultar2_win.transient(cartera_win)

                sw = consultar2_win.winfo_screenwidth()       # posicion
                sh = consultar2_win.winfo_screenheight()
                h = sh * 0.7
                sd = (sw - sh)
                consultar2_win.geometry('770x%d+%d+%d' % (h, sd/2, sd/6))

                frame_con1 = Frame(consultar2_win)
                img = PhotoImage(file="img/trends.gif")
                logo = Label(frame_con1, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)

                msg_consultar2 = fondo_consultar + "\n" + isin_consultar[0]
                texto_consultar2 = Label(frame_con1, text=msg_consultar2,
                    justify="left",  wraplength=600, font=(12))
                texto_consultar2.config(font=(NONE, '12', 'bold'))
                texto_consultar2.pack(fill=X, pady=20)
                #frame_con1.pack(fill=X, padx=10, pady=5)

                frame_botones = Frame(frame_con1)
                boton_con = Button(frame_botones, text="Editar",
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF", command=editar)
                boton_con.bind('<Return>', lambda e:editar())
                boton_con.pack(side="left", padx=5)

                boton3_con = Button(frame_botones, text="Invertir",
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF", command=invertir)
                boton3_con.bind('<Return>', lambda e:invertir())
                boton3_con.pack(side="left", padx=5)

                boton2_con = Button(frame_botones, text="Exportar",
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF", command=exportar)
                boton2_con.bind('<Return>', lambda e:exportar())
                boton2_con.pack(side="left", padx=5)

                #frame_con3 = Frame(consultar2_win)
                boton1_con = Button(frame_botones, text="Volver",
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF", command=seguir)
                boton1_con.bind('<Return>', lambda e:seguir())
                boton1_con.focus()
                boton1_con.pack(side="left", padx=5)
                #frame_con3.pack(pady=5)

                frame_botones.pack()
                frame_con1.pack(fill=X, padx=10, pady=5)

                frame_con2 = Frame(consultar2_win)
                #scrollbar = Scrollbar(frame_con2, orient=VERTICAL)

                #listbox_consultar2 = Listbox(frame_con2,
                    #selectmode=EXTENDED, activestyle='none',
                    #disabledforeground="black",
                    #yscrollcommand=scrollbar.set, selectborderwidth=2)
                #texto_consultar = Text(frame_con2,
                #    yscrollcommand=scrollbar.set, selectborderwidth=2)

                texto_consultar = Text(frame_con2)
                scroll = Scrollbar(texto_consultar, command=texto_consultar.yview)
                texto_consultar.configure(yscrollcommand=scroll.set)

                db = sqlite3.connect(base_datos)
                cursor = db.cursor()
                cursor.execute("SELECT * from {} ORDER BY fecha".format(isin_consultar[0]))
                historico = cursor.fetchall()
                db.close()

                #db = sqlite3.connect(base_datos)
                #cursor = db.cursor()
                #cursor.execute("SELECT * from {} where capital != ''".format(isin_consultar[0]))
                #inversion = cursor.fetchone()
                #valor_inv = inversion[1]
                #inversion = inversion[2]
                #db.close()

                #if ((inversion == "") or (inversion == 0.0) or (inversion is None)):
                    #print("NADA")
                #else:
                    #print(inversion)

                #for valor_ha in historico:
                    #fecha_or = str(valor_ha[0])
                    #fecha_Y = fecha_or[-4:]
                    #fecha_m = fecha_or[3:5]
                    #fecha_d = fecha_or[0:2]
                    #fecha_total = fecha_Y + "/" + fecha_m + "/" + fecha_d
                    #print(fecha_total)

                #fecha_in = datetime.strptime(fecha_in, "%d/%m/%Y")
                #fecha_in = datetime.strftime(fecha_in, "%d/%m/%Y")

                if len(fechas_consultar) > 1:
                    texto_consultar.tag_configure('big', font=(NONE, 14, 'bold'), foreground='#476042')
                    #texto_consultar.tag_configure('derecha', tabs=10)
                    if diferencia[0] == "-":
                        texto_consultar.tag_configure('color', foreground='red')
                    else:
                        texto_consultar.tag_configure('color', foreground='#476042')

                    if ((capital_existe == "SI") and (valia == "Plusvalía")):
                        texto_consultar.tag_configure('color2', font=(NONE, 12, 'bold'), foreground='#476042')
                    else:
                        texto_consultar.tag_configure('color2', font=(NONE, 12, 'bold'), foreground='red')

                    texto_consultar.insert(END, "Índices de Rentabilidad" + "\n", 'big')
                    texto_consultar.insert(END, "Balance período: ")
                    texto_consultar.insert(END, diferencia + "\n", 'color')
                    texto_consultar.insert(END, "Ratio rentabilidad: ")
                    texto_consultar.insert(END, ratio + "\n", 'color')
                    texto_consultar.insert(END, "Variabilidad: ")
                    texto_consultar.insert(END, desviacion + "\n", 'color')
                    texto_consultar.insert(END, "Rentab. Económica: ")
                    texto_consultar.insert(END, rentabilidad + " %" + "\n", 'color')
                    texto_consultar.insert(END, "Rentab. Anualizada: ")
                    texto_consultar.insert(END, tae + " %" + "\n", 'color')

                    #if (capital_existe == "NO"):
                    if ((capital_existe == "NO") or (inversion == "0,00")):
                    #if ((inversion == "") or (inversion == 0.0) or (inversion is None)):
                        texto_consultar.insert(END, "\n\n")

                    #elif (capital_existe == "SI"):
                    elif ((capital_existe == "SI") and (inversion != "0,00")):
                        #inversion = str(inversion)
                        #reembolso = str(reembolso)
                        #fecha_inv = str(fecha_inv)
                        #plus = str(plus)
                        texto_consultar.insert(END, "Suscripción (" + fe1 + "): ")
                        texto_consultar.insert(END, inversion + " €" + "\n")
                        texto_consultar.insert(END, "Reembolso  (" + fe2 + "): ")
                        texto_consultar.insert(END, reembolso + " €" + "\n")
                        texto_consultar.insert(END, valia + ": ")
                        texto_consultar.insert(END, plus + " €" + "\n\n", 'color2')

                    else:
                        texto_consultar.insert(END, "\n\n")

                    texto_consultar.insert(END, "Histórico de Valores" + "\n", 'big')
                    #texto_consultar.insert(END, "Fechas" + "\t\t" + "Valores" + "\n")
                    #if ((inversion == "") or (inversion == 0.0) or (inversion is None)):
                    texto_consultar.insert(
                        END, "FECHAS" + "\t\t" + "VALORES".rjust(10) +
                        "\t\t" + "CAMBIO".rjust(14) + "\t\t" +
                        "% CAMBIO".rjust(12) + "\n")
                    #else:
                        #texto_consultar.insert(
                            #END, "FECHAS" + "\t\t" + "VALORES".rjust(10) +
                            #"\t\t" + "CAMBIO".rjust(14) + "\t\t" +
                            #"% CAMBIO".rjust(12) + "\t\t" + "CAPITAL" + "\n")

                valores_cambio = []
                for valor_h in historico:
                    #listbox_consultar2.insert(END, valor_h[0] + ":   " + valor_h[1].rjust(4)+ " EUR")
                    fecha_or = str(valor_h[0])
                    fecha_Y = fecha_or[0:4]
                    fecha_m = fecha_or[5:7]
                    fecha_d = fecha_or[8:10]
                    fecha_total = fecha_d + "/" + fecha_m + "/" + fecha_Y

                    cada_valor = valor_h[1].replace(".", "").replace(",", ".")
                    cada_valor = float(cada_valor)
                    valores_cambio.append(cada_valor)

                    contador = len(valores_cambio)
                    if contador > 1:
                        i = 1
                        for val in range(contador - 1):
                            dif = valores_cambio[i] - valores_cambio[i-1]
                            dif = round(dif, 6)
                            #dif_por = (100 * dif) / valores_cambio[i-1]
                            dif_por = dif / valores_cambio[i-1]

                            dif = format(dif, '.6f')
                            dif_por = format(dif_por, '.2%')
                            #if dif == "+0.00":
                                #dif = "0.00"
                            i += 1
                    else:
                        dif = "---"
                        dif_por = "---"

                    texto_consultar.insert(
                        END, fecha_total + "\t\t" + valor_h[1].rjust(4) +
                        " EUR" + "\t\t" + dif.rjust(14) + "\t\t" +
                        dif_por.rjust(14)+ "\n")

                    #texto_consultar.insert(END, fecha_total + "\t\t" + valor_h[1].rjust(4)+ " EUR" + "\n")

                #db.close()      # ¿MEJOR MÁS ARRIBA?

                #scrollbar.config(command=listbox_consultar2.yview)
                #scrollbar.config(command=texto_consultar.yview)
                #scrollbar.pack(side=RIGHT, fill=Y)
                #listbox_consultar2.config(exportselection=0,
                    #font=(NONE, '10', 'bold'), state=DISABLED)
                #listbox_consultar2.pack(side=LEFT, fill=BOTH, expand=1)
                texto_consultar.config(exportselection=0,
                    font=(NONE, '10', 'bold'), state=DISABLED)
                texto_consultar.pack(side=LEFT, fill=BOTH, expand=1)
                scroll.pack(side=RIGHT, fill=Y)
                frame_con2.pack(fill=BOTH, expand=1)

                #frame_con3 = Frame(consultar2_win)
                #boton1_con = Button(frame_con3, text="Volver",
                    #cursor="hand1", bd=3, activebackground="#ACD1E9",
                    #activeforeground="#FFFFFF", command=seguir)
                #boton1_con.bind('<Return>', lambda e:seguir())
                #boton1_con.focus()
                #boton1_con.pack(side="left", padx=10)
                #frame_con3.pack(pady=5)
                consultar2_win.bind('<Escape>', lambda e:seguir())
                consultar2_win.mainloop()

        if comprobar_cartera():
            fondos_isin = []
            fondos_nombre = []
            db = sqlite3.connect(base_datos)
            cursor = db.cursor()
            cursor.execute("SELECT * from CARTERA1")
            total_cartera = cursor.fetchall()
            for cart in total_cartera:
                fondos_isin.append(cart[0])
                fondos_nombre.append(cart[1])
            db.close()

            indice = listbox_fondos.curselection()

            def volver_consultar():
                mensaje_win.destroy()
                cartera_win.grab_set()

            # Si se hace clic en OK sin ninguna selección
            if len(indice) == 0:
                mensaje_win = Toplevel()
                mensaje_win.title('Cartera: Error de Selección')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(cartera_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/noselect.gif")
                logo = Label(mensaje_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje_win)
                msg = "No ha seleccionado ningún Fondo para consultar."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje_win, text="Volver", command=volver_consultar,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:volver_consultar())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje_win.bind('<Escape>', lambda e:volver_consultar())
                mensaje_win.mainloop()

            elif len(indice) > 1:
                mensaje_win = Toplevel()
                mensaje_win.title('Cartera: Error de Selección')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(cartera_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/noselect.gif")
                logo = Label(mensaje_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje_win)
                msg = "¿Qué Fondo quieres consultar?\n" \
                    "Selecciona sólo un Fondo para consultar."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje_win, text="Volver", command=volver_consultar,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:volver_consultar())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje_win.bind('<Escape>', lambda e:volver_consultar())
                mensaje_win.mainloop()

            else:
                fondos_consultar = [listbox_fondos.get(idx) for idx in listbox_fondos.curselection()]
                fondo_consultar = fondos_consultar[0]
                inicia_consultar(fondo_consultar)


    ## BORRAR
    def activa_borrar(fondos_nombre):

        if comprobar_cartera():

            fondos_isin = []
            fondos_nombre = []
            db = sqlite3.connect(base_datos)
            cursor = db.cursor()
            cursor.execute("SELECT * from CARTERA1")
            total_cartera = cursor.fetchall()
            for cart in total_cartera:
                fondos_isin.append(cart[0])
                fondos_nombre.append(cart[1])
            db.close()

            fondos_borrar = [listbox_fondos.get(idx) for idx in listbox_fondos.curselection()]

            #if fondos_borrar != None:   # Cuando se hace click en OK

            def volver_borrar():
                mensaje_win.destroy()
                cartera_win.grab_set()

            # Si se hace clic en OK sin ninguna selección
            if len(fondos_borrar) == 0:
                mensaje_win = Toplevel()
                mensaje_win.title('Cartera: Error de Selección')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(cartera_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/noselect.gif")
                logo = Label(mensaje_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje_win)
                msg = "No ha seleccionado ningún Fondo para borrar."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600).pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje_win, text="Volver",
                    command=volver_borrar,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:volver_borrar())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje_win.bind('<Escape>', lambda e:volver_borrar())
                mensaje_win.mainloop()

            else:

                def confirma():
                    def ir_cartera3():
                        mensaje2_win.destroy()
                        #cartera_win.grab_set()
                        cartera_win.destroy()
                        operaciones(base_datos)

                    db = sqlite3.connect(base_datos)
                    cursor = db.cursor()
                    for cada_fondo in fondos_borrar:
                        cursor.execute("SELECT isin from CARTERA1 WHERE nombre = ?", (cada_fondo,))
                        for isin_borrar in cursor:
                            cursor.execute("DELETE from {}".format(isin_borrar[0]))
                            db.commit()
                    db.commit()
                    db.close()

                    # Mensaje de confirmación de borrado
                    mensaje_win.destroy()

                    mensaje2_win = Toplevel()
                    mensaje2_win.title('Cartera: ARCHIVO BORRADO')
                    mensaje2_win.resizable(width=False, height=False)

                    mensaje2_win.grab_set()
                    mensaje2_win.transient(cartera_win)

                    sw = mensaje2_win.winfo_screenwidth()       # posicion
                    sh = mensaje2_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje2_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/borrar.gif")
                    logo = Label(mensaje2_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt = Frame(mensaje2_win)
                    msg = "Han sido borrados " \
                        "los datos de {} Fondo(s).".format(
                        len(fondos_borrar))
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600)
                    texto.config(font=(None, '12'))
                    texto.pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    boton = Button(mensaje2_win, text="Continuar", command=ir_cartera3,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:ir_cartera3())
                    boton.focus()
                    boton.pack(side="left", expand=1, pady=10)
                    mensaje2_win.bind('<Escape>', lambda e:ir_cartera3())
                    mensaje2_win.mainloop()

                def no_confirma():
                    mensaje_win.destroy()
                    cartera_win.grab_set()

                mensaje_win = Toplevel()
                mensaje_win.title('Cartera: Confirma Borrar Valores')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(cartera_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                h = sh * 0.7
                sd = (sw - sh)
                mensaje_win.geometry('770x%d+%d+%d' % (h, sd/2, sd/6))

                frame1_bor = Frame(mensaje_win)

                img = PhotoImage(file="img/caution.gif")
                logo = Label(frame1_bor, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)

                frame_txt = Frame(frame1_bor)
                msg = "IMPORTANTE:\nLos Fondos seleccionados  " \
                    "perderán todos los datos archivados.\n" \
                    "Esos Fondos continuarán en tu Cartera.\n\nSe " \
                    "borrará el histórico de valores de {} Fondo(s):".format(
                    len(fondos_borrar))
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600).pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=10)

                frame = Frame(frame1_bor)
                boton1 = Button(frame, text='Borrar', cursor="hand1", bd=3,
                    activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=confirma)
                boton1.bind('<Return>', lambda e:confirma())
                boton1.pack(side="left", padx=10)
                boton2 = Button(frame, text='Volver', cursor="hand1", bd=3,
                    activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=no_confirma)
                boton2.bind('<Return>', lambda e:no_confirma())
                boton2.focus()
                boton2.pack(padx=10)
                frame.pack(pady=10)

                frame1_bor.pack(fill=X, padx=10, pady=5)

                frame_bor = Frame(mensaje_win)
                texto = scrolledtext.ScrolledText(frame_bor, wrap="word")
                texto.configure(state=NORMAL)
                #texto.insert(END, fondos_borrar)
                for cada_fondo in fondos_borrar:
                    texto.insert(END, cada_fondo+"\n")
                texto.configure(state=DISABLED, padx=5)
                texto.pack(fill=BOTH, expand=1)
                frame_bor.pack(fill=BOTH, expand=1)

                mensaje_win.bind('<Escape>', lambda e:no_confirma())
                mensaje_win.mainloop()


    ## NUEVO FONDO
    def activa_nuevo():

        fondo_nombre = ""
        fondo_url = ""

        def control_isin():
            # Enlaces de salida
            def ir_nuevo1():
                mensaje1_win.destroy()
                nuevo_win1.grab_set()
            def no_reintentar():
                mensaje1_win.destroy()
                nuevo_win1.destroy()
                cartera_win.grab_set()
            def ir_nuevoc():
                mensajec_win.destroy()
                nuevo_win1.grab_set()
            def no_reintentarc():
                mensajec_win.destroy()
                nuevo_win1.destroy()
                cartera_win.grab_set()

            def verificado_isin():
                # Define los elementos del fondo (nombre, url y archivo)
                fondo_url = "http://www.quefondos.com/m/es/fondos/ficha/index.html?isin=" + isin

                def ir_nuevo3():
                    mensaje3_win.destroy()
                    nuevo_win1.grab_set()
                def ir_nuevo4():
                    mensaje4_win.destroy()
                    nuevo_win1.grab_set()
                def ir_nuevo5():
                    mensaje5_win.destroy()

                # Abre la web para extraer el nombre
                try:                    # Para comprobar que carga la web
                    # web = urlopen(web, timeout=5)
                    web_fondo = urlopen(fondo_url, timeout=5)   # 5

                except URLError:        # Mensaje de error si no reconoce la URL
                    mensaje3_win = Toplevel()
                    mensaje3_win.title('ERROR: URL no encontrada')
                    mensaje3_win.resizable(width=False, height=False)

                    mensaje3_win.grab_set()
                    mensaje3_win.transient(nuevo_win1)

                    sw = mensaje3_win.winfo_screenwidth()       # posicion
                    sh = mensaje3_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje3_win.geometry('770x280+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/cerrado.gif")
                    logo = Label(mensaje3_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt= Frame(mensaje3_win)
                    msg = "Lo siento, pero ha sido imposible conectar con la " \
                        "página web de ese fondo.\n\nComprueba tu conexión a internet " \
                        "y que has introducido correctamente el código ISIN.\n\n" \
                        "Quizá VDOS Stochastics S.L no suministra información " \
                        "sobre ese fondo en su plataforma o la web no está " \
                        "disponible en este momento.\nPrueba más tarde."
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600).pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    boton = Button(mensaje3_win, text="Continuar", command=ir_nuevo3,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:ir_nuevo3())
                    boton.focus()
                    boton.pack(side="left", expand=1, pady=10)
                    mensaje3_win.bind('<Escape>', lambda e:ir_nuevo3())
                    mensaje3_win.mainloop()

                except timeout:         # Error si no abre la web en 5 segundos
                    mensaje4_win = Toplevel()
                    mensaje4_win.title('ERROR: Tiempo de conexión excedido')
                    mensaje4_win.resizable(width=False, height=False)

                    mensaje4_win.grab_set()
                    mensaje4_win.transient(nuevo_win1)

                    sw = mensaje4_win.winfo_screenwidth()       # posicion
                    sh = mensaje4_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje4_win.geometry('770x280+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/cerrado.gif")
                    logo = Label(mensaje4_win, image=img).pack(side="left", padx=10)
                    frame_txt = Frame(mensaje4_win)
                    msg = "Lo siento, pero ha sido imposible conectar con la " \
                        "página web de ese fondo.\n\nComprueba tu conexión a internet " \
                        "y que has introducido correctamente el código ISIN.\n\n" \
                        "Quizá VDOS Stochastics S.L no suministra información " \
                        "sobre ese fondo en su plataforma o la web no está " \
                        "disponible en este momento.\nPrueba más tarde."
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600).pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    boton = Button(mensaje4_win, text="Continuar", command=ir_nuevo4,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:ir_nuevo4())
                    boton.focus()
                    boton.pack(side="left", expand=1, pady=10)
                    mensaje4_win.bind('<Escape>', lambda e:ir_nuevo4())
                    mensaje4_win.mainloop()

                for line in web_fondo:              # Recorre el texto de la web abierta
                    linea_fondo = str(line)         # Convierte el texto en una cadena
                    # Busca las líneas con los datos coincidentes y las limpia
                    # b'<h2>ING DIRECT FONDO NARANJA DINAMICO, FI</h2>\n'
                    if "b'<h2>" in linea_fondo and "</h2>" in linea_fondo:
                        fondo_nombre = linea_fondo[6:-8]
                    elif "<h2>" in linea_fondo and "</h2>" in linea_fondo:
                        fondo_nombre = linea_fondo[6:-8]
                fondo_nombre = fondo_nombre.replace("&amp;", "&")
                fondo_nombre = fondo_nombre.replace("&Ntilde;", "Ñ")
                # nuevo_fondo = [fondo_nombre, fondo_url, fondo_archivo]
                fondo_nombre = repr(fondo_nombre)
                fondo_url = repr(fondo_url)
                #fondo_archivo = repr(fondo_archivo)
                #nuevo_fondo = fondo_nombre + ", " + fondo_url + ", " + fondo_archivo
                web_fondo.close()

                # Después de confirmar "Añadir"
                def continuar5():

                    def nuevo6():
                        mensaje6_win.destroy()
                    def ir_portada():
                        mensaje7_win.destroy()
                        cartera_win.destroy()
                        operaciones(base_datos)

                    # Confirma que el fondo no existe en el archivo

                    # Confirma que el fondo no existe en la base de datos
                    #fondo_nombre_db = fondo_nombre.strip("'")
                    #fondo_url_db = fondo_url.strip("'")
                    db = sqlite3.connect(base_datos)
                    cursor = db.cursor()
                    cursor.execute("SELECT isin from CARTERA1 WHERE isin = ?", (isin,))
                    existe = cursor.fetchone()
                    db.close()

                    if existe is None:      #no existe el fondo
                        # Añade el nuevo fondo a la tabla CARTERA
                        fondo_nombre_db = fondo_nombre.strip("'")
                        fondo_url_db = fondo_url.strip("'")

                        db = sqlite3.connect(base_datos)
                        cursor = db.cursor()
                        cursor.execute("INSERT INTO CARTERA1 VALUES (?,?)", (isin, fondo_nombre_db))
                        db.commit()
                        #db.close()

                        #Crea una nueva tabla para el fondo
                        #db = sqlite3.connect('carfoins.db')
                        #cursor = db.cursor()
                        cursor.execute("CREATE TABLE {} (fecha text unique, valor real)".format(isin))
                        db.commit()
                        #db.close()

                        #Actualización de menú
                        #db = sqlite3.connect('carfoins.db')
                        #cursor = db.cursor()
                        cursor.execute("SELECT * from CARTERA1")
                        tabla_vacia = cursor.fetchall()
                        db.commit()
                        db.close()

                        if len(tabla_vacia) == 0:
                            cartera_menu.entryconfig(0, state=DISABLED)
                            cartera_menu.entryconfig(1, state=DISABLED)
                            cartera_menu.entryconfig(2, state=DISABLED)
                            mercado_menu.entryconfig(1, state=DISABLED)
                        else:
                            cartera_menu.entryconfig(0, state=NORMAL)
                            cartera_menu.entryconfig(1, state=NORMAL)
                            cartera_menu.entryconfig(2, state=NORMAL)
                            mercado_menu.entryconfig(1, state=NORMAL)

                        # Mensaje de Fondo Añadido
                        mensaje5_win.destroy()
                        mensaje7_win = Toplevel()
                        mensaje7_win.title('Mercado: NUEVO FONDO')
                        mensaje7_win.resizable(width=False, height=False)

                        mensaje7_win.grab_set()
                        mensaje7_win.transient(cartera_win)

                        sw = mensaje7_win.winfo_screenwidth()       # posicion
                        sh = mensaje7_win.winfo_screenheight()
                        sd = (sw - sh)
                        mensaje7_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                        img = PhotoImage(file="img/check.gif")
                        logo = Label(mensaje7_win, image=img)
                        logo.image = img
                        logo.pack(side="left", padx=10)
                        frame_txt = Frame(mensaje7_win)
                        msg = "El Fondo {} se ha incorporado a tu Cartera.\n\nAhora puedes " \
                            "obtener el último valor desde la opción 'Actualizar' de " \
                            "'Mi Cartera' o seguir en 'Mercado' para añadir más " \
                            "Fondos.".format(fondo_nombre)
                        texto = Label(frame_txt, text=msg, justify="left",
                            font=(12), wraplength=600).pack(side="left")
                        frame_txt.pack(fill=X, padx=10, pady=20)
                        boton = Button(mensaje7_win, text="Continuar", command=ir_portada,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton.bind('<Return>', lambda e:ir_portada())
                        boton.focus()
                        boton.pack(side="left", expand=1, pady=10)
                        mensaje7_win.bind('<Escape>', lambda e:ir_portada())
                        mensaje7_win.mainloop()

                    else:       #ya existe el fondo
                        mensaje5_win.destroy()
                        mensaje6_win = Toplevel()
                        mensaje6_win.title('Mercado: FONDO DUPLICADO')
                        mensaje6_win.resizable(width=False, height=False)

                        mensaje6_win.grab_set()
                        mensaje6_win.transient(cartera_win)

                        sw = mensaje6_win.winfo_screenwidth()       # posicion
                        sh = mensaje6_win.winfo_screenheight()
                        sd = (sw - sh)
                        mensaje6_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                        img = PhotoImage(file="img/info.gif")
                        logo = Label(mensaje6_win, image=img)
                        logo.image = img
                        logo.pack(side="left", padx=10)
                        frame_txt = Frame(mensaje6_win)
                        msg = "Nada que hacer: ese Fondo ya forma parte de tu Cartera."
                        texto = Label(frame_txt, text=msg, justify="left",
                            font=(12), wraplength=600).pack(side="left")
                        frame_txt.pack(fill=X, padx=10, pady=20)
                        boton = Button(mensaje6_win, text="Continuar", command=nuevo6,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton.bind('<Return>', lambda e:nuevo6())
                        boton.focus()
                        boton.pack(side="left", expand=1, pady=10)
                        mensaje6_win.bind('<Escape>', lambda e:nuevo6())
                        mensaje6_win.mainloop()

                # Confirma el nombre del fondo
                nuevo_win1.destroy()            ## CIERRA LA PRIMERA VENTANA
                mensaje5_win = Toplevel()
                mensaje5_win.title('Mercado: FONDO ENCONTRADO')
                mensaje5_win.resizable(width=False, height=False)

                mensaje5_win.grab_set()
                mensaje5_win.transient(cartera_win)

                sw = mensaje5_win.winfo_screenwidth()       # posicion
                sh = mensaje5_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje5_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/abierto.gif")
                logo = Label(mensaje5_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje5_win)
                msg = "El ISIN introducido corresponde al fondo\n{}.\n\n¿Quieres " \
                    "añadir este Fondo?".format(fondo_nombre)
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600).pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                frame_en = Frame(mensaje5_win)
                boton1 = Button(frame_en, text="Añadir",
                    command=lambda: continuar5(), cursor="hand1",
                    bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF")
                boton1.bind('<Return>', lambda e:continuar5())
                boton1.focus()
                boton1.pack(side="left")
                boton2 = Button(frame_en, text="Cancelar", command=ir_nuevo5,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton2.bind('<Return>', lambda e:ir_nuevo5())
                boton2.pack(side="left", padx=10)
                frame_en.pack(pady=5)
                mensaje5_win.bind('<Escape>', lambda e:ir_nuevo5())
                mensaje5_win.mainloop()

            # Obtiene la entrada introducida
            isin = isin_win.get()
            # Control ISIN por formato
            if ((len(isin) != 12) or (isin.isalnum() == False) or
                (isin == "") or (isin[0:2].isalpha() == False) or
                ("Ñ" in isin) or ("ñ" in isin)):
            #or (isin[2:].isdigit() == False):
                # nuevo_win1.destroy()
                mensaje1_win = Toplevel()
                mensaje1_win.title('ERROR ISIN: Formato')
                mensaje1_win.resizable(width=False, height=False)

                mensaje1_win.grab_set()
                mensaje1_win.transient(nuevo_win1)

                sw = mensaje1_win.winfo_screenwidth()       # posicion
                sh = mensaje1_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje1_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/cerrado.gif")
                logo = Label(mensaje1_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje1_win)
                msg = "Eso no parece correcto: Un código ISIN debe contener 12 " \
                    "caracteres alfanuméricos y cumplir una estructura " \
                    "específica para los Fondos de Inversión.\n\n" \
                    "Inténtalo otra vez."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600).pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                frame1 = Frame (mensaje1_win)
                boton1 = Button(frame1, text="Reintentar", command=ir_nuevo1,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton1.bind('<Return>', lambda e:ir_nuevo1())
                boton1.focus()
                boton1.pack(side="left", padx=10)
                boton2 = Button(frame1, text="Cancelar", command=no_reintentar,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton2.bind('<Return>', lambda e:no_reintentar())
                boton2.pack(side="left", padx=10)
                frame1.pack(pady=10)
                mensaje1_win.bind('<Escape>', lambda e:no_reintentar())
                mensaje1_win.mainloop()

            # Superado primer control de formato
            elif isin:
                isin = isin.upper()
                isin_control = []
                isin_valor = {
                    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                    '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10,
                    'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
                    'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20,
                    'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25,
                    'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30,
                    'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}
                ind = 0

                # Control ISIN por caracteres
                for caracter_isin in isin:
                    if caracter_isin not in isin_valor:
                        mensajec_win = Toplevel()
                        mensajec_win.title('ERROR ISIN: Carácter no reconocido')
                        mensajec_win.resizable(width=False, height=False)

                        mensajec_win.grab_set()
                        mensajec_win.transient(nuevo_win1)

                        sw = mensajec_win.winfo_screenwidth()       # posicion
                        sh = mensajec_win.winfo_screenheight()
                        sd = (sw - sh)
                        mensajec_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                        img = PhotoImage(file="img/cerrado.gif")
                        logo = Label(mensajec_win, image=img)
                        logo.image = img
                        logo.pack(side="left", padx=10)
                        frame_txt = Frame(mensajec_win)
                        msg = "Eso no parece correcto: Un código ISIN debe contener 12 " \
                            "caracteres alfanuméricos y cumplir una estructura " \
                            "específica para los Fondos de Inversión.\n\n" \
                            "Inténtalo otra vez."
                        texto = Label(frame_txt, text=msg, justify="left",
                            font=(12), wraplength=600).pack(side="left")
                        frame_txt.pack(fill=X, padx=10, pady=20)
                        frame1 = Frame (mensajec_win)
                        boton1 = Button(frame1, text="Reintentar", command=ir_nuevoc,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton1.bind('<Return>', lambda e:ir_nuevoc())
                        boton1.focus()
                        boton1.pack(side="left", padx=10)
                        boton2 = Button(frame1, text="Cancelar", command=no_reintentarc,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton2.bind('<Return>', lambda e:no_reintentarc())
                        boton2.pack(side="left", padx=10)
                        frame1.pack(pady=10)
                        mensajec_win.bind('<Escape>', lambda e:no_reintentarc())
                        mensajec_win.mainloop()

                # Control ISIN por dígito de control
                for caracter_isin in enumerate(isin):  # Recorre caracteres ISIN
                    valor_caracter = isin_valor[isin[ind]]     # Asigna valores
                    ind += 1
                    isin_control.append(valor_caracter)  # Añade valores a lista
                del isin_control[11]                 # Elimina dígito de control

                valores_letras=[]
                for valores in isin_control:
                    if valores < 10:
                        #valores = str(valores)
                        valores_letras.append(valores)
                    elif valores > 9:
                        valores = str(valores)
                        valor_1=int(valores[0])
                        valor_2=int(valores[1])
                        valores_letras.append(valor_1)
                        valores_letras.append(valor_2)
                isin_control = valores_letras

                # Fórmula para calcular dígito de control
                isin_impares = isin_control[::2]
                isin_pares = isin_control[1::2]

                if (len(isin_impares)) > (len(isin_pares)):
                    isin_imparesx2 = [caract * 2 for caract in isin_impares]
                    valores_impares = []
                    for ci in isin_imparesx2:    # Cuando aparecen números de 2 dígitos
                        if ci < 10:
                            valores_impares.append(ci)
                        elif ci > 9:
                            ci = str(ci)
                            ci1 = int(ci[0])
                            ci2 = int(ci[1])
                            valores_impares.append(ci1)
                            valores_impares.append(ci2)
                    isin_imparesx2 = valores_impares
                    isin_digitos = isin_imparesx2 + isin_pares

                else:
                    isin_paresx2 = [caract * 2 for caract in isin_pares]
                    valores_pares = []
                    for cp in isin_paresx2:    # Cuando aparecen números de 2 dígitos
                        if cp < 10:
                            valores_pares.append(cp)
                        elif cp > 9:
                            cp = str(cp)
                            cp1 = int(cp[0])
                            cp2 = int(cp[1])
                            valores_pares.append(cp1)
                            valores_pares.append(cp2)
                    isin_paresx2 = valores_pares
                    isin_digitos = isin_paresx2 + isin_impares
                suma = 0
                for dig in isin_digitos:
                    suma += dig
                suma = str(suma)        # Suma todos los dígitos
                digit_control = int(suma) % 10
                digit_control = 10 - digit_control
                digit_control = digit_control % 10
                digit_control = int(digit_control)

                def ir_nuevo2():
                    mensaje2_win.destroy()
                    nuevo_win1.grab_set()
                def no_reintentar2():
                    mensaje2_win.destroy()
                    nuevo_win1.destroy()
                    cartera_win.grab_set()

                # Comparar digit_control con el último caracter de isin
                if digit_control != int(isin[11]):

                    mensaje2_win = Toplevel()
                    mensaje2_win.title('ERROR ISIN: Dígito de Control')
                    mensaje2_win.resizable(width=False, height=False)

                    mensaje2_win.grab_set()
                    mensaje2_win.transient(nuevo_win1)

                    sw = mensaje2_win.winfo_screenwidth()       # posicion
                    sh = mensaje2_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje2_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/cerrado.gif")
                    logo = Label(mensaje2_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt = Frame(mensaje2_win)
                    msg = "Eso no parece correcto: Sistema de verificación por " \
                        "dígito de control no superado.\n\nComprueba que has " \
                        "introducido correctamente el código ISIN.\nInténtalo otra vez."
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600).pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    frame2 = Frame (mensaje2_win)
                    boton1 = Button(frame2, text="Reintentar", command=ir_nuevo2,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton1.bind('<Return>', lambda e:ir_nuevo2())
                    boton1.focus()
                    boton1.pack(side="left", padx=10)
                    boton2 = Button(frame2, text="Cancelar", command=no_reintentar2,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton2.bind('<Return>', lambda e:no_reintentar2())
                    boton2.pack(side="left", padx=10)
                    frame2.pack(pady=10)
                    mensaje2_win.bind('<Escape>', lambda e:no_reintentar2())
                    mensaje2_win.mainloop()

                elif digit_control == int(isin[11]):    # ISIN Verificado
                    verificado_isin()

        ################ Solicita código ISIN: Ventana de código ISIN
        nuevo_win1 = Toplevel()
        nuevo_win1.title('Mercado: CÓDIGO ISIN')
        nuevo_win1.resizable(width=False, height=False)

        nuevo_win1.grab_set()
        nuevo_win1.transient(cartera_win)
        nuevo_win1.update()

        sh = nuevo_win1.winfo_screenheight()       # position
        sw = nuevo_win1.winfo_screenwidth()
        sd = (sw - sh)
        nuevo_win1.geometry('770x250+%d+%d' % (sd/2, sd/6))

        frame_n1 = Frame (nuevo_win1)
        img_nuevo_win1 = PhotoImage(file="img/key.gif")
        logo_nuevo_win1 = Label(frame_n1, image=img_nuevo_win1)
        logo_nuevo_win1.image = img_nuevo_win1
        logo_nuevo_win1.pack(side="left", padx=10)
        msg_nuevo_win1 = "Introduce el código ISIN del Fondo de " \
            "Inversión que quieres incorporar a tu Cartera.\n\nEl programa " \
            "verifica ese código y lo utiliza como clave para buscar vía " \
            "internet el Fondo vinculado."
        texto_nuevo_win1 = Label(frame_n1, text=msg_nuevo_win1, justify="left",
            wraplength=600, font=(12)).pack(fill=X, pady=10)
        Label(frame_n1, text="Código ISIN:", bd=10, font=(12)).pack(side="left")
        isin_win = Entry(frame_n1, font=(12))
        isin_win.pack(side="left")
        isin_win.focus_set()
        # botón para limpiar entry
        limpiar = Button(frame_n1, text="⌫", command=lambda: isin_win.delete(0, 'end'))
        limpiar.bind('<Return>', lambda e:isin_win.delete(0, 'end'))
        limpiar.pack(side="left")
        frame_n1.pack(fill=X, padx=10, pady=20)

        frame_nuevo_win1 = Frame(nuevo_win1)
        boton_ok = Button(frame_nuevo_win1, text="OK", cursor="hand1",
            bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
            command=control_isin)
        boton_ok.bind('<Return>', lambda e:control_isin())
        boton_ok.pack(side="left", padx=10)
        boton_cancel = Button(frame_nuevo_win1, text="Volver", cursor="hand1",
            bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
            command=nuevo_win1.destroy)
        boton_cancel.bind('<Return>', lambda e:nuevo_win1.destroy())
        boton_cancel.pack(side="left", padx=10)
        frame_nuevo_win1.pack(pady=10)

        nuevo_win1.bind('<Escape>', lambda e:nuevo_win1.destroy())
        nuevo_win1.mainloop()


    ## ELIMINAR FONDO
    def activa_eliminar():

        if comprobar_cartera():
            cartera = []
            fondo = []

            fondos_isin = []
            fondos_nombre = []
            db = sqlite3.connect(base_datos)
            cursor = db.cursor()
            cursor.execute("SELECT * from CARTERA1")
            total_cartera = cursor.fetchall()
            for cart in total_cartera:
                fondos_isin.append(cart[0])
                fondos_nombre.append(cart[1])
            db.close()

            fondos_eliminar = [listbox_fondos.get(idx) for idx in listbox_fondos.curselection()]

            ##if fondos_eliminar != None:   # Cuando se hace click en OK

            def volver_quitar():
                mensaje_win.destroy()
                cartera_win.grab_set()

            # Si se hace clic en OK sin ninguna selección
            if len(fondos_eliminar) == 0:

                mensaje_win = Toplevel()
                mensaje_win.title('Mercado: Error de Selección')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(cartera_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/noselect.gif")
                logo = Label(mensaje_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje_win)
                msg = "No ha seleccionado ningún Fondo para eliminar."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje_win, text="Volver",
                    command=lambda: volver_quitar(),  # invocar funcion para además eliminar_win.grab_set()
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:volver_quitar())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje_win.bind('<Escape>', lambda e:volver_quitar())
                mensaje_win.mainloop()

            else:

                # Ventana de confirmación
                def confirma():
                    def ir_operar3():
                        mensaje2_win.destroy()
                        cartera_win.destroy()
                        operaciones(base_datos)

                    # Para cada fondo seleccionado para quitar
                    #Por cada_fondo in fondos_eliminar:
                    db = sqlite3.connect(base_datos)
                    cursor = db.cursor()
                    for cada_fondo in fondos_eliminar:
                        cursor.execute("SELECT isin from CARTERA1 WHERE nombre = ?", (cada_fondo,))
                        for isin_eliminar in cursor:
                            cursor.execute("DROP TABLE {}".format(isin_eliminar[0]))
                            db.commit()
                        cursor.execute("DELETE from CARTERA1 WHERE nombre = ?", (cada_fondo,))
                        db.commit()
                    db.commit()
                    #db.close()

                    #Actualización de menú
                    #db = sqlite3.connect('carfoins.db')
                    #cursor = db.cursor()
                    cursor.execute("SELECT * from CARTERA1")
                    tabla_vacia = cursor.fetchall()
                    db.commit()
                    db.close()
                    if len(tabla_vacia) == 0:
                        cartera_menu.entryconfig(0, state=DISABLED)
                        cartera_menu.entryconfig(1, state=DISABLED)
                        cartera_menu.entryconfig(2, state=DISABLED)
                        mercado_menu.entryconfig(1, state=DISABLED)
                    else:
                        cartera_menu.entryconfig(0, state=NORMAL)
                        cartera_menu.entryconfig(1, state=NORMAL)
                        cartera_menu.entryconfig(2, state=NORMAL)
                        mercado_menu.entryconfig(1, state=NORMAL)

                    # Mensaje de confirmación de borrado
                    mensaje_win.destroy()

                    mensaje2_win = Toplevel()
                    mensaje2_win.title('Mercado: FONDOS ELIMINADOS')
                    mensaje2_win.resizable(width=False, height=False)

                    mensaje2_win.grab_set()
                    mensaje2_win.transient(cartera_win)

                    sw = mensaje2_win.winfo_screenwidth()       # posicion
                    sh = mensaje2_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje2_win.geometry('770x200+%d+%d' % (sd/2, sd/6))
                    #('770x250+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/flame.gif")
                    logo = Label(mensaje2_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt = Frame(mensaje2_win)
                    msg = "Eliminado(s) {} fondos.".format(
                        len(fondos_eliminar))
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600)
                    texto.config(font=(None, '12'))
                    texto.pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    boton = Button(mensaje2_win, text="Continuar",
                        command=ir_operar3,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:ir_operar3())
                    boton.focus()
                    boton.pack(side="left", expand=1, pady=10)
                    mensaje2_win.bind('<Escape>', lambda e:ir_operar3())
                    mensaje2_win.mainloop()

                def no_confirma():
                    mensaje_win.destroy()
                    cartera_win.grab_set()

                # Si se hace clic en OK con alguna selección
                mensaje_win = Toplevel()
                mensaje_win.title('Mercado: Confirma Eliminar Fondos')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(cartera_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                h = sh * 0.7
                mensaje_win.geometry('770x%d+%d+%d' % (h, sd/2, sd/6))

                frame1_eli = Frame(mensaje_win)

                img = PhotoImage(file="img/caution.gif")
                logo = Label(frame1_eli, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)

                frame_txt = Frame(frame1_eli)

                msg = "IMPORTANTE:\nLos fondos seleccionados se perderán " \
                    "definitivamente.\nTambién se borrarán los datos de sus " \
                    "valores.\n\nSe eliminarán de tu Cartera {} " \
                    "fondo(s):".format(len(fondos_eliminar))
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)

                frame = Frame(frame1_eli)
                boton1 = Button(frame, text='Eliminar', cursor="hand1", bd=3,
                    activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=confirma)
                boton1.bind('<Return>', lambda e:confirma())
                boton1.pack(side="left", padx=10)
                boton2 = Button(frame, text='Volver', cursor="hand1", bd=3,
                    activebackground="#ACD1E9", activeforeground="#FFFFFF",
                    command=no_confirma)
                boton2.bind('<Return>', lambda e:no_confirma())
                boton2.focus()
                boton2.pack(side="left", padx=10)
                frame.pack(pady=10)

                frame1_eli.pack(fill=X, padx=10, pady=5)

                frame_eli = Frame(mensaje_win)
                texto = scrolledtext.ScrolledText(frame_eli, wrap="word")
                texto.configure(state=NORMAL)
                #texto.insert(END, fondos_quitar)
                for cada_fondo in fondos_eliminar:
                    texto.insert(END, cada_fondo+"\n")
                texto.configure(state=DISABLED, padx=5)
                texto.pack(fill=BOTH, expand=1)
                frame_eli.pack(fill=BOTH, expand=1)

                mensaje_win.bind('<Escape>', lambda e:no_confirma())
                mensaje_win.mainloop()

    ### FRAME CUERPO
    frame_cuerpo = Frame(cartera_win, height=cuerpo)

    ### FRAME TITULO
    frame_titulo = Frame(frame_cuerpo)
    #img_cartera = PhotoImage(file="img/cartera.gif")
    #logo_cartera = Label(frame_titulo, image=img_cartera)
    #logo_cartera.image = img_cartera
    #logo_cartera.pack(side="left", padx=10, pady=30)
    titulo = Label(frame_titulo, text='Cartera: ' + base_datos[0:-3])
    titulo.config(font=(NONE, 20, 'bold'), fg='#6D929B')
    titulo.pack(expand=YES, fill=BOTH)

    db = sqlite3.connect(base_datos)
    cursor = db.cursor()
    cursor.execute("SELECT * from CARTERA1")
    tabla_vacia = cursor.fetchall()
    db.close()

    if len(tabla_vacia) == 0:
        msg_rt = ""

    else:
        todos_isin = []
        db = sqlite3.connect(base_datos)
        cursor = db.cursor()
        cursor.execute("SELECT * from CARTERA1")
        total_isin = cursor.fetchall()
        for cada_isin in total_isin:
            todos_isin.append(cada_isin[0])
        db.close()

        #total_rentabilidad = []
        #total_tae = []
        suma_rt = 0
        #suma_tae = 0
        n_fondos = 0
        for un_isin in todos_isin:
            # Calcula índices de rentabilidad para cada fondo de la cartera
            fechas_consultar = []
            valores_consultar = []

            db = sqlite3.connect(base_datos)
            cursor = db.cursor()
            cursor.execute("SELECT * from {} ORDER BY fecha".format(un_isin))
            historico = cursor.fetchall()
            for valor_h in historico:
                fechas_consultar.append(valor_h[0])
                valores_consultar.append(valor_h[1])
            db.close()

            if len(fechas_consultar) > 1:
                n_fondos += 1
                fecha_ini = fechas_consultar[0]
                fecha_fin = fechas_consultar[-1]
                fecha_ini = fecha_ini[0:10]
                fecha_fin = fecha_fin[0:10]

                #fecha_ini = datetime.strptime(fecha_ini, "%d/%m/%Y")
                #fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
                fecha_ini = datetime.strptime(fecha_ini, "%Y-%m-%d")
                fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
                delta = (fecha_fin - fecha_ini).days
                delta = int(delta)

                valor_ini = valores_consultar[0]
                valor_fin = valores_consultar[-1]

                #if len(valor_ini) < 11:
                    #valor_ini = valor_ini.replace(",", ".")
                #else:
                    #valor_ini = valor_ini.replace(".", "")
                    #valor_ini = valor_ini.replace(",", ".")

                #if len(valor_fin) < 11:
                    #valor_fin = valor_fin.replace(",", ".")
                #else:
                    #valor_fin = valor_fin.replace(".", "")
                    #valor_fin = valor_fin.replace(",", ".")

                valor_ini = valor_ini.replace(".", "").replace(",", ".")
                valor_fin = valor_fin.replace(".", "").replace(",", ".")

                valor_ini = float(valor_ini)
                valor_fin = float(valor_fin)

                rentabilidad = 0
                tae = 0
                #diferencia = (valor_fin - valor_ini)
                rentabilidad = ((valor_fin - valor_ini) / valor_ini) * 100
                #tae = ((valor_fin/valor_ini) ** (365/delta)-1) * 100
                #diferencia = (format(diferencia, '.6f'))
                #rentabilidad = (format(rentabilidad, '.2f'))
                #tae = (format(tae, '.2f'))
                #total_rentabilidad.append(rentabilidad)
                #total_tae.append(tae)
                suma_rt += rentabilidad
                #suma_tae += tae

        if suma_rt != 0:
            media_rt = suma_rt / n_fondos

            #suma_rt = "{:+.2f}".format(suma_rt)
            suma_rt = format(suma_rt, '+.2f')
            media_rt = format(media_rt, '+.2f')

            #media_tae = suma_tae / n_fondos
            #suma_tae = format(suma_tae, '.2f')
            #media_tae = format(media_tae, '.2f')

            #suma_rt = 0
            #for rt in total_rentabilidad:
                #suma_rt += rt
            msg_rt = "Rentabilidad Total: " + suma_rt + "%" + "\t\t" + "Rentabilidad Media: " + media_rt + "%"

        else:
            msg_rt = ""

    rentabilidad_total = Label(frame_titulo, text=msg_rt)
    rentabilidad_total.config(font=(NONE, '10', 'bold'))
    rentabilidad_total.pack()

    frame_titulo.pack()

    ### FRAME DE BOTONES DE ACCIÓN

    frame_botones = Frame(frame_cuerpo)
    botones_cartera = LabelFrame(frame_botones, bd=5, relief=GROOVE,
        padx=10, pady=10, text="CARTERA")

    img_boton_act = PhotoImage(file="img/bajarboton.gif")
    boton_act = Button(botones_cartera, text="Actualizar", image=img_boton_act,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=lambda:activa_actualizar(fondos_nombre))
    boton_act.image = img_boton_act
    boton_act.bind('<Return>', lambda e:activa_actualizar(fondos_nombre))
    boton_act.pack(padx=10, pady=5, fill=X)

    img_boton_con = PhotoImage(file="img/lupaboton.gif")
    boton_con = Button(botones_cartera, text="Consultar", image=img_boton_con,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=lambda:activa_consultar(fondos_nombre))
    boton_con.bind('<Return>', lambda e:activa_consultar(fondos_nombre))
    boton_con.pack(padx=10, pady=5, fill=X)

    img_boton_bor = PhotoImage(file="img/recycleboton.gif")
    boton_bor = Button(botones_cartera, text="Borrar    ", image=img_boton_bor,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command= lambda:activa_borrar(fondos_nombre))
    boton_bor.bind('<Return>', lambda e:activa_borrar(fondos_nombre))
    boton_bor.pack(padx=10, pady=5, fill=X)

    botones_cartera.pack()
    botones_mercado = LabelFrame(frame_botones, bd=5, relief=GROOVE,
        padx=10, pady=10, text="MERCADO")

    img_boton_nue = PhotoImage(file="img/nuevoboton.gif")
    boton_nue = Button(botones_mercado, text="Nuevo     ", image=img_boton_nue,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=activa_nuevo)
    boton_nue.bind('<Return>', lambda e:activa_nuevo())
    boton_nue.pack(padx=10, pady=5, fill=X)

    img_boton_eli = PhotoImage(file="img/eliminarboton.gif")
    boton_eli = Button(botones_mercado, text="Eliminar", image=img_boton_eli,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=activa_eliminar)
    boton_eli.bind('<Return>', lambda e:activa_eliminar())
    boton_eli.pack(padx=10, pady=5, fill=X)

    botones_mercado.pack(pady=20)

    img_boton_ini = PhotoImage(file="img/start.gif")
    boton_ini = Button(frame_botones, text="Inicio    ", image=img_boton_ini,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=ir_bienvenida)
    boton_ini.bind('<Return>', lambda e:ir_bienvenida())
    boton_ini.pack(padx=10, pady=5)

    frame_botones.pack(side="left", padx=50)

    ### FRAME VENTANA DE FONDOS

    frame_fondos = Frame(frame_cuerpo)

    scrollbar = Scrollbar(frame_fondos, orient=VERTICAL)
    listbox_fondos = Listbox(frame_fondos, selectmode=EXTENDED, activestyle='dotbox',
        yscrollcommand=scrollbar.set, selectborderwidth=2)

    db = sqlite3.connect(base_datos)
    cursor = db.cursor()
    cursor.execute("SELECT * from CARTERA1 ORDER BY nombre")
    total_fondos = cursor.fetchall()
    for fondo in total_fondos:
        listbox_fondos.insert(END, fondo[1])
    db.close()

    scrollbar.config(command=listbox_fondos.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox_fondos.config(font=(NONE, '10', 'bold'))
    listbox_fondos.focus()
    listbox_fondos.pack(side=LEFT, fill=BOTH, expand=1)

    #frame_fondos.config(width=mitad_w)
    frame_fondos.pack(padx=30, side="left", fill=BOTH, expand=1)

    frame_cuerpo.pack(fill=X)

    cartera_win.bind("<Control-n>", lambda event:ir_nuevo())
    cartera_win.bind("<Control-q>", lambda event:sys.exit())
    cartera_win.bind('<F1>', lambda event:ir_info())
    cartera_win.bind('<Alt-i>', lambda event:ir_bienvenida())
    cartera_win.mainloop()               # FIN VENTANA DE OPERACIONES


# INICIO. Mensaje de Bienvenida
def bienvenida(tab=1):

    ## Crear tabla si no existe
    if os.path.isfile("carfoins.db"):
        pass
    else:
        db = sqlite3.connect("carfoins.db")
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE CARTERAS
            (cartera text unique)
            ''')
        db.commit()
        db.close()

    def paypal():
        webbrowser.open(
            "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=986PSAHLH6N4L")
    def carfoins_web():
        webbrowser.open("http://www.carfoins.esy.es/")

    # Ventana de Presentación
    bienvenida_win = Tk()
    bienvenida_win.title('Inicio')
    bienvenida_win.resizable(width=False, height=False)

    sw = bienvenida_win.winfo_screenwidth()    # tamaño y posicion
    sh = bienvenida_win.winfo_screenheight()

    sd = (sw - sh)
    bienvenida_win.geometry("%dx%d+0+0" % (sw, sh))  #Posicion
    cuerpo = int(sh*0.85)
    pie = int(sh-cuerpo)

    note = ttk.Notebook(bienvenida_win, height=cuerpo)  #sh-150

    #################### PESTAÑA 1: INICIO
    tab1 = Frame(note)

    frame_inicio = Frame(tab1)
    msg_bienvenida = "\nCARFOIN$© 2015\nJesús Cuerda Villanueva\n" \
        "Versión: 0.4.6 - Licencia GPLv3"
    texto_bienvenida = Label(frame_inicio, text=msg_bienvenida,
        bg="#ACD1E9", fg='#2E64FE').pack(fill=X)
    img_bienvenida = PhotoImage(file="img/carfoins.gif")
    logo_bienvenida = Label(frame_inicio, image=img_bienvenida,
        bg="#ACD1E9").pack(fill=X)
    frame_inicio.pack(padx=10, pady=10, fill=X)

    def nueva_cartera():

        def control_cartera():

            def reintentar():
                mensaje1_win.destroy()
                nuevo_win.grab_set()
            def no_reintentar():
                mensaje1_win.destroy()
                nuevo_win.destroy()
                bienvenida_win.grab_set()
            def entrar():
                mi_cartera = nombre_cartera + ".db"
                mensaje_win.destroy()
                bienvenida_win.destroy()
                operaciones(mi_cartera)

            nombre_cartera = car_win.get()  # Obtiene el nombre introducido

            if ((len(nombre_cartera) > 15) or (nombre_cartera.isalnum() == False) or
                (nombre_cartera == "") or (nombre_cartera == "carfoins")):

                mensaje1_win = Toplevel()
                mensaje1_win.title('ERROR NOMBRE CARTERA')
                mensaje1_win.resizable(width=False, height=False)

                mensaje1_win.grab_set()
                mensaje1_win.transient(bienvenida_win)

                sw = mensaje1_win.winfo_screenwidth()       # posicion
                sh = mensaje1_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje1_win.geometry('770x250+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/error.gif")
                logo = Label(mensaje1_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje1_win)
                msg = "Eso no parece correcto. Comprueba que el " \
                    "nombre introducido:\n" \
                    "- No supera los 15 caracteres.\n" \
                    "- Está compuesto sólo de letras y/o números.\n" \
                    "- No contiene espacios en blanco, acentos, " \
                    "guiones ni otros símbolos.\n" \
                    "- La palabra 'carfoins' está reservada para " \
                    "el sistema.\n\nInténtalo otra vez."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600).pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                frame1 = Frame (mensaje1_win)
                boton1 = Button(frame1, text="Reintentar", command=reintentar,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton1.bind('<Return>', lambda e:reintentar())
                boton1.focus()
                boton1.pack(side="left", padx=10)
                boton2 = Button(frame1, text="Cancelar", command=no_reintentar,
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton2.bind('<Return>', lambda e:no_reintentar())
                boton2.pack(side="left", padx=10)
                frame1.pack(pady=10)
                mensaje1_win.bind('<Escape>', lambda e:no_reintentar())
                mensaje1_win.mainloop()

            elif nombre_cartera:    #Superado el primer control

                caracter_valido = ["0", "1", "2", "3", "4", "5", "6",
                    "7", "8", "9", "a", "A", "b", "B", "c", "C", "d",
                    "D", "e", "E", "f", "F", "g", "G", "h", "H", "i",
                    "I", "j", "J", "k", "K", "l", "L", "m", "M", "n",
                    "N", "ñ", "Ñ", "o", "O", "p", "P", "q", "Q", "r",
                    "R", "s", "S", "t", "T", "u", "U", "v", "V", "w",
                    "W", "x", "X", "y", "Y", "z", "Z"]
                for caracter in nombre_cartera:
                    if caracter not in caracter_valido:

                        mensaje1_win = Toplevel()
                        mensaje1_win.title('ERROR NOMBRE CARTERA')
                        mensaje1_win.resizable(width=False, height=False)

                        mensaje1_win.grab_set()
                        mensaje1_win.transient(bienvenida_win)

                        sw = mensaje1_win.winfo_screenwidth()       # posicion
                        sh = mensaje1_win.winfo_screenheight()
                        sd = (sw - sh)
                        mensaje1_win.geometry('770x250+%d+%d' % (sd/2, sd/6))

                        img = PhotoImage(file="img/error.gif")
                        logo = Label(mensaje1_win, image=img)
                        logo.image = img
                        logo.pack(side="left", padx=10)
                        frame_txt = Frame(mensaje1_win)
                        msg = "Eso no parece correcto. Comprueba que el " \
                            "nombre introducido:\n" \
                            "- No supera los 15 caracteres.\n" \
                            "- Está compuesto sólo de letras y/o números.\n" \
                            "- No contiene espacios en blanco, acentos, " \
                            "guiones ni otros símbolos.\n" \
                            "- La palabra 'carfoins' está reservada para " \
                            "el sistema.\n\nInténtalo otra vez."
                        texto = Label(frame_txt, text=msg, justify="left",
                            font=(12), wraplength=600).pack(side="left")
                        frame_txt.pack(fill=X, padx=10, pady=20)
                        frame1 = Frame (mensaje1_win)
                        boton1 = Button(frame1, text="Reintentar", command=reintentar,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton1.bind('<Return>', lambda e:reintentar())
                        boton1.focus()
                        boton1.pack(side="left", padx=10)
                        boton2 = Button(frame1, text="Cancelar", command=no_reintentar,
                            cursor="hand1", bd=3, activebackground="#ACD1E9",
                            activeforeground="#FFFFFF")
                        boton2.bind('<Return>', lambda e:no_reintentar())
                        boton2.pack(side="left", padx=10)
                        frame1.pack(pady=10)
                        mensaje1_win.bind('<Escape>', lambda e:no_reintentar())
                        mensaje1_win.mainloop()

                # 1) Comprueba que el nombre no existe ya
                db = sqlite3.connect("carfoins.db")
                cursor = db.cursor()
                cursor.execute("SELECT cartera from CARTERAS WHERE cartera = ?", (nombre_cartera,))
                existe = cursor.fetchone()
                db.close()

                def duplicado():
                    mensaje_win.destroy()
                    nuevo_win.grab_set()

                def volver_inicio():
                    mensaje_win.destroy()
                    bienvenida_win.destroy()
                    bienvenida()  # 3) Refresca la ventana de Carteras

                if existe is None:
                    # 2) Lo introduce en la base de datos
                    db = sqlite3.connect("carfoins.db")
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO CARTERAS VALUES (?)", (nombre_cartera,))
                    db.commit()
                    db.close()

                    # Mensaje de Fondo Añadido
                    nuevo_win.destroy()
                    mensaje_win = Toplevel()
                    mensaje_win.title('NUEVO CARTERA')
                    mensaje_win.resizable(width=False, height=False)

                    mensaje_win.grab_set()
                    mensaje_win.transient(bienvenida_win)

                    sw = mensaje_win.winfo_screenwidth()       # posicion
                    sh = mensaje_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/check.gif")
                    logo = Label(mensaje_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt = Frame(mensaje_win)
                    msg = "Has creado la cartera {}.\n\nAhora puedes " \
                        "entrar en ella para incorporar los Fondos de " \
                        "Inversión que te interesa seguir o volver a " \
                        "la pantalla de inicio.".format(nombre_cartera)
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600).pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)

                    frame_botones = Frame(mensaje_win)
                    boton = Button(frame_botones, text="Entrar", command=entrar,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:entrar())
                    boton.focus()
                    boton.pack(side="left", padx=10, pady=10)

                    boton = Button(frame_botones, text="Volver", command=volver_inicio,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:volver_inicio())
                    boton.pack(side="left", padx=10, pady=10)
                    frame_botones.pack()

                    mensaje_win.bind('<Escape>', lambda e:volver_inicio())
                    mensaje_win.mainloop()

                else:

                    #mensaje5_win.destroy()
                    mensaje_win = Toplevel()
                    mensaje_win.title('CARTERA DUPLICADA')
                    mensaje_win.resizable(width=False, height=False)

                    mensaje_win.grab_set()
                    mensaje_win.transient(nuevo_win)

                    sw = mensaje_win.winfo_screenwidth()       # posicion
                    sh = mensaje_win.winfo_screenheight()
                    sd = (sw - sh)
                    mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                    img = PhotoImage(file="img/info.gif")
                    logo = Label(mensaje_win, image=img)
                    logo.image = img
                    logo.pack(side="left", padx=10)
                    frame_txt = Frame(mensaje_win)
                    msg = "Ya existe una Cartera con ese nombre."
                    texto = Label(frame_txt, text=msg, justify="left",
                        font=(12), wraplength=600).pack(side="left")
                    frame_txt.pack(fill=X, padx=10, pady=20)
                    boton = Button(mensaje_win, text="Continuar", command=duplicado,
                        cursor="hand1", bd=3, activebackground="#ACD1E9",
                        activeforeground="#FFFFFF")
                    boton.bind('<Return>', lambda e:duplicado())
                    boton.focus()
                    boton.pack(side="left", expand=1, pady=10)
                    mensaje_win.bind('<Escape>', lambda e:duplicado())
                    mensaje_win.mainloop()

        ################ Solicita nombre nueva Cartera
        nuevo_win = Toplevel()
        nuevo_win.title('NUEVA CARTERA')
        nuevo_win.resizable(width=False, height=False)

        nuevo_win.grab_set()
        nuevo_win.transient(bienvenida_win)
        nuevo_win.update()

        sh = nuevo_win.winfo_screenheight()       # position
        sw = nuevo_win.winfo_screenwidth()
        sd = (sw - sh)
        nuevo_win.geometry('770x250+%d+%d' % (sd/2, sd/6))

        img_nuevo_win = PhotoImage(file="img/cartera.gif")
        logo_nuevo_win = Label(nuevo_win, image=img_nuevo_win)
        logo_nuevo_win.image = img_nuevo_win
        logo_nuevo_win.pack(side="left", padx=10)

        frame_nc = Frame(nuevo_win)
        msg_nuevo_win = "Introduce el nombre de tu nueva Cartera.\n\n" \
            "Hasta 15 caracteres alfanuméricos."
        texto_nuevo_win = Label(frame_nc, text=msg_nuevo_win, justify="left",
            wraplength=600, font=(12)).pack(side="left", pady=10)
        frame_nc.pack(fill=X, padx=10, pady=10)

        frame_entrada = Frame(nuevo_win)
        Label(frame_entrada, text="Cartera:", bd=10, font=(12)).pack(side="left")
        car_win = Entry(frame_entrada, font=(12))
        car_win.pack(side="left")
        car_win.focus_set()
        # botón para limpiar entry
        limpiar = Button(frame_entrada, text="⌫", command=lambda: car_win.delete(0, 'end'))
        limpiar.bind('<Return>', lambda e:car_win.delete(0, 'end'))
        limpiar.pack(side="left")
        frame_entrada.pack(fill=X, pady=20)

        frame_nuevo_win = Frame(nuevo_win)
        boton_ok = Button(frame_nuevo_win, text="OK", cursor="hand1",
            bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
            command=control_cartera)
        boton_ok.bind('<Return>', lambda e:control_cartera())
        boton_ok.pack(side="left", padx=10)
        boton_cancel = Button(frame_nuevo_win, text="Volver", cursor="hand1",
            bd=3, activebackground="#ACD1E9", activeforeground="#FFFFFF",
            command=nuevo_win.destroy)
        boton_cancel.bind('<Return>', lambda e:nuevo_win.destroy())
        boton_cancel.pack(side="left", padx=10)
        frame_nuevo_win.pack()

        nuevo_win.bind('<Escape>', lambda e:nuevo_win.destroy())
        nuevo_win.mainloop()


    def comprobar_sel():
        indice_cartera = listbox_carteras.curselection()

        if len(indice_cartera) == 0:
            mensaje_win = Toplevel()
            mensaje_win.title('Error de Selección')
            mensaje_win.resizable(width=False, height=False)

            mensaje_win.grab_set()
            mensaje_win.transient(bienvenida_win)

            sw = mensaje_win.winfo_screenwidth()       # posicion
            sh = mensaje_win.winfo_screenheight()
            sd = (sw - sh)
            mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

            img = PhotoImage(file="img/noselect.gif")
            logo = Label(mensaje_win, image=img)
            logo.image = img
            logo.pack(side="left", padx=10)
            frame_txt = Frame(mensaje_win)
            msg = "No ha seleccionado ninguna Cartera."
            texto = Label(frame_txt, text=msg, justify="left",
                font=(12), wraplength=600)
            texto.config(font=(None, '12'))
            texto.pack(side="left")
            frame_txt.pack(fill=X, padx=10, pady=20)
            boton = Button(mensaje_win, text="Volver",
                command=lambda: mensaje_win.destroy(),
                cursor="hand1", bd=3, activebackground="#ACD1E9",
                activeforeground="#FFFFFF")
            boton.bind('<Return>', lambda e:mensaje_win.destroy())
            boton.focus()
            boton.pack(side="left", expand=1, pady=10)
            mensaje_win.bind('<Escape>', lambda e:mensaje_win.destroy())
            mensaje_win.mainloop()
            return False
        else:
            return True

    def ir_operaciones():
        if comprobar_sel():
            mi_cartera = listbox_carteras.get(listbox_carteras.curselection())
            mi_cartera = mi_cartera + ".db"
            bienvenida_win.destroy()
            operaciones(mi_cartera)

    def eliminar_car():
        if comprobar_sel():

            cartera_eliminar = listbox_carteras.get(listbox_carteras.curselection())

            def confirma():
                db = sqlite3.connect("carfoins.db")
                cursor = db.cursor()
                cursor.execute("DELETE from CARTERAS WHERE cartera = ?", (cartera_eliminar,))
                db.commit()
                db.close()
                try:
                    archivo_eliminar = cartera_eliminar+".db"
                    remove(archivo_eliminar)
                except:
                    pass
                mensaje_win.destroy()
                bienvenida_win.destroy()
                bienvenida()

            def no_confirma():
                mensaje_win.destroy()
                bienvenida_win.grab_set()

            # Si se hace clic en OK con alguna selección
            mensaje_win = Toplevel()
            mensaje_win.title('Confirma Eliminar Cartera')
            mensaje_win.resizable(width=False, height=False)

            mensaje_win.grab_set()
            mensaje_win.transient(bienvenida_win)

            sw = mensaje_win.winfo_screenwidth()       # posicion
            sh = mensaje_win.winfo_screenheight()
            sd = (sw - sh)
            h = sh * 0.7
            mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

            frame1_eli = Frame(mensaje_win)

            img = PhotoImage(file="img/caution.gif")
            logo = Label(frame1_eli, image=img)
            logo.image = img
            logo.pack(side="left", padx=10)

            frame_txt = Frame(frame1_eli)

            msg = "IMPORTANTE:\nLa cartera {}\ny los fondos que contiene " \
                "se perderán definitivamente.".format(cartera_eliminar)
            texto = Label(frame_txt, text=msg, justify="left",
                font=(12), wraplength=600)
            texto.config(font=(None, '12'))
            texto.pack(side="left")
            frame_txt.pack(fill=X, padx=10, pady=20)

            frame = Frame(frame1_eli)
            boton1 = Button(frame, text='Eliminar', cursor="hand1", bd=3,
                activebackground="#ACD1E9", activeforeground="#FFFFFF",
                command=confirma)
            boton1.bind('<Return>', lambda e:confirma())
            boton1.pack(side="left", padx=10)
            boton2 = Button(frame, text='Volver', cursor="hand1", bd=3,
                activebackground="#ACD1E9", activeforeground="#FFFFFF",
                command=no_confirma)
            boton2.bind('<Return>', lambda e:no_confirma())
            boton2.focus()
            boton2.pack(side="left", padx=10)
            frame.pack(pady=10)

            frame1_eli.pack(fill=X, padx=10, pady=5)

            mensaje_win.bind('<Escape>', lambda e:no_confirma())
            mensaje_win.mainloop()


    def backup():
        cartera_exportar = ""
        original = ""

        def volver_backup():
            mensaje_win.destroy()
            bienvenida_win.grab_set()

        if comprobar_sel():
            cartera_exportar = listbox_carteras.get(listbox_carteras.curselection())
            original = cartera_exportar + ".db"
            copia = 'backup/{}'.format(original)
            try:
                shutil.copy(original, copia)

            except:
                mensaje_win = Toplevel()
                mensaje_win.title('Error de Copia')
                mensaje_win.resizable(width=False, height=False)

                mensaje_win.grab_set()
                mensaje_win.transient(bienvenida_win)

                sw = mensaje_win.winfo_screenwidth()       # posicion
                sh = mensaje_win.winfo_screenheight()
                sd = (sw - sh)
                mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

                img = PhotoImage(file="img/error.gif")
                logo = Label(mensaje_win, image=img)
                logo.image = img
                logo.pack(side="left", padx=10)
                frame_txt = Frame(mensaje_win)
                msg = "Se ha producido un error al intentar hacer una " \
                    "copia de seguridad.\n\nComprueba que:\n" \
                    "- existe la carpeta carfoins/backup.\n" \
                    "- esa Cartera tiene Fondos."
                texto = Label(frame_txt, text=msg, justify="left",
                    font=(12), wraplength=600)
                texto.config(font=(None, '12'))
                texto.pack(side="left")
                frame_txt.pack(fill=X, padx=10, pady=20)
                boton = Button(mensaje_win, text="Volver",
                    command=lambda: volver_backup(),
                    cursor="hand1", bd=3, activebackground="#ACD1E9",
                    activeforeground="#FFFFFF")
                boton.bind('<Return>', lambda e:volver_backup())
                boton.focus()
                boton.pack(side="left", expand=1, pady=10)
                mensaje_win.bind('<Escape>', lambda e:volver_backup())
                mensaje_win.mainloop()

            mensaje_win = Toplevel()
            mensaje_win.title('Copia de Seguridad realizada')
            mensaje_win.resizable(width=False, height=False)

            mensaje_win.grab_set()
            mensaje_win.transient(bienvenida_win)

            sw = mensaje_win.winfo_screenwidth()       # posicion
            sh = mensaje_win.winfo_screenheight()
            sd = (sw - sh)
            mensaje_win.geometry('770x200+%d+%d' % (sd/2, sd/6))

            img = PhotoImage(file="img/check.gif")
            logo = Label(mensaje_win, image=img)
            logo.image = img
            logo.pack(side="left", padx=10)
            frame_txt = Frame(mensaje_win)
            msg = "Copia de Seguridad realizada con éxito.\n" \
                "En la carpeta carfoins/backup hay una copia de la " \
                "Cartera {}.".format(cartera_exportar)
            texto = Label(frame_txt, text=msg, justify="left",
                font=(12), wraplength=600)
            texto.config(font=(None, '12'))
            texto.pack(side="left")
            frame_txt.pack(fill=X, padx=10, pady=20)
            boton = Button(mensaje_win, text="Volver",
                command=lambda: mensaje_win.destroy(),
                cursor="hand1", bd=3, activebackground="#ACD1E9",
                activeforeground="#FFFFFF")
            boton.bind('<Return>', lambda e:mensaje_win.destroy())
            boton.focus()
            boton.pack(side="left", expand=1, pady=10)
            mensaje_win.bind('<Escape>', lambda e:mensaje_win.destroy())
            mensaje_win.mainloop()

            #bienvenida_win.withdraw()
            #myfiletypes = [('Bases de datos', '*.db'), ('All files', '*')]
            #archivos = filedialog.asksaveasfile(filetypes = myfiletypes, initialfile = original)
            #if archivos is None:  # asksaveasfile return `None` si "cancel".
                #bienvenida_win.deiconify()
                #return
            #bienvenida_win.deiconify()

    frame_texto2 = Frame(tab1)

    #msg_bienvenida1 = "Bienvenido Inversor.\n\n"
    #texto_bienvenida1 = Label(frame_texto2, text=msg_bienvenida1,
        #wraplength=sw-200, justify="left", anchor=W)
    #texto_bienvenida1.config(font=('', 11))
    #texto_bienvenida1.pack(fill=X)

    frame_botones = Frame(frame_texto2)

    img_boton1 = PhotoImage(file="img/entrar.gif")
    boton1 = Button(frame_botones, text="Entrar ", image=img_boton1,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=lambda:ir_operaciones())
    boton1.bind('<Return>', lambda e:ir_operaciones())
    boton1.pack(padx=10, pady=5, fill=X)

    img_boton2 = PhotoImage(file="img/cartera2.gif")
    boton2 = Button(frame_botones, text="Nueva  ", image=img_boton2,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=lambda:nueva_cartera())
    boton2.bind('<Return>', lambda e:nueva_cartera())
    boton2.pack(padx=10, pady=5, fill=X)

    img_boton3 = PhotoImage(file="img/recycleboton.gif")
    boton3 = Button(frame_botones, text="Eliminar", image=img_boton3,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=lambda:eliminar_car())
    boton3.bind('<Return>', lambda e:eliminar_car())
    boton3.pack(padx=10, pady=5, fill=X)

    img_boton5 = PhotoImage(file="img/backup.gif")
    boton5 = Button(frame_botones, text="Backup  ", image=img_boton5,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=lambda:backup())
    boton5.bind('<Return>', lambda e:backup())
    boton5.pack(padx=10, pady=5, fill=X)

    frame_botones.pack(side="left", padx=10)

    frame_carteras = Frame(frame_texto2)
    scrollbar = Scrollbar(frame_carteras, orient=VERTICAL)
    listbox_carteras = Listbox(frame_carteras, selectmode=BROWSE, activestyle='dotbox',
        yscrollcommand=scrollbar.set, selectborderwidth=2)

    db = sqlite3.connect("carfoins.db")
    cursor = db.cursor()
    cursor.execute("SELECT * from CARTERAS ORDER BY cartera")
    total_carteras = cursor.fetchall()
    for car in total_carteras:
        listbox_carteras.insert(END, car[0])
    db.close()

    scrollbar.config(command=listbox_carteras.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox_carteras.config(font=(NONE, '10', 'bold')) # height=7
    listbox_carteras.focus()
    listbox_carteras.pack(side=LEFT, fill=BOTH, expand=1)
    frame_carteras.pack(pady=10, padx=10, side="left", fill=BOTH, expand=1)

    #frame_texto2.config(width=500)
    frame_texto2.pack(padx=50)

    frame_texto = Frame(tab1)

    s = ttk.Separator(frame_texto, orient=HORIZONTAL).pack(fill=X,
        padx=80, pady=20)

    frame_fin=Frame(frame_texto)
    frame_link = Frame(frame_fin)
    msg1_link = "Visita la página web del proyecto"
    msg2_link = "carfoins.esy.es."
    texto_link = Label(frame_link, text=msg1_link)
    texto_link.config(font=('', 11))
    texto_link.pack(side="left")
    link = Label(frame_link, text=msg2_link, fg="blue", cursor="hand1")
    link.config(font=('', 11))
    link.pack(side="left")
    link.bind("<Button-1>", lambda e:carfoins_web())
    frame_link.pack(fill=X, padx=80)

    img_boton4 = PhotoImage(file="img/power.gif")
    boton4 = Button(frame_fin, text="Salir      ", image=img_boton4,
        compound=LEFT, cursor="hand1", bd=3, activebackground="#ACD1E9",
        activeforeground="#FFFFFF", command=lambda:sys.exit())
    boton4.bind('<Return>', lambda event:sys.exit())
    boton4.pack(padx=80, pady=5, side="left")

    frame_fin.pack(fill=X)
    frame_texto.pack(fill=X, padx=50, pady=20)

    tab1.pack()
    note.add(tab1, text='Inicio')

    #################### PESTAÑA 2: AYUDA
    tab2 = Frame(note)

    try:                # Comprueba que existe el archivo
        with open("README.txt", "r", encoding='utf-8') as archivo:
            leeme = archivo.read()

        text = scrolledtext.ScrolledText(tab2, width=100, wrap="word", font=(10))
        text.insert(END, leeme)
        text.configure(state=DISABLED, padx=10)
        text.pack(fill=BOTH, expand=1)

    except:             # En caso de que el archivo no se encuentre
        error_readme = Frame(tab2)
        img_readme = PhotoImage(file="img/nopasar.gif")
        logo_readme = Label(error_readme, image=img_readme).pack(pady=20)

        # text.insert(END, legal_tab)
        msg_readme = "ERROR\n\nLo siento, pero el documento 'README.txt' " \
            "no se encuentra o está dañado.\n\nVuelve a descargar la " \
            "aplicación para disponer de todos los archivos del programa."
        texto = Label(error_readme, text=msg_readme,
            font=(12), wraplength=sw-200).pack()
        error_readme.pack(fill=BOTH, expand=1, pady=30)

    tab2.pack()
    note.add(tab2, text='Ayuda')

    #################### PESTAÑA 3: LICENCIA
    tab3 = Frame(note)

    try:                # Comprueba que existe el archivo
        legal = open("LICENSE.txt")
        legal.close()
        with open("LICENSE.txt", "r", encoding='utf-8') as archivo_legal:
            legal_tab = archivo_legal.read()
        text = scrolledtext.ScrolledText(tab3, wrap="word")
        # text.config(state=NORMAL)
        text.insert(END, legal_tab)
        text.configure(state=DISABLED, padx=10)
        text.pack(fill=BOTH, expand=1)

    except:             # En caso de que el archivo no se encuentre
        error_licencia = Frame(tab3)
        img_licencia = PhotoImage(file="img/nopasar.gif")
        logo_licencia = Label(error_licencia, image=img_licencia).pack(pady=20)

        # text.insert(END, legal_tab)
        msg_licencia = "ERROR\n\nLo siento, pero el documento sobre la licencia " \
            "no se encuentra o está dañado.\n\nVuelve a descargar la " \
            "aplicación para disponer de todos los archivos del programa."
        texto = Label(error_licencia, text=msg_licencia,
            font=(12), wraplength=sw-200).pack()
        error_licencia.pack(fill=BOTH, expand=1, pady=30)

    tab3.pack()
    note.add(tab3, text='Licencia')

    #################### PESTAÑA 4: CRÉDITOS
    tab4 = Frame(note)

    frame_0 = Frame(tab4)
    frame_0.pack(pady=40, fill=X)

    frame1 = Frame(tab4)
    img_bienvenida2 = PhotoImage(file="img/python-powered.gif")
    logo_bienvenida2 = Label(frame1, image=img_bienvenida2).pack(side="left")
    msg_bienvenida2 = "Versión 0.4.6 " \
        "en desarrollo, prácticamente estable y relativamente " \
        "libre de errores (actualiza en carfoins.esy.es).\nEn fase de pruebas para su " \
        "optimización e incorporación de nuevas funciones.\nRequiere " \
        "que el sistema tenga instalado Python versión 3.x (más detalles " \
        "sobre requisitos y ejecución en 'Ayuda')."
    texto_bienvenida2 = Label(frame1, text=msg_bienvenida2,
        wraplength=sw-sw*0.2, justify="left")
    texto_bienvenida2.config(font=('', 11))
    texto_bienvenida2.pack(side="left", padx=10)
    frame1.pack(fill=X, padx=100, pady=20)

    frame2 = Frame(tab4)
    img_bienvenida3 = PhotoImage(file="img/gplv3.gif")
    logo_bienvenida3 = Label(frame2, image=img_bienvenida3).pack(side="left")
    msg_bienvenida3 = "Software libre de código abierto bajo " \
        "Licencia Pública General de GNU (GPL) versión 3.\nMás detalles " \
        "sobre los derechos de autor y la licencia en 'Ayuda' y en " \
        "'Licencia' (en inglés).\nEste programa se distribuye con " \
        "la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA."
    texto_bienvenida3 = Label(frame2, text=msg_bienvenida3,
        wraplength=sw-sw*0.2, justify="left")
    texto_bienvenida3.config(font=('', 11))
    texto_bienvenida3.pack(side="left", padx=10)
    frame2.pack(fill=X, padx=100, pady=20)

    frame3 = Frame(tab4)
    img_vdos = PhotoImage(file="img/vdos2.gif")
    logo_vdos = Label(frame3, image=img_vdos).pack(side="left")
    msg_vdos = "El programa utiliza información suministrada " \
        "por VDOS Stochastics S.L. a través de la web quefondos.com.\n" \
        "Ver los términos y condiciones de esa información en 'Acerca " \
        "de' y en la Información Legal de la página web de vdos.com."
    texto_vdos = Label(frame3, text=msg_vdos,
        wraplength=sw-sw*0.2, justify="left")
    texto_vdos.config(font=('', 11))
    texto_vdos.pack(side="left", padx=10)
    frame3.pack(fill=X, padx=100, pady=20)

    frame4 = Frame(tab4)
    img_paypal = PhotoImage(file="img/donate.gif")
    boton_paypal = Button(frame4, image=img_paypal, cursor="hand1",
        bd=0, activebackground="#BDBDBD", command=paypal).pack(side="left")
    msg_bienvenida4 = "Aplicación gratuita y sin publicidad. No se " \
        "utiliza ningún dato del usuario.\nLibre de spyware, " \
        "malware, virus o cualquier proceso que atente contra tu " \
        "dispositivo o viole tu privacidad.\nTe invito a colaborar con " \
        "un donativo vía PayPal para mantener y mejorar este programa y " \
        "desarrollar nuevas aplicaciones.\n"
    texto_bienvenida4 = Label(frame4, text=msg_bienvenida4,
        wraplength=sw-sw*0.2, justify="left")
    texto_bienvenida4.config(font=('', 11))
    texto_bienvenida4.pack(side="left", padx=10)
    frame4.pack(fill=X, padx=100, pady=20)

    #def key_return1(event = None):
        #volver_portada()
    #def key_return2(event = None):
        #ir_info()
    #def key_return3(event = None):
        #ir_legal()
    #def key_return4(event = None):
        #exit()

    tab4.pack()
    note.add(tab4, text='Créditos')
    #################### FIN PESTAÑAS

    if tab == 1:
        note.select(tab1)
    if tab == 2:
        note.select(tab2)
    if tab == 3:
        note.select(tab3)
    if tab == 4:
        note.select(tab4)

    note.pack(fill=BOTH, padx=5)
    # note.pack(fill=BOTH) padx = 5, pady=5

    def ir_bienvenida():
        note.select(tab1)
    def ir_info():
        note.select(tab2)

    bienvenida_win.bind("<Control-q>", lambda event:sys.exit())
    bienvenida_win.bind('<F1>', lambda event:ir_info())
    bienvenida_win.bind('<Alt-i>', lambda event:ir_bienvenida())

    bienvenida_win.mainloop()               # FIN VENTANA

# EMPEZAMOS
bienvenida()
