import inspect
import sys

TOKEN = "MTIzMTM0MjgzMzk2NTczMTkyMg.GNvaPO.b8OqbZLlUvb5kqDB_K-EWJT_O5E1UQIzgB5pAo"
YT_API = "AIzaSyDq4ROZColssRSxsQl1Rpt0weyrAb7uMrw"
BOT_ID = 1231342833965731922
BOT_AUTH_HEADER = "https://discord.com/oauth2/authorize"

# начальные настройки
TIME_MUTE = 3600
ROLE_ID = 1232060135908835348
GIT_LINK = None
GIT_ACCESSIONS_LOG = None


# инициализация настроек из файла settings.txt
def init_settings():
    with open('settings.txt', 'r') as file:
        line = file.readline()
        while line:
            line = line.split('=')
            line = list(map(str.strip, line))
            if line[1] == "None":
                line[1] = None
            elif not line[0] == "GIT_LINK":
                line[1] = int(line[1])
            globals()[line[0]] = line[1]
            line = file.readline()


init_settings()
SETTINGS = {"TIME_MUTE": TIME_MUTE, "ROLE_ID": ROLE_ID, "GIT_LINK": GIT_LINK, "GIT_ACCESSIONS_LOG": GIT_ACCESSIONS_LOG}


def cog_log(bot, name):
    clsmembers = inspect.getmembers(sys.modules[name], inspect.isclass)
    for elem in clsmembers:
        try:
            if type(elem[0]) is str:
                cog = bot.get_cog(str(elem[0]))
                command = cog.get_commands()
                print(f"{elem[0]}_commands:{[c.name for c in command]}")
        except AttributeError:
            pass


def parser(string: str):
    string = list(map(str.strip, string.split('=')))
    for i in range(0, len(string), 2):
        if string[i] in list(SETTINGS.keys()):
            SETTINGS[string[i]] = string[i + 1]
            globals()[string[i]] = string[i + 1]
    with open('settings.txt', 'w', encoding='utf-8') as file:
        for elem in list(SETTINGS.keys()):
            print(f"{elem} = {globals()[elem]}", file=file)
            print(f"{elem} = {globals()[elem]}")
