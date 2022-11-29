from webex_bot.models.command import Command
from webex_bot.formatting import quote_danger
from webex_bot.models.response import Response
from jinja2 import Environment, FileSystemLoader
import json
from apis import fifa_api
import pytz
from dateutil.parser import parse

tzmex = pytz.timezone("America/Mexico_City")
tzqat = pytz.timezone("Asia/Qatar")


class MatchDetails(Command):
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN
        super().__init__(
            command_keyword="partidos",
            help_message="'partidos': Obtener información de partidos",
            delete_previous_message=True,
        )

    def get_matches(self):
        matches = fifa_api.matches_today(self.TOKEN)
        if matches.get("status") != "success":
            print("Falló la conexión a la API")
            return False
        else:
            matches = matches["data"]
            # parsear tiempo a mexico

            for match in matches:
                match["local_date"] = (
                    tzqat.localize(parse(match["local_date"]), False)
                    .astimezone(tzmex)
                    .strftime("%H:%M:%S")
                )
        return matches

    def pre_card_load_reply(self, message, attachment_actions, activity):
        return "Cargando tarjeta"

    def pre_execute(self, message, attachment_actions, activity):
        return "Obteniendo información..."

    def execute(self, message, attachment_actions, activity):
        # TODO: comando que regrese card con los partidos de hoy
        # si time_elapsed="notstarted", mostrar paises banderitas
        # y horario
        # # si ya empezó, mostrar ongoing y que tiempo time_elapsed,
        # mostrar paises banderitas goles
        # si ya termino, mostrar finished, mostrar paises banderitas
        # y goles
        matches = self.get_matches()
        if not matches:
            return quote_danger("No me pude conectar a la API")

        env_jinja = Environment(
            loader=FileSystemLoader("cards"), autoescape=True
        )
        env_jinja.filters["jsonify"] = json.dumps
        template = env_jinja.get_template("matches.json")
        card_data = json.loads(template.render(matches=matches))
        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }

        response = Response()
        response.text = "Detalles de partidos de hoy"
        response.attachments = card_payload
        return response
