#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#  jmd.py
#  
#  Copyright (C) 2013  Juan Bertinetti <juanbertinetti@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

help_string = u"""
Johny's Mark Down: Post-procesador personalizado para Markdown.

'jmd' carga un archivo markdown, ejecuta markdown para convertirlo a HTML
y después hace un post-proceso donde busca los códigos especiales para abrir
un enlace en una nueva página, para alinear imágenes y para escribir texto
en color.
También convierte los caracteres latinos con acentos en equivalentes HTML
('á' en '&aacute; etc.).

* Enlaces en nueva página:

    Añadir al enlace el texto alternativo "!". Ej.:
    [Enlace con target = blank](http://una-url.com "!")

* Alinear imágenes:

    Para alinear imágenes usar uno de estos comandos como texto alternativo:

    * l: alinear a la izquierda
    * r: alinear a la derecha
    * c: alinear al centro
    * lf: flotante alineado a la izquierda
    * rf: flotante alineado a la derecha

    'lf' y 'rf' permite poner la imagen flotante dentro del párrafo usando
    una etiqueta <div> con style="float".

    Se puede especificar un margen (o varios) para la imagen agregando un !
    y alguna o varias de estas opciones (todas juntas, sin importar el orden):

    * t: margen arriba (top)
    * b: margen abajo (bottom)
    * l: margen izquierdo (left)
    * r: margen derecho (right)

    Ej.:
    Imagen centrada con todos los márgenes:
    ![c!tblr](img/imagen.png)

    Imagen flotante a la derecha con margen izquierdo:
    ![rf!l](img/imagen.png)

    Imagen alineada a la izquierda sin márgenes:
    ![l](img/imagen.png)

* Colores:

    Para poner un texto con color, rodearlo con '[#' y ']' especificando el
    color junto al #. Ej.:

    Texto con color rojo:
    "En este texto [#red esta parte está en rojo] y ésta no."

    Texto con otro color HTML:
    "Usando un [#A08C6E color raro]."


Requiere:
    El módulo Markdown de Python, se puede descargar de Pypi:
    http://pypi.python.org/pypi/Markdown

Versión:
    0.2
    Creado por Juan Bertinetti.
    Sitio web: https://bitbucket.org/johny65/jmd
"""

import markdown
import codecs

def escape_latin(text):
    """
    Convierte los caracteres con acentos en *text* a equivalentes HTML y
    devuelve el texto convertido.
    """
    s = ""
    #caracteres a reemplazar y sus conversiones:
    chars = "áéíóúÁÉÍÓÚñÑ"
    codes = {
        "á": "&aacute;",
        "é": "&eacute;",
        "í": "&iacute;",
        "ó": "&oacute;",
        "ú": "&uacute;",
        "Á": "&Aacute;",
        "É": "&Eacute;",
        "Í": "&Iacute;",
        "Ó": "&Oacute;",
        "Ú": "&Uacute;",
        "ñ": "&ntilde;",
        "Ñ": "&Ntilde;"
    }
    pos = 0
    for i, c in enumerate(text):
        if c in chars:
            s += text[pos:i] + codes[c]
            pos = i+1
    s += text[pos:]
    return s

def target_blank(text):
    """
    Procesa los enlaces con el comando "!" (abrir en nueva página) y agrega el
    HTML necesario (target="_blank"). Devuelve el texto procesado.
    """
    s = ""
    ini = 0
    pos = text.find('title="!"')
    while pos != -1:
        pos_a = text.rfind("<a ", 0, pos)
        s += text[ini:pos_a+3] + 'target="_blank" '
        s += text[pos_a+3:pos-1]
        ini = text.find(">", pos)
        pos = text.find('title="!"', ini)
    s += text[ini:]
    return s

def alinear_imagenes(text):
    """
    Procesa el texto en *text* buscando los comandos para alinear imágenes
    y generando el HTML necesario. Devuelve el texto procesado.
    """

    # opciones para las distintas alineaciones:
    aligns = {
        "l": "text-align: left;",
        "c": "text-align: center;",
        "r": "text-align: right;",
        "lf": "float: left;",
        "rf": "float: right;"
    }
    #opciones para los distintos márgenes:
    margins = {
        "t": " margin-top: 1em;",
        "b": " margin-bottom: 1em;",
        "l": " margin-left: 1em;",
        "r": " margin-right: 1em;"
    }
    
    s = ""
    aux = "<img alt="
    ini = 0
    pos = text.find(aux)
    while pos != -1:

        p2 = pos + len(aux) + 1 #inicio de lo que está dentro de "alt"
        op = text[p2:text.find('"', p2)] #texto dentro de "alt"

        if op:
            #sólo procesamos si img tiene algún dato, sino es una imagen
            #que no hay que procesar (alt="")
            
            #extraemos toda la etiqueta <img ... />:
            finimg = text.find("/>", pos) + 2
            img = text[pos:finimg]

            #analizar op:
            l = op.split("!")

            div = '<div style="' + aligns[l[0]]
            if len(l) == 2: #hay opciones de márgenes
                for m in l[1]:
                    div += margins[m]
            div += '">'

            #metemos todo en el texto de salida:
            s += text[ini:pos]
            s += div
            img = img.replace('alt="' + op + '" ', "") #quitamos texto alt
            s += img + "</div>"

            ini = finimg
        #end if
        pos = text.find(aux, p2)
    #end while
    s += text[ini:]
    return s
        
def colorear(text):
    """
    Procesa el texto en *text* buscando los códigos de colores y generando
    el HTML necesario. Devuelve el texto procesado.
    """
    s = ""
    ini = 0
    pos = text.find("[#")
    while pos != -1:
        s += text[ini:pos]
        fincolor = text.find(" ", pos)
        color = text[pos + 2:fincolor]
        s += '<span style="color: ' + color + '">'
        fincorchete = text.find("]", fincolor)
        s += text[fincolor + 1:fincorchete]
        s += "</span>"
        ini = fincorchete + 1
        pos = text.find("[#", ini)
    s += text[ini:]
    return s

def procesar(html, latin=True):
    """
    Aplica todos los post-procesos al texto contenido en *html*. Si *latin*
    es True (por defecto) hace la conversión de caracteres latinos.
    Devuelve el texto procesado.
    """
    s = markdown.markdown(html)
    #markdown devuelve una cadena en Unicode, la transformo a string normal
    s = s.encode("iso-8859-1")
    s = target_blank(s)
    s = alinear_imagenes(s)
    s = colorear(s)
    if latin:
        #cambiar todos los acentos por códigos HTML
        s = escape_latin(s)
    return s

if __name__ == "__main__":
    usage = u"""jmd: Post-procesador personalizado para Markdown.

Uso:
python jmd.py archivo.markdown > archivo.htm
El archivo de entrada debe estar codificado en UTF-8. Si se pasa la
opción -n después del archivo, no se hace la conversión de caracteres
latinos."""

    import sys
    if sys.argv[1:]:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            #mostrar ayuda larga:
            print help_string
        else:
            try:
                input_file = codecs.open(sys.argv[1], mode="r", encoding="utf-8")
                text = input_file.read()
                text = text.lstrip('\ufeff') # remove the byte-order mark
                if sys.argv[2:] and sys.argv[2] == "-n":
                    latin = False
                else:
                    latin = True
                print procesar(text, latin)
                input_file.close()
            except UnicodeDecodeError:
                print u"Error: El archivo de entrada debe estar en Unicode (UTF-8)."
            except:
                print u"Error: No se pudo abrir el archivo u opción inválida."
    else:
        print usage
