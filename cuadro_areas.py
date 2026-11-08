precio_m2 = 12000

espacios = [
    ("Sala", 5.0, 4.0),
    ("Comedor", 3.5, 3.0),
    ("Cocina", 3.0, 3.0),
    ("Recámara 1", 4.0, 3.5),
    ("Baño", 2.0, 1.8),
]

total = 0
for nombre, largo, ancho in espacios:
    total += largo * ancho

# 2. Imprimimos la tabla con porcentaje y costo
print(f"{'Espacio':<15}{'Largo':>8}{'Ancho':>8}{'Área m²':>10}{'%':>8}{'Costo $':>14}")
for nombre, largo, ancho in espacios:
    area = largo * ancho
    porcentaje = area / total * 100
    costo = area * precio_m2
    print(f"{nombre:<15}{largo:>8.2f}{ancho:>8.2f}{area:>10.2f}{porcentaje:>7.1f}%{costo:>14,.2f}")
print(f"{'TOTAL':<15}{'':>16}{total:>10.2f}{100:>7.1f}%{total * precio_m2:>14,.2f}")