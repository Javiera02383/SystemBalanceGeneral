from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def generar_pdf_cuenta(registros, total_activos_corrientes, total_activos_no_corrientes, total_pasivos_corrientes, total_pasivos_no_corrientes, total_capital, totalEfectivo,
                inversiones, cuentasPorCobrar, inventarios, pagosAnticipados, inversionesValores, propiedadPlantaEquipo, intangibles, propiedadesInversion, otrosActivos,
                cuentasDocumentosPagar, prestamos, provisiones, cobrosAnticipados, cuentasDocumentosPagarNC, prestamosNC, provisionesNC,
                cobrosAnticipadosNC, capital, resultadosAcumuladosCI, reservas, resultadosAcumuladosEJ, empresa, anio):
    """Genera un PDF con los datos ingresados."""
    # Crear el archivo PDF
    pdf_filename = f"Balance_de_{empresa}_{anio}_Cuenta.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = styles["Normal"]
    subtitle_style = styles["Heading2"]

    # Contenido del PDF
    content = []

    # Título con el nombre de la empresa y el año
    title = Paragraph(f"{empresa}<br/>ESTADO DE SITUACIÓN FINANCIERA<br/>AL 31 DE DICIEMBRE DE {anio}", title_style)
    content.append(title)
    content.append(Spacer(1, 12))

    # Función para crear una tabla con registros
    def crear_tabla_cuenta(registros, nombre_subgrupo=None, total_subgrupo=None, nombre_grupo=None, total_grupo=None):
        data = []
        for registro in registros:
            # Reemplazar 0 por una cadena vacía
            depre = registro["depre"] if registro["depre"] != 0 else ""
            monto = registro["monto"] if registro["monto"] != 0 else ""
            subgrupo = registro["subgrupo"] if registro["subgrupo"] != 0 else ""
            
            data.append([
                registro["nombre"],
                depre,
                monto,
                subgrupo,
                "",  # Columna de grupo vacía para los registros
            ])
        
        # Agregar el total del subgrupo como una fila adicional
        if total_subgrupo is not None and nombre_subgrupo is not None:
            data.append([f"Total {nombre_subgrupo}", "", "", f"{total_subgrupo}", ""])
        
        # Agregar el total del grupo como una fila adicional
        if total_grupo is not None and nombre_grupo is not None:
            data.append([f"Total {nombre_grupo}", "", "", "", f"{total_grupo}"])
        
        table = Table(data, colWidths=[250, 80, 80, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Fondo gris en encabezados
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Texto blanco en encabezados
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear todo al centro
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para encabezados
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fuente normal para datos
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),  # Bordes de la tabla
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),  # Espaciado en encabezados
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Fondo blanco para el resto
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Texto negro en celdas
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Negrita en totales
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Fondo gris claro en totales
        ]))
        return table

    # Función para crear una tabla de cuenta (manteniendo lógica existente)
    #def crear_tabla_cuenta(nombre, monto):
     #   """Crea una fila de tabla con una cuenta y su valor."""
      #  return Table([[nombre, monto]], colWidths=[300, 80])

    # Función para obtener el nombre del subgrupo
    def obtener_nombre_subgrupo(codigo):
        return {
            "111": "Efectivo y Equivalente al Efectivo",
            "112": "Inversiones",
            "113": "Cuentas y Documentos Por cobrar",
            "114": "Inventarios",
            "115": "Pagos Anticipados",
            "121": "Inversiones y valores",
            "122": "Propiedad planta y equipo",
            "123": "Intangibles",
            "124": "Propiedades de Inversion",
            "125": "Otros Activos",
            "211": "Cuentas y Documentos Por pagar",
            "212": "Prestamos",
            "213": "Provisiones",
            "214": "Cobros Anticipados",
            "221": "Cuentas y Documentos Por pagar",
            "222": "Prestamos",
            "223": "ProvisionesNC",
            "224": "Cobros AnticipadosNC",
            "311": "Capital",
            "312": "Resultados Acumulados",
            "322": "Reservas",
            "323": "Resultados Acumulados",
        }.get(codigo[:3], "Otros")

    # Agrupar registros por grupo y subgrupo
    grupos = {}
    for registro in registros:
        grupo = registro["grupo"]
        subgrupo_codigo = registro["codigo"][:3]
        subgrupo_nombre = obtener_nombre_subgrupo(registro["codigo"])
        
        if grupo not in grupos:
            grupos[grupo] = {}
        if subgrupo_nombre not in grupos[grupo]:
            grupos[grupo][subgrupo_nombre] = []
        
        grupos[grupo][subgrupo_nombre].append(registro)

    # Mostrar los registros agrupados por grupo y subgrupo
    for grupo, subgrupos in grupos.items():
        content.append(Paragraph(f"<b>{grupo}</b>", subtitle_style))
        for subgrupo_nombre, registros_subgrupo in subgrupos.items():
            # Mostrar el subgrupo solo si hay registros
            if registros_subgrupo:
                content.append(Paragraph(f"{subgrupo_nombre}", normal_style))
                
                # Obtener el total del subgrupo
                total_subgrupo = 0
                if subgrupo_nombre == "Efectivo y Equivalente al Efectivo":
                    total_subgrupo = totalEfectivo
                elif subgrupo_nombre == "Inversiones":
                    total_subgrupo = inversiones
                elif subgrupo_nombre == "Cuentas y Documentos Por cobrar":
                    total_subgrupo = cuentasPorCobrar
                elif subgrupo_nombre == "Inventarios":
                    total_subgrupo = inventarios
                elif subgrupo_nombre == "Pagos Anticipados":
                    total_subgrupo = pagosAnticipados
                elif subgrupo_nombre == "Inversiones y valores":
                    total_subgrupo = inversionesValores
                elif subgrupo_nombre == "Propiedad planta y equipo":
                    total_subgrupo = propiedadPlantaEquipo
                elif subgrupo_nombre == "Intangibles":
                    total_subgrupo = intangibles
                elif subgrupo_nombre == "Propiedades de Inversion":
                    total_subgrupo = propiedadesInversion
                elif subgrupo_nombre == "Otros Activos":
                    total_subgrupo = otrosActivos
                elif subgrupo_nombre == "Cuentas y Documentos Por pagar":
                    total_subgrupo = cuentasDocumentosPagar
                elif subgrupo_nombre == "Prestamos":
                    total_subgrupo = prestamos
                elif subgrupo_nombre == "Provisiones":
                    total_subgrupo = provisiones
                elif subgrupo_nombre == "Cobros Anticipados":
                    total_subgrupo = cobrosAnticipados
                elif subgrupo_nombre == "Capital":
                    total_subgrupo = capital
                elif subgrupo_nombre == "Resultados Acumulados":
                    total_subgrupo = resultadosAcumuladosCI
                elif subgrupo_nombre == "Reservas":
                    total_subgrupo = reservas
                elif subgrupo_nombre == "Resultados Acumulados":
                    total_subgrupo = resultadosAcumuladosEJ
                
                # Crear la tabla con el total del subgrupo y su nombre
                content.append(crear_tabla_cuenta(registros_subgrupo, subgrupo_nombre, total_subgrupo))
                content.append(Spacer(1, 12))
        
        # Mostrar el total del grupo después de todos los subgrupos
        if grupo == "Activos Corrientes":
            content.append(crear_tabla_cuenta([], None, None, grupo, total_activos_corrientes))
        elif grupo == "Activos No Corrientes":
            content.append(crear_tabla_cuenta([], None, None, grupo, total_activos_no_corrientes))
        elif grupo == "Pasivos Corrientes":
            content.append(crear_tabla_cuenta([], None, None, grupo, total_pasivos_corrientes))
        elif grupo == "Pasivos No Corrientes":
            content.append(crear_tabla_cuenta([], None, None, grupo, total_pasivos_no_corrientes))
        elif grupo == "Capital":
            content.append(crear_tabla_cuenta([], None, None, grupo, total_capital))
        
        content.append(Spacer(1, 12))

    # Calcular y mostrar patrimonio
    total_activos = total_activos_corrientes + total_activos_no_corrientes
    total_pasivos = total_pasivos_corrientes + total_pasivos_no_corrientes
    patrimonio = total_activos - total_pasivos
    total = total_pasivos + patrimonio
    content.append(Paragraph(f"<b>Activo (pasivo + patrimonio):</b> {total}", normal_style))

    # Espacio para firmas
    content.append(Spacer(1, 24))
    content.append(Paragraph("_______________              _____________________            ______________________________"))
    content.append(Paragraph("Contador                           Gerente                                       Auditor"))

    # Generar el PDF
    doc.build(content)
    messagebox.showinfo("Éxito", f"PDF generado: {pdf_filename}")