import re
import texthero as hero

NEWS_SITES = {
    "Lajmi": "https://lajmi.net/",
    "GazetaExpress": "https://www.gazetaexpress.com/",
    "Insajderi": "https://insajderi.com/",
    "GazetaBlic": "https://gazetablic.com/",
    "Ballkani": "https://ballkani.info/",
    "Indeksonline": "https://indeksonline.net/",
    "Klankosova": "https://klankosova.tv/",
    "Kallxo.com": "https://kallxo.com/",
    "Telegrafi": "https://telegrafi.com/",
    "Kungulli": "https://www.kungulli.com/",
}
STOPWORDS = ["e", "te", "i", "me", "qe", "ne", "nje", "a", "per", "sh", "nga", "ka", "u", "eshte", "dhe", "shih", "nuk",
             "m", "dicka", "ose", "si", "shume", "etj", "se", "pa", "sipas", "s", "t", "dikujt", "dike", "mire", "vet",
             "bej", "ai", "vend", "prej", "ja", "duke", "tjeter", "kur", "ia", "ku", "ta", "keq", "dy", "ben", "bere",
             "behet", "dickaje", "edhe", "madhe", "la", "sa", "gjate", "zakonisht", "pas", "veta", "mbi", "disa", "iu",
             "mos", "c", "para", "dikush", "gje", "be", "pak", "tek", "fare", "beri", "po", "bie", "k", "do", "gjithe",
             "vete", "mund", "kam", "le", "jo", "beje", "tij", "kane", "ishte", "jane", "vjen", "ate", "kete", "neper",
             "cdo", "na", "marre", "merr", "mori", "rri", "deri", "b", "kishte", "mban", "perpara", "tyre", "marr",
             "gjitha", "as", "vetem", "nen", "here", "tjera", "tjeret", "drejt", "qenet", "ndonje", "nese", "jap",
             "merret", "rreth", "lloj", "dot", "saj", "nder", "ndersa", "cila", "veten", "ma", "ndaj", "mes", "ajo",
             "cilen", "por", "ndermjet", "prapa", "mi", "tere", "jam", "ashtu", "kesaj", "tille", "behem", "cilat",
             "kjo", "menjehere", "ca", "je", "aq", "aty", "prane", "ato", "pasur", "qene", "cilin", "teper", "njera",
             "tej", "krejt", "kush", "bejne", "ti", "bene", "midis", "cili", "ende", "keto", "kemi", "sic", "kryer",
             "cilit", "atij", "gjithnje", "andej", "siper", "sikur", "ketej", "ciles", "ky", "papritur", "ua",
             "kryesisht", "gjithcka", "pasi", "kryhet", "mjaft", "ketij", "perbashket", "ata", "atje", "vazhdimisht",
             "kurre", "tone", "keshtu", "une", "sapo", "rralle", "vetes", "ishin", "afert", "tjetren", "ketu", "cfare",
             "to", "anes", "jemi", "asaj", "secila", "kundrejt", "ketyre", "pse", "tilla", "mua", "nepermjet", "cilet",
             "ndryshe", "kishin", "ju", "tani", "atyre", "dic", "yne", "kudo", "sone", "sepse", "cilave", "kem", "ty",
             "t'i", "nbsp", "tha", "re", "the"]


def remove_tags(text: str):
    """
    Removes html tags from text
    @param text:
    @return:
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def clean_text(s):
    """
    Cleans text using texthero
    @param s:
    @return:
    """
    s = hero.remove_brackets(s)
    s = hero.remove_whitespace(s)
    return s


def preprocess_text(s):
    s = hero.fillna(s)
    s = hero.lowercase(s)
    s = hero.remove_digits(s)
    s = hero.remove_punctuation(s)
    s = hero.remove_diacritics(s)
    s = hero.remove_whitespace(s)
    return s
