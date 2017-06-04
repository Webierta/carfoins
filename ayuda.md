# Ayuda

## Requisitos

**Conexión a internet** (para añadir fondos y actualizar sus valores).

**Aplicación multiplataforma**. Si bien los requisitos de ejecución son compatibles con distintas plataformas, la aplicación sólo está probada en distintas versiones de Debian, Xubuntu y  Manjaro, y puntualmente en Windows 7 y Windows 8.1. Se agradecen las aportaciones de todos los que puedan probarla en otros sistemas. Realmente el hábitat natural del software libre son los sistemas abiertos. ¡Te invito a probar linux!

**Python versión 3.x**. Requiere que el sistema tenga instalado Python versión 3.x, disponible en python.org para distintas plataformas: Windows, Linux/UNIX, Mac OS X y otras. Python se encuentra instalado por defecto en la mayoría de sistemas GNU/Linux, si bien en muchas ocasiones se trata de una versión 2.x. La versión 3.x suele estar incluida en los repositorios de casi todas las distribuciones linux, por lo que su instalación es sencilla. Las últimas versiones de Carfoin$ sólo utilizan componentes de la librería estándar de Python, eliminando módulos de terceros.

**El paquete 'tkinter' para Python**. Actualmente se incluye con todas las distribuciones estándar de Python3.x. Este paquete ofrece la interfaz estándar de Python para el conjunto de herramientas gráficas. En Windows ya se instaló cuando instalaste Python 3. Aunque tkinter es parte de la biblioteca estándar de Python, muchas distribuciones linux lo empaquetan separado del paquete principal de Python. Para comprobar si está instalado en tu sistema, desde consola: $ python3, y luego >>>import tkinter

Si aparece un mensaje de error, tkinter no está instalado. En los repositorios de la mayoría de distribuciones linux lo encontrarás con el nombre **python3-tk**.

Puedes comprobar si has instalado 'tkinter' correctamente ejecutando cualquiera de estos comandos:

    python3 -m tkinter
    tkinter._test()

Cualquiera de ellos debería abrir una simple ventana de demostración de la interfaz gráfica de tkinter.
            
## Ejecución

