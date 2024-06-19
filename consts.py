from os import environ

class Consts:
    BOT_ID = environ.get('BOT_ID')
    TOKEN = environ.get('TOKEN')
    TOPGG_AUTHTOKEN = environ.get('TOPGG_AUTHTOKEN')
    DATABASE_URL = environ.get('DATABASE_URL')
    URI = environ.get('URI')
    BUILD_URL = "https://www.unite-db.com"
    LOGO_ADDRESS = "https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/unitelogo512.png"
    ONLY_REQUESTOR_CAN_TOGGLE = "Only the requester can manipulate this embed."
    POKEMONUNITEGG_ICONURL = "https://www.pokemonunite.gg/res/img/favicon/favicon-32x32.png"