import imp
from discord import ApplicationContext, Embed, Color

def msgFormat(MsgGroup: str, ErrType: str, code: str, ctx: ApplicationContext):
    message_format = {
            "error": {
                "permissions": {
                    "manage_channel_settings": "権限エラー: `MANAGE_SERVER`, `MANAGE_CHANNELS` いずれかの権限があなたになかったため実行できません。\n**エラーコード**: `permissions.manage_channel_settings`",
                    "manage_user_mute": "権限エラー: `MUTE_MEMBERS` いずれかの権限があなたになかったため実行できません。\n**エラーコード**: `permissions.manage_user_mute`",
                    "manage_user_deaf": "権限エラー: `DEAFEN_MEMBERS` いずれかの権限があなたになかったため実行できません。\n**エラーコード**: `permissions.manage_user_deaf`",
                    "manage_user_ban": "権限エラー: `BAN_MEMBERS` いずれかの権限があなたになかったため実行できません。\n**エラーコード**: `permissions.manage_user_ban`",
                    "manage_user_kick": "権限エラー: `KICK_MEMBERS` いずれかの権限があなたになかったため実行できません。\n**エラーコード**: `permissions.manage_user_kick`",
                    "manage_user_move": "権限エラー: `MOVE_MEMBERS` いずれかの権限があなたになかったため実行できません。\n**エラーコード**: `permissions.manage_user_move`"
                },
                "server_limited": {
                    "required_eight_kbps": "最低でも8Kbps以上を指定する必要があります。\n**エラーコード**: `server_limited.required_eight_kbps`",
                    "required_ninety_nine": "制限は99までです。\n100以上の制限は課せられません。\n**エラーコード**: `server_limited.required_ninety_nine`",
                    "required_bst_bitrate": f"このサーバーでは、{ctx.author.guild.bitrate_limit / 1000}Kbpsまでしか利用できません。\n**エラーコード**: `server_limited.required_bst_bitrate`"
                }
            }
        }
    return Embed(title="エラーが発生しました。", description=message_format[MsgGroup][ErrType][code], color=Color.dark_red())