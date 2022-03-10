import json, os

default_bot_settings = {
    "accept_license": False,

    "extensions": {
        "addon_exts": [],
        "default_exts": ["Cog.ChannelCommand", "Cog.GuildCommand", "Cog.HelpCommand", "Cog.UserCommand", "Cog.UtilityCommand", "Cog.VoiceCommand", "Cog.WikiCommand", "Cog.EventListener"]
    },

    "settings": {
        "enable_console": True,
        "name": "NKZNK",
        "unix": False,
        "token": "",
        "version": "2022.03.10"
    }
}

default_user_settings = {
    "locale": {
        "language": "ja",
        "timezone": 9
    },

    "sns": {
        "github": None,
        "twitter": None,
        "youtube": None
    }
}

def reset_bot_cfg():
    with open("config.json", "w+", encoding="UTF-8") as config_file:
        json.dump(default_bot_settings, config_file, indent=4)

def reset_usr_cfg(id: int):
    if (not os.path.exists("configuration/")):
        os.mkdir("configuration")
    if (not os.path.exists("configuration/users")):
        os.mkdir("configuration/users")

    with open(f"configuration/users/{id}.json", "w+", encoding="UTF-8") as config_file:
        json.dump(default_user_settings, config_file, indent=4)        