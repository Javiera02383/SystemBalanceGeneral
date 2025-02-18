import tkinter as tk
from tkinter import ttk, messagebox
from cuentas import cuentas  # Importar el diccionario de cuentas
from ttkthemes import ThemedTk
from estilos import aplicar_estilos

class AbrirCatalogo(ThemedTk):
    def __init__(self):
        super().__init__(theme="equilux")
        self.title("Catálogo de Cuentas")
        self.geometry("700x500")
        
        # Aplicar estilos
        aplicar_estilos(self)
        
        # Usar el diccionario de cuentas importado
        self.cuentas = cuentas  # Diccionario de cuentas (simulación de una base de datos)
        
        # Crear widgets
        self.crear_widgets()
        
    def crear_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label_codigo = ttk.Label(frame, text="Código:")
        label_codigo.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_codigo = ttk.Entry(frame)
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        label_descripcion = ttk.Label(frame, text="Descripción:")
        label_descripcion.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_descripcion = ttk.Entry(frame)
        self.entry_descripcion.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        btn_agregar = ttk.Button(frame, text="Agregar", command=self.agregar_cuenta)
        btn_agregar.grid(row=2, column=0, padx=10, pady=10)
        btn_actualizar = ttk.Button(frame, text="Actualizar", command=self.actualizar_cuenta)
        btn_actualizar.grid(row=2, column=1, padx=10, pady=10)
        btn_eliminar = ttk.Button(frame, text="Eliminar", command=self.eliminar_cuenta)
        btn_eliminar.grid(row=2, column=2, padx=10, pady=10)

         # Tabla
        columns = ("Código", "Descripción")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)

        # Insertar las cuentas en el Treeview
        for codigo, descripcion in self.cuentas.items():
            self.tree.insert("", "end", values=(codigo, descripcion))

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_cuenta)

    def agregar_cuenta(self):
        codigo = self.entry_codigo.get()
        descripcion = self.entry_descripcion.get()
        if codigo and descripcion:
            if codigo in self.cuentas:
                messagebox.showwarning("Error", "El código ya existe.")
            else:
                self.cuentas[codigo] = descripcion
                self.tree.insert("", "end", values=(codigo, descripcion))
                
                # Actualizar la lista de cuentas en cuentas.py
                self.actualizar_archivo_cuentas()

                self.entry_codigo.delete(0, tk.END)
                self.entry_descripcion.delete(0, tk.END)
                messagebox.showinfo("Éxito", "Cuenta agregada correctamente.")
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")

    def eliminar_cuenta(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            codigo = str(item['values'][0])  # Asegurarse de que el código sea una cadena
            if codigo in self.cuentas:
                del self.cuentas[codigo]
                self.tree.delete(selected_item)
                self.actualizar_archivo_cuentas()
                self.entry_codigo.delete(0, tk.END)
                self.entry_descripcion.delete(0, tk.END)
                messagebox.showinfo("Éxito", "Cuenta eliminada correctamente.")
            else:
                messagebox.showwarning("Error", "El código no existe en el diccionario de cuentas.")
        else:
            messagebox.showwarning("Error", "Seleccione una cuenta para eliminar")

    def actualizar_cuenta(self):
        selected_item = self.tree.selection()
        if selected_item:
            codigo = self.entry_codigo.get()
            descripcion = self.entry_descripcion.get()
            if codigo and descripcion:
                item = self.tree.item(selected_item)
                old_codigo = str(item['values'][0])  # Asegurarse de que el código antiguo sea una cadena
                if old_codigo != codigo and codigo in self.cuentas:
                    messagebox.showwarning("Error", "El nuevo código ya existe.")
                else:
                    # Eliminar la cuenta antigua y agregar la nueva
                    if old_codigo != codigo:
                        del self.cuentas[old_codigo]
                    self.cuentas[codigo] = descripcion
                    self.tree.item(selected_item, values=(codigo, descripcion))
                    self.actualizar_archivo_cuentas()
                    self.entry_codigo.delete(0, tk.END)
                    self.entry_descripcion.delete(0, tk.END)
                    messagebox.showinfo("Éxito", "Cuenta actualizada correctamente.")
            else:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
        else:
            messagebox.showwarning("Error", "Seleccione una cuenta para actualizar")

    def seleccionar_cuenta(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            valores = self.tree.item(selected_item, "values")
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.insert(0, valores[0])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[1])

    def actualizar_archivo_cuentas(self):
        with open('cuentas.py', 'w') as f:
            f.write('cuentas = {\n')
            for codigo, descripcion in self.cuentas.items():
                f.write(f'    "{codigo}": "{descripcion}",\n')
            f.write('}\n')

if __name__ == "__main__":
    app = AbrirCatalogo()
    app.mainloop()