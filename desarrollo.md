# Desarrollo

## Versiones

Prácticamente estable y relativamente libre de errores pero todavía en fase de pruebas para su optimización e incorporación de nuevas funciones. Se agradece la participación de todos los betatesters que quieran probar la aplicación y aportar sus impresiones, comentarios, observaciones críticas o sugerencias que ayuden a mejorarlo.

En proyecto (mantenimiento prácticamente suspendido):

* Optimización del código.
* Mejorar sistema de restauración copias de seguridad.
* Mejorar cálculos de rentabilidad.
* Mejorar entorno gráfico.
* Bugs conocidos:
    - en Windows algunos atajos de teclado no funcionan hasta que la ventana recibe el foco con el ratón.
    - en Windows: los botones no cambian de color cuando el ratón pasa sobre ellos.

0.4.6 (abril 2015): Corregidos errores persistentes.
    
0.4.5 (abril 2015): Corregido error de versión anterior que impedía consultar los Fondos.
    
0.4.4 (abril 2015): Corregido error por el que algunos Fondos no se actualizaban.
    
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

## Reconocimientos

**Programación**:
- Python versión 3 (Python Software Foundation "PSF", python.org). 
- SQLite (http://www.sqlite.org).  Public Domain.

**Fuente de datos**:
- VDOS Stochastics S.L (quefondos.com). El programa utiliza información suministrada por VDOS Stochastics S.L. a través de la web quefondos.com. Los datos se suministran  exclusivamente con fines informativos y se proporcionan sin garantía de ninguna clase, ni explícita ni implícita. Ver los términos y condiciones de esa información en la [Información Legal](http://www.vdos.com/es/informacionLegal.html) de la página web de vdos.com.

**Imágenes**:
- Logo Carfoni$: Cool Text (cooltext.com).
- Logo python: Python Software Foundation "PSF" (python.org).
- Logo SQLite: http://www.sqlite.org.  Public Domain.
- Logo VDOS: VDOS Stochastics S.L (vdos.com).
- Iconos: Free Flat Icons designed by ElegantThemes.com (elegantthemes.com). License: GNU General Public.

