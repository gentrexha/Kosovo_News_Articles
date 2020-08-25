import re

NEWS_SITES = {
    "Lajmi": "https://lajmi.net/",
    "GazetaExpress": "https://www.gazetaexpress.com/",
    "Insajderi": "https://insajderi.com/",
    "GazetaBlic": "https://gazetablic.com/",
    "Ballkani": "https://ballkani.info/",
    "KosovaSot": "https://www.kosova-sot.info/",
    "Indeksonline": "https://indeksonline.net/",
    "Klankosova": "https://klankosova.tv/",
    "Kallxo.com": "https://kallxo.com/",
    "Telegrafi": "https://telegrafi.com/",
    "KlanKosova": "https://klankosova.tv/",
}


def remove_tags(text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)
