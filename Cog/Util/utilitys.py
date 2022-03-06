
from discord import StageChannel, VoiceChannel, VoiceRegion

def NoneToNashi(none_obj):
    if (none_obj is None):
        rtnObj = "なし"
    else:
        rtnObj = none_obj
    return rtnObj

def RTCSwitcher(channel: VoiceChannel | StageChannel, region: VoiceRegion):
    rtn = []

    if (channel.rtc_region == VoiceRegion.amsterdam):
        rtn = ["サーバー", ":flag_nl: アムステルダム（オランダ）"]
    elif (channel.rtc_region == VoiceRegion.brazil):
        rtn = ["サーバー",":flag_br: ブラジル"]
    elif (channel.rtc_region == VoiceRegion.dubai):
        rtn = ["サーバー", ":flag_ae: ドバイ（アラブ首長国連邦）"]
    elif (channel.rtc_region == VoiceRegion.eu_central):
        rtn = ["サーバー", ":flag_eu: EU（中央）"]
    elif (channel.rtc_region == VoiceRegion.eu_west):
        rtn = ["サーバー", ":flag_eu: EU（西）"]
    elif (channel.rtc_region == VoiceRegion.frankfurt):
        rtn = ["サーバー", ":flag_hk: フランクフルト（ドイツ）"]
    elif (channel.rtc_region == VoiceRegion.hongkong):
        rtn = ["サーバー", ":flag_hk: 香港"]
    elif (channel.rtc_region == VoiceRegion.india):
        rtn = ["サーバー", ":flag_in: インド"]
    elif (channel.rtc_region == VoiceRegion.japan):
        rtn = ["サーバー", ":flag_jp: 日本"]
    elif (channel.rtc_region == VoiceRegion.london):
        rtn = ["サーバー", ":flag_gb: ロンドン（イギリス）"]
    elif (channel.rtc_region == VoiceRegion.russia):
        rtn = ["サーバー", ":flag_ru: ロシア連邦"]
    elif (channel.rtc_region == VoiceRegion.singapore):
        rtn = ["サーバー", ":flag_sg: シンガポール"]
    elif (channel.rtc_region == VoiceRegion.southafrica):
        rtn = ["サーバー", ":flag_za: 南アフリカ"]
    elif (channel.rtc_region == VoiceRegion.south_korea):
        rtn = ["サーバー", ":flag_kr: 韓国"]
    elif (channel.rtc_region == VoiceRegion.sydney):
        rtn = ["サーバー", ":flag_au: シドニー"]
    elif (channel.rtc_region == VoiceRegion.us_central):
        rtn = ["サーバー", ":flag_us: アメリカ合衆国（中央）"]
    elif (channel.rtc_region == VoiceRegion.us_east):
        rtn = ["サーバー", ":flag_us: アメリカ合衆国（東）"]
    elif (channel.rtc_region == VoiceRegion.us_south):
        rtn = ["サーバー", ":flag_us: アメリカ合衆国（南）"]
    elif (channel.rtc_region == VoiceRegion.us_west):
        rtn = ["サーバー", ":flag_us: アメリカ合衆国（西）"]
    elif (channel.rtc_region == VoiceRegion.vip_amsterdam):
        rtn = ["サーバー", ":flag_nl: :gem: VIP用 アムステルダム（オランダ）"]
    elif (channel.rtc_region == VoiceRegion.vip_us_east):
        rtn = ["サーバー", ":flag_us: :gem: VIP用 アメリカ合衆国（東）"]
    elif (channel.rtc_region == VoiceRegion.vip_us_west):
        rtn = ["サーバー", ":flag_us: :gem: VIP用 アメリカ合衆国（西）"]
    return rtn

def toRegion(region: str):
    r = None
    if (region == "amsterdam"):
        r = VoiceRegion.amsterdam
    elif (region == "brazil"):
        r = VoiceRegion.brazil
    elif (region == "dubai"):
        r = VoiceRegion.dubai
    elif (region == "eu_central"):
        r = VoiceRegion.eu_central
    elif (region == "eu_west"):
        r = VoiceRegion.eu_west
    elif (region == "frankfurt"):
        r = VoiceRegion.frankfurt
    elif (region == "hongkong"):
        r = VoiceRegion.hongkong
    elif (region == "india"):
        r = VoiceRegion.india
    elif (region == "japan"):
        r = VoiceRegion.japan
    elif (region == "london"):
        r = VoiceRegion.london
    elif (region == "russia"):
        r = VoiceRegion.russia
    elif (region == "singapore"):
        r = VoiceRegion.singapore
    elif (region == "southafrica"):
        r = VoiceRegion.southafrica
    elif (region == "south_korea"):
        r = VoiceRegion.south_korea
    elif (region == "sydney"):
        r = VoiceRegion.sydney
    elif (region == "us_central"):
        r = VoiceRegion.us_central
    elif (region == "us_east"):
        r = VoiceRegion.us_east
    elif (region == "us_south"):
        r = VoiceRegion.us_south
    elif (region == "us_west"):
        r = VoiceRegion.us_west
    
    return r