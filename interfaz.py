from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os.path
from io import open
from datos import *
from sintaxis import *

#funcion para establecer kernel y memoria por defecto --------------------------
def por_defecto():
    input_ker.delete(0, END)
    input_mem.delete(0, END)
    input_ker.insert(0, 5) # 69 -> 10 * Z + 9 (Z ultimo digito cedula -> 6 ) 
    input_mem.insert(0, 100)

#funcion para validar el kernel y memoria ingresados por el usuario-------------
def validar_ker_mem(tam_ker, tam_mem):
    if(tam_ker > 0 and tam_mem > 0 and tam_mem <= 9999 and tam_ker < tam_mem):
        mensaje_pre_v.config(text = "Datos correctos!!! Presiona ACEPTAR", fg = "green")
        boton_aceptar = Button(pre_ventana, text = "   ACEPTAR   ", command = lambda: cerrar_ventana(pre_ventana))
        boton_aceptar.place(x = 115, y = 180)
        asignar_kernel(memoria, tam_ker)
        datos_ker_mem(tam_ker, tam_mem)
    else:
        mensaje_pre_v.config(text = "Datos inválidos, Prueba de nuevo", fg = "red")

#funcion para asignar kernel a la memoria-------------------------------------------
una_vez = 0
def asignar_kernel(memoria, tam_ker):
    global una_vez
    if(una_vez < 1):
        una_vez += 1
        memoria.append("ACUMULADOR")
        for i in range(1, tam_ker + 1 ):
            memoria.append("SISTEMA OPERATIVO")

#funcion para cerrar ventana------------------------------------------------------
def cerrar_ventana(pre_ventana):
    pre_ventana.destroy()

#funcion para abrir el archivo.ch------------------------------------------------
def abrir():
    global ruta
    global codigo_ch
    ruta = filedialog.askopenfilename(initialdir= os.path.dirname(__file__) + '/programas_ch/', title="Abrir archivo CH.") #filetypes=(("Ficheros de texto", "*.ch") )

    # Si la ruta es válida abrimos el contenido en lectura
    if ruta != "":  
        archivo = open(ruta, 'r')
        #contenido = archivo.read()         
        print("archivo leido correctamente")
        codigo_ch = archivo.readlines()
        archivo.close()

        tabla_pro.delete(*tabla_pro.get_children())
        for i in range(0, len(codigo_ch)):
            tabla_pro.insert("", 'end',text = "          " + str(i+1), values=(codigo_ch[i],))
        print(codigo_ch)

#funcion para boton MOSTRAR MEMORIA------------------------------------------------
def mostrar_memoria():
    tabla_memoria.delete(*tabla_memoria.get_children())
    for j in range(0, len(memoria)):
        tabla_memoria.insert("", 'end',text = str(j), values=(memoria[j],))


#funcion boton COMPILAR----------------------------------
def compilar(memoria): 
    verificar_sintaxis(codigo_ch)
    if(len(errores) == 0): 
        memoria += codigo_ch
        ventana_errores = Tk()
        ventana_errores.geometry("200x200")
        msj_error = Label(ventana_errores, text  = "NO HAY ERRORES", fg = "green")
        msj_error.place(x = 50, y = 50)
        btn_error = Button(ventana_errores, text = " CONTINUAR ", command = lambda: cerrar_ventana(ventana_errores))
        btn_error.place(x = 50, y = 100)
        
        tabla_var.delete(*tabla_var.get_children())
        for i in range(0, len(variables)):
            tabla_var.insert("", 'end',text = str(i), values=(variables[i],))

        mostrar_memoria()
        ventana_errores.mainloop()
    else:
        tabla_var.delete(*tabla_var.get_children())
        ventana_errores = Tk()
        ventana_errores.geometry("520x300")
        msj_error = Label(ventana_errores, text  = "LISTA DE ERRORES", fg = "red")
        msj_error.place(x = 150, y = 30)

        tabla_error = ttk.Treeview(ventana_errores, columns = (), height = 8)

        tabla_error.place(x = 20, y =60)
        tabla_error.heading("#0", text  = "Lista de errores")
        tabla_error.column("#0",minwidth=480, width = 480, stretch=NO)
        
        tabla_error.delete(*tabla_error.get_children())
        for j in range(0, len(errores)):
            tabla_error.insert("", 'end',text = errores[j])
        print(errores)
        ventana_errores.mainloop()
#--------------------INTERFAZ GRAFICA --------------------------------------------

