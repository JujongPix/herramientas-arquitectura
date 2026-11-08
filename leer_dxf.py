import ezdxf
import csv
ARCHIVO = "plano.dxf"
CAPA = "ESPACIOS"
UNIDAD_A_METROS = 1  
precio_m2 = 8000

doc = ezdxf.readfile(ARCHIVO)
msp = doc.modelspace()

areas = []
for entidad in msp.query("LWPOLYLINE"):
    if entidad.dxf.layer != CAPA or not entidad.closed:
        continue
    puntos = [(p[0], p[1]) for p in entidad.get_points("xy")]
    # Fórmula del zapatero (shoelace) para el área de un polígono
    suma = 0
    for i in range(len(puntos)):
        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % len(puntos)]
        suma += x1 * y2 - x2 * y1
    areas.append(abs(suma) / 2 * UNIDAD_A_METROS ** 2)

if not areas:
    print(f"No encontré polilíneas cerradas en la capa {CAPA}.")
    exit()

total = sum(areas)
print(f"{'Espacio':<15}{'Área m²':>10}{'%':>8}{'Costo $':>14}")
for i, area in enumerate(areas, start=1):
    print(f"{'Espacio ' + str(i):<15}{area:>10.2f}{area / total * 100:>7.1f}%{area * precio_m2:>14,.2f}")
print(f"{'TOTAL':<15}{total:>10.2f}{100:>7.1f}%{total * precio_m2:>14,.2f}")
with open("areas_dxf.csv", "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Espacio", "Area m2", "Porcentaje", "Costo"])
    for i, area in enumerate(areas, start=1):
        escritor.writerow([f"Espacio {i}", round(area, 2), round(area / total * 100, 1), round(area * precio_m2, 2)])
    escritor.writerow(["TOTAL", round(total, 2), 100, round(total * precio_m2, 2)])

print("Guardado en areas_dxf.csv")