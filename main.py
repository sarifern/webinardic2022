from webex_bot.webex_bot import WebexBot
from teams import TeamDetails
from matches import MatchDetails
import os

WEBEX_TOKEN = os.environ.get("WEBEX_TOKEN")

# TODO: implementacion de Bot
bot = WebexBot(WEBEX_TOKEN, approved_domains=['cisco.com'])

# TODO: comando sencillo que regrese texto con endpoint de informacion
# de equipo endpoint teams_per_id
# TODO: agregar el comando help
bot.add_command(TeamDetails())
bot.add_command(MatchDetails())

bot.run()


# TODO: comando que regrese card con los partidos de hoy
# si time_elapsed="notstarted", mostrar paises banderitas y horario
# si ya empezó, mostrar ongoing y que tiempo time_elapsed, mostrar
# paises banderitas goles y quien los metio
# si ya termino, mostrar finished, mostrar paises banderitas
# y goles y quien los metio
