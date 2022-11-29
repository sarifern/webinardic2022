from webex_bot.formatting import quote_danger
from webex_bot.models.command import Command
from webex_bot.models.response import Response
from jinja2 import Environment, FileSystemLoader
from apis import fifa_api

import json


class TeamDetails(Command):
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN
        super().__init__(
            command_keyword="equipos",
            help_message="'equipos': Obtener detalles equipo",
            chained_commands=[TeamCallback(self.TOKEN)],
            delete_previous_message=True,
        )

    def execute(self, message, attachment_actions, activity):
        """
        Si quieres responder dependiendo de la información del usuario
        desde una tarjeta, hay que escribir aquí nuestro código.

        Podrías regresar una cadena de texto aquí o alguna otra tarjeta
        (Response).

        Esta función regresa los detalles de algún equipo de la FIFA.

        :param message: mensaje sin el comando clave
        :param attachment_actions: objeto attachment_actions
        :param activity: actividad del objeto

        :return: un objeto Response
        """

        # Format response message for user
        teams = self.get_teams()

        if not teams:
            return quote_danger("No me pude conectar a la API")

        env_jinja = Environment(
            loader=FileSystemLoader("cards"), autoescape=True
        )
        env_jinja.filters["jsonify"] = json.dumps
        template = env_jinja.get_template("search-team.json")
        card_data = json.loads(template.render(teams=teams))
        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }

        response = Response()
        response.text = "Selecciona el equipo"
        response.attachments = card_payload

        return response

    def get_teams(self):
        teams = fifa_api.teams(self.TOKEN)
        if teams.get("status") != "success":
            print("Falló la conexión a la API")
            return False
        return teams["data"]


class TeamCallback(Command):
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN
        super().__init__(card_callback_keyword="team_callback")

    def pre_execute(self, message, attachment_actions, activity):
        return "Obteniendo información..."

    def execute(self, message, attachment_actions, activity):
        team_id = attachment_actions.inputs.get("equipo")
        team_details = self.get_team_details(team_id)
        if not team_details:
            return quote_danger("No me pude conectar a la API")

        env_jinja = Environment(
            loader=FileSystemLoader("cards"), autoescape=True
        )
        env_jinja.filters["jsonify"] = json.dumps
        template = env_jinja.get_template("team-details.json")
        card_data = json.loads(template.render(team_details=team_details))
        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }

        response = Response()
        response.text = "Detalles del equipo"
        response.attachments = card_payload
        return response

    def get_team_details(self, team_id):
        team_details = fifa_api.teams_per_id(self.TOKEN, team_id)
        if team_details.get("status") != "success":
            # si la api no sirve, poner un json de prueba
            team_details = {
                "status": "success",
                "data": [
                    {
                        "_id": "629c9c6b5749c4077500eab2",
                        "name_en": "Mexico",
                        "name_fa": "مکزیک",
                        "flag": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Flag_of_Mexico.svg/125px-Flag_of_Mexico.svg.png",
                        "fifa_code": "MEX",
                        "iso2": "MX",
                        "groups": "C",
                        "id": "13",
                    }
                ],
            }

        team_details = team_details["data"][0]

        standing_group = fifa_api.standings_by_group(
            self.TOKEN, team_details["groups"]
        )
        if standing_group.get("status") != "success":
            print("Falló la conexión a la API")
            return False
        standing_group = standing_group["data"][0]["teams"]
        for team in standing_group:
            if team["team_id"] == team_id:
                return team
        return False
