import csv
import ezdxf

ARCHIVO = "plano_ejecutivo.dxf"
CAPA = "ESPACIOS"
precio_m2 = 8000
CAPA_CONTORNO = "CONTORNOS"


def punto_dentro(x, y, puntos):
    """Dice si el punto (x, y) está dentro del polígono."""
    dentro = False
    n = len(puntos)
    for i in range(n):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_cruce = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_cruce:
                dentro = not dentro
    return dentro


def area_poligono(puntos):
    suma = 0
    for i in range(len(puntos)):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % len(puntos)]
        suma += x1 * y2 - x2 * y1
    return abs(suma) / 2


doc = ezdxf.readfile(ARCHIVO)
msp = doc.modelspace()
# Detectamos las unidades con las que está guardado el plano
FACTORES = {1: 0.0254, 2: 0.3048, 4: 0.001, 5: 0.01, 6: 1}   # pulgadas, pies, mm, cm, m
codigo = doc.header.get("$INSUNITS", 0)
if codigo not in FACTORES:
    print("El plano no tiene unidades definidas (o no reconozco las que tiene).")
    print("En AutoCAD escribe UNITS, elige las unidades de inserción y guarda de nuevo el DXF.")
    exit()
UNIDAD_A_METROS = FACTORES[codigo]
print(f"Unidades detectadas: código {codigo} (factor a metros: {UNIDAD_A_METROS})")
# 1. Juntamos los textos del plano (sin saltos de línea)
textos = []
for e in msp.query("TEXT"):
    textos.append((" ".join(e.dxf.text.split()), e.dxf.insert.x, e.dxf.insert.y))
for e in msp.query("MTEXT"):
    textos.append((" ".join(e.plain_text().split()), e.dxf.insert.x, e.dxf.insert.y))

# 2. Leemos todos los polígonos de la capa
poligonos = []
for entidad in msp.query("LWPOLYLINE"):
    if entidad.dxf.layer != CAPA or not entidad.closed:
        continue
    puntos = [(p[0], p[1]) for p in entidad.get_points("xy")]
    area = area_poligono(puntos) * UNIDAD_A_METROS ** 2
    poligonos.append({"puntos": puntos, "area": area, "nombre": None})

# 3. Cada texto se asigna al polígono MÁS CHICO que lo contiene
IGNORAR = {"NPT"}   # marcas que no son nombres de espacio
fuera = 0
for texto, x, y in textos:
    if not texto or texto in IGNORAR or texto.startswith(("+", "-")):
        continue
    candidatos = [p for p in poligonos if punto_dentro(x, y, p["puntos"])]
    if not candidatos:
        fuera += 1
        continue
    elegido = min(candidatos, key=lambda p: p["area"])
    if elegido["nombre"] is None:
        elegido["nombre"] = texto
    else:
        print(f"Aviso: el texto '{texto}' cae en '{elegido['nombre']}' y no se usó")
print(f"Textos fuera de los espacios (cotas, ejes, accesos, etc.): {fuera}")

espacios = [(p["nombre"], p["area"]) for p in poligonos if p["nombre"]]
ignorados = len(poligonos) - len(espacios)
print(f"Polígonos leídos: {len(poligonos)} | con nombre: {len(espacios)} | sin nombre (ignorados): {ignorados}")

if not espacios:
    print("Ningún polígono tiene texto adentro.")
    exit()

total = sum(area for nombre, area in espacios)
# Contorno exterior, para comparar contra la suma de espacios
area_contorno = None
for entidad in msp.query("LWPOLYLINE"):
    if entidad.dxf.layer == CAPA_CONTORNO and entidad.closed:
        puntos = [(p[0], p[1]) for p in entidad.get_points("xy")]
        area = area_poligono(puntos) * UNIDAD_A_METROS ** 2
        if area_contorno is None or area > area_contorno:
            area_contorno = area
# 3. Tabla en pantalla
print(f"{'Espacio':<15}{'Área m²':>10}{'%':>8}{'Costo $':>14}")
for nombre, area in espacios:
    print(f"{nombre:<15}{area:>10.2f}{area / total * 100:>7.1f}%{area * precio_m2:>14,.2f}")
print(f"{'TOTAL':<15}{total:>10.2f}{100:>7.1f}%{total * precio_m2:>14,.2f}")
if area_contorno is not None:
    diferencia = area_contorno - total
    print(f"\nContorno: {area_contorno:.2f} m² | Suma de espacios: {total:.2f} m² | Diferencia: {diferencia:.2f} m² ({diferencia / area_contorno * 100:.1f} %)")
    print("La diferencia corresponde a muros, huecos y espacios sin nombre.")
else:
    print(f"\nNo encontré una polilínea cerrada en la capa {CAPA_CONTORNO}.")
# 4. Guardamos en CSV
with open("areas_dxf.csv", "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Espacio", "Area m2", "Porcentaje", "Costo"])
    for nombre, area in espacios:
        escritor.writerow([nombre, round(area, 2), round(area / total * 100, 1), round(area * precio_m2, 2)])
    escritor.writerow(["TOTAL", round(total, 2), 100, round(total * precio_m2, 2)])

print("Guardado en areas_dxf.csv")