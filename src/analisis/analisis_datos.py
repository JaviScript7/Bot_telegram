import matplotlib.pyplot as plt
from datetime import datetime

def crear_grafico(result,dia):
    resultados = result
    print(resultados)

    tipos_equipos_completos = ['PC', 'Movil', 'Tablet','Laptop']
    # Crear un diccionario con valores iniciales en 0
    equipos_dict = {equipo: 0 for equipo in tipos_equipos_completos}

    # Actualizar el diccionario con los resultados de la consulta
    for fila in resultados:
        equipo = fila[0]  # El tipo de equipo ('Movil', 'PC', etc.)
        cantidad = fila[1]  # La cantidad de reparaciones para ese equipo
        equipos_dict[equipo] = cantidad

    # Procesar los resultados
    tipos_equipos = list(equipos_dict.keys())
    cantidades = list(equipos_dict.values())

    # Crear gráfico de barras
    #plt.figure(figsize=(10,6))
    #plt.bar(tipos_equipos, cantidades, color=['blue', 'green', 'red'])
    #plt.xlabel('Tipo de Equipo')
    #plt.ylabel('Cantidad de Reparaciones')
    #plt.title(f'Reparaciones por Tipo de Equipo - {dia}')
    #plt.tight_layout()

    # Crear gráfico de líneas con marcadores
    plt.figure(figsize=(10,6))
    plt.plot(tipos_equipos, cantidades, marker='o', linestyle='-', color='blue')
    plt.xlabel('Tipo de Equipo')
    plt.ylabel('Cantidad de Reparaciones')
    plt.title(f'Reparaciones por Tipo de Equipo - {dia}')
    plt.tight_layout()

    # Ajustar los ticks del eje Y para que vayan de 1 en 1
    plt.yticks(range(0, max(cantidades) + 1, 1))
    plt.ylim(0, max(5, max(cantidades)))

    # Guardar el gráfico como imagen
    plt.savefig('analisis/reparaciones_diarias.png')
    return ["reparaciones_diarias",dia]

