
regions = ["auto", "amsterdam", "brazil", "dubai", "eu_central", "eu_west", "europe", "frankfurt", "hongkong", "india", "japan", "london", "russia", "singapore", "southafrica", "south_korea", "sydney", "us_central", "us_east", "us_south", "us_west"]
sregions = ['auto', 'us_west', 'brazil', 'hongkong', 'india', 'japan', 'rotterdam', 'russia', 'singapore', 'south_korea', 'southafrica', 'sydney', 'us_central', 'us_east', 'us_south']


async def regionSelector(ctx) -> list[str]:
    return [region for region in regions if region.startswith(ctx.value)]

async def sregionSelector(ctx):
    return [sregion for sregion in sregions if sregion.startswith(ctx.value)]