# -*- coding: utf-8 -*-
""" Albanian stemmer taken from https://github.com/arditdine/albanian-nlp
"""


import re


class AlbStem(object):
    chars = [
        (
            "a",
            [
                "Á",
                "á",
                "Å",
                "Ä",
                "ä",
                "Α",
                "α",
                "Ά",
                "Ὰ",
                "Ἀ",
                "Ἄ",
                "Ἂ",
                "Ἆ",
                "Ἁ",
                "Ἅ",
                "Ἃ",
                "Ἇ",
                "Ᾱ",
                "Ᾰ",
                "ά",
                "ὰ",
                "ᾶ",
                "ἀ",
                "ἄ",
                "ἂ",
                "ἆ",
                "ἁ",
                "ἅ",
                "ἃ",
                "ἇ",
                "ᾱ",
                "ᾰ",
                "ᾼ",
                "ᾈ",
                "ᾌ",
                "ᾊ",
                "ᾎ",
                "ᾉ",
                "ᾍ",
                "ᾋ",
                "ᾏ",
                "ᾳ",
                "ᾴ",
                "ᾲ",
                "ᾷ",
                "ᾀ",
                "ᾄ",
                "ᾂ",
                "ᾆ",
                "ᾁ",
                "ᾅ",
                "ᾃ",
                "ᾇ",
                "å",
                "À",
                "à",
                "Â",
                "â",
                "Æ",
                "æ",
                "А",
                "а",
                "Ъ",
                "ъ",
                "Ă",
                "ă",
                "Ь",
                "ь",
                "Я",
                "я",
                "Ą",
                "ą",
                "Ã",
                "ã",
            ],
        ),
        ("b", ["Β", "β", "Б", "б"]),
        ("c", ["ç", "Ç", "Č", "č", "Ξ", "ξ", "Ћ", "ћ", "Ć", "ć", "Ц", "ц", "Ч", "ч"]),
        ("d", ["Ď", "ď", "Δ", "δ", "Д", "д", "Ђ", "ђ", "Đ", "đ", "Џ", "џ", "D", "d̂̂"]),
        (
            "e",
            [
                "ë",
                "Ë",
                "É",
                "é",
                "Ě",
                "ě",
                "Ε",
                "ε",
                "Έ",
                "Ὲ",
                "Ἐ",
                "Ἔ",
                "Ἒ",
                "Ἑ",
                "Ἕ",
                "Ἓ",
                "έ",
                "ὲ",
                "ἐ",
                "ἔ",
                "ἒ",
                "ἑ",
                "ἕ",
                "ἓ",
                "È",
                "è",
                "Ê",
                "ê",
                "Е",
                "е",
                "Ё",
                "ё",
                "Є",
                "є",
                "Ѣ",
                "ѣ",
                "Э",
                "э",
                "Ė",
                "ė",
                "Ę",
                "ę",
            ],
        ),
        ("f", ["Φ", "φ", "Ф", "ф"]),
        (
            "g",
            [
                "Γ",
                "γ",
                "Г",
                "г",
                "Ґ",
                "ґ",
                "G",
                "g",
                "Ѓ",
                "ѓ",
                "Ǵ",
                "ǵ",
                "ǵ̀̀",
                "Ğ",
                "ğ",
            ],
        ),
        (
            "h",
            [
                "Η",
                "η",
                "Ή",
                "Ὴ",
                "Ἠ",
                "Ἤ",
                "Ἢ",
                "Ἦ",
                "Ἡ",
                "Ἥ",
                "Ἣ",
                "Ἧ",
                "ή",
                "ὴ",
                "ῆ",
                "ἠ",
                "ἤ",
                "ἢ",
                "ἦ",
                "ἡ",
                "ἥ",
                "ἣ",
                "ἧ",
                "ῌ",
                "ᾘ",
                "ᾜ",
                "ᾚ",
                "ᾞ",
                "ᾙ",
                "ᾝ",
                "ᾛ",
                "ᾟ",
                "ῃ",
                "ῄ",
                "ῂ",
                "ῇ",
                "ᾐ",
                "ᾔ",
                "ᾒ",
                "ᾖ",
                "ᾑ",
                "ᾕ",
                "ᾓ",
                "ᾗ",
            ],
        ),
        (
            "i",
            [
                "Í",
                "í",
                "Ι",
                "ι",
                "Ί",
                "Ὶ",
                "Ἰ",
                "Ἴ",
                "Ἲ",
                "Ἶ",
                "Ἱ",
                "Ἵ",
                "Ἳ",
                "Ἷ",
                "Ϊ",
                "Ῑ",
                "Ῐ",
                "ί",
                "ὶ",
                "ῖ",
                "ἰ",
                "ἴ",
                "ἲ",
                "ἶ",
                "ἱ",
                "ἵ",
                "ἳ",
                "ἷ",
                "ϊ",
                "ΐ",
                "ῒ",
                "ῗ",
                "ῑ",
                "ῐ",
                "Î",
                "î",
                "Ï",
                "ï",
                "ì",
                "Ì",
                "И",
                "и",
                "I",
                "Ī",
                "i",
                "ī",
                "Ї",
                "ї",
                "İ",
                "ı",
            ],
        ),
        ("j", ["Й", "й", "Ĭ", "ĭ", "Ј", "ј", "J", "ǰ̌"]),
        ("k", ["Κ", "κ", "К", "к", "k", "Ќ", "ќ", "Ḱ", "ḱ", "Х", "х"]),
        ("l", ["Λ", "λ", "Л", "л", "Љ", "љ", "L", "l̂̂", "Ł", "ł", "Ĺ", "ĺ", "Ľ", "ľ"]),
        ("m", ["Μ", "μ", "М", "м"]),
        ("n", ["Ň", "ň", "Ν", "ν", "ñ", "Н", "н", "Њ", "њ", "N", "n̂̂", "Ń", "ń"]),
        (
            "o",
            [
                "Ó",
                "ó",
                "Ø",
                "Ö",
                "ö",
                "Ο",
                "ο",
                "Ό",
                "Ὸ",
                "Ὀ",
                "Ὄ",
                "Ὂ",
                "Ὁ",
                "Ὅ",
                "Ὃ",
                "ό",
                "ὸ",
                "ὀ",
                "ὄ",
                "ὂ",
                "ὁ",
                "ὅ",
                "ὃ",
                "Ô",
                "ô",
                "Œ",
                "œ",
                "ő",
                "Ő",
                "ò",
                "Ò",
                "о",
                "О",
                "ø",
                "Õ",
                "õ",
            ],
        ),
        ("p", ["Π", "π", "П", "п"]),
        ("q", ["Θ", "θ"]),
        ("r", ["Ř", "ř", "Ρ", "ρ", "Ῥ", "ῤ", "ῥ", "Р", "р", "Ŕ", "ŕ"]),
        (
            "s",
            [
                "Š",
                "š",
                "Σ",
                "σ",
                "ς",
                "С",
                "с",
                "Ш",
                "ш",
                "Щ",
                "щ",
                "Ŝ",
                "ŝ",
                "Ŝŝ",
                "Ś",
                "ś",
                "Ș",
                "ș",
                "Ş",
                "ş",
            ],
        ),
        ("t", ["Ť", "ť", "Τ", "τ", "Т", "т", "Ț", "ț", "Ţ", "ţ"]),
        (
            "u",
            [
                "Ú",
                "ú",
                "Ů",
                "ů",
                "Ü",
                "ü",
                "Υ",
                "υ",
                "Ύ",
                "Ὺ",
                "Ὑ",
                "Ὕ",
                "Ὓ",
                "Ὗ",
                "Ϋ",
                "Ῡ",
                "Ῠ",
                "ύ",
                "ὺ",
                "ῦ",
                "ὐ",
                "ὔ",
                "ὒ",
                "ὖ",
                "ὑ",
                "ὕ",
                "ὓ",
                "ὗ",
                "ϋ",
                "ΰ",
                "ῢ",
                "ῧ",
                "ῡ",
                "ῠ",
                "Ù",
                "ù",
                "Û",
                "û",
                "ű",
                "Ű",
                "Ŭ",
                "ŭ",
                "Ю",
                "ю",
            ],
        ),
        ("v", ["В", "в",]),
        (
            "w",
            [
                "Ω",
                "ω",
                "Ώ",
                "Ὼ",
                "Ὠ",
                "Ὤ",
                "Ὢ",
                "Ὦ",
                "Ὡ",
                "Ὥ",
                "Ὣ",
                "Ὧ",
                "ώ",
                "ὼ",
                "ῶ",
                "ὠ",
                "ὤ",
                "ὢ",
                "ὦ",
                "ὡ",
                "ὥ",
                "ὣ",
                "ὧ",
                "ῼ",
                "ᾨ",
                "ᾬ",
                "ᾪ",
                "ᾮ",
                "ᾩ",
                "ᾭ",
                "ᾫ",
                "ᾯ",
                "ῳ",
                "ῴ",
                "ῲ",
                "ῷ",
                "ᾠ",
                "ᾤ",
                "ᾢ",
                "ᾦ",
                "ᾡ",
                "ᾥ",
                "ᾣ",
                "ᾧ",
            ],
        ),
        ("x", ["Χ", "χ"]),
        ("y", ["Ý", "ý", "Ψ", "ψ", "Ÿ", "ÿ", "У", "у", "Ў", "ў", "Ы", "ы"]),
        ("z", ["Ž", "ž", "Ζ", "ζ", "Ж", "ж", "Ẑ", "ẑ", "Ź", "ź", "Ż", "ż", "з"]),
        ("ae", ["Æ", "æ"]),
        ("ss", ["ß"]),
        (
            " ",
            [
                "\r",
                "\n",
                "\t",
                '"',
                "\\",
                "’",
                "'",
                "~",
                "!",
                "@",
                "#",
                "$",
                "%",
                "^",
                "&",
                "*",
                "(",
                ")",
                "_",
                "+",
                "-",
                "=",
                "¨",
                "«",
                "»",
                "`",
                "[",
                "]",
                "{",
                "}",
                "|",
                ":",
                "<",
                ">",
                "?",
                ",",
                "/",
                ".",
                "¡",
                "¢",
                "£",
                "¤",
                "¥",
                "¦",
                "§",
                "¨",
                "©",
                "ª",
                "¬",
                "­",
                "®",
                "¯",
                "°",
                "±",
                "²",
                "³",
                "´",
                "µ",
                "¶",
                "·",
                "¸",
                "¹",
                "º",
                "»",
                "¼",
                "½",
                "¾",
                "¿",
                "₤",
                "₠",
                "₡",
                "₢",
                "₣",
                "₧",
                "⅓",
                "⅔",
                "⅛",
                "⅜",
                "⅝",
                "⅞",
                "⅞",
            ],
        ),
    ]

    suffixes_strip = [
        "tarine",
        "tarise",
        "tari",
        "shme",
        "isht",
        "shem",
        "iste",
        "mjet",
        "sore",
        "tare",
        "uar",
        "ore",
        "eve",
        "ave",
        "esi",
        "are",
        "ike",
        "ake",
        "jes",
        "ste",
        "nte",
        "ist",
        "yer",
        "et",
        "ur",
        "te",
        "re",
        "je",
        "ar",
        "en",
        "it",
        "ve",
        "es",
        "in",
        "im",
        "on",
        "ne",
        "a",
        "u",
        "e",
        "i",
    ]

    suffixes_keep = ["are", "ire", "ure", "ore", "ere", "yre"]

    minWordLength = 2

    minRemainingChars = 3

    def stem(self, word):
        word = self.transliterate(word)
        word = self.strip(word)
        word = self.keep(word)
        return word

    def transliterate(self, word):
        for i, value in self.chars:
            for char in value:
                if char in word:
                    word = word.replace(char, i)

        word = word.lower()
        word = re.sub(r"\/s+/", "", word.rstrip())
        return word

    def strip(self, word):
        result = word
        for value in self.suffixes_strip:
            if word[-len(value) :] == value and len(word) > (
                len(value) + self.minRemainingChars
            ):
                result = word[0 : -len(value)]
        return result

    def keep(self, word):
        result = word
        for value in self.suffixes_keep:
            if word[-len(value) :] == value:
                break
        return result
