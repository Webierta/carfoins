# Carfoin$

![Carfoin$ Logo](http://www.carfoins.esy.es/data/_uploaded/image/carfoins.gif)

CARFOIN$: Gestión de una Cartera de Fondos de Inversión. Visita la [web del proyecto](http://www.carfoins.esy.es)

Copyright© 2015 Jesús Cuerda Villanueva. Software libre bajo Licencia Pública General de GNU (GPL) versión 3.

## INFORMACIÓN

### DESCRIPCIÓN

CARFOIN$© es una sencilla utilidad multiplataforma para la gestión de múltiples Carteras de Fondos de Inversión. Permite crear fácilmente Carteras personalizadas y seguir su evolución. Opera rápidamente con los Fondos para consultar, actualizar y archivar sus valores liquidativos.

### AUTOR

Derechos de autor: © 2015 - Jesús Cuerda Villanueva. http://www.carfoins.esy.es

Se agradece cualquier sugerencia, crítica, comentario o aviso de error: http://www.carfoins.esy.es/Contacto.

Aplicación gratuita y sin publicidad. No se utiliza ningún dato del usuario. Software de código abierto, libre de spyware, malware, virus o cualquier proceso que atente contra tu dispositivo o viole tu privacidad.

Te invito a colaborar con un donativo vía PayPal para mantener este programa y desarrollar nuevas aplicaciones: http://www.carfoins.esy.es/Licencia

## AYUDA

### REQUISITOS DEL SISTEMA

* Conexión a internet (para añadir fondos y actualizar sus valores).
* Aplicación multiplataforma. Si bien los requisitos de ejecución son compatibles con distintas plataformas, la aplicación sólo está probada en distintas versiones de Debian, Xubuntu, Manjaro, Windows 7 y Windows 8.1. Se agradecen las aportaciones de todos los que puedan probarla en otros sistemas. Realmente el hábitat natural del software libre son los sistemas abiertos. ¡Te invito a probar linux!
* Python versión 3.x. Requiere que el sistema tenga instalado Python versión 3.x, disponible en python.org para distintas plataformas: Windows, Linux/UNIX, Mac OS X y otras. Python se encuentra instalado por defecto en la mayoría de sistemas GNU/Linux, si bien en muchas ocasiones se trata de una versión 2.x. La versión 3.x suele estar incluida en los repositorios de casi todas las distribuciones linux, por lo que su instalación es sencilla. Las últimas versiones de Carfoin$ sólo utilizan componentes de la librería estándar de Python, eliminando módulos de terceros.
* El paquete 'tkinter' para Python. Actualmente se incluye con todas las distribuciones estándar de Python3.x. Este paquete ofrece la interfaz estándar de Python para el conjunto de herramientas gráficas. En Windows ya se instaló cuando instalaste Python 3. Aunque tkinter es parte de la biblioteca estándar de Python, muchas distribuciones linux lo empaquetan separado del paquete principal de Python. Para comprobar si está instalado en tu sistema, desde consola:

    $ python3
    >>> import tkinter

Si aparece un mensaje de error, tkinter no está instalado. En los repositorios de la mayoría de distribuciones linux lo encontrarás con el nombre python3-tk.

Puedes comprobar si has instalado 'tkinter' correctamente ejecutando cualquiera de estos comandos:
    python3 -m tkinter
    tkinter._test()

Cualquiera de ellos debería abrir una simple ventana de demostración de la interfaz gráfica de tkinter.
   
### EJECUCIÓN

1. Comprueba que tu sistema cumple los requisitos necesarios para la correcta ejecución de la aplicación.
2. Descarga el archivo comprimido zip con la última versión. 
3. Descomprime el archivo zip y copia la carpeta principal llamada carfoins a cualquier lugar de tu sistema.
4. En muchos sitemas, puedes ejecutarlo desde el entorno gráfico haciendo doble clic en el archivo carfoins.py. Si no funciona, comprueba las preferencias de tu administrador de archivos: por ejemplo, en Nautilus, en Preferencias --> Comportamiento, selecciona 'Ejecutar los archivos de texto ejecutables al abrirlos'. También puedes probar haciendo clic con el botón secundario del ratón y seleccionar "Ejecutar" o "Abrir" o bien "Abrir con..." y luego «Python(v3.x)». 
5. Para ejecutarlo desde consola (en Windows la abres con cmd), desplázate al directorio donde se encuentra la carpeta principal (por ejemplo, con cd Descargas/carfoins) y ejecuta:
    - en linux: python3 carfoins.py. También funciona con: ./carfoins.py
    - en Windows, dependiendo de la versión y de la configuración: carfoins.py o bien python carfoins.py
      
### USO

La aplicación pretende ofrecer una interfaz gráfica clara y de fácil manejo, por lo que estas instrucciones pueden resultar innecesarias a muchos usuarios.

El programa se divide en dos ventanas principales:

1. VENTANA DE INICIO. El programa arranca en esta ventana que a través de distintas pestañas (Ayuda, Licencia y Créditos) ofrece información básica sobre la aplicación. La pestaña por defecto permite operar con las Carteras. Las opciones principales consisten en Acceder, Crear, Eliminar y Copiar las Carteras. Para utilizar las copias de seguridad (IMPORTANTE: las versiones 0.4.2 y superiores no son compatibles con copias de seguridad de versiones previas):
    - Selecciona una Cartera y presiona el botón «Backup»: automáticamente se crea una copia con el mismo nombre que se guarda en el directorio carfoins/backup. Si existiera una copia previa con el mismo nombre, el archivo nuevo elimina el anterior.
    - Para restaurar una copia, cierra la aplicación y copia el archivo creado en la carpeta backup en la carpeta principal carfoins. Después, abre la aplicación y desde el panel principal crea una Carpeta con el mismo nombre (sin la extensión db) y ya puedes acceder a los Fondos de esa Cartera. 
2. VENTANA DE CARTERAS CREADAS. Desde aquí se opera con los Fondos de esa Cartera y se muestran algunos índices de rentabilidad.
    * MERCADO. Herramienta para configurar la Cartera añadiendo y quitando Fondos. Para incorporar nuevos Fondos necesitas el código ISIN (International Securities Identification Number) que identifica de forma unívoca cada valor mobiliario a nivel internacional. Este código debe contener 12 caracteres alfanuméricos y cumplir una estructura específica para los Fondos de Inversión. El programa verifica ese código y lo utiliza como clave para buscar vía internet el Fondo vinculado. Desde Mercado también puedes eliminar los Fondos que ya no te interesa seguir en tu Cartera. Por ejemplo, quizá quieres eliminar los Fondos que incluye el programa a modo de demostración. Puedes seleccionarlos todos y eliminarlos conjuntamente. La acción de «Eliminar» permite acciones en bloque seleccionando más de un Fondo. 
    * CARTERA. Herramienta para «Actualizar», «Consultar» y «Borrar» los fondos de la Cartera seleccionados (las acciones de Actualizar y Borrar permiten acciones en bloque seleccionando más de un Fondo).
        + «Actualizar» la cotización de los Fondos. El programa busca vía internet el último valor de los Fondos Seleccionados. La actualización en bloque de muchos fondos puede ralentizar el proceso de actualización. Después se muestra una ventana con un informe que detalla el resultado del proceso de actualización sobre cada Fondo. La actualización periódica de un Fondo permite el seguimiento de su evolución a través de la consulta de sus valores liquidativos.
        + «Consultar» el histórico archivado. Muestra el histórico de valores archivados y algunos índices de rentabilidad. Desde esta ventana se puede:
            - Editar: Utilidad para añadir, editar y eliminar valores manualmente.
            - Invertir: Permite incorporar la fecha de suscripción y el capital invertido.
            - Exportar: Exporta la tabla del histórico a un archivo csv. El archivo, que recibe el nombre del código ISIN del Fondo, contine el histórico de valores y se guarda en carfoins/backup. Se puede abrir con una hoja de cálculo (LibreOffice, Excel,...). Para asegurarte la máxima compatibilidad es conveniente utilizar caracteres Unicode (UTF-8), seleccionar 'Coma' como separador de columnas y 'Dobles comillas' como delimitador de texto. 
        + «Borrar» los valores guardados. Puedes seleccionar uno o varios Fondos de Inversión para borrar los valores guardados. Los archivos de esos Fondos quedarán vacíos y los datos se perderán definitivamente pero los Fondos continuarán en tu Cartera. Desde Mercado puedes eliminar el Fondo y su valores simultáneamente.
 
### ATAJOS DE TECLADO

La aplicación pretende que todas las funciones y ventanas sean accesibles indistintamente con el ratón y a través de atajos del teclado. En Windows algunos atajos de teclado no funcionan hasta que la ventana recibe el foco con el ratón. Se utilizan las combinaciones de teclas comunes:

* Botones: Con la tecla del tabulador «Tab» puedes recorrer los botones (y otros elementos activos) y pulsarlos con «Enter».
* Menús: Con la tecla «Alt» + la letra subrayada accedes a los submenús (en algunos sistemas Windows no se ve la letra subrayada hasta que presionas «Alt»). Los Menús se recorren con las teclas de desplazamiento «←↑↓→». «Enter» para pulsar el elemento seleccionado. «Esc» para salir del Menú.
* Pestañas: Accedes con «Tab» y después las recorres con las teclas de desplazamiento a izquierda y derecha.
* Cuadros de texto: Accedes con «Tab» y con las teclas de desplazamiento arriba y abajo se recorre línea a línea. Con «AvPág» y «RePág» se recorre por fragmentos.
* Cuadros de texto seleccionable: Accedes con «Tab» y con las teclas de desplazamiento arriba y abajo para seleccionar líneas. Si se permite la multiselección, con 'Mayús' pulsado seleccionas un rango de líneas.
* Desde las ventanas principales: «F1» para acceder a Ayuda y «Ctrl + Q» para Salir.
* En las ventanas secundarias: «Esc» para cerrar esa ventana.

## DESARROLLO

### VERSIONES

Prácticamente estable y relativamente libre de errores pero todavía en fase de pruebas para su optimización e incorporación de nuevas funciones. Se agradece la participación de todos los betatesters que quieran probar la aplicación y aportar sus impresiones, comentarios, observaciones críticas o sugerencias que ayuden a mejorarlo. Utiliza el formulario de contacto: carfoins.esy.es/Contacto

En proyecto (prácticamente paralizado):

* Optimización del código.
* Mejorar sistema de restauración copias de seguridad.
* Mejorar cálculos de rentabilidad.
* Mejorar entorno gráfico.
* Bugs conocidos:
    - en Windows algunos atajos de teclado no funcionan hasta que la ventana recibe el foco con el ratón.
    - en Windows: los botones no cambian de color cuando el ratón pasa sobre ellos.

0.4.6 (abril 2015):
 
* Corregidos errores persistentes.
    
0.4.5 (abril 2015):

* Corregido error de versión anterior que impedía consultar los Fondos.
    
0.4.4 (abril 2015):
 
* Corregido error por el que algunos Fondos no se actualizaban.
    
0.4.3 (abril 2015):
    
* Permite incorporar la fecha de suscripción y el capital invertido.
* Exporta la tabla del histórico de valores a un archivo csv (hoja de cálculo).
* Corrección de errores menores.
    
0.4.2 (abril 2015):
 
* Entrada de datos manual. Posibilidad de añadir, editar y eliminar valores manualmente.
* Nuevos índices de rentabilidad.
* Correcciones menores.
    
0.4.1 (abril 2015):
    
* Posibilidad de crear múltiples carteras independientes.
* Posibilidad de hacer copias de seguridad de las carteras.
* Optimización del código.
    
0.4.0 (abril 2015):
    
* Incorporación de base de datos. 
* Añadido cálculo de rentabilidad global de la cartera.
* Cambios de diseños para mejorar la experiencia de uso.
* Posibilidad de actualización de fondos en bloque (informe de actualización).
* Optimización del código y corrección de errores menores.
    
0.3.0 (abril 2015):
    
* Bugs corregidos:
    - verificación de ISIN cuando el código nacional de identificación del valor en un país tiene caracteres alfabéticos.
    - en pantallas pequellas en Windows desaparecían algunos botones.
* Navegación por pestañas (agrupación de ventanas). 
* Mejor adaptación a pantallas pequeñas.
* Cambiados diálogos estándar de tkinter por mensajes personalizados.
* Añadidos atajos de teclado. 
* Correcciones y optimizaciones de código.
* Incorporación de algunos cálculos de rentabilidad. 
* Eliminados módulos de terceros (ahora funciona sólo con librerías estándar):
    - Sustitución del módulo EasyGui por el paquete estándar tkinter.
    - Eliminación importación de Pillow. 
* Procesos de control por si se han borrado manualmente archivos generados por el programa.

0.2.0 (marzo 2015):
    
* Incorporación del módulo EasyGui junto al programa.
* Sistema de verificación de ISIN por dígito de control.
* Posibilidad de borrar archivos de valores. 
* Sustitución del modelo de cartera preconfigurada por cartera personalizable. Añadida posibilidad de añadir y eliminar fondos.
* Cambios en diseño.
           
0.1.1 (febrero 2015):
    
* Añadida la función de borrar datos de los archivos.
* Auto-detección de errores.
* Aumentada la cartera de fondos de inversión.
* Código optimizado. 
    
0.1.0 (enero 2015)

### RECONOCIMIENTOS

* Programación: Python versión 3 (Python Software Foundation "PSF", python.org). 
* Fuente de datos: VDOS Stochastics S.L (quefondos.com).
* Imágenes:
    - Logo Carfoni$: Cool Text (cooltext.com).
    - Logo python: Python Software Foundation "PSF" (python.org).
    - Logo VDOS: VDOS Stochastics S.L (vdos.com).
    - Iconos: Free Flat Icons designed by ElegantThemes.com (elegantthemes.com). License: GNU General Public.
    
## LEGAL

### LICENCIA

Copyright © 2015, Jesús Cuerda Villanueva. All rights reserved.
Licencia Pública General de GNU (GPL) versión 3. Véase el archivo adjunto "LICENSE.txt" o en http://www.gnu.org/licenses/gpl-3.0.txt.

Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de COMERCIALIZACIÓN o IDONEIDAD PARA UN PROPÓSITO PARTICULAR.

Este programa es software libre: usted puede redistribuirlo y / o modificarlo bajo los términos de la Licencia Pública General GNU publicada por la Fundación para el Software Libre, versión 3 (GPLv3). La Licencia Pública General de GNU no permite incorporar este programa en programas propietarios.

> «This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License, either version 3 of the License, or any later version.»
> «This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.»
> «You should have received a copy of the GNU General Public License along with this program (LICENSE.txt). If not, see http://www.gnu.org/licenses/.»

### VDOS Stochastics S.L.

El programa utiliza información suministrada por VDOS Stochastics S.L. a través de la web quefondos.com. La información de esta página web se proporciona sin garantía de ninguna clase, ni explícita ni implícita, y podrá cambiarse o actualizarse sin previo aviso.

VDOS Stochastics basa su información en datos públicos obtenidos directamente de las Sociedades Gestoras de Instituciones de Inversión Colectiva, de la CNMV, de la DGS y de procesos propios. En todo caso la información no debe usarse a efectos de realizar transacciones; los datos contenidos son de carácter informativo, no vinculante. No se están facilitando ni valorando datos financieros ni inversores del público usuario y, por tanto, el servicio no comporta recomendación de asesoramiento sobre el producto más apropiado a sus objetivos ni incitación para la suscripción, reembolso, canje o traspaso de participaciones. La rentabilidad de cualquiera de los Instrumentos Financieros no puede ser establecida de antemano; por tanto las rentabilidades históricas resultan orientativas y no presuponen rentabilidades futuras. La información no sustituye ni modifica la contenida en los folletos informativos, documentos de especificaciones, hechos relevantes, memoria, informes semestrales y trimestrales que siempre prevalecerán sobre ésta y que se encuentra disponible en el domicilio de la Sociedad Gestora y en los organismos oficiales competentes. VDOS Stochastics S.L. no tendrá obligación o responsabilidad alguna por cualquier reclamación derivada de un uso distinto del anteriormente expuesto de la información presentada.

Más información sobre los términos y condiciones de esta información en http://www.vdos.com/es/informacionLegal.html.
