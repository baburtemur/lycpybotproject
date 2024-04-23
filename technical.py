import sys, inspect

TOKEN = "MTIzMTM0MjgzMzk2NTczMTkyMg.G8yRvV.HVb_qr_EfC5GzyE9GR1LicN36fHczxRE7z3J-A"

YT_API = "AIzaSyDq4ROZColssRSxsQl1Rpt0weyrAb7uMrw"


def cog_log(bot, name):
    clsmembers = inspect.getmembers(sys.modules[name], inspect.isclass)
    for elem in clsmembers:
        if type(elem[0]) is str:
            cog = bot.get_cog(str(elem[0]))
            command = cog.get_commands()
            print(f"{elem[0]}_commands:{[c.name for c in command]}")