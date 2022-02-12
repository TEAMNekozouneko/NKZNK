
regions = ["auto", "amsterdam", "brazil", "dubai", "eu_central", "eu_west", "europe", "frankfurt", "hongkong", "india", "japan", "london", "russia", "singapore", "southafrica", "south_korea", "sydney", "us_central", "us_east", "us_south", "us_west"]

async def regionSelector(ctx):
    return [region for region in regions if region.startswith(ctx.value)]