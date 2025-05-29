# verificar_vehiculos.py

import mysql.connector
import os
import cv2

# Configuración de la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='r00t123',
    database='ovial'
)
cursor = conn.cursor()

# Obtener vehículos únicos
cursor.execute("SELECT id_vehiculo, identificador_unico FROM vehiculo")
vehiculos = cursor.fetchall()

print(f"Total vehículos únicos en base de datos: {len(vehiculos)}")

for vehiculo_id, identificador in vehiculos:
    print(f"\nID: {vehiculo_id} | Identificador: {identificador}")
    
    # Buscar el seguimiento correspondiente
    cursor.execute("""
        SELECT frame_path FROM seguimientovehiculo 
        WHERE Vehiculo_id_vehiculo = %s 
        ORDER BY id_SeguimientoVehiculo ASC LIMIT 1
    """, (vehiculo_id,))
    
    resultado = cursor.fetchone()
    if resultado:
        imagen_path = resultado[0]
        print(f"Mostrando imagen: {imagen_path}")
        if os.path.exists(imagen_path):
            img = cv2.imread(imagen_path)
            cv2.imshow(f"Vehículo ID {vehiculo_id}", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("⚠️ Imagen no encontrada:", imagen_path)
    else:
        print("⚠️ Sin seguimiento registrado para este vehículo.")

cursor.close()
conn.close()
