"""Filtros utilizados por las ventanas de exportación."""

from datetime import datetime


def _texto(valor):
    return "" if valor is None else str(valor).strip()


def _fecha_valida(valor):
    """Devuelve una fecha comparable cuando el valor tiene formato YYYY-MM-DD."""
    if valor is None or valor == "":
        return None

    if hasattr(valor, "strftime"):
        return valor.strftime("%Y-%m-%d")

    texto = _texto(valor)
    try:
        return datetime.strptime(texto[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None


def _en_rango_fecha(valor, fecha_desde=None, fecha_hasta=None):
    fecha = _fecha_valida(valor)

    # Un valor sin fecha no puede satisfacer un filtro de fechas.
    if fecha is None:
        return not (fecha_desde or fecha_hasta)

    if fecha_desde and fecha < fecha_desde:
        return False
    if fecha_hasta and fecha > fecha_hasta:
        return False

    return True


def _en_rango_numero(valor, minimo=None, maximo=None):
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return False if (minimo is not None or maximo is not None) else True

    if minimo not in (None, "") and numero < float(minimo):
        return False
    if maximo not in (None, "") and numero > float(maximo):
        return False

    return True


def filtrar_reservas(
    rows,
    fecha_desde=None,
    fecha_hasta=None,
    estado=None,
    metodo_pago=None
):
    filtradas = []

    for row in rows:
        fecha_creacion = row[1]
        metodo = row[11]
        estado_actual = row[12]

        if not _en_rango_fecha(fecha_creacion, fecha_desde, fecha_hasta):
            continue

        if estado and estado != "Todos" and _texto(estado_actual) != estado:
            continue

        if metodo_pago and metodo_pago != "Todos" and _texto(metodo) != metodo_pago:
            continue

        filtradas.append(row)

    return filtradas


def filtrar_clientes(
    rows,
    fecha_desde=None,
    fecha_hasta=None,
    nacionalidad=None,
    nivel_fidelizacion=None
):
    """Filtra clientes por fecha de nacimiento, nacionalidad y fidelización."""
    filtradas = []

    for row in rows:
        # ID, nombre, apellido, documento, nacionalidad, fecha_nacimiento, ...
        fecha_nacimiento = row[5]
        nacionalidad_actual = row[4]
        nivel_actual = row[9]

        if not _en_rango_fecha(fecha_nacimiento, fecha_desde, fecha_hasta):
            continue

        if nacionalidad and nacionalidad != "Todos":
            if _texto(nacionalidad_actual) != nacionalidad:
                continue

        if nivel_fidelizacion and nivel_fidelizacion != "Todos":
            if _texto(nivel_actual) != nivel_fidelizacion:
                continue

        filtradas.append(row)

    return filtradas


def filtrar_habitaciones(
    rows,
    estado=None,
    ID_tipo=None,
    ID_hotel=None,
    tarifa_desde=None,
    tarifa_hasta=None
):
    """Filtra habitaciones por estado, tipo, hotel y rango de tarifa base."""
    filtradas = []

    for row in rows:
        # ID, numero, piso, ID_tipo, orientacion, estado, tarifa_base, ID_hotel
        tipo_actual = row[3]
        estado_actual = row[5]
        tarifa_actual = row[6]
        hotel_actual = row[7]

        if estado and estado != "Todos" and _texto(estado_actual) != estado:
            continue

        if ID_tipo not in (None, "", "Todos") and _texto(tipo_actual) != _texto(ID_tipo):
            continue

        if ID_hotel not in (None, "", "Todos") and _texto(hotel_actual) != _texto(ID_hotel):
            continue

        if not _en_rango_numero(tarifa_actual, tarifa_desde, tarifa_hasta):
            continue

        filtradas.append(row)

    return filtradas


def detectar_indice_fecha_tarifa(rows):
    """Busca una columna de fecha adicional en los datos de tarifas.

    El proyecto actual devuelve 6 columnas desde sp_GetAllTarifas. Si en una
    versión de la BD el procedimiento devuelve una fecha adicional, esta
    función permite encontrarla sin cambiar el resto del filtro.
    """
    if not rows:
        return None

    max_columnas = max(len(row) for row in rows)
    for indice in range(6, max_columnas):
        valores = [row[indice] for row in rows if len(row) > indice]
        if valores and sum(_fecha_valida(v) is not None for v in valores) == len(valores):
            return indice

    return None


def filtrar_tarifas(
    rows,
    fecha_desde=None,
    fecha_hasta=None,
    ID_tipo=None,
    precio_desde=None,
    precio_hasta=None,
    fecha_index=None
):
    """Filtra tarifas por fecha, tipo de habitación y rango de precio.

    La fecha solo puede aplicarse si sp_GetAllTarifas devuelve una columna de
    fecha. fecha_index permite indicarla explícitamente o detectarla con
    detectar_indice_fecha_tarifa().
    """
    filtradas = []

    for row in rows:
        tipo_actual = row[1]
        precio_actual = row[2]

        if ID_tipo not in (None, "", "Todos") and _texto(tipo_actual) != _texto(ID_tipo):
            continue

        if not _en_rango_numero(precio_actual, precio_desde, precio_hasta):
            continue

        if fecha_desde or fecha_hasta:
            if fecha_index is None or len(row) <= fecha_index:
                # El controlador se encarga de informar al usuario de que
                # la BD no proporciona una fecha para este módulo.
                continue
            if not _en_rango_fecha(row[fecha_index], fecha_desde, fecha_hasta):
                continue

        filtradas.append(row)

    return filtradas
