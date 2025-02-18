import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from catalogo import AbrirCatalogo
from estilos import aplicar_estilos


class PantallaPrincipal(ThemedTk):
    def __init__(self, abrir_interfaz_callback):
        super().__init__(theme="equilux")
        self.title("Pantalla Principal")
        self.geometry("700x500")
        self.configure(bg="#f0f0f0")  # Color de fondo
        
        self.abrir_interfaz_callback = abrir_interfaz_callback  # Callback para abrir la interfaz
        
        # Aplicar estilos
        aplicar_estilos(self)
        
        # Crear un frame para contener los widgets
        frame = ttk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiquetas y campos de texto
        self.label_empresa = ttk.Label(frame, text="Nombre de la Empresa:")
        self.input_empresa = ttk.Entry(frame)
        
        self.label_anio = ttk.Label(frame, text="Año:")
        self.input_anio = ttk.Entry(frame)

       # Botón para continuar
        self.boton_continuar = ttk.Button(frame, text="Estado Resultado", command=self.continuar)
        
        # Botón para Catálogo de Cuentas
        self.boton_catalogo = ttk.Button(frame, text="Catálogo de Cuentas", command=self.abrir_catalogo)
        
        # Botón para salir
        self.boton_salir = ttk.Button(frame, text="Salir", command=self.quit)
        
        # Diseño de la interfaz
        self.label_empresa.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.input_empresa.grid(row=1, column=1, padx=10, pady=5)
        
        self.label_anio.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.input_anio.grid(row=2, column=1, padx=10, pady=5)
        
        #self.boton_continuar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        #self.boton_catalogo.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
       
       # Crear un frame para los botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=10)

        self.boton_continuar.grid(row=3, column=0, padx=(0, 5), pady=10)
        self.boton_catalogo.grid(row=3, column=1, padx=(5, 0), pady=10)
        self.boton_salir.grid(row=4, column=3, columnspan=2, padx=10, pady=(20, 10))



    def continuar(self):
        """Valida los datos y abre la interfaz de registro."""
        empresa = self.input_empresa.get().strip()
        anio = self.input_anio.get().strip()
        
        # Validaciones
        if not empresa:
            messagebox.showerror("Error", "El nombre de la empresa es obligatorio.")
            return
        
        if not anio.isdigit() or len(anio) != 4:
            messagebox.showerror("Error", "El año debe ser un número de 4 dígitos.")
            return
        
        # Cerrar la pantalla principal y abrir la interfaz de registro
        self.destroy()
        self.abrir_interfaz_callback(empresa, anio)


    def abrir_catalogo(self):
        AbrirCatalogo() 

  #  def abrir_estado_financiero(self):
   #     estado_financiero()