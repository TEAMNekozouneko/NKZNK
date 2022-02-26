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

    return defaultConfig