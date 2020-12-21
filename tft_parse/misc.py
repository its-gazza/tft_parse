
def dict_add_count(dt: dict, key):
    """Static method to add count to a dict given a key"""
    if dt.get(key) is None:
        dt[key] = 1
    else:
        dt[key] += 1

    return dt


def route_region(region: str):
    region = region.upper()
    if region in ['NA1', 'BR1', 'LA1', 'LA2', 'OC1']:
        return 'AMERICAS'
    elif region in ['KR', 'JP1']:
        return 'ASIA'
    elif region in ['EUN1', 'EUW1', 'TR1', 'RU']:
        return 'EUROPE'
    else:
        raise ValueError(f"{region} is not defined")


regions = ['BR1', 'EUN1', 'EUW1', 'JP1', 'KR', 'LA1', 'LA2', 'NA1', 'OC1', 'TR1', 'RU']