#-Interfaz grafica: ventana asignar kernel y memoria-------------------------------
pre_ventana = Tk()
pre_ventana.title("IMPORTANTE")
pre_ventana.geometry("300x260")
pre_ventana.resizable(False, False)

tker = IntVar()
tmem = IntVar()

input_ker_lab= Label(pre_ventana, text="Kernel", font=('Calibri', 12,'bold'))
input_ker_lab.place(x=60, y=30)

input_mem_lab= Label(pre_ventana, text="Memoria", font=('Calibri', 12,'bold'))
input_mem_lab.place(x=60, y=80)

input_ker = Entry(pre_ventana, textvariable = tker)
input_ker.place(x=140, y=30, width = 110, height = 30)

input_mem = Entry(pre_ventana, textvariable = tmem)
input_mem.place(x=140, y=80, width = 110, height = 30)

mensaje_pre_v = Label(pre_ventana, text = "Comprueba los datos ingresados", fg = "dark orange")
mensaje_pre_v.place(x=60, y=115)

boton_comprobar = Button(pre_ventana, text =" COMPROBAR ", command = lambda: validar_ker_mem(int(tker.get()), int(tmem.get())))
boton_comprobar.place(x = 60, y = 140)

boton_defecto = Button(pre_ventana, text =" POR DEFECTO ", command = lambda: por_defecto())
boton_defecto.place(x = 160, y = 140)



pre_ventana.mainloop()

#-Interfaz grafica: ventana pricipal----------------------------------------------------- 
ventana = Tk()

ventana.title("Chmaquina")
dimx = 1280
dimy = 720
ventana.geometry(str(dimx) + "x" + str(dimy))
ventana.resizable(0, 0)
color = 'light grey'

frame1 = Frame(ventana, bg = color)#, bg = "purple")
frame1.config(width = dimx/2, height = dimy)
frame1.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')

frame11 = Frame(frame1, bg = color)#, bg = "blue")
frame11.config(width = dimx/2, height = 110)
frame11.grid(row = 0, column = 0, sticky = 'nsew')

frame12 = Frame(frame1, bg = color)#, bg = "yellow")
frame12.config(width = dimx/2, height =450)
frame12.grid(row = 1, column = 0, sticky = 'nsew')

frame121 = Frame(frame12, bg = color)#, bg = "orange")
frame121.config(width = dimx/4, height = 450)
frame121.grid(row = 0, column = 0, sticky = 'nsew')

frame122 = Frame(frame12, bg = color)#, bg = "grey")
frame122.config(width = dimx/4, height = 450/2)
frame122.grid(row = 0, column = 1, sticky = 'nsew')

frame1221 = Frame(frame122, bg = color)#, bg = "violet")
frame1221.config(width = dimx/4, height = 450/2)
frame1221.grid(row = 0, column = 0, sticky = 'nsew')

frame1222 = Frame(frame122, bg = color)#, bg = "white")
frame1222.config(width = dimx/4, height = 450/2)
frame1222.grid(row = 1, column = 0, sticky = 'nsew')

frame13 = Frame(frame1, bg = color)#, bg = "pink")
frame13.config(width = dimx/2, height =160)
frame13.grid(row = 2, column = 0, sticky = 'nsew')

frame2 = Frame(ventana, bg = color)#, bg = "green")
frame2.config(width = dimx/2, height = dimy)
frame2.grid(row = 0, column = 2, sticky = 'nsew')

frame21 = Frame(frame2, bg = color)#, bg = "red")
frame21.config(width = dimx/4, height = dimy)
frame21.grid(row = 0, column = 0, sticky = 'nsew')

frame22 = Frame(frame2, bg = color)#, bg = "skyblue")
frame22.config(width = dimx/4, height = dimy)
frame22.grid(row = 0, column = 1, sticky = 'nsew')

frame221 = Frame(frame22,bg = color)#bg = "brown"
frame221.config(width = dimx/4, height = 650)
frame221.grid(row = 0, column = 0, sticky = 'nsew')

frame222= Frame(frame22, bg = color)#bg = "indigo"
frame222.config(width = dimx/4, height = 65)
frame222.grid(row = 1, column = 0, sticky = 'nsew')

#Barra menu----------------------------------------------------------
barra_menu = Menu(ventana)
ventana.config(menu = barra_menu)

menu_archivo = Menu(barra_menu, tearoff = 0)
menu_archivo.add_command(label="Abrir", command = lambda: abrir() , activeforeground = 'red')
menu_archivo.add_separator()
menu_archivo.add_command(label="otra opcion")

