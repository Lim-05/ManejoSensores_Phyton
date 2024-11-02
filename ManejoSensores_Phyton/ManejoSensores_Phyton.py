import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

arduino_port = "COM3"  
baud_rate = 9600
arduino = None  

# Funci�n para conectar al Arduino y enviar el l�mite de temperatura
def conectar():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)  # Espera para que se establezca la conexi�n
        lbConexion.config(text="Estado: Conectado", fg="green")
        start_reading()
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al Arduino. Verifique")

# Funci�n para desconectar el Arduino
def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConexion.config(text="Estado: Desconectado", fg="red")
        messagebox.showinfo("Conexion", "Conexion terminada.")
    else:
        messagebox.showwarning("Advertencia", "No hay conexion activa.")

# Funci�n para iniciar la lectura en un hilo separado
def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

# Configuraci�n de la interfaz gr�fica
root = tk.Tk()
root.title("Interfaz de Monitoreo de Temperatura")
root.geometry("300x350")


lbTitleTemp = tk.Label(root, text="Temperatura Actual", font=("Arial", 12))
lbTitleTemp.pack(pady=10)

# Etiqueta para mostrar la temperatura
lbTemp = tk.Label(root, text="-- C", font=("Arial", 24))
lbTemp.pack()

# Etiqueta de estado de conexi�n
lbConexion = tk.Label(root, text="Estado: Desconectado", fg="red", font=("Arial", 10))
lbConexion.pack(pady=5)

# Entrada para el l�mite de temperatura
lbLimitTemp = tk.Label(root, text="Limite de Temperatura:")
lbLimitTemp.pack(pady=5)
tbLimTemp = tk.Entry(root, width=10)
tbLimTemp.pack()

# Funci�n para enviar el l�mite de temperatura al Arduino
def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        limite = tbLimTemp.get()
        if limite.isdigit():  # Verifica si el limite es un n�mero v�lido
            arduino.write(f"{limite}\n".encode())  # Env�a el l�mite al Arduino
            messagebox.showinfo("Enviado", f"Limite de temperatura ({limite}C) enviado.")
        else:
            messagebox.showerror("Error", "Ingrese un valor numerico para el limite.")
    else:
        messagebox.showwarning("Advertencia", "Conectese al Arduino antes de enviar el limite.")

# Funci�n para leer datos desde el Arduino
def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip()  
            if "Temperatura" in data:  
                temp_value = data.split(":")[1].strip().split(" ")[0]
                lbTemp.config(text=f"{temp_value} C")
            time.sleep(1)
        except Exception as e:
            print(f"Error leyendo datos: {e}")
            break

# Bot�n de Conectar
btnConectar = tk.Button(root, text="Conectar", command=conectar, font=("Arial", 10))
btnConectar.pack(pady=5)

# Bot�n de Desconectar
btnDesconectar = tk.Button(root, text="Desconectar", command=desconectar, font=("Arial", 10))
btnDesconectar.pack(pady=5)

# Bot�n para enviar el l�mite de temperatura
btnEnviar = tk.Button(root, text="Enviar Limite", command=enviar_limite, font=("Arial", 10))
btnEnviar.pack(pady=5)

# Ejecuta la interfaz
root.mainloop()

