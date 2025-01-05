from google.cloud import bigquery
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

def get_artifacts(request):
    # Manejar la solicitud preflight de CORS (OPTIONS)
    if request.method == 'OPTIONS':
        # Responder a la solicitud OPTIONS con los encabezados CORS correctos
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 204

    # Extraer los datos del request
    data = request.get_json()

    # Validar que se proporcionen todos los datos necesarios
    if not data or 'set_name' not in data or 'main_stat' not in data or 'sub_stats' not in data:
        return jsonify({"error": "Faltan datos requeridos: 'set_name', 'main_stat' y 'sub_stats' son necesarios."}), 400

    set_name = data['set_name']
    main_stat = data['main_stat']
    sub_stats = data['sub_stats']  # Es un array de sub_stats

    # Crear cliente de BigQuery
    client = bigquery.Client()

    # Consulta SQL con parámetros
    query = """
    WITH InputArtefacto AS (
        SELECT
            @set_name AS set_name,
            @main_stat AS main_stat,
            @sub_stats AS sub_stats
    )

    SELECT 
        personajes.name AS personaje,
        artefact.name AS artefacto_set,
        artefact.slot AS slot_artefacto,
        artefact.main_stat AS main_stat_artefacto,
        artefact.sub_stats AS sub_stats_artefacto
    FROM 
        `micros-chile.genshin.personajes_v2` AS personajes,
        UNNEST(personajes.artifacts) AS artefact,
        InputArtefacto
    WHERE 
        artefact.name = InputArtefacto.set_name
        AND artefact.main_stat = InputArtefacto.main_stat
        AND ARRAY_LENGTH(
            ARRAY(
                SELECT sub_stat
                FROM UNNEST(InputArtefacto.sub_stats) AS sub_stat
                WHERE sub_stat IN UNNEST(artefact.sub_stats)
            )
        ) = ARRAY_LENGTH(InputArtefacto.sub_stats)
    """

    # Configurar la consulta con parámetros
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("set_name", "STRING", set_name),
            bigquery.ScalarQueryParameter("main_stat", "STRING", main_stat),
            bigquery.ArrayQueryParameter("sub_stats", "STRING", sub_stats)
        ]
    )

    # Ejecutar la consulta
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Convertir los resultados a una lista
    artifacts = [{"personaje": row.personaje,
                  "artefacto_set": row.artefacto_set,
                  "slot_artefacto": row.slot_artefacto,
                  "main_stat_artefacto": row.main_stat_artefacto,
                  "sub_stats_artefacto": row.sub_stats_artefacto}
                 for row in results]

    # Crear la respuesta con los encabezados CORS para la solicitud POST
    response = make_response(jsonify(artifacts))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Para ejecutar la función localmente (opcional)
if __name__ == '__main__':
    app.run(debug=True)
