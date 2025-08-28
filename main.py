import numpy as np
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar
from tkinter import ttk 

from config import FILE_PATH_GRAB, FILE_PATH_TIME, FILE_PATH_TRACK, OUTPUT_JSON
from data_loader import cargar_json
from utils import generar_id, convertir_posiciones
from modelo import crear_modelo, evaluar_speedrun
from send_data import post_data
import json

root = Tk()
root.title("Evaluación de Usuario")

width, height = 500, 250
root.geometry(f"{width}x{height}")

font_label = ("Arial", 12)
font_entry = ("Arial", 12)
font_button = ("Arial", 12, "bold")

pad_x_total = width // 10
pad_y_total = height // 10

entry_nombre = Entry(root, font=font_entry, width=25)
entry_id = Entry(root, font=font_entry, width=25)
genero_var = StringVar(value="Hombre")
combo_genero = ttk.Combobox(
    root, textvariable=genero_var, values=["Hombre", "Mujer"],
    font=font_entry, width=15, state="readonly"
)

dia_var = StringVar()
combo_dia = ttk.Combobox(
    root, textvariable=dia_var, values=["1", "2", "3"],
    font=font_entry, width=15, state="readonly"
)

Label(root, text="Nombre:", font=font_label).grid(row=0, column=0, padx=pad_x_total, pady=8, sticky="e")
entry_nombre.grid(row=0, column=1, padx=pad_x_total, pady=8, sticky="w")

Label(root, text="ID:", font=font_label).grid(row=1, column=0, padx=pad_x_total, pady=8, sticky="e")
entry_id.grid(row=1, column=1, padx=pad_x_total, pady=8, sticky="w")

Label(root, text="Día:", font=font_label).grid(row=2, column=0, padx=pad_x_total, pady=8, sticky="e")
combo_dia.grid(row=2, column=1, padx=pad_x_total, pady=8, sticky="w")

Label(root, text="Género:", font=font_label).grid(row=3, column=0, padx=pad_x_total, pady=8, sticky="e")
combo_genero.grid(row=3, column=1, padx=pad_x_total, pady=8, sticky="w")

def generar_resultado():
    nombre = entry_nombre.get()
    user_id = entry_id.get()
    genero = genero_var.get()
    dia = dia_var.get()

    if not nombre:
        messagebox.showerror("Error", "Debes ingresar un nombre")
        return
    if not user_id:
        user_id = generar_id()
        entry_id.insert(0, user_id)
        messagebox.showinfo("Info", f"Se generó un ID automáticamente: {user_id}")
    if not genero:
        messagebox.showerror("Error", "Debes seleccionar un género")
        return
    if not dia:
        messagebox.showerror("Error", "Debes seleccionar un día")
        return

    grab_data = cargar_json(FILE_PATH_GRAB)
    time_data = cargar_json(FILE_PATH_TIME)
    track_data = cargar_json(FILE_PATH_TRACK)

    grab_attempts = int(grab_data["GrabAttempts"])
    score = int(grab_data["TotalScore"])
    tiempos = [float(v) for v in time_data.values()]
    posiciones = convertir_posiciones(track_data)

    speedrun = {
        'nombre': nombre,
        'id': user_id,
        'genero': genero,
        'dia' : dia,
        'score': score,
        'tiempo_prom': np.mean(tiempos),
        'grab_attempts': grab_attempts,
        'num_posiciones_prom': 4,
        'tiempos': tiempos,
        'posiciones': posiciones
    }

    global modelo
    speedrun = evaluar_speedrun(modelo, speedrun)

    post_data(speedrun)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(speedrun, f, indent=4, ensure_ascii=False)

    messagebox.showinfo(
        "Éxito",
        f"Resultado generado y guardado en {OUTPUT_JSON}\nProbabilidad de ser apto: {speedrun['prob_apto']:.2f}"
    )

Button(root, text="Generar Resultado", font=font_button, command=generar_resultado).grid(
    row=4, column=0, columnspan=2, pady=15
)

modelo = crear_modelo()

root.mainloop()