# reto
Reto

Ambas bases contienen la información de los nombres de las encuestas y las opciones. La información que tiene separada son los votos y las estadísticas. Los votos sólo están en la base correspondiente al "Poll service" y las estadísticas (conteos) sólo se encuentran en la base correspondiente al "Poll Stats service". Se utilizó Django/Python, Postres, RabbitMQ y Nginx.

Nota: La intención era que la forma de validar si ya se había votado fuera por IP. Después de ponerse tras un nginx para separar los PUT y GET, no logré hacer que django recibiera la ip del cliente y siempre recibía la ip del contenedor de nginx, por lo cual para cualquier encuesta sólo se podía votar una única vez. En aras de que se pudiera probar el resto del desarrollo, se deshabilitó esta función (./reto_poll/poll/views.py: 125 -> if False: #len(vote_already) > 0: )

Ej.

Crear encuesta:

PUT http://localhost/poll/

{
    "name" : "",
    "options" : ["","","","",""]
}

--------------------------------------

Votar:

PUT http://localhost/poll/{id}/vote

{ 
    "option" : "" 
}


--------------------------------------

Resultados generales:

GET http://localhost/poll/{id}/


--------------------------------------

Resultados por hora:

GET http://localhost/poll/{id}/vote/hourly/



