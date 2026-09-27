def filtrar_reservas(
    rows,
    fecha_desde=None,
    fecha_hasta=None,
    estado=None,
    metodo_pago=None
):
    filtradas = []

    for row in rows:

        # Índices según el orden de las columnas de Reservas
        fecha_creacion = row[1]
        metodo = row[11]
        estado_actual = row[12]

        # Filtro por fecha
        if fecha_desde:
            if str(fecha_creacion) < fecha_desde:
                continue

        if fecha_hasta:
            if str(fecha_creacion) > fecha_hasta:
                continue

        # Filtro por estado
        if estado and estado != "Todos":
            if str(estado_actual) != estado:
                continue

        # Filtro por método de pago
        if metodo_pago and metodo_pago != "Todos":
            if str(metodo) != metodo_pago:
                continue

        filtradas.append(row)

    return filtradas

def filtrar_clientes(
    rows,
    nacionalidad=None,
    nivel_fidelizacion=None
):
    filtradas = []

    for row in rows:

        # Índices según el orden de las columnas de Reservas
        metodo = row[5]
        estado_actual = row[10]

        # Filtro por nacionalidad
        if nacionalidad and nacionalidad != "Todos":
            if str(estado_actual) != nacionalidad:
                continue

        # Filtro por método de pago
        if nivel_fidelizacion and nivel_fidelizacion != "Todos":
            if str(metodo) != nivel_fidelizacion:
                continue

        filtradas.append(row)

    return filtradas