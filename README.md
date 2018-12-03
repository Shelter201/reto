# reto
Reto

Ambas bases contienen la información de los nombres de las encuestas y las opciones. La información que tiene separada son los votos y las estadísticas. Los votos sólo están en la base correspondiente al "Poll service" y las estadísticas (conteos) sólo se encuentran en la base correspondiente al "Poll Stats service".


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



