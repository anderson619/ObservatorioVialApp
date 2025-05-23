import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    def __init__(self, host, user, password, database):
        """Inicializa la conexión a la base de datos"""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.conn.is_connected():
                print("✅ Conexión a la base de datos establecida.")
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            self.conn = None

    def get_or_create_vehicle(self, tipo, color, modelo, marca, tipo_servicio, camara_id, zona_id, identificador):
        if not self.conn:
            print("❌ No hay conexión con la base de datos.")
            return None

        cursor = self.conn.cursor()

        # Validar por identificador único
        query = """
            SELECT CamaraSeguridad_id_CamaraSeguridad
            FROM vehiculo
            WHERE identificador_unico = %s
        """
        cursor.execute(query, (identificador,))
        result = cursor.fetchone()

        if result:
            return result[0]

    # Insertar nuevo
        insert_query = """
            INSERT INTO vehiculo (
                Tipo, Color, Modelo, Marca, TipoServicio,
                CamaraSeguridad_id_CamaraSeguridad,
                CamaraSeguridad_ZonaCritica_id_ZonaCritica,
                identificador_unico
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            tipo, color, modelo, marca, tipo_servicio,
            camara_id, zona_id, identificador
        ))
        self.conn.commit()

        return cursor.lastrowid


    def insert_tracking(self, vehiculo_id, coordenadas, frame_path, velocidad, fecha, hora):
        """
        Inserta un nuevo registro en la tabla seguimientovehiculo.
        """
        if not self.conn:
            print("❌ No hay conexión con la base de datos.")
            return

        cursor = self.conn.cursor()
        insert_query = """
            INSERT INTO seguimientovehiculo (
                Vehiculo_id_vehiculo,
                coordenadas,
                velocidad,
                fecha_seguimiento,
                hora_seguimiento,
                frame_path
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            vehiculo_id, coordenadas, velocidad, fecha, hora, frame_path
        ))
        self.conn.commit()
        print("✅ Seguimiento insertado correctamente.")


    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
