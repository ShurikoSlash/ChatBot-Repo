import csv
import os

ARCHIVO_EMPLEADOS = "vacacionesDB.csv"
ARCHIVO_SOLICITUDES = "solicitudes_log.csv"

DIAS_POR_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def fecha_es_valida(dia, mes, anio):
    if mes < 1 or mes > 12:
        return False

    if dia < 1 or dia > DIAS_POR_MES[mes - 1]:
        return False

    if anio < 1900 or anio > 2100:
        return False

    return True


def pedir_fecha(mensaje):
    texto = input(mensaje + " (DD/MM/AAAA): ").strip()
    partes = texto.split("/")

    if len(partes) != 3:
        return None

    dia_texto, mes_texto, anio_texto = partes

    if not (
        dia_texto.isdigit()
        and mes_texto.isdigit()
        and anio_texto.isdigit()
    ):
        return None

    dia = int(dia_texto)
    mes = int(mes_texto)
    anio = int(anio_texto)

    if not fecha_es_valida(dia, mes, anio):
        return None

    return [dia, mes, anio]


def fecha_a_numero(fecha):
    dia, mes, anio = fecha

    dias_de_meses_anteriores = 0

    for i in range(mes - 1):
        dias_de_meses_anteriores += DIAS_POR_MES[i]

    return anio * 366 + dias_de_meses_anteriores + dia


def fecha_a_texto(fecha):
    return str(fecha[0]) + "/" + str(fecha[1]) + "/" + str(fecha[2])


def cargar_empleados():
    empleados = []

    with open(
        ARCHIVO_EMPLEADOS,
        "r",
        newline="",
        encoding="utf-8"
    ) as archivo:

        lector = csv.reader(archivo)

        primera_fila = True

        for fila in lector:

            if primera_fila:
                primera_fila = False
                continue

            empleados.append([
                fila[0],
                fila[1],
                int(fila[2])
            ])

    return empleados


def guardar_empleados(empleados):

    with open(
        ARCHIVO_EMPLEADOS,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow([
            "legajo",
            "nombre",
            "dias_disponibles"
        ])

        for fila in empleados:
            escritor.writerow(fila)


def buscar_empleado(empleados, legajo):

    for fila in empleados:

        if fila[0] == legajo:
            return fila

    return None


def registrar_solicitud(
    legajo,
    nombre,
    fecha_inicio,
    fecha_fin,
    dias,
    estado
):

    archivo_existe = os.path.exists(
        ARCHIVO_SOLICITUDES
    )

    with open(
        ARCHIVO_SOLICITUDES,
        "a",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.writer(archivo)

        if not archivo_existe:
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


def proceso_vacaciones(empleados):

    print("\nChat Bot: Iniciando solicitud de vacaciones...")

    legajo = input(
        "Ingresá tu número de legajo: "
    ).strip()

    empleado = buscar_empleado(
        empleados,
        legajo
    )

    if empleado is None:
        print(
            "Chat Bot: No encontramos ese legajo. "
            "Te derivamos a RR.HH."
        )
        return

    nombre = empleado[1]
    saldo = empleado[2]

    print(
        "Chat Bot: ¡Hola, "
        + nombre
        + "! Tenés "
        + str(saldo)
        + " día(s) disponible(s)."
    )

    fecha_inicio = pedir_fecha(
        "Fecha de inicio"
    )

    if fecha_inicio is None:
        print(
            "Chat Bot: Esa fecha de inicio no es válida."
        )
        return

    fecha_fin = pedir_fecha(
        "Fecha de fin"
    )

    if fecha_fin is None:
        print(
            "Chat Bot: Esa fecha de fin no es válida."
        )
        return

    numero_inicio = fecha_a_numero(
        fecha_inicio
    )

    numero_fin = fecha_a_numero(
        fecha_fin
    )

    if numero_fin < numero_inicio:
        print(
            "Chat Bot: La fecha de fin no puede "
            "ser anterior a la de inicio."
        )
        return

    dias_solicitados = (
        numero_fin - numero_inicio + 1
    )

    if dias_solicitados > saldo:

        print(
            "Chat Bot: Pediste "
            + str(dias_solicitados)
            + " día(s) pero solo tenés "
            + str(saldo)
            + ". Solicitud RECHAZADA."
        )

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

    print("\nChat Bot: Solicitud APROBADA y registrada:")
    print(
        "- Empleado: "
        + nombre
        + " (legajo "
        + legajo
        + ")"
    )
    print(
        "- Desde: "
        + fecha_a_texto(fecha_inicio)
    )
    print(
        "- Hasta: "
        + fecha_a_texto(fecha_fin)
    )
    print(
        "- Días tomados: "
        + str(dias_solicitados)
    )
    print(
        "- Saldo restante: "
        + str(empleado[2])
    )


def main():

    print(
        "¡Bienvenido al Chat Bot de Vacaciones!"
    )

    empleados = cargar_empleados()

    while True:

        print(
            "\nEscribe 'vacaciones' o 'salir'"
        )

        user_input = input(
            "Tú: "
        ).lower().strip()

        if user_input in [
            "salir",
            "chau",
            "adiós",
            "adios"
        ]:

            print(
                "Chat Bot: Hasta luego."
            )

            break

        elif "vacaciones" in user_input:

            proceso_vacaciones(
                empleados
            )

        else:

            print(
                "Chat Bot: No entendí el comando."
            )


if __name__ == "__main__":
    main()