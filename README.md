# Herramientas de automatización para arquitectura

Scripts en Python que calculan cuadros de áreas y costos a partir de planos
DXF de AutoCAD. Leen los espacios del dibujo, toman su nombre del texto que
tienen adentro, y comparan la suma contra el contorno exterior para detectar
errores.

## Qué hace `leer_dxf_nombres.py`
- Lee las polilíneas cerradas de la capa `ESPACIOS`.
- Asigna a cada espacio el texto que está dentro (si hay varios espacios
  anidados, usa el más pequeño).
- Calcula área, porcentaje y costo por espacio (precio por m² configurable).
- Compara la suma de espacios contra la polilínea de la capa `CONTORNO`.
- Detecta las unidades del plano y se detiene si no están definidas.
- Guarda el resultado en `areas_dxf.csv`, listo para abrir en Excel.

## Cómo preparar el plano en AutoCAD
1. Crea una capa `ESPACIOS` y dibuja en ella una **polilínea cerrada** por
   cada espacio (por ejemplo con `BOUNDARY`). Si usas `PLINE`, termina el
   comando con la opción **Cerrar** (`C`).
2. Escribe el nombre de cada espacio con `TEXT` o `MTEXT`, de modo que el
   punto de inserción quede **dentro** del contorno.
3. (Opcional) Dibuja el contorno exterior en una capa `CONTORNO`
   como polilínea cerrada.
4. Revisa las unidades con el comando `UNITS` (escala de inserción).
5. Guarda como **AutoCAD DXF** en la misma carpeta que el script.

## Uso
```
py -m pip install ezdxf
py leer_dxf_nombres.py
```
Antes de ejecutar, ajusta al inicio del script:
- `ARCHIVO`: nombre del DXF.
- `CAPA` y `CAPA_CONTORNO`: nombres de las capas.
- `precio_m2`: costo por metro cuadrado (el valor incluido es solo un ejemplo).
- `IGNORAR`: textos que no son nombres de espacio (por ejemplo, marcas de nivel).

## Ejemplo de salida (datos de prueba)
```
Unidades detectadas: código 6 (factor a metros: 1)
Textos fuera de los espacios (cotas, ejes, accesos, etc.): 12
Polígonos leídos: 3 | con nombre: 3 | sin nombre (ignorados): 0
Espacio           Área m²       %       Costo $
SALA                22.02    49.1%    176,160.00
COMEDOR             12.65    28.2%    101,200.00
REC. 1              10.17    22.7%     81,360.00
TOTAL               44.84   100.0%    358,720.00

Contorno: 47.00 m² | Suma de espacios: 44.84 m² | Diferencia: 2.16 m² (4.6 %)
```

## Limitaciones
- Las áreas son **netas** (interior de cada espacio), no área construida.
- Solo lee polilíneas cerradas con lados rectos; los arcos no se consideran.
- El nombre se toma por la posición del punto de inserción del texto.
- Un polígono sin texto adentro se ignora, y el programa lo avisa.
- Requiere que el plano tenga unidades definidas.
- Probado con planos de prueba y con una planta real de oficinas.

## Requisitos
Python 3 y la librería [ezdxf](https://ezdxf.mozman.at/).