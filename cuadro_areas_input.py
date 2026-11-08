precio_m2 = float(input("Costo por m² ($): "))

# Capturamos los espacios uno por uno
espacios = []
while True:
    nombre = input("Nombre del espacio (Enter para terminar): ")
    if nombre == "":
        break
    largo = float(input("  Largo (m): "))
    ancho = float(input("  Ancho (m): "))
    espacios.append((nombre, largo, ancho))

if not espacios:
    print("No capturaste ningún espacio.")
    exit()

# Calculamos el total
total = 0
for nombre, largo, ancho in espacios:
    total += largo * ancho

# Imprimimos la tabla
print()
print(f"{'Espacio':<15}{'Largo':>8}{'Ancho':>8}{'Área m²':>10}{'%':>8}{'Costo $':>14}")
for nombre, largo, ancho in espacios:
    area = largo * ancho
    porcentaje = area / total * 100
    costo = area * precio_m2
    print(f"{nombre:<15}{largo:>8.2f}{ancho:>8.2f}{area:>10.2f}{porcentaje:>7.1f}%{costo:>14,.2f}")
print(f"{'TOTAL':<15}{'':>16}{total:>10.2f}{100:>7.1f}%{total * precio_m2:>14,.2f}")
import csv

with open("cuadro_areas.csv", "w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Espacio", "Largo", "Ancho", "Area m2", "Porcentaje", "Costo"])
    for nombre, largo, ancho in espacios:
        area = largo * ancho
        escritor.writerow([nombre, largo, ancho, round(area, 2), round(area / total * 100, 1), round(area * precio_m2, 2)])
    escritor.writerow(["TOTAL", "", "", round(total, 2), 100, round(total * precio_m2, 2)])

print("Guardado en cuadro_areas.csv")