from flask import Flask, render_template, request, jsonify
import pandas as pd
from openpyxl import load_workbook
import os

app = Flask(__name__)

# Ruta principal que sirve el formulario HTML
# En el Browser digita esta dirección una vez ejecutado el programa python: http://127.0.0.1:5000
@app.route('/')
def index():
    return render_template('index.html')  # Cargar el archivo HTML desde templates/

# Ruta para recibir los datos del formulario y guardarlos en Excel
@app.route('/guardar_datos', methods=['POST'])
def guardar_datos():
    try:
        # Captura los datos enviados desde el formulario HTML
        nombre = request.form['nombre']
        ide = request.form['ide']
        correo = request.form['correo']

        # Validación de datos
        if not nombre or not ide or not correo:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Crear un DataFrame con los datos recibidos
        nuevo_dato = pd.DataFrame({'Nombre': [nombre], 'Identificación': [ide], 'Correo': [correo]})

        # Nombre del archivo Excel
        archivo_excel = 'datos.xlsx'

        if os.path.exists(archivo_excel):
            # Cargar datos existentes del archivo
            datos_existentes = pd.read_excel(archivo_excel)
            # Combinar los datos existentes con los nuevos
            datos_actualizados = pd.concat([datos_existentes, nuevo_dato], ignore_index=True)
        else:
            # Si no existe el archivo, los nuevos datos serán los únicos
            datos_actualizados = nuevo_dato

        # Escribir los datos actualizados en el archivo Excel
        datos_actualizados.to_excel(archivo_excel, index=False)

        return jsonify({"message": "Datos guardados en Excel correctamente"}), 200

    except Exception as e:
        # Manejo de errores genéricos
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
