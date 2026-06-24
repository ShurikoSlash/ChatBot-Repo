import csv
import os

ARCHIVO_EMPLEADOS = "vacacionesDB.csv"
ARCHIVO_SOLICITUDES = "solicitudes_log.csv"

DIAS_POR_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DIAS_INICIALES = 14


def fecha_es_valida(dia, mes, anio):
    return 1 <= mes <= 12 and 1 <= dia <= DIAS_POR_MES[mes - 1] and 1900 <= anio <= 2100


def pedir_fecha(mensaje):
    texto = input(mensaje + " (DD/MM/AAAA): ").strip()
    partes = texto.split("/")

    if len(partes) != 3:
        return None

    if not all(p.isdigit() for p in partes):
        return None

    dia, mes, anio = map(int, partes)

    if not fecha_es_valida(dia, mes, anio):
        return None

    return [dia, mes, anio]


def fecha_a_numero(fecha):
    dia, mes, anio = fecha
    return anio * 366 + sum(DIAS_POR_MES[:mes - 1]) + dia


def fecha_a_texto(fecha):
    return f"{fecha[0]}/{fecha[1]}/{fecha[2]}"


def cargar_empleados():
    empleados = []

    with open(ARCHIVO_EMPLEADOS, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)

        for fila in lector:
            empleados.append([fila[0], fila[1], int(fila[2])])

    return empleados


def guardar_empleados(empleados):
    with open(ARCHIVO_EMPLEADOS, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["legajo", "nombre", "dias_disponibles"])

        for empleado in empleados:
            escritor.writerow(empleado)


def buscar_empleado_por_nombre(empleados, nombre):
    for empleado in empleados:
        if empleado[1].lower() == nombre.lower():
            return empleado

    return None


def generar_nuevo_legajo(empleados):
    mayor = 1000

    for empleado in empleados:
        numero = int(empleado[0])

        if numero > mayor:
            mayor = numero

    return str(mayor + 1)


def registrar_solicitud(legajo, nombre, fecha_inicio,
                         fecha_fin, dias, estado):

    existe = os.path.exists(ARCHIVO_SOLICITUDES)

    with open(ARCHIVO_SOLICITUDES, "a",
              newline="", encoding="utf-8") as archivo:

        escritor = csv.writer(archivo)

        if not existe:
            escritor.writerow([
                "legajo",
                "nombre",
                "fecha_inicio",
                "fecha_fin",
                "dias_solicitados",
                "estado"
            ])

        escritor.writerow([
            legajo,
            nombre,
            fecha_a_texto(fecha_inicio),
            fecha_a_texto(fecha_fin),
            dias,
            estado
        ])


def proceso_registro(empleados):

    print("\nChat Bot: Vamos a registrarte en el sistema.")

    nombre_ingresado = input("Ingresá tu nombre completo: ").strip()

    if nombre_ingresado == "":
        print("Chat Bot: El nombre no puede estar vacío.")
        return

    empleado_existente = buscar_empleado_por_nombre(empleados, nombre_ingresado)

    if empleado_existente is not None:
        print("\nChat Bot: Ya existe un registro con ese nombre.")
        print(f"Legajo: {empleado_existente[0]}")
        print(f"Días disponibles: {empleado_existente[2]}")
        return

    nuevo_legajo = generar_nuevo_legajo(empleados)

    nuevo_empleado = [nuevo_legajo, nombre_ingresado, DIAS_INICIALES]

    empleados.append(nuevo_empleado)
    guardar_empleados(empleados)

    print("\nChat Bot: ¡Registro exitoso!")
    print(f"Nombre: {nombre_ingresado}")
    print(f"Legajo asignado: {nuevo_legajo}")
    print(f"Días disponibles: {DIAS_INICIALES}")


def proceso_vacaciones(empleados):

    print("\nChat Bot: Iniciando solicitud de vacaciones...")

    nombre_ingresado = input("Ingresá tu nombre completo: ").strip()

    if nombre_ingresado == "":
        print("Chat Bot: El nombre no puede estar vacío.")
        return

    empleado = buscar_empleado_por_nombre(empleados, nombre_ingresado)

    if empleado is None:
        print("Chat Bot: No encontramos tu nombre en el sistema.")
        print("Chat Bot: Por favor, registrate primero usando la opción 1.")
        return

    legajo = empleado[0]
    nombre = empleado[1]
    saldo = empleado[2]

    print(f"\nChat Bot: Bienvenido {nombre}")
    print(f"Tu número de legajo es: {legajo}")
    print(f"Disponés de {saldo} día(s) de vacaciones.")

    fecha_inicio = pedir_fecha("Fecha de inicio")

    if fecha_inicio is None:
        print("Chat Bot: La fecha ingresada no es válida.")
        return

    fecha_fin = pedir_fecha("Fecha de fin")

    if fecha_fin is None:
        print("Chat Bot: La fecha ingresada no es válida.")
        return

    numero_inicio = fecha_a_numero(fecha_inicio)
    numero_fin = fecha_a_numero(fecha_fin)

    if numero_fin < numero_inicio:
        print("Chat Bot: La fecha de fin no puede ser anterior a la fecha de inicio.")
        return

    dias_solicitados = numero_fin - numero_inicio + 1

    if dias_solicitados > saldo:

        print("\nChat Bot: Solicitud RECHAZADA.")
        print(f"Solicitaste {dias_solicitados} día(s) y solo disponés de {saldo}.")

        registrar_solicitud(
            legajo,
            nombre,
            fecha_inicio,
            fecha_fin,
            dias_solicitados,
            "Rechazada"
        )

        return

    empleado[2] = saldo - dias_solicitados

    guardar_empleados(empleados)

    registrar_solicitud(
        legajo,
        nombre,
        fecha_inicio,
        fecha_fin,
        dias_solicitados,
        "Aprobada"
    )

    print("\nChat Bot: Solicitud APROBADA.")
    print(f"Empleado: {nombre}")
    print(f"Legajo: {legajo}")
    print(f"Desde: {fecha_a_texto(fecha_inicio)}")
    print(f"Hasta: {fecha_a_texto(fecha_fin)}")
    print(f"Días solicitados: {dias_solicitados}")
    print(f"Saldo restante: {empleado[2]}")


def main():

    print("Bienvenido al Chat Bot de Solicitud de Vacaciones")

    empleados = cargar_empleados()

    while True:

        print("\nOpciones:")
        print("1. Registrarse")
        print("2. Pedir vacaciones")
        print("3. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            proceso_registro(empleados)

        elif opcion == "2":
            proceso_vacaciones(empleados)

        elif opcion == "3":
            print("Chat Bot: ¡Hasta luego!")
            break

        else:
            print("Chat Bot: Opción inválida. Ingresá 1, 2 o 3.")


if __name__ == "__main__":
    main()