1. Comprueba que tu sistema cumple los [requisitos](https://webierta.github.io/carfoins/#!ayuda.md#Requisitos) necesarios para la correcta ejecución de la aplicación.
2. [Descarga](https://webierta.github.io/carfoins/#!descarga.md) el archivo comprimido zip con la última versión.
3. Descomprime el archivo zip y copia la carpeta principal llamada carfoins a cualquier lugar de tu sistema.
4. En muchos sitemas, puedes ejecutarlo desde el entorno gráfico haciendo doble clic en el archivo **carfoins.py**. Si no funciona, comprueba las preferencias de tu administrador de archivos: por ejemplo, en Nautilus, en Preferencias --> Comportamiento, selecciona 'Ejecutar los archivos de texto ejecutables al abrirlos'. También puedes probar haciendo clic con el botón secundario del ratón y seleccionar "Ejecutar" o "Abrir" o bien "Abrir con..." y luego «Python(v3.x)».
5. Para ejecutarlo desde consola (en Windows la abres con cmd), desplázate al directorio donde se encuentra la carpeta principal (por ejemplo, con cd Descargas/carfoins) y ejecuta:
    - en linux: **python3 carfoins.py**. También funciona con: ./carfoins.py
    - en Windows, dependiendo de la versión y de la configuración: carfoins.py o bien python carfoins.py

## Uso

La aplicación pretende ofrecer una interfaz gráfica clara y de fácil manejo, por lo que estas instrucciones pueden resultar innecesarias a muchos usuarios.

El programa se divide en dos ventanas principales:

### VENTANA DE INICIO. CARTERAS

El programa arranca en esta ventana que a través de distintas pestañas (Ayuda, Licencia y Créditos) ofrece información básica sobre la aplicación.

La pestaña por defecto permite operar con las Carteras. Las opciones principales consisten en Acceder, Crear, Eliminar y Copiar las Carteras.

Para utilizar las **copias de seguridad** (IMPORTANTE: las versiones 0.4.2 y superiores no son compatibles con copias de seguridad de versiones previas):

- Selecciona una Cartera y presiona el botón «Backup»: automáticamente se crea una copia con el mismo nombre que se guarda en el directorio carfoins/backup. Si existiera una copia previa con el mismo nombre, el archivo nuevo elimina el anterior.
- Para restaurar una copia, cierra la aplicación y copia el archivo creado en la carpeta backup en la carpeta principal carfoins. Después, abre la aplicación y desde el panel principal crea una Carpeta con el mismo nombre (sin la extensión db) y ya puedes acceder a los Fondos de esa Cartera. 

### VENTANA DE FONDOS

Desde aquí se opera con los Fondos de las Carteras y se muestran algunos índices de rentabilidad.

#### MERCADO

Herramienta para configurar la Cartera añadiendo y quitando Fondos.

Para incorporar **nuevos Fondos** necesitas el código ISIN (International Securities Identification Number) que identifica de forma unívoca cada valor mobiliario a nivel internacional. Este código debe contener 12 caracteres alfanuméricos y cumplir una estructura específica para los Fondos de Inversión. El programa verifica ese código y lo utiliza como clave para buscar vía internet el Fondo vinculado.

Desde Mercado también puedes **eliminar los Fondos** que ya no te interesa seguir en tu Cartera. Por ejemplo, quizá quieres eliminar los Fondos que incluye el programa a modo de demostración. Puedes seleccionarlos todos y eliminarlos conjuntamente. La acción de «Eliminar» permite acciones en bloque seleccionando más de un Fondo.

#### CARTERA

Herramienta para «Actualizar», «Consultar» y «Borrar» los fondos de la Cartera seleccionados (las acciones de Actualizar y Borrar permiten acciones en bloque seleccionando más de un Fondo).

- **«Actualizar»** la cotización de los Fondos. El programa busca vía internet el último valor de los Fondos Seleccionados. La actualización en bloque de muchos fondos puede ralentizar el proceso de actualización. Después se muestra una ventana con un informe que detalla el resultado del proceso de actualización sobre cada Fondo. La actualización periódica de un Fondo permite el seguimiento de su evolución a través de la consulta de sus valores liquidativos.
- **«Consultar»** el histórico archivado. Muestra el histórico de valores archivados y algunos índices de rentabilidad. Desde esta ventana se puede:
    * **Editar**: Utilidad para añadir, editar y eliminar valores manualmente.
    * **Invertir**: Permite incorporar la fecha de suscripción y el capital invertido.
    * **Exportar**: Exporta la tabla del histórico a un archivo csv. El archivo, que recibe el nombre del código ISIN del Fondo, contine el histórico de valores y se guarda en carfoins/backup. Se puede abrir con una hoja de cálculo (LibreOffice, Excel,...). Para asegurarte la máxima compatibilidad es conveniente utilizar caracteres Unicode (UTF-8), seleccionar 'Coma' como separador de columnas y 'Dobles comillas' como delimitador de texto.
- **«Borrar»** los valores guardados. Puedes seleccionar uno o varios Fondos de Inversión para borrar los valores guardados. Los archivos de esos Fondos quedarán vacíos y los datos se perderán definitivamente pero los Fondos continuarán en tu Cartera. Desde Mercado puedes eliminar el Fondo y su valores simultáneamente.

## Atajos de Teclado

La aplicación pretende que todas las funciones y ventanas sean accesibles indistintamente con el ratón y a través de atajos del teclado. En Windows algunos atajos de teclado no funcionan hasta que la ventana recibe el foco con el ratón. Se utilizan las combinaciones de teclas comunes:

- Botones: Con la tecla del tabulador «Tab» puedes recorrer los botones (y otros elementos activos) y pulsarlos con «Enter».
- Menús: Con la tecla «Alt» + la letra subrayada accedes a los submenús (en algunos sistemas Windows no se ve la letra subrayada hasta que presionas «Alt»). Los Menús se recorren con las teclas de desplazamiento «←↑↓→». «Enter» para pulsar el elemento seleccionado. «Esc» para salir del Menú.
- Pestañas: Accedes con «Tab» y después las recorres con las teclas de desplazamiento a izquierda y derecha.
- Cuadros de texto: Accedes con «Tab» y con las teclas de desplazamiento arriba y abajo se recorre línea a línea. Con «AvPág» y «RePág» se recorre por fragmentos.
- Cuadros de texto seleccionable: Accedes con «Tab» y con las teclas de desplazamiento arriba y abajo para seleccionar líneas. Si se permite la multiselección, con 'Mayús' pulsado seleccionas un rango de líneas.
- Desde las ventanas principales: «F1» para acceder a Ayuda y «Ctrl + Q» para Salir.
- En las ventanas secundarias: «Esc» para cerrar esa ventana.

