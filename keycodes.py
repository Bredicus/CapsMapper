cpKeySecondary = {
    "!": "!",
    "@": "@",
    "#": "#",
    "$": "$",
    "%": "%",
    "^": "^",
    "*": "*",
    "&": "&",
    "(": "(",
    ")": ")",
    "_": "_",
    "+": "+",
    "{": "{",
    "}": "}",
    "|": "|",
    ":": ":",
    "\"": "\"",
    "<": "<",
    ">": ">",
    "?": "?"
}

cpKeyToDisplayName = {
    "tic": "`",
    "equal": "=",
    "open_bracket": "[",
    "close_bracket": "]",
    "backslash": "\\",
    "semicolon": ";",
    "quote": "'",
    "comma": ",",
    "period": ".",
    "slash": "/"
}

cpKeyToCode = {
    "esc": 1,
    "f1": 59,
    "f2": 60,
    "f3": 61,
    "f4": 62,
    "f5": 63,
    "f6": 64,
    "f7": 65,
    "f8": 66,
    "f9": 67,
    "f10": 68,
    "f11": 87,
    "f12": 88,
    "tic": 41,
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "6": 7,
    "7": 8,
    "8": 9,
    "9": 10,
    "0": 11,
    "-": 12,
    "equal": 13,
    "backspace": 14,
    "tab": 15,
    "q": 16,
    "w": 17,
    "e": 18,
    "r": 19,
    "t": 20,
    "y": 21,
    "u": 22,
    "i": 23,
    "o": 24,
    "p": 25,
    "open_bracket": 26,
    "close_bracket": 27,
    "backslash": 43,
    "a": 30,
    "s": 31,
    "d": 32,
    "f": 33,
    "g": 34,
    "h": 35,
    "j": 36,
    "k": 37,
    "l": 38,
    "semicolon": 39,
    "quote": 40,
    "enter": 28,
    "Lshift": 42,
    "z": 44,
    "x": 45,
    "c": 46,
    "v": 47,
    "b": 48,
    "n": 49,
    "m": 50,
    "comma": 51,
    "period": 52,
    "slash": 53,
    "Rshift": 54,
    "Lctrl": "ctrl",
    "Lwin": 91,
    "Lalt": "alt",
    "space": 57,
    "Ralt": "right alt",
    "Rwin": 92,
    "menu": 93,
    "Rctrl": "right ctrl",
    "insert": "insert",
    "delete": "delete",
    "decimal": "decimal",
    "home": "home",
    "end": "end",
    "PgUp": "page up",
    "PgDn": "page down",
    "left": "left",
    "up": "up",
    "right": "right",
    "down": "down",
    "clear": "clear",
    "!": "shift+1",
    "@": "shift+2",
    "#": "shift+3",
    "$": "shift+4",
    "%": "shift+5",
    "^": "shift+6",
    "&": "shift+7",
    "*": "*",
    "(": "shift+9",
    ")": "shift+0",
    "_": "shift+-",
    "+": "+",
    "{": "shift+[",
    "}": "shift+]",
    "|": "shift+\\",
    ":": "shift+;",
    "\"": "shift+\'",
    "<": "shift+<",
    ">": "shift+.",
    "?": "shift+/"
}

cpSpecialKeyCodeDict = {
    29: True,
    56: True,
    28: True,
    53: True,
    69: True,
    55: True,
    82: True,
    83: True,
    71: True,
    79: True,
    73: True,
    81: True,
    75: True,
    72: True,
    77: True,
    80: True,
    76: True
}

cpKeyCodeNameDict = {
    "ctrl": "Lctrl",
    "right ctrl": "Rctrl",
    "alt": "Lalt",
    "right alt": "Ralt",
    "enter": "enter",
    "/": "slash",
    "pause": "pause",
    "print screen": "PrntScrn",
    "insert": "insert",
    "delete": "delete",
    "home": "home",
    "end": "end",
    "page up": "PgUp",
    "page down": "PgDown",
    "left": "left",
    "up": "up",
    "right": "right",
    "down": "down"
}

cpNumpadKeyCodeNameDict = {
    "enter": "enter",
    "/": "slash",
    "num lock": "numlock",
    "*": "*",
    "0": "0",
    "insert": "insert",
    "decimal": "decimal",
    "delete": "delete",
    "7": "7",
    "home": "home",
    "1": "1",
    "end": "end",
    "9": "9",
    "page up": "PgUp",
    "3": "3",
    "page down": "PgDn",
    "4": "4",
    "left": "left",
    "8": "8",
    "up": "up",
    "6": "6",
    "right": "right",
    "2": "2",
    "down": "down",
    "5": "5",
    "clear": "clear"
}

cpKeyCodeDict = {
    1: "esc",

    59: "f1",
    60: "f2",
    61: "f3",
    62: "f4",
    63: "f5",
    64: "f6",
    65: "f7",
    66: "f8",
    67: "f9",
    68: "f10",
    87: "f11",
    88: "f12",  

    41: "tic",

    2: "1",
    3: "2",
    4: "3",
    5: "4",
    6: "5",
    7: "6",
    8: "7",
    9: "8",
    10: "9",
    11: "0",

    12: "-",
    13: "equal",
    14: "backspace",

    15: "tab",

    16: "q",
    17: "w",
    18: "e",
    19: "r",
    20: "t",
    21: "y",
    22: "u",
    23: "i",
    24: "o",
    25: "p",
    
    26: "open_bracket",
    27: "close_bracket",
    43: "backslash",
    
    58: "caps",

    30: "a",
    31: "s",
    32: "d",
    33: "f",
    34: "g",
    35: "h",
    36: "j",
    37: "k",
    38: "l",
    
    39: "semicolon",
    40: "quote",
    
    42: "Lshift",
    
    44: "z",
    45: "x",
    46: "c",
    47: "v",
    48: "b",
    49: "n",
    50: "m",
    
    51: "comma",
    52: "period",
    54: "Rshift",

    91: "Lwin",
    57: "space",
    92: "Rwin",
    93: "menu",

    70: "scroll_lock",

    78: "+",
    74: "-"
}

class KeyData:
    def __init__(self, code, key):
        self.code = code
        self.key = key

def GetKeySet(event):
    keyname = cpKeySecondary.get(event.name, False)
    if keyname:
        return KeyData(event.name, keyname)

    keyname = cpSpecialKeyCodeDict.get(event.scan_code, False)
    if keyname:
        code = event.name
        key = False
        if event.is_keypad:
            key = cpNumpadKeyCodeNameDict.get(code, False)
        if False == key:
            key = cpKeyCodeNameDict.get(code, False)
        return KeyData(code, key) if False != key else key
        
    code = event.scan_code
    key = cpKeyCodeDict.get(code, False)
    return KeyData(code, key) if False != key else key
