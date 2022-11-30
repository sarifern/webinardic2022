from webex_bot.webex_bot import WebexBot
from commands.teams import TeamDetails
from commands.matches import MatchDetails
from apis import fifa_api
import os
from dotenv import load_dotenv

load_dotenv()

WEBEX_TOKEN = os.environ.get("WEBEX_TOKEN")


EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

FIFA_TOKEN = fifa_api.login(email=EMAIL, password=PASSWORD)

bot = WebexBot(
    WEBEX_TOKEN,
    bot_help_subtitle="Hola! Estos son los comandos que tengo habilitados:",
)

bot.add_command(TeamDetails(TOKEN=FIFA_TOKEN))
bot.add_command(MatchDetails(TOKEN=FIFA_TOKEN))

bot.run()
