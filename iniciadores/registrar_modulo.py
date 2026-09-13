import sqlite3

conexion = sqlite3.connect('database.db')

# Asumiendo que las columnas son id, nombre, activo, orden
conexion.execute('''
    INSERT INTO modulos (id, nombre_legible, activo, orden) 
    VALUES ('servicios', 'Servicios / Características', 1, 3)
''')

conexion.commit()
conexion.close()
print("¡Módulo 'servicios' registrado correctamente!")