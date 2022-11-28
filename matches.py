from webex_bot.models.command import Command


class MatchDetails(Command):
    def __init__(self):
        super().__init__(
            command_keyword="partidos",
            help_message="Obtener información de partidos",
            delete_previous_message=True)

    def execute(self, message, attachment_actions, activity):
        return
