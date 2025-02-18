from tkinter import messagebox
from interfaz import VentanaRegistro
from Reporte import generar_pdf
from principal import PantallaPrincipal
from FormaCuenta import generar_pdf_cuenta  # Importar la función desde Formacuenta.py



def main():
    # Función para generar el PDF (callback)
    def generar_pdf_callback(registros, total_activos_corrientes, total_activos_no_corrientes, total_pasivos_corrientes, total_pasivos_no_corrientes, total_capital,totalEfectivo,
            inversiones,
            cuentasPorCobrar,
            inventarios,
            pagosAnticipados,
            inversionesValores,
            propiedadPlantaEquipo,
            intangibles,
            propiedadesInversion,
            otrosActivos,
            cuentasDocumentosPagar,
            prestamos,
            provisiones,
            cobrosAnticipados,
            cuentasDocumentosPagarNC,
            prestamosNC,
            provisionesNC,
            cobrosAnticipadosNC,
            capital,
            resultadosAcumuladosCI,
            reservas,
            resultadosAcumuladosEJ,empresa, anio):
        generar_pdf(registros, total_activos_corrientes, total_activos_no_corrientes, total_pasivos_corrientes, total_pasivos_no_corrientes, total_capital,totalEfectivo,
            inversiones,
            cuentasPorCobrar,
            inventarios,
            pagosAnticipados,
            inversionesValores,
            propiedadPlantaEquipo,
            intangibles,
            propiedadesInversion,
            otrosActivos,
            cuentasDocumentosPagar,
            prestamos,
            provisiones,
            cobrosAnticipados,
            cuentasDocumentosPagarNC,
            prestamosNC,
            provisionesNC,
            cobrosAnticipadosNC,
            capital,
            resultadosAcumuladosCI,
            reservas,
            resultadosAcumuladosEJ, empresa, anio)





    # Función para abrir la interfaz de registro
    def abrir_interfaz_registro(empresa, anio):
        app = VentanaRegistro(generar_pdf_callback, empresa, anio)
        app.mainloop()
        

    # Crear la pantalla principal
    pantalla_principal = PantallaPrincipal(abrir_interfaz_registro)
    pantalla_principal.mainloop()

if __name__ == "__main__":
    main()