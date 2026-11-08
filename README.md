# Herramientas de automatización para arquitectura

Scripts en Python para calcular cuadros de áreas y costos a partir de
archivos DXF de AutoCAD.

## Qué hace
- Lee polilíneas cerradas de una capa (por defecto "ESPACIOS").
- Toma el nombre de cada espacio del texto que está dentro.
- Calcula área, porcentaje y costo, y guarda el resultado en CSV.
- Detecta las unidades del plano y avisa si no están definidas.

## Uso
py leer_dxf_nombres.py

Requiere Python 3 y la librería ezdxf (py -m pip install ezdxf).
