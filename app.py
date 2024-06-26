from flask import Flask, render_template, request
from pymongo import MongoClient
from config import Config  # Archivo de configuración donde está definida la URI de MongoDB

app = Flask(__name__)
app.config.from_object(Config)

# Conexión a la base de datos MongoDB
client = MongoClient(app.config['MONGO_URI'])
db = client.calidadAire  
barrios_collection = db.estacion  
datos_collection = db.datos
contaminantes_collection = db.contaminantes

@app.route('/', methods=['GET', 'POST'])
def form():

    if request.method == 'POST':
        barrio = request.form['barrio']
        dia = int(request.form['dia'])
        documento_barrio = barrios_collection.find_one({"Nom_barri": barrio})
        numEstacion = documento_barrio["Estacio"]
        #segun el dia y el numEstacion todos los valores de CODI_CONTAMINANT 
        numContaminante = []
        nombreContaminante = []
        cantidadContaminante= []
        unidadesContaminantes = []
        
        estacionSelect = datos_collection.find({"DIA": dia, "ESTACIO": numEstacion})
        for dato in estacionSelect:
            numContaminante.append(dato['CODI_CONTAMINANT'])
            cantidadContaminante.append(dato['H12'])
        for contaminante in numContaminante:
            nombreContaminante.append(contaminantes_collection.find_one({"Codi_Contaminant":contaminante})['Desc_Contaminant'])
            unidadesContaminantes.append(contaminantes_collection.find_one({"Codi_Contaminant":contaminante})['Unitats'])

        contaminantes = zip(nombreContaminante, cantidadContaminante, unidadesContaminantes)
    
        return render_template('results.html', barrio=barrio, dia=dia, contaminantes=contaminantes)

    barrios = barrios_collection.distinct("Nom_barri")
    return render_template('index.html', barrios=barrios)


if __name__ == '__main__':
    app.run(debug=True)
