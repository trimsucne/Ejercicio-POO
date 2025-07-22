# !/usr/bin/python3
# -*- coding: utf-8 -*-

''' 
    Programación Orientada a Objetos (G10)
    Integrantes del equipo:
       Nombre completo                   Documento     Correo
    -- Harrison Angel Pineda             1001298813    hangelp@unal.edu.co
    -- Sergio Nicolás Correa Escobar     1014739037    secorreae@unal.edu.co
    -- Fidel Murillo Carvajal            1116813569    fmurillo@unal.edu.co
    -- Daniel Steven Guerrero Santiago   1052384478    dguerreros@unal.edu.co
    -- Wilson Daniel Rojas Aroca         1000129178    wrojasa@unal.edu.co
    -- Arnaud Edouard Paul Sinet         22AD03800     asinet@unal.edu.co
'''

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from datetime import datetime
import os

class Inventario:
  def __init__(self, master=None):
    self.path = os.path.dirname(__file__)
    self.dbName = self.path + r'\BD\Inventario.db'
    # Variables de instancia para controlar eventos
    self.error = None        
    self.active = False      
    self.respondido = False
    self.answer = False      
    self.states = []         

    # Crea ventana principal
    self.win = tk.Tk() 
    self.alto = int(self.win.winfo_screenheight() * 0.7)
    self.ancho = int(self.alto * 1.5)
    self.win.withdraw()
    try:
      self.win.iconbitmap(self.path + r'\imgs\f2.ico')
    except: 
      pth = r"\imgs\f2.ico"
      txt = f'No se encontró la imagen en {pth}.\nSe usará el icóno predeterminado.'
      mssg.showerror('Atención!!',txt)
    self.win.resizable(False, False)
    self.win.title("Manejo de Proveedores")

    # Centra la pantalla
    self.centra(self.win,self.ancho,self.alto)
    self.win.deiconify() # Se usa para restaurar la ventana

    # Creación del TopLevel para preguntas
    self.top = tk.Toplevel()
    self.top.withdraw()
    self.top.overrideredirect(True)
    self.top.resizable(False,False)
    self.top.configure(borderwidth=2, relief="groove", highlightthickness=2, highlightbackground="#2271b3", highlightcolor="#2271b3")
    height = int(self.alto * 0.24)
    width = int(height * 2.4)
    self.centra(self.top,width,height)

    self.titleFrm = tk.LabelFrame(master=self.top, background="#e0e0e0")
    self.titleFrm.place(relheight=0.2, relwidth=1.0)
    self.topIcon = tk.Label(master=self.titleFrm, text="?", font="{Calibri} 12 {bold}", foreground= "#2271b3", background="#e0e0e0")
    self.topTitle = tk.Label(master=self.titleFrm, text="Pregunta", font="{Arial} 10 {bold}", background="#e0e0e0")
    self.topIcon.place(relheight=1, relwidth=0.1)
    self.topTitle.place(relx=0.1, relheight=1, relwidth=0.3)

    self.questFrm = tk.LabelFrame(master=self.top, background="#FFFFFF", font="{Arial} 12 {bold}")
    self.questFrm.place(rely=0.2, relheight=0.45, relwidth=1)
    self.quest = tk.Label(master=self.questFrm, text='')
    self.quest.place(relheight=1, relwidth=1)

    self.ansFrm = tk.Frame(master=self.top, background="#e0e0e0")
    self.ansFrm.place(rely=0.65, relheight=0.35, relwidth=1)
    self.yes = ttk.Button(master=self.ansFrm, text="Sí", command= self.yesAnswer)
    self.no = ttk.Button(master=self.ansFrm, text="No", command = self.noAnswer)
    self.yes.place(relx=0.1, rely=0.25, relheight=0.5, relwidth=0.35)
    self.no.place(relx=0.55, rely=0.25, relheight=0.5, relwidth=0.35)

    # Contenedor de widgets   
    self.win = tk.LabelFrame(master)
    self.win.configure(background="#e0e0e0",font="{Arial} 12 {bold}",
                       height=self.alto,labelanchor="n",width=self.ancho)
    self.tabs = ttk.Notebook(self.win)
    self.tabs.configure(height=int(self.alto*0.975), width=int(self.ancho*0.99))

    #Frame de datos
    self.frm1 = ttk.Frame(self.tabs)
    self.frm1.configure(height=int(self.alto*0.975*0.917), width=int(self.ancho*0.99))

    #Etiqueta IdNit del Proveedor
    self.lblIdNit = ttk.Label(self.frm1)
    self.lblIdNit.configure(text='Id/Nit', width=6)
    self.lblIdNit.place(anchor="nw", relx=0.019, rely=0.053)

    #Captura IdNit del Proveedor
    self.entryIdNit = ttk.Entry(self.frm1)
    self.entryIdNit.place(anchor="nw", relx=0.073, rely=0.053)
    self.entryIdNit.bind("<Control-KeyRelease-v>", self.validaIdNit)
    self.entryIdNit.bind("<KeyRelease>", self.validaIdNit)
    self.entryIdNit.configure(state='normal')
    self.entryIdNit.focus()

    #Etiqueta razón social del Proveedor
    self.lblRazonSocial = ttk.Label(self.frm1)
    self.lblRazonSocial.configure(text='Razon social', width=12)
    self.lblRazonSocial.place(anchor="nw", relx=0.273, rely=0.053)

    #Captura razón social del Proveedor
    self.entryRazonSocial = ttk.Entry(self.frm1)
    self.entryRazonSocial.configure(width=36)
    self.entryRazonSocial.place(anchor="nw", relx=0.371, rely=0.053)
    self.entryRazonSocial.bind("<Control-KeyRelease-v>", self.validaRazonSocial)
    self.entryRazonSocial.bind("<KeyRelease>", self.validaRazonSocial)
    self.entryRazonSocial.configure(state='normal')

    #Etiqueta ciudad del Proveedor
    self.lblCiudad = ttk.Label(self.frm1)
    self.lblCiudad.configure(text='Ciudad', width=7)
    self.lblCiudad.place(anchor="nw", relx=0.683, rely=0.053)

    #Captura ciudad del Proveedor
    self.entryCiudad = ttk.Entry(self.frm1)
    self.entryCiudad.configure(width=30)
    self.entryCiudad.place(anchor="nw", relx=0.746, rely=0.053)
    self.entryCiudad.bind("<Control-KeyRelease-v>", self.validaCiudad)
    self.entryCiudad.bind("<KeyRelease>", self.validaCiudad)
    self.entryCiudad.configure(state='normal')

    #Separador
    self.separador1 = ttk.Separator(self.frm1)
    self.separador1.configure(orient="horizontal")
    self.separador1.place(anchor="nw", relwidth=1.0, rely=0.107)

    #Etiqueta Código del Producto
    self.lblCodigo = ttk.Label(self.frm1)
    self.lblCodigo.configure(text='Código', width=7)    
    self.lblCodigo.place(anchor="nw", relx=0.019, rely=0.16)

    #Captura el código del Producto
    self.entryCodigo = ttk.Entry(self.frm1)
    self.entryCodigo.configure(width=13)
    self.entryCodigo.bind("<Control-KeyRelease-v>", self.validaCodigo)
    self.entryCodigo.bind("<KeyRelease>", self.validaCodigo)
    self.entryCodigo.place(anchor="nw", relx=0.085, rely=0.16)
    self.entryCodigo.configure(state='normal')

    #Etiqueta descripción del Producto
    self.lblDescripcion = ttk.Label(self.frm1)
    self.lblDescripcion.configure(text='Descripción', width=11)
    self.lblDescripcion.place(anchor="nw", relx=0.273, rely=0.16)

    #Captura la descripción del Producto
    self.entryDescripcion = ttk.Entry(self.frm1)
    self.entryDescripcion.configure(width=36)
    self.entryDescripcion.place(anchor="nw", relx=0.37, rely=0.16)
    self.entryDescripcion.bind("<Control-KeyRelease-v>", self.validaDescripcion)
    self.entryDescripcion.bind("<KeyRelease>", self.validaDescripcion)
    self.entryDescripcion.configure(state='normal')

    #Etiqueta unidad o medida del Producto
    self.lblUnidad = ttk.Label(self.frm1)
    self.lblUnidad.configure(text='Unidad', width=7)
    self.lblUnidad.place(anchor="nw", relx=0.683, rely=0.16)

    #Captura la unidad o medida del Producto
    self.entryUnidad = ttk.Entry(self.frm1)
    self.entryUnidad.configure(width=10)
    self.entryUnidad.place(anchor="nw", relx=0.746, rely=0.16)
    self.entryUnidad.bind("<Control-KeyRelease-v>", self.validaUnidad)
    self.entryUnidad.bind("<KeyRelease>", self.validaUnidad)
    self.entryUnidad.configure(state='normal')

    #Etiqueta cantidad del Producto
    self.lblCantidad = ttk.Label(self.frm1)
    self.lblCantidad.configure(text='Cantidad', width=8)
    self.lblCantidad.place(anchor="nw", relx=0.019, rely=0.235)

    #Captura la cantidad del Producto
    self.entryCantidad = ttk.Entry(self.frm1)
    self.entryCantidad.configure(width=12)
    self.entryCantidad.place(anchor="nw", relx=0.097, rely=0.235)
    self.entryCantidad.bind("<Control-KeyRelease-v>", self.formatoCantidad)
    self.entryCantidad.bind("<KeyRelease>", self.formatoCantidad)
    self.entryCantidad.configure(state='normal')

    #Etiqueta precio del Producto
    self.lblPrecio = ttk.Label(self.frm1)
    self.lblPrecio.configure(text='Precio $', width=8)
    self.lblPrecio.place(anchor="nw", relx=0.224, rely=0.235)

    #Captura el precio del Producto
    self.entryPrecio = ttk.Entry(self.frm1)
    self.entryPrecio.configure(width=15)
    self.entryPrecio.place(anchor="nw", relx=0.283, rely=0.235)
    self.entryPrecio.bind("<Control-KeyRelease-v>", self.formatoPrecio)
    self.entryPrecio.bind("<KeyRelease>", self.formatoPrecio)
    self.entryPrecio.configure(state='normal')

    #Etiqueta fecha de compra del Producto
    self.lblFecha = ttk.Label(self.frm1)
    self.lblFecha.configure(text='Fecha', width=6)
    self.lblFecha.place(anchor="nw", relx=0.458, rely=0.235)

    #Formato de la fecha
    self.lblFechamm = ttk.Label(self.frm1)
    self.lblFechamm.configure(text='DD/MM/AAAA', width=14, font="{Arial} 7")
    self.lblFechamm.place(anchor="nw", relx=0.508, rely=0.214)

    #Captura la fecha de compra del Producto
    self.entryFecha = ttk.Entry(self.frm1)
    self.entryFecha.bind("<Control-KeyRelease-v>", self.formatoFecha)
    self.entryFecha.bind("<KeyRelease>", self.formatoFecha)
    self.entryFecha.configure(width=10)
    self.entryFecha.place(anchor="nw", relx=0.508, rely=0.235)
    self.entryFecha.configure(state='normal')

    #Separador
    self.separador2 = ttk.Separator(self.frm1)
    self.separador2.configure(orient="horizontal")
    self.separador2.place(anchor="nw", relwidth=1.0, rely=0.299)
    
    #tablaTreeView
    self.style=ttk.Style()
    self.style.configure("estilo.Treeview", highlightthickness=0, bd=0, background="#e0e0e0", font=('Calibri Light',10))
    self.style.configure("estilo.Treeview.Heading", background='Azure', font=('Calibri Light', 10,'bold')) 
    self.style.layout("estilo.Treeview", [('estilo.Treeview.treearea', {'sticky': 'nswe'})])

    #Árbol para mosrtar los datos de la B.D.
    self.treeProductos = ttk.Treeview(self.frm1, style="estilo.Treeview")
    self.treeProductos.configure(selectmode="extended")
    self.treeProductos.bind("<Button-1>", self.cargaDatos)

    # Etiquetas de las columnas para el TreeView
    self.treeProductos["columns"]=("Codigo","Descripcion","Und","Cantidad","Precio","Fecha")
    # Características de las columnas del árbol
    self.treeProductos.column ("#0",          anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Codigo",      anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Descripcion", anchor="w",stretch=True,width=150)
    self.treeProductos.column ("Und",         anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Cantidad",    anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Precio",      anchor="w",stretch=True,width=8)
    self.treeProductos.column ("Fecha",       anchor="w",stretch=True,width=3)

    # Etiquetas de columnas con los nombres que se mostrarán por cada columna
    self.treeProductos.heading("#0",          anchor="center", text='ID / Nit')
    self.treeProductos.heading("Codigo",      anchor="center", text='Código')
    self.treeProductos.heading("Descripcion", anchor="center", text='Descripción')
    self.treeProductos.heading("Und",         anchor="center", text='Unidad')
    self.treeProductos.heading("Cantidad",    anchor="center", text='Cantidad')
    self.treeProductos.heading("Precio",      anchor="center", text='Precio')
    self.treeProductos.heading("Fecha",       anchor="center", text='Fecha')

    self.treeProductos.place(anchor="nw", relx=0.005, rely=0.317, relwidth=0.99, relheight=0.575)
    self.treeProductos.bind('<Motion>', 'break')

    #Scrollbar en el eje Y de treeProductos
    self.scrollbary=ttk.Scrollbar(self.treeProductos, orient='vertical', command=self.treeProductos.yview)
    self.treeProductos.configure(yscroll=self.scrollbary.set)
    self.scrollbary.place(anchor="nw", relx=0.986, rely=0.066, relwidth=0.01, relheight=0.934)

    # Título de la pestaña Ingreso de Datos
    self.frm1.pack(side="top")
    self.tabs.add(self.frm1, compound="center", text='Ingreso de datos')
    self.tabs.pack(side="top")

    #Frame 2 para contener los botones
    self.frm2 = ttk.Frame(self.win)

    #Botón para Buscar un Proveedor
    self.btnBuscar = ttk.Button(self.frm2)
    self.btnBuscar.configure(text='Buscar', command = self.buscaRegistro)
    self.btnBuscar.place(anchor="nw", relwidth=0.083, relx=0.244, rely=0.17)

    #Botón para Guardar los datos
    self.btnGrabar = ttk.Button(self.frm2)
    self.btnGrabar.configure(text='Grabar', command = self.adicionaRegistro)
    self.btnGrabar.place(anchor="nw", relwidth=0.083, relx=0.341, rely=0.17)

    #Botón para Editar los datos
    self.btnEditar = ttk.Button(self.frm2)
    self.btnEditar.configure(text='Editar', command = self.editaRegistro)
    self.btnEditar.place(anchor="nw", relwidth=0.083, relx=0.434, rely=0.17)

    #Botón para Elimnar datos
    self.btnEliminar = ttk.Button(self.frm2)
    self.btnEliminar.configure(text='Eliminar', command = self.eliminaRegistro)
    self.btnEliminar.place(anchor="nw", relwidth=0.083, relx=0.527, rely=0.17)

    #Botón para cancelar una operación
    self.btnCancelar = ttk.Button(self.frm2)
    self.btnCancelar.configure(text='Cancelar', width=80, command = self.cancelaOperacion)
    self.btnCancelar.place(anchor="nw", relwidth=0.083, relx=0.621, rely=0.17)

    #Ubicación del Frame 2
    self.frm2.place(anchor="nw", relx=0.005, relheight=0.084, relwidth=0.99, rely=0.897)
    self.win.pack(anchor="center", side="top")

    # widget Principal del sistema
    self.mainwindow = self.win

  #Función de manejo de eventos del sistema
  def run(self):
      self.mainwindow.mainloop()

  ''' ......... Métodos utilitarios del sistema .............'''
  #Rutina de centrado de pantalla
  def centra(self,win,ancho,alto): 
      """ centra las ventanas en la pantalla """ 
      x = win.winfo_screenwidth() // 2 - ancho // 2 
      y = win.winfo_screenheight() // 2 - alto // 2 
      win.geometry(f'{ancho}x{alto}+{x}+{y-((win.winfo_screenheight() // 2 - self.alto // 2)//2)}')


 # Validaciones del sistema
  def validaIdNit(self, event):
    ''' Valida que la longitud no sea mayor a 15 caracteres'''
    if event:
      if len(self.entryIdNit.get()) > 15:
        self.entryIdNit.delete(15,'end')
        mssg.showerror('Atención!!',f'.. ¡Máximo 15 caracteres! ..')
         
  def validaRazonSocial(self, event):
    ''' Valida que la longitud no sea mayor a 50 caracteres'''
    if event:
      if len(self.entryRazonSocial.get()) > 50:
        self.entryRazonSocial.delete(50,'end')  
        mssg.showerror('Atención!!',f'.. ¡Máximo 50 caracteres! ..')

  def validaCiudad(self, event):
    ''' Valida que la longitud no sea mayor a 50 caracteres'''
    if event:
      if len(self.entryCiudad.get()) > 50:
        self.entryCiudad.delete(50,'end')  
        mssg.showerror('Atención!!',f'.. ¡Máximo 50 caracteres! ..')

  def validaCodigo(self, event):
    ''' Valida que la longitud no sea mayor a 15 caracteres'''
    if event:
      if len(self.entryCodigo.get()) > 15:
        self.entryCodigo.delete(15,'end')  
        mssg.showerror('Atención!!',f'.. ¡Máximo 15 caracteres! ..')

  def validaDescripcion(self, event):
    ''' Valida que la longitud no sea mayor a 50 caracteres'''
    if event:
      if len(self.entryDescripcion.get()) > 50:
        self.entryDescripcion.delete(50,'end')  
        mssg.showerror('Atención!!',f'.. ¡Máximo 50 caracteres! ..')
  
  def validaUnidad(self, event):
    ''' Valida que la longitud no sea mayor a 10 caracteres'''
    if event:
      if len(self.entryUnidad.get()) > 10:
        self.entryUnidad.delete(10,'end')  
        mssg.showerror('Atención!!',f'.. ¡Máximo 10 caracteres! ..')
  
  def formatoCantidad(self, event):
    ''' Valida que la longitud no sea mayor a 50 caracteres'''
    if event:
      if len(self.entryCantidad.get()) > 50:
        self.entryCantidad.delete(50,'end')  
        mssg.showerror('Atención!!',f'.. ¡Máximo 50 caracteres! ..')

  def formatoPrecio(self, event):
    ''' Valida que la longitud no sea mayor a 50 caracteres'''
    if event:
      if len(self.entryPrecio.get()) > 50:
        self.entryPrecio.delete(50,'end')  
        mssg.showerror('Atención!!',f'.. ¡Máximo 50 caracteres! ..')

  def validaCantidad(self, cantidad):
    ''' Valida que el valor sea numérico'''
    try:
      if (cantidad == ""): return True
      else:
        float(cantidad)
        return True
    except:
      mssg.showerror('Atención!!',f'.. ¡Solamente se permiten números en la cantidad! ..')
      return False

  def validaPrecio(self, precio):
    ''' Valida que el valor sea numérico'''
    try:
      if (precio == ""): return True
      else:
        float(precio)
        return True
    except:
      mssg.showerror('Atención!!',f'.. ¡Solamente se permiten números en el precio! ..')
      return False

  def validaFecha(self,fecha):
    try:
      datetime.strptime(fecha, "%d/%m/%Y")
      return True
    except ValueError:
      mssg.showerror('Atención!!',f'.. ¡La fecha es inválida! ..')
      return False
    
  # Forzar formato de la fecha
  def formatoFecha(self, event):
    fecha = self.entryFecha.get()
    if (event.keycode == 32):
      length = len(self.entryFecha.get()) - 1
      self.entryFecha.delete(length)
    elif (event.keycode != 8):
      if len(fecha) in (2, 5):
        self.entryFecha.insert('end', "/")
    if len(fecha) > 10:
        self.entryFecha.delete(10,'end')
    
  #Rutina de limpieza de datos
  def limpiaCampos(self):
      ''' Limpia todos los campos de captura'''
      self.entryIdNit.delete(0,'end')
      self.entryRazonSocial.delete(0,'end')
      self.entryCiudad.delete(0,'end')
      self.entryIdNit.delete(0,'end')
      self.entryCodigo.delete(0,'end')
      self.entryDescripcion.delete(0,'end')
      self.entryUnidad.delete(0,'end')
      self.entryCantidad.delete(0,'end')
      self.entryPrecio.delete(0,'end')
      self.entryFecha.delete(0,'end')

  def limpiaTreeview(self):
    tablaTreeView = self.treeProductos.get_children()
    for fila in tablaTreeView:
        self.treeProductos.delete(fila)

  # Rutina para cargar los datos en el árbol  
  def cargaDatos(self,event):
    if (self.active == False):
      idNit = self.treeProductos.item(self.treeProductos.selection())['text']
      if (idNit != ''):
        self.limpiaCampos()
        self.entryIdNit.insert(0,idNit)
        datosProv = self.buscaProveedor(idNit)
        self.entryRazonSocial.insert(0,datosProv[1])
        self.entryCiudad.insert(0,datosProv[2])
        self.entryCodigo.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][0])
        self.entryDescripcion.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][1])
        self.entryUnidad.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][2])
        self.entryCantidad.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][3])
        self.entryPrecio.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][4])
        self.entryFecha.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][5])
        self.estadoIdNitCodigo('disabled')

  # Buscar un proveedor
  def buscaProveedor(self,idNit):
    query = '''SELECT * FROM Proveedor WHERE idNitProv = ?'''
    proveedor = self.runQuery(query,(idNit,))
    if (proveedor != False):
      if (len(proveedor) != 0):
        return proveedor[0]
      else: 
        return False

  # Cargar los datos del TreeView
  def cargaDatosProveedor(self):
    idNit = self.entryIdNit.get()
    razonSocial = self.entryRazonSocial.get()
    ciudad = self.entryCiudad.get()
    datosProv = (idNit,razonSocial,ciudad)
    return datosProv
  
  def cargaDatosProducto(self):
    idNit = self.entryIdNit.get()
    codigo = self.entryCodigo.get()
    descripcion = self.entryDescripcion.get()
    unidad = self.entryUnidad.get()
    cantidad = self.entryCantidad.get()
    precio = self.entryPrecio.get()
    fecha = self.entryFecha.get()
    datosProv = (idNit,codigo,descripcion,unidad,cantidad,precio,fecha)
    return datosProv

  # Habilitar o desabilitar IdNit y Codigo
  def estadoIdNitCodigo(self,estado):
    self.entryIdNit.configure(state = estado)
    self.entryCodigo.configure(state = estado)
    self.states = []
    for widget in self.frm1.winfo_children():
      if (isinstance(widget, ttk.Entry)):
        self.states.append(widget.state())

  # Operaciones con la base de datos
  def runQuery(self, query, parametros = ()):
    ''' Función para ejecutar los Querys a la base de datos '''
    try:
      with sqlite3.connect(self.dbName) as conn:     
        cursor = conn.cursor()
        cursor.execute(query, parametros)
        result = cursor.fetchall()
        conn.commit()
    except Exception as exc:
        if (exc.args == ('unable to open database file',)):
          mssg.showerror('ATENCION',r'No se encontró la base de datos en "\BD\Inventario.db"')
        else:
          mssg.showerror('ATENCION',f'Error con la petición: {exc}')
        self.error = True
        result = False
    return result
  
  # Mostrar mensaje de confirmación
  def showMessage(self, query, parametros, mensaje = ''):
    result = self.runQuery(query,parametros)
    if (result != False):
      mssg.showinfo(message=mensaje, title="Anuncio")

  # Metodo para hacer preguntas cancelables
  def askYesNo(self, pregunta):
    self.active = True
    self.quest.configure(text=pregunta)
    self.top.deiconify()
    self.top.transient(self.win)
    self.top.focus()
    for widget in self.frm1.winfo_children():
      if (isinstance(widget, ttk.Entry)):
        self.states.append(widget.state())
        widget.configure(state='disabled')
    for widget in self.frm2.winfo_children():
      if (widget != self.btnCancelar):
        widget.configure(state='disabled')
    self.treeProductos.configure(selectmode='none')
    # Ciclo interno que evita seguir hasta responder la pregunta
    waiting = True
    while waiting:
      self.win.update()
      self.top.deiconify()
      self.top.focus()
      if (self.respondido == True): 
        self.top.withdraw()
        self.respondido = False
        return self.answer

  # Métodos para guardar las respuestas y manejar TopLevel de preguntas
  def answered(self):
    i = 0
    for widget in self.frm1.winfo_children():
      if (isinstance(widget, ttk.Entry)):
        widget.configure(state=self.states[i])
        i += 1
    for widget in self.frm2.winfo_children():
      widget.configure(state='normal')
    self.treeProductos.configure(selectmode='extended')
    self.top.withdraw()
    self.active = False

  def yesAnswer(self):
    self.answered()
    self.answer = True
    self.respondido = True

  def noAnswer(self):
    if (self.active == True):
      self.answered()
      self.answer = False
      self.respondido = True

  # Metodos de los botones
  def buscarProv(self):
      idNitProv = self.entryIdNit.get()
      if idNitProv == "":
        mssg.showerror('Atención!!','Se requiere el Id/Nit')
      else:
        datosProv = self.buscaProveedor(idNitProv)
        self.limpiaCampos()
        if (datosProv != False):
          self.entryIdNit.insert(0,datosProv[0])
          self.entryRazonSocial.insert(0,datosProv[1])
          self.entryCiudad.insert(0,datosProv[2])
          query = '''SELECT * FROM Productos WHERE idNit = ?'''     
          productos = self.runQuery(query,(idNitProv,))
          if (productos != False):
            if (len(productos) != 0):
              for prod in productos:
                self.treeProductos.insert('',0, text = prod[0], values = [prod[1],prod[2],prod[3],prod[4],prod[5],prod[6]])
              mssg.showinfo(message="Los productos han sido encontrados", title="Anuncio")
            else:
              mssg.showinfo(message="El Proveedor no tiene productos", title="Anuncio")
        else:
            mssg.showerror('Atención!!','El proveedor no existe')

  def grabarProv(self):
      datosProv = self.cargaDatosProveedor()
      codigo = self.entryCodigo.get()
      fecha = self.entryFecha.get()
      if datosProv[0] == "":
          mssg.showerror('Atención!!','Se requiere el IdNit')
          self.error = True
      elif (((codigo == '') & (fecha == '')) | ((codigo != '') & (fecha != ''))):
        proveedor = self.buscaProveedor(datosProv[0])
        if (self.error is None):
          if (proveedor != False):
            if (((datosProv[1] != '') | (datosProv[2] != '')) & 
                ((datosProv[1] != proveedor[1]) | (datosProv[2] != proveedor[2]))):
              edit = self.askYesNo("El proveedor ya existe\n ¿Desea modificar su información?")          
              if (edit == True):
                query = '''UPDATE Proveedor SET Razon_Social=?,Ciudad=? WHERE idNitProv=?'''
                parametros = (datosProv[1],datosProv[2],datosProv[0])
                self.showMessage(query,parametros,"El Proveedor ha sido modificado")
            elif ((codigo == '') & (fecha == '')):
              mssg.showinfo(message="El proveedor ya existe", title="Anuncio")
          else:
            query = '''INSERT INTO Proveedor(idNitProv,Razon_Social,Ciudad) VALUES (?,?,?)'''
            self.showMessage(query,datosProv,"El Proveedor ha sido agregado")
      else:
        mssg.showerror('Atención!!','Se requiere Codigo y Fecha')
        self.error = True      
  
  def grabarProd(self):
    datosProd = self.cargaDatosProducto()
    idNitProv = datosProd[0];codigo = datosProd[1]; fecha = datosProd[6]; 
    cantidad = datosProd[4]; precio = datosProd[5]
    if ((codigo != '') & (fecha != '')):
      query = '''SELECT * FROM Productos WHERE idNit = ? AND Codigo = ?'''     
      producto = self.runQuery(query,(idNitProv,codigo))
      if (producto != False):
        if (len(producto) != 0):
          edit = self.askYesNo("El proveedor ya tiene un producto con ese codigo\n¿Desea modificarlo?")
          if (edit == True):
            if (self.validaFecha(fecha) and self.validaCantidad(cantidad) and self.validaPrecio(precio)):
              query = '''UPDATE Productos SET Descripcion=?,Und=?,Cantidad=?,Precio=?,Fecha=? WHERE idNit=? AND Codigo=?'''
              parametros = (datosProd[2:7]+(idNitProv,codigo))
              self.showMessage(query,parametros,"El Producto ha sido modificado")
        else:
          query = '''INSERT INTO Productos(idNit,Codigo,Descripcion,Und,Cantidad,Precio,Fecha) VALUES (?,?,?,?,?,?,?)'''
          if (self.validaFecha(fecha) and self.validaCantidad(cantidad) and self.validaPrecio(precio)):
            self.showMessage(query,datosProd,"El Producto ha sido agregado")

  def eliminarProv(self):
    idNit = self.entryIdNit.get()
    if idNit == "":
        mssg.showerror('Atención!!','Se requiere el IdNit')
        self.error = True
    else:
      proveedor = self.buscaProveedor(idNit)
      if (proveedor != False):
        if (len(proveedor) != 0):
          query = '''SELECT * FROM Productos WHERE idNit = ?'''     
          productos = self.runQuery(query,(idNit,))
          if (productos != False):
            if (len(productos) != 0):
              edit = self.askYesNo("¿Desea eliminar al proveedor con todos sus productos?")
              if (edit == True):
                query = '''DELETE FROM Productos WHERE idNit = ?'''
                result = self.runQuery(query,(idNit,))
                if (result != False):
                  query = '''DELETE FROM Proveedor WHERE idNitProv = ?'''
                  self.showMessage(query,(idNit,),"El proveedor y sus productos han sido eliminados")
            else:
              edit = self.askYesNo("¿Desea eliminar el Proveedor?")
              if (edit == True):
                query = '''DELETE FROM Proveedor WHERE idNitProv = ?'''
                self.showMessage(query,(idNit,),"El proveedor ha sido eliminado")
      else:
        mssg.showerror('Atención!!','No existe el proveedor')

  def eliminarProd(self):
    idNit = self.entryIdNit.get()
    codigo = self.entryCodigo.get()
    if (codigo == ""):
      self.error = True
    elif (idNit != ""):
      query = '''SELECT * FROM Productos WHERE idNit = ? AND Codigo = ?''' 
      producto = self.runQuery(query,(idNit,codigo))
      if (producto != False):
        if (len(producto) != 0):
          edit = self.askYesNo("¿Desea eliminar el producto?")
          if (edit == True):
            query = '''DELETE FROM Productos WHERE idNit = ? AND Codigo = ?'''  
            self.showMessage(query,(idNit,codigo,),"El producto ha sido eliminado")    
        else:
          mssg.showerror('Atención!!','El proveedor no tiene productos con ese codigo')

  def editarProv(self):
    idNit = self.entryIdNit.get()
    if idNit == "":
        mssg.showerror('Atención!!','Se requiere el IdNit')
        self.error = True
    else:
      datosProv = self.cargaDatosProveedor()
      proveedor = self.buscaProveedor(datosProv[0])
      if (((datosProv[1] != '') | (datosProv[2] != '')) & 
            ((datosProv[1] != proveedor[1]) | (datosProv[2] != proveedor[2]))):
              edit = self.askYesNo("¿Desea modificar la información del proveedor?")
              if (edit == True):
                query = '''UPDATE Proveedor SET Razon_Social=?,Ciudad=? WHERE idNitProv=?'''
                parametros = (datosProv[1],datosProv[2],datosProv[0])
                self.showMessage(query,parametros,"El Proveedor ha sido modificado")
        
  def editarProd(self):
    datosProd = self.cargaDatosProducto()
    idNitProv = datosProd[0];codigo = datosProd[1]; fecha = datosProd[6]; 
    cantidad = datosProd[4]; precio = datosProd[5]
    if ((codigo == "") | (fecha == "")):
        self.error = True
    else:
      query = '''SELECT * FROM Productos WHERE idNit = ? AND Codigo = ?'''   
      producto = self.runQuery(query,(idNitProv,codigo))
      if (producto != False):
        if (len(producto) != 0):
          edit = self.askYesNo("¿Desea modificar el Producto?")
          if (edit == True):
            if (self.validaFecha(fecha) and self.validaCantidad(cantidad) and self.validaPrecio(precio)):
              query = '''UPDATE Productos SET Descripcion=?,Und=?,Cantidad=?,Precio=?,Fecha=? WHERE idNit=? AND Codigo=?'''
              parametros = (datosProd[2:7]+(idNitProv,codigo))
              self.showMessage(query,parametros,"El Producto ha sido modificado")
      else:
        self.error = True
    
  # Botones
  def buscaRegistro(self, event=None):
    self.estadoIdNitCodigo('normal')
    self.limpiaTreeview()
    self.buscarProv()
    
  def adicionaRegistro(self, event=None):
    '''Adiciona un producto a la BD si la validación es True'''
    self.grabarProv()
    if (self.error is None):
      self.grabarProd()
    self.estadoIdNitCodigo('normal')
    self.error = None
    self.entryIdNit.focus()
    
  def editaRegistro(self, event=None):
    ''' Edita una tupla del TreeView'''
    self.editarProv()
    if (self.error is None):
      self.editarProd()
    if (self.answer is True):
      self.estadoIdNitCodigo('normal')
      self.limpiaCampos()
      self.limpiaTreeview()
    self.error = None
    self.entryIdNit.focus()
    
  def eliminaRegistro(self, event=None):
    '''Elimina un Registro en la BD'''
    self.eliminarProd()
    if (self.error is True):
      self.eliminarProv()
      if (self.error is None):
        self.estadoIdNitCodigo('normal')
        self.limpiaCampos()
        self.limpiaTreeview()
    else:
      if (self.answer is True):
        self.estadoIdNitCodigo('normal')
        self.limpiaCampos()
        self.limpiaTreeview()
    self.error = None
    self.entryIdNit.focus()

  def cancelaOperacion(self, event=None):
    self.noAnswer()
    self.estadoIdNitCodigo('normal')
    self.limpiaCampos()
    self.limpiaTreeview()
    self.error = None
    self.entryIdNit.focus()


if __name__ == "__main__":
    app = Inventario()
    app.run()