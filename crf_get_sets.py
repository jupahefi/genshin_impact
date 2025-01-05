from google.cloud import bigquery
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

def get_sets(request):
    # Manejar la solicitud preflight de CORS (OPTIONS)
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 204

    # Crear cliente de BigQuery
    client = bigquery.Client()

    # Consulta SQL para obtener los sets únicos de artefactos
    query = """
    SELECT DISTINCT artefact.name AS artefacto_set
    FROM `micros-chile.genshin.personajes_v2` AS personajes,
    UNNEST(personajes.artifacts) AS artefact
    """

    # Ejecutar la consulta
    query_job = client.query(query)
    results = query_job.result()

    # Convertir los resultados a una lista
    sets = [{"artefacto_set": row.artefacto_set} for row in results]

    # Crear la respuesta con los encabezados CORS
    response = make_response(jsonify(sets))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Para ejecutar la función localmente (opcional)
if __name__ == '__main__':
    app.run(debug=True)
