import csv

precio_m2 = 8000

# Leemos los espacios desde el archivo
espacios = []
with open("espacios.csv", encoding="utf-8-sig") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        espacios.append((fila["Espacio"], float(fila["Largo"]), float(fila["Ancho"])))

# Calculamos el total
total = 0
for nombre, largo, ancho in espacios:
    total += largo * ancho

# Imprimimos la tabla
print(f"{'Espacio':<15}{'Largo':>8}{'Ancho':>8}{'Área m²':>10}{'%':>8}{'Costo $':>14}")
for nombre, largo, ancho in espacios:
    area = largo * ancho
    porcentaje = area / total * 100
    costo = area * precio_m2
    print(f"{nombre:<15}{largo:>8.2f}{ancho:>8.2f}{area:>10.2f}{porcentaje:>7.1f}%{costo:>14,.2f}")
print(f"{'TOTAL':<15}{'':>16}{total:>10.2f}{100:>7.1f}%{total * precio_m2:>14,.2f}")
