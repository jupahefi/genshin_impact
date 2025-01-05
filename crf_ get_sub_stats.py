from google.cloud import bigquery
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

def get_sub_stats(request):
    # Manejar la solicitud preflight de CORS (OPTIONS)
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 204

    # Extraer los datos del request (set_name y main_stat)
    data = request.get_json()

    if not data or 'set_name' not in data or 'main_stat' not in data:
        return jsonify({"error": "Faltan los parámetros 'set_name' o 'main_stat'."}), 400

    set_name = data['set_name']
    main_stat = data['main_stat']

    # Crear cliente de BigQuery
    client = bigquery.Client()

    # Consulta SQL para obtener los sub_stats únicos
    query = f"""
    SELECT DISTINCT sub_stat
    FROM `micros-chile.genshin.personajes_v2` AS personajes,
    UNNEST(personajes.artifacts) AS artefact,
    UNNEST(artefact.sub_stats) AS sub_stat
    WHERE artefact.name = @set_name
    AND artefact.main_stat = @main_stat
    """

    # Configurar el job con parámetros
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("set_name", "STRING", set_name),
            bigquery.ScalarQueryParameter("main_stat", "STRING", main_stat)
        ]
    )

    # Ejecutar la consulta
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Convertir los resultados a una lista
    sub_stats = [{"sub_stat": row.sub_stat} for row in results]

    # Crear la respuesta con los encabezados CORS
    response = make_response(jsonify(sub_stats))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Para ejecutar la función localmente (opcional)
if __name__ == '__main__':
    app.run(debug=True)