barra_menu.add_cascade(label="Archivo ", menu  = menu_archivo)
barra_menu.add_cascade(label="Mostrar Memoria ", command = lambda: mostrar_memoria())#asignar_kernel(memoria, tam_ker))
barra_menu.add_cascade(label="Compilar ", command = lambda: compilar(memoria))
#barra_menu.add_cascade(label="Ejecutar ")
#barra_menu.add_cascade(label="Pausa " )
#barra_menu.add_cascade(label="Paso a paso ")  funciones para faces futuras
#barra_menu.add_cascade(label="PROBAR ")
barra_menu.add_cascade(label="Salir ", command=ventana.quit)

#output Ejecutando---------------------------------------------------------
a = StringVar()
b = StringVar()
c = StringVar()
d = StringVar()


#imagen monitor e impresora------------------------------------------------
dir_monitor = os.path.dirname(__file__) + '/pictures/pantalla.png'
img_monitor = PhotoImage(file = dir_monitor)
monitor = img_monitor.monitor = Label(frame21, image = img_monitor).grid(row = 0, column = 0)

#pantalla del monitor------------------------------------------------------------------
pant_mon = Entry(frame21,textvariable = c, font=('Times new roman', 20,'bold',))
pant_mon.place(x = 34, y = 103, width = 250, height = 142)
pant_mon.config(background="light grey")

#papel de la impresora-----------------------------------------------------------------
pant_imp = Entry(frame21,textvariable = d, font=('Times new roman', 20,'bold',))
pant_imp.place(x = 108, y = 490, width = 102, height = 112)
pant_imp.config(background="light grey")

# tabla programa-------------------------------------------------------------
frame121.config(bd = 13) 
frame121.grid_propagate(False)
tabla_pro = ttk.Treeview(frame121, columns = ("#0"), height = 20)

tabla_pro.grid(row=0, column=0, columnspan = 2)
tabla_pro.heading("#0", text  = "Linea de código")
tabla_pro.heading("#1", text  = "Instrucción")

tabla_pro.column("#0",minwidth=100, width = 100, stretch=NO)
tabla_pro.column("#1",minwidth=190, width = 190, stretch=NO)

# tabla variables-------------------------------------------------------------
frame1221.config(bd = 13) 
frame1221.grid_propagate(False)

style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0)
style.configure("mystyle.Treeview.Heading")

tabla_var = ttk.Treeview(frame1221, columns = ("#0"), height = 8, style = "mystyle.Treeview")

tabla_var.tag_configure('odd', background='#E8E8E8')
tabla_var.tag_configure('even', background='#DFDFDF')

tabla_var.grid(row=0, column=0, columnspan = 2)
tabla_var.heading("#0", text  = "Dirección")
tabla_var.heading("#1", text  = "Variable")

tabla_var.column("#0",minwidth=145, width = 145, stretch=NO)
tabla_var.column("#1",minwidth=145, width = 145, stretch=NO)

# tabla etiquetas-------------------------------------------------------------
frame1222.config(bd = 13) 
frame1222.grid_propagate(False)

tabla_eti = ttk.Treeview(frame1222, columns = ("#0"), height = 8)

tabla_eti.grid(row=0, column=0, columnspan = 2)
tabla_eti.heading("#0", text  = "Dirección")
tabla_eti.heading("#1", text  = "Etiqueta")

tabla_eti.column("#0",minwidth=145, width = 145, stretch=NO)
tabla_eti.column("#1",minwidth=145, width = 145, stretch=NO)



# tabla memoria---------------------------------------------------------------
frame221.config(bd = 13) 
frame221.grid_propagate(False)
tabla_memoria = ttk.Treeview(frame221, columns = ("#0"), height = 30)

tabla_memoria.grid(row=0, column=0, columnspan = 2)
tabla_memoria.heading("#0", text  = "Dirección")
tabla_memoria.heading("#1", text  = "Instrucción")

tabla_memoria.column("#0",minwidth=80, width = 80, stretch=NO)
tabla_memoria.column("#1",minwidth=210, width = 210, stretch=NO)
#-----------------------------------------------------------------------------
tam_ker = tker.get()
tam_mem = tmem.get()
kernel_final_lab = Label(frame22, text = "Kernel: " + str(tam_ker),  font= ('Calibri', 12,'bold'))
memoria_final_lab = Label(frame22, text = "Memoria: " + str(tam_mem),  font=('Calibri', 12,'bold'))
kernel_final_lab.place(x = 70, y = 665)
memoria_final_lab.place(x = 170, y = 665)
#------------------------------------------------------------------------------
ventana.mainloop()
