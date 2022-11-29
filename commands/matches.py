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
            # si la api no funciona, mandar un json
            matches = {
                "status": "success",
                "data": [
                    {
                        "_id": "629c9c8a5749c4077500eaf4",
                        "away_score": 0,
                        "away_scorers": ["null"],
                        "away_team_id": "8",
                        "finished": "FALSE",
                        "group": "B",
                        "home_score": 0,
                        "home_scorers": ["null"],
                        "home_team_id": "5",
                        "id": "33",
                        "local_date": "11/29/2022 22:00",
                        "matchday": "10",
                        "persian_date": "1400-09-08 22:30",
                        "stadium_id": "1",
                        "time_elapsed": "notstarted",
                        "type": "group",
                        "home_team_fa": "انگلستان",
                        "away_team_fa": "ولز",
                        "home_team_en": "England",
                        "away_team_en": "Wales",
                        "home_flag": "https://upload.wikimedia.org/wikipedia/en/thumb/b/be/Flag_of_England.svg/125px-Flag_of_England.svg.png",
                        "away_flag": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Flag_of_Wales_%281959%29.svg/125px-Flag_of_Wales_%281959%29.svg.png",
                    },
                    {
                        "_id": "629c9c8a5749c4077500eaf5",
                        "away_score": 0,
                        "away_scorers": ["null"],
                        "away_team_id": "7",
                        "finished": "FALSE",
                        "group": "B",
                        "home_score": 0,
                        "home_scorers": ["null"],
                        "home_team_id": "6",
                        "id": "34",
                        "local_date": "11/29/2022 22:00",
                        "matchday": "10",
                        "persian_date": "1400-09-08 22:30",
                        "stadium_id": "1",
                        "time_elapsed": "notstarted",
                        "type": "group",
                        "home_team_fa": "ایران",
                        "away_team_fa": "آمریکا",
                        "home_team_en": "Iran",
                        "away_team_en": "United States",
                        "home_flag": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Flag_of_Iran.svg/125px-Flag_of_Iran.svg.png",
                        "away_flag": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/125px-Flag_of_the_United_States.svg.png",
                    },
                    {
                        "_id": "629c9c8a5749c4077500eaf6",
                        "away_score": 2,
                        "away_scorers": ["Ismaïla Sarr,Kalidou Koulibaly"],
                        "away_team_id": "3",
                        "finished": "TRUE",
                        "group": "A",
                        "home_score": 1,
                        "home_scorers": ["Moisés Caicedo"],
                        "home_team_id": "2",
                        "id": "35",
                        "local_date": "11/29/2022 18:00",
                        "matchday": "10",
                        "persian_date": "1400-09-08 18:30",
                        "stadium_id": "1",
                        "time_elapsed": "finished",
                        "type": "group",
                        "home_team_fa": "اکوادور",
                        "away_team_fa": "سنگال",
                        "home_team_en": "Ecuador",
                        "away_team_en": "Senegal",
                        "home_flag": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Flag_of_Ecuador.svg/125px-Flag_of_Ecuador.svg.png",
                        "away_flag": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Flag_of_Senegal.svg/125px-Flag_of_Senegal.svg.png",
                    },
                    {
                        "_id": "629c9c8a5749c4077500eaf7",
                        "away_score": 0,
                        "away_scorers": ["null"],
                        "away_team_id": "1",
                        "finished": "TRUE",
                        "group": "A",
                        "home_score": 2,
                        "home_scorers": ["Cody Gakpo,Frenkie de Jong"],
                        "home_team_id": "4",
                        "id": "36",
                        "local_date": "11/29/2022 18:00",
                        "matchday": "10",
                        "persian_date": "1400-09-08 18:30",
                        "stadium_id": "1",
                        "time_elapsed": "finished",
                        "type": "group",
                        "home_team_fa": "هلند",
                        "away_team_fa": "قطر",
                        "home_team_en": "Netherlands",
                        "away_team_en": "Qatar",
                        "home_flag": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/125px-Flag_of_the_Netherlands.svg.png",
                        "away_flag": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Flag_of_Qatar.svg/125px-Flag_of_Qatar.svg.png",
                    },
                ],
            }
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
