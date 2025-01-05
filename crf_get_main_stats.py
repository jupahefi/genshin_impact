from google.cloud import bigquery
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

def get_main_stats(request):
    # Manejar la solicitud preflight de CORS (OPTIONS)
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 204

    # Extraer los datos del request (el set_name en este caso)
    data = request.get_json()

    if not data or 'set_name' not in data:
        return jsonify({"error": "Falta el parámetro 'set_name'."}), 400

    set_name = data['set_name']

    # Crear cliente de BigQuery
    client = bigquery.Client()

    # Consulta SQL para obtener los main_stat únicos pertenecientes al set_name
    query = f"""
    SELECT DISTINCT artefact.main_stat AS main_stat_artefacto
    FROM `micros-chile.genshin.personajes_v2` AS personajes,
    UNNEST(personajes.artifacts) AS artefact
    WHERE artefact.name = @set_name
    """

    # Configurar el job con parámetros
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("set_name", "STRING", set_name)
        ]
    )

    # Ejecutar la consulta
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Convertir los resultados a una lista
    main_stats = [{"main_stat_artefacto": row.main_stat_artefacto} for row in results]

    # Crear la respuesta con los encabezados CORS
    response = make_response(jsonify(main_stats))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Para ejecutar la función localmente (opcional)
if __name__ == '__main__':
    app.run(debug=True)
