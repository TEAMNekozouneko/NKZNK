from typing import Any
from discord import ApplicationContext, Embed, Color

def msgFormat(MsgGroup: str, ErrType: str, code: str, ctx: ApplicationContext, arg1: Any = None):
    errcode = "\n**{0}**: `{1}.{2}`".format("エラー",ErrType, code)
    message_format = {
            "error": {
                "permissions": {
                    "manage_channel_settings": "`MANAGE_SERVER`, `MANAGE_CHANNELS` いずれかの権限があなたになかったため実行できません。"+errcode,
                    "manage_user_mute": "`MUTE_MEMBERS` いずれかの権限があなたになかったため実行できません。"+errcode,
                    "manage_user_deaf": "`DEAFEN_MEMBERS` いずれかの権限があなたになかったため実行できません。"+errcode,
                    "manage_user_ban": "`BAN_MEMBERS` いずれかの権限があなたになかったため実行できません。"+errcode,
                    "manage_user_kick": "`KICK_MEMBERS` いずれかの権限があなたになかったため実行できません。"+errcode,
                    "manage_user_move": "`MOVE_MEMBERS` いずれかの権限があなたになかったため実行できません。"+errcode,
                },
                "server_limited": {
                    "required_eight_kbps": "最低でも8Kbps以上を指定する必要があります。"+errcode,
                    "required_ninety_nine": "制限は99までです。\n100以上の制限は課せられません。"+errcode,
                    "required_bst_bitrate": "このサーバーでは、{0}Kbpsまでしか利用できません。".format(ctx.author.guild.bitrate_limit / 1000)+errcode
                },
                "voice": {
                    "not_connected": "ボイスチャンネルまたはステージチャンネルに接続していませんでした。"+errcode,
                    "not_played": "音楽は再生中ではないため、音楽を一時停止できませんでした。"+errcode,
                    "already_played": "音楽はすでに再生してるため再生できませんでした。"+errcode,
                    "not_connected_mute": "ユーザーがボイスチャンネルに接続していないためミュートできません"+errcode,
                    "author_not_connected": "{0}がボイスチャンネルに接続していません".format(arg1)+errcode,
                    "cant_connect_voice": "ボイスチャンネルを選択するか、接続してください。"+errcode,
                    "cant_connect_stage": "ステージチャンネルを選択するか、接続してください。"+errcode,
                    "already_disconnected": "すでに切断済みです。"+errcode
                },
                "type": {
                    "do_not_minus": "負の数ではない数字を入力してください。"+errcode,
                    "arg_type_error": "引数 \"edtion\" で問題が発生しました。"+errcode
                },
                "failed": {
                    "server": "サーバーの取得に失敗しました。"+errcode,
                    "member": "入力されたユーザーはこのサーバーに存在していません。"+errcode,
                    "bedrock_server": "サーバーにアクセスできませんでした。ポート指定/開放またはUDPプロトコル以外で開いている場合があります\nIP指定の例: nekozouneko.ddns.net:19132"+errcode,
                    "java_server": "サーバーにアクセスできませんでした。ポート指定/開放またはTCPプロトコル以外で開いている場合があります\n`IP指定の例: mc.hypixel.net:25565`"+errcode,
                    "bot_lang_data": "ボットの言語データが古いため正しくエラーを表示できませんでした。\n**本来出るエラーコード**: {0}\n**エラーコード**: `faild.bot_lang_data`".format(errcode)
                }
            }
        }
    try:
        return Embed(title="エラーが発生しました。", description=message_format[MsgGroup][ErrType][code], color=Color.dark_red())
    except:
        print("Error: 一旦ボットデータを削除し、レポジトリからダウンロードし直してください。")
        return Embed(title="エラーが発生してました。", description=message_format["error"]["failed"]["bot_data"])