from models.database import DatabaseConnector


class HabitacionModel:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    def get_all(self):
        return self.db.call_procedure('sp_GetAllHabitaciones')

    def get_by_id(self, ID_habitacion: int):
        return self.db.call_procedure(
            'sp_GetHabitacion',
            (ID_habitacion,)
        )

    def get_tipos_habitacion(self):
        return self.db.call_procedure(
            'sp_GetAllTiposHabitacion'
        )

    def get_hoteles(self):
        return self.db.call_procedure(
            'sp_GetAllHoteles'
        )

    def insert(
        self,
        numero_habitacion,
        piso,
        ID_tipo,
        orientacion,
        estado,
        tarifa_base,
        ID_hotel,
        imagen

    ):
        return self.db.call_procedure(
            'sp_InsertHabitacion',
            (
                numero_habitacion,
                piso,
                ID_tipo,
                orientacion,
                estado,
                tarifa_base,
                ID_hotel,
                imagen
            )
        )

    def update(
        self,
        ID_habitacion,
        numero_habitacion,
        piso,
        ID_tipo,
        orientacion,
        estado,
        tarifa_base,
        ID_hotel,
        imagen
    ):
        return self.db.call_procedure(
            'sp_UpdateHabitacion',
            (
                ID_habitacion,
                numero_habitacion,
                piso,
                ID_tipo,
                orientacion,
                estado,
                tarifa_base,
                ID_hotel,
                imagen
            )
        )

    def delete(self, ID_habitacion: int):
        return self.db.call_procedure(
            'sp_DeleteHabitacion',
            (ID_habitacion,)
        )