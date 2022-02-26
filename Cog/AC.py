regions = ["auto", "amsterdam", "brazil", "dubai", "eu_central", "eu_west", "europe", "frankfurt", "hongkong", "india", "japan", "london", "russia", "singapore", "southafrica", "south_korea", "sydney", "us_central", "us_east", "us_south", "us_west"]
sregions = ['auto', 'brazil', 'hongkong', 'india', 'japan', 'rotterdam', 'russia', 'singapore', 'south_korea', 'southafrica', 'sydney', 'us_central', 'us_east', 'us_south', 'us_west']

async def regionSelector(ctx):
    return [region for region in regions if region.startswith(ctx.value)]

async def sregionSelector(ctx):
    return [sregion for sregion in sregions if sregion.startswith(ctx.value)]

def resetConfig():
    newConfig = open("config.json", "w", encoding="UTF-8")

    defaultConfig = str(
"""{
    "accept_license": false,

    "extensions": {
        "addon_exts": [],
        "default_exts": ["Cog.ChannelCommand", "Cog.GuildCommand", "Cog.HelpCommand", "Cog.UserCommand", "Cog.UtilityCommand", "Cog.VoiceCommand", "Cog.WikiCommand", "Cog.EventListener"]
    },

    "settings": {
        "enable_console": true,
        "name": "NKZNK",
        "unix": false,
        "token": "",
        "version": "2022.02.25"
    }
}""")

    newConfig.write(defaultConfig)
    newConfig.close()