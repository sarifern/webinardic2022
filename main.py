import os
import fifa_api

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

TOKEN = fifa_api.login(email=EMAIL, password=PASSWORD)
if TOKEN:
    print(fifa_api.matches_today(TOKEN))

# TODO: implementacion de Bot
# TODO: comando sencillo que regrese texto con endpoint de informacion
# de equipo endpoint teams_per_id
# TODO: agregar el comando help
# TODO: comando que regrese card con los partidos de hoy
# si time_elapsed="notstarted", mostrar paises banderitas y horario
# si ya empezó, mostrar ongoing y que tiempo time_elapsed, mostrar
# paises banderitas goles y quien los metio
# si ya termino, mostrar finished, mostrar paises banderitas
# y goles y quien los metio
