import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

def aplicar_estilos(root):
    # Aplicar un tema usando ttkthemes
    root.set_theme("equilux")  # Puedes cambiar "arc" por cualquier otro tema disponible

    # Configurar estilos adicionales
    estilo = ttk.Style()
    estilo.configure("TLabel", font=("Arial", 16), padding=5)
    estilo.configure("TButton", font=("Arial", 16), padding=10,foreground="#ffffff")
    estilo.configure("TEntry", font=("Arial", 16), padding=5)
    root.configure(bg="#464646")  # Color de fondo
