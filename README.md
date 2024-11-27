### **Descripción Detallada del Script**

El script tiene como objetivo **automatizar la consulta de información asociada a RUTs (números de identificación personal en Chile)** en un portal web gubernamental. Utiliza Python y la biblioteca Selenium para interactuar con la página web, y organiza los resultados en un archivo Excel.

---

### **Flujo del Script**

1. **Configuración del Navegador Web**:
   - Configura un navegador Firefox mediante Selenium con opciones personalizadas:
     - Define un **agente de usuario** para imitar un navegador común.
     - Especifica una **carpeta de descargas** predeterminada (`Downloads/Certificados`).
     - Ajusta configuraciones para evitar interacciones manuales, como la selección de ubicaciones de descarga o la apertura automática de PDFs.
   - Activa el **modo de impresión automática** sin necesidad de confirmación manual.

2. **Selección del Archivo Excel**:
   - Solicita al usuario que seleccione un archivo Excel mediante una ventana emergente de Tkinter.
   - Este archivo debe contener una columna con RUTs.

3. **Ingreso de Credenciales**:
   - Muestra ventanas emergentes para que el usuario ingrese su **nombre de usuario** y **contraseña** necesarios para acceder al portal web.

4. **Inicio de Sesión**:
   - Navega al portal web gubernamental y utiliza Selenium para rellenar y enviar el formulario de inicio de sesión con las credenciales proporcionadas.

5. **Procesamiento de RUTs**:
   - Lee el archivo Excel seleccionado y extrae la columna de RUTs.
   - Para cada RUT:
     - Accede a la página de consulta específica.
     - Ingresa el RUT en el campo de búsqueda y espera los resultados.
     - Extrae información clave del resultado, como:
       - RUT asociado.
       - Nombre completo.
       - Estado (por ejemplo, si el registro está activo o no).
   - Si no se encuentra información o ocurre un error, muestra un mensaje en la consola.

6. **Exportación de Resultados**:
   - Organiza los datos extraídos en un DataFrame de Pandas.
   - Genera un archivo Excel con los resultados, utilizando el nombre del archivo original como base y agregando el sufijo `_resultados.xlsx`.

7. **Tiempos de Ejecución**:
   - Calcula el tiempo total del proceso y lo muestra al final.

---

### **Casos de Uso**

1. **Validación Masiva de RUTs**:
   - Verifica si una lista de RUTs está registrada en el sistema y obtiene detalles relevantes.

2. **Automatización para Grandes Volúmenes de Datos**:
   - Ahorra tiempo y reduce errores al consultar decenas o cientos de registros manualmente.

3. **Generación de Informes**:
   - Crea reportes en Excel con los resultados de la consulta de forma automática.

---

### **Librerías Utilizadas**

- **`pandas`**: Para manipular y organizar los datos extraídos.
- **`selenium`**: Para automatizar la interacción con el navegador web.
- **`tkinter`**: Para interfaces gráficas de selección de archivos y entrada de credenciales.
- **`webdriver_manager`**: Para instalar automáticamente el controlador de Firefox (GeckoDriver).

---

### **Requisitos para Ejecutar el Script**

1. **Navegador Firefox** instalado en el sistema.
2. **GeckoDriver**: Administrado automáticamente por `webdriver_manager`.
3. **Archivo Excel** con una columna llamada `RUT` que contenga los datos a procesar.
4. **Credenciales válidas** para el portal web gubernamental.
5. **Conexión a Internet** estable.

---

### **Beneficios del Script**

- **Eficiencia**: Realiza consultas masivas de forma automatizada, reduciendo la intervención manual.
- **Precisión**: Minimiza errores humanos al extraer datos.
- **Flexibilidad**: Permite al usuario seleccionar diferentes archivos Excel y credenciales cada vez que se ejecuta.
- **Portabilidad**: Al ser escrito en Python, puede ejecutarse en diferentes sistemas operativos.

Este script es ideal para instituciones o usuarios que necesiten consultar registros en línea de manera recurrente y generar reportes detallados de los resultados.

## Requisitos
- Python 3.9+
- Selenium
- Tkinter
- Pandas

## Instalación
1. Clona este repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r src/requirements.txt
