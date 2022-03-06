from discord import ApplicationContext

voice_region = ["auto", "amsterdam", "brazil", "dubai", "eu_central", "eu_west", "europe", "frankfurt", "hongkong", "india", "japan", "london", "russia", "singapore", "southafrica", "south_korea", "sydney", "us_central", "us_east", "us_south", "us_west"]
stage_region = ['auto', 'brazil', 'hongkong', 'india', 'japan', 'rotterdam', 'russia', 'singapore', 'south_korea', 'southafrica', 'sydney', 'us_central', 'us_east', 'us_south', 'us_west']

async def VoiceRegion(ctx):
    return_obj = [region for region in voice_region if region.startswith(ctx.value)]
    return return_obj

async def StageRegion(ctx : ApplicationContext):
    return_obj = [region for region in stage_region if region.startswith(ctx.value)]
    return return_obj