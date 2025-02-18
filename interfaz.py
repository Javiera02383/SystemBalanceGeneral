import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from cuentas import cuentas  # Importar el diccionario de cuentas
from estilos import aplicar_estilos


class VentanaRegistro(ThemedTk):
    def __init__(self, generar_pdf_callback, empresa, anio):
        super().__init__(theme="equilux")  # Puedes cambiar "arc" por cualquier otro tema disponible
        self.title("Registro de Cuenta")
        self.geometry("700x500")
        self.configure(bg="#464646")  # Color de fondo
        
        self.generar_pdf_callback = generar_pdf_callback  # Callback para generar el PDF
        self.empresa = empresa  # Nombre de la empresa
        self.anio = anio  # Año
        
        # Aplicar estilos
        aplicar_estilos(self)
        
        # Usar el diccionario de cuentas importado
        self.cuentas = cuentas  # Diccionario de cuentas (simulación de una base de datos)
     
        # Lista para almacenar los registros
        self.registros = []
        
        # Variables para calcular totales
        #  subgrpos activos
        self.totalEfectivo = 0
        self.inversiones = 0
        self.cuentasPorCobrar = 0
        self.inventarios = 0
        self.pagosAnticipados = 0
        # subgrupos activos no corriente
        self.inversionesValores = 0
        self.propiedadPlantaEquipo = 0
        self.intangibles = 0
        self.propiedadesInversion = 0
        self.otrosActivos = 0
        # pasivos corrientes
        self.cuentasDocumentosPagar = 0
        self.prestamos = 0
        self.provisiones = 0
        self.cobrosAnticipados = 0
        # pasivos no corrientes
        self.cuentasDocumentosPagarNC = 0   
        self.prestamosNC = 0
        self.provisionesNC = 0
        self.cobrosAnticipadosNC = 0
        # patrimonio neto
        self.capital = 0
        self.resultadosAcumuladosCI = 0
        self.reservas = 0
        self.resultadosAcumuladosEJ = 0
        # Variables para calcular totales
        self.total_activos_corrientes = 0
        self.total_activos_no_corrientes = 0
        self.total_pasivos_corrientes = 0
        self.total_pasivos_no_corrientes = 0
        self.total_capital = 0
        
        # Etiquetas y campos de texto
        self.label_codigo = ttk.Label(self, text="Código:")
        self.input_codigo = ttk.Entry(self)
        self.input_codigo.bind("<KeyRelease>", self.buscar_cuenta)  # Evento para autocompletar el nombre
        
        self.label_nombre = ttk.Label(self, text="Cuenta:")
        self.input_nombre = ttk.Label(self, text="---", font=("Arial", 12, "bold"), foreground="gray")
        
        self.label_monto = ttk.Label(self, text="Monto:")
        self.input_monto = ttk.Entry(self)
        
        # Botones
        self.boton_ingresar = ttk.Button(self, text="Ingresar", command=self.ingresar)
        self.boton_imprimir = ttk.Button(self, text="Imprimir/Reporte", command=self.imprimir)
        self.boton_imprimir2 = ttk.Button(self, text="Imprimir/Cuenta", command=self.imprimir)
        self.boton_salir = ttk.Button(self, text="Salir", command=self.quit)

        # Label para mostrar la lista de registros
     #  self.label_lista_registros = ttk.Label(self, text="", font=("Arial", 12))
        
         # Crear el Treeview para mostrar los registros
        self.tree = ttk.Treeview(self, columns=("Código", "Nombre", "Depre", "Monto", "Grupo"), show="headings")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Depre", text="Depre")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Grupo", text="Grupo")

         # Ajustar el ancho de las columnas
        self.tree.column("Código", width=100)
        self.tree.column("Nombre", width=200)
        self.tree.column("Depre", width=100)
        self.tree.column("Monto", width=100)
        self.tree.column("Grupo", width=150)

        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Configurar el Treeview para que se expanda
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        # Diseño de la interfaz
        self.label_codigo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.input_codigo.grid(row=0, column=1, columnspan=3, padx=10, pady=5, sticky="w")
        
        self.label_nombre.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.input_nombre.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="w")
        
        self.label_monto.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.input_monto.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="w")
        
        self.boton_ingresar.grid(row=3, column=0, padx=10, pady=10)
        self.boton_imprimir.grid(row=3, column=1, padx=10, pady=10)
        self.boton_imprimir2.grid(row=3, column=2, padx=10, pady=10)
        self.boton_salir.grid(row=3, column=3, padx=10, pady=10)
    
    def buscar_cuenta(self, event):
        """Busca el nombre de la cuenta según el código ingresado."""
        codigo = self.input_codigo.get()
        nombre = self.cuentas.get(codigo, "No encontrado")
        self.input_nombre.config(text=nombre)
    
    def ingresar(self):
        """Valida y registra los datos ingresados."""
        codigo = self.input_codigo.get().strip()
        monto = self.input_monto.get().strip()
        
        # Validaciones
        if not codigo.isdigit():
            messagebox.showerror("Error", "El código debe ser numérico.")
            return
        
        if codigo not in self.cuentas:
            messagebox.showerror("Error", "El código ingresado no existe.")
            return
        
        if not monto.replace(".", "").isdigit() or float(monto) <= 0:
            messagebox.showerror("Error", "El monto debe ser un número positivo.")
            return
        
        # Convertir a números
        monto = float(monto)
        
        # Lógica para asignar "Monto" o "Depreciaciones"
        if codigo in ["12221", "12231", "12241", "12251", "12261", "12271", "12281"]:
            depre = monto
            monto = 0  # No se asigna monto si el código es mayor a 10000
        else:
            depre = 0  # No se asigna depreciación si el código es menor o igual a 10000
        
        # Calcular Subgrupo (resta del monto anterior con la depreciación)
        subgrupo =0
        
        # Calcular Grupo (total de activos corrientes, no corrientes, pasivos corrientes, no corrientes o capital)
        
        if codigo.startswith("11"):  # Activos corrientes
            self.total_activos_corrientes += monto - depre
            grupo = "Activos Corrientes"
        elif codigo.startswith("12"):  # Activos no corrientes
            self.total_activos_no_corrientes += monto - depre
            grupo = "Activos No Corrientes"
        elif codigo.startswith("21"):  # Pasivos corrientes
            self.total_pasivos_corrientes += monto - depre
            grupo = "Pasivos Corrientes"
        elif codigo.startswith("22"):  # Pasivos no corrientes
            self.total_pasivos_no_corrientes += monto - depre
            grupo = "Pasivos No Corrientes"
        elif codigo.startswith("3"):  # Capital
            self.total_capital += monto - depre
            grupo = "Capital"
        else:
            grupo = "Otros"
            # efectivo y equivalente al efectivo
        if codigo.startswith("111"):
            self.totalEfectivo += monto - depre
        elif codigo.startswith("112"):
            self.inversiones += monto - depre
        elif codigo.startswith("113"):
            self.cuentasPorCobrar += monto - depre
        elif codigo.startswith("114"):
            self.inventarios += monto - depre
        elif codigo.startswith("115"):
            self.pagosAnticipados += monto - depre
            # inversiones y valores
        elif codigo.startswith("121"):
            self.inversionesValores += monto - depre
        elif codigo.startswith("122"):
            self.propiedadPlantaEquipo += monto - depre
        elif codigo.startswith("123"):
            self.intangibles += monto - depre
        elif codigo.startswith("124"):
            self.propiedadesInversion += monto - depre
        elif codigo.startswith("125"):
            self.otrosActivos += monto - depre
            # cuentas y documentos por pagar
        elif codigo.startswith("211"):
            self.cuentasDocumentosPagar += monto - depre
        elif codigo.startswith("212"):
            self.prestamos += monto - depre
        elif codigo.startswith("213"):
            self.provisiones += monto - depre
        elif codigo.startswith("214"):
            self.cobrosAnticipados += monto - depre
            # cuentas y documentos por pagar
        elif codigo.startswith("221"):
            self.cuentasDocumentosPagarNC += monto - depre
        elif codigo.startswith("222"):
            self.prestamosNC += monto - depre
        elif codigo.startswith("223"):
            self.provisionesNC += monto - depre
        elif codigo.startswith("224"):
            self.cobrosAnticipadosNC += monto - depre
        
            # capital
        elif codigo.startswith("311"):
            self.capital += monto - depre
        elif codigo.startswith("312"):
            self.resultadosAcumuladosCI += monto - depre
        elif codigo.startswith("322"):
            self.reservas += monto - depre
        elif codigo.startswith("323"):
            self.resultadosAcumuladosEJ += monto - depre

 
                    
        # Guardar el registro en la lista
        registro = {
            "codigo": codigo,
            "nombre": self.cuentas[codigo],
            "depre": depre,
            "monto": monto,
            "subgrupo": subgrupo,
            "grupo": grupo,
        }

        depre = registro["depre"] if registro["depre"] != 0 else ""
        monto = registro["monto"] if registro["monto"] != 0 else ""
        

        self.registros.append(registro)
  
        self.actualizar_lista_registros()

        # Limpiar los campos de entrada
        self.input_codigo.delete(0, tk.END)
        self.input_nombre.config(text="---")
        self.input_monto.delete(0, tk.END)

        messagebox.showinfo("Éxito", "Datos ingresados correctamente.")
        # registro = self.input_registro.get().strip()

        


    def actualizar_lista_registros(self):
        """Actualiza el Treeview con la lista de registros."""
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar los registros en el Treeview
        for r in self.registros:
            self.tree.insert("", "end", values=(r["codigo"], r["nombre"], r["depre"], r["monto"], r["grupo"]))


    def imprimir2(self):
        """Llama a la función para generar el PDF."""
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay datos para imprimir.")
            return       
       
        """Función para manejar la impresión del botón Imprimir 2."""
        #generar_pdf_cuenta(self.registros)
        # Llamar al callback para generar el PDF
        self.generar_pdf_callback_cuenta(
            self.registros,
            self.total_activos_corrientes,
            self.total_activos_no_corrientes,
            self.total_pasivos_corrientes,
            self.total_pasivos_no_corrientes,
            self.total_capital,
            self.totalEfectivo,
            self.inversiones,
            self.cuentasPorCobrar,
            self.inventarios,
            self.pagosAnticipados,
            self.inversionesValores,
            self.propiedadPlantaEquipo,
            self.intangibles,
            self.propiedadesInversion,
            self.otrosActivos,
            self.cuentasDocumentosPagar,
            self.prestamos,
            self.provisiones,
            self.cobrosAnticipados,
            self.cuentasDocumentosPagarNC,
            self.prestamosNC,
            self.provisionesNC,
            self.cobrosAnticipadosNC,
            self.capital,
            self.resultadosAcumuladosCI,
            self.reservas,
            self.resultadosAcumuladosEJ,
            self.empresa,  # Pasar el nombre de la empresa
            self.anio,  # Pasar el año
        )

    def imprimir(self):
        """Llama a la función para generar el PDF."""
        if not self.registros:
            messagebox.showwarning("Advertencia", "No hay datos para imprimir.")
            return
        
        # Llamar al callback para generar el PDF
        self.generar_pdf_callback(
            self.registros,
            self.total_activos_corrientes,
            self.total_activos_no_corrientes,
            self.total_pasivos_corrientes,
            self.total_pasivos_no_corrientes,
            self.total_capital,
            self.totalEfectivo,
            self.inversiones,
            self.cuentasPorCobrar,
            self.inventarios,
            self.pagosAnticipados,
            self.inversionesValores,
            self.propiedadPlantaEquipo,
            self.intangibles,
            self.propiedadesInversion,
            self.otrosActivos,
            self.cuentasDocumentosPagar,
            self.prestamos,
            self.provisiones,
            self.cobrosAnticipados,
            self.cuentasDocumentosPagarNC,
            self.prestamosNC,
            self.provisionesNC,
            self.cobrosAnticipadosNC,
            self.capital,
            self.resultadosAcumuladosCI,
            self.reservas,
            self.resultadosAcumuladosEJ,
            self.empresa,  # Pasar el nombre de la empresa
            self.anio,  # Pasar el año
        )


