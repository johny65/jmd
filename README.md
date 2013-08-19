jmd
===

_Post-procesador personalizado para Markdown._

---

**jmd** (_Johny's Mark Down_) es un post-procesador personalizado para Markdown, que permite usar algunos añadidos a su sintaxis para controlar ciertos aspectos del HTML resultante, como por ejemplo el color de la fuente o propiedades de las imágenes.

Aunque **jmd** es un post-procesador en sí, se encarga del proceso completo, es decir, su entrada es un archivo escrito en Markdown. **jmd** carga este archivo (`.markdown` o `.md`), ejecuta `markdown` para convertirlo a HTML y después hace el post-proceso.

**jmd** reconoce códigos especiales en el archivo de entrada que pueden ser usados para abrir un enlace en una nueva página (usar `target=_blank` en el enlace), para alinear imágenes y para escribir texto en color. También **jmd** convierte los caracteres latinos con acentos en equivalentes HTML (por ejemplo 'á' en '&aacute;'.).


Sintaxis agregada por `jmd`:
---------------------------

Al escribir en Markdown puedes usar estos códigos añadidos que luego **jmd** podrá interpretar para retocar el HTML generado:

* Enlaces en nueva página:

    Añadir al enlace el texto alternativo `"!"`. Ej.:

        [Enlace con target = blank](http://una-url.com "!")

* Alinear imágenes:

    Para alinear imágenes usar uno de estos comandos como texto alternativo:
    
    * `l`: alinear a la izquierda
    * `r`: alinear a la derecha
    * `c`: alinear al centro
    * `lf`: flotante alineado a la izquierda
    * `rf`: flotante alineado a la derecha

    `lf` y `rf` permite poner la imagen flotante dentro del párrafo usando una etiqueta `<div>` con `style="float"`.

    Se puede especificar un margen (o varios) para la imagen agregando un `!` y alguna o varias de estas opciones (todas juntas, sin importar el orden):

    * `t`: margen arriba (top)
    * `b`: margen abajo (bottom)
    * `l`: margen izquierdo (left)
    * `r`: margen derecho (right)

    Ej.:
    Imagen centrada con todos los márgenes:

        ![c!tblr](img/imagen.png)

    Imagen flotante a la derecha con margen izquierdo:

        ![rf!l](img/imagen.png)

    Imagen alineada a la izquierda sin márgenes:

        ![l](img/imagen.png)

* Colores:

    Para poner un texto con color, rodearlo con `[#` y `]` especificando el color junto al `#`. Ej.:

    Texto con color rojo:

        "En este texto [#red esta parte está en rojo] y ésta no."

    Texto con otro color HTML:

        "Usando un [#A08C6E color raro]."


Uso:
---

Para usarlo se debe ejecutar de la siguiente manera:

    $ python jmd.py archivo.markdown > salida.htm

Por defecto la salida del programa es impresa en la salida estándar, es por eso que debe pasarse un archivo de salida con `'>'` si se desea.

También se le puede dar permiso de ejecución al script y así ejecutarlo directamente:

    $ chmod +x jmd.py
    $ mv jmd.py jmd
    $ ./jmd

Para ver la ayuda detallada pasarle la opción `-h` o `--help`:

    $ ./jmd -h
    $ ./jmd --help


Opciones:
--------

Por ahora la única opción configurable es si se desea convertir los caracteres con acentos en entidades HTML. Por defecto la conversión sí se realiza, si se desea desactivar pasarle la opción `-n`.

Requiere:
--------

El módulo Markdown de Python, se puede descargar de Pypi:

<http://pypi.python.org/pypi/Markdown>

Además está hecho para funcionar con Python 2.

Versión:
-------
0.2

Domingo 22 de abril de 2012.

Creado por Juan Bertinetti.

Sitio web: <https://bitbucket.org/johny65/jmd>

Cambios:
-------

**0.2**:

* Ahora la opción -h o --help muestra la ayuda completa.
* Se corrigió el manejo de errores al pasar un archivo que no existe.
