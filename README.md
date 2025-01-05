# genshin_impact
lo divido en lo que hice:
1. db en json (esa la uso en GCP en mi caso) - ese fue mi input y lo cargué a bigquery manualmente (puedes verlo como una db sql como postgre)
2. la query es lo primero que armé para primero conocer el dato - me entretuve analizando y explorando los datos
3. cuando estuve satisfecho, armé la funcion principal que teniendo todo los inputs del usuario, entrega el dato final de la recomendacion.
4. acá ya entré al proceso de backend, con un front end muy básico con html puro - para ir ajustando iba probando y desarrollando a la vez. Cruzaba referencias con una experta en genshin para saber si lo que desarrollaba estaba bien. 
5. cuando todo ya estaba funcionando como debería, lo tiré a vercel para desplegar el front
6. hice un front bonito con mi amigo chatgpt... simplesito -- pero siempre acompañado de ir probando en celu y en pc
7. acá en vercel la app se caía a veces y fui enriqueciendo el backend y front end

Resultado final (necesitas cuenta en vercel): https://genshin-impact-gcf2hkgof-jupahefis-projects.vercel.app/
