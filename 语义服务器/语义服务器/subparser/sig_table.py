SIG_TABLE_DICT = {
    'if' : 0,
    'else' : 1,
    'while' : 2,
    'read' : 3,
    'write' : 4,
    'int' : 5,
    'real' : 6,
    '+' : 7,
    '-' : 8,
    '*' : 9,
    '/' : 10,
    '=' : 11,
    '<' : 12,
    '>' : 13,
    '==' : 14,
    '<>' : 15,
    '(' : 16,
    ')' : 17,
    ';' : 18,
    '{' : 19,
    '}' : 20,
    '/*' : 21,
    '*/' : 22,
    '[' : 23,
    ']' : 24,
    'constnum' : 25,
    'identity' : 26,
    '#': 27,
    'comment': 28,
    ',': 29,
    '<=': 30,
    '>=':31
}

INT = 0
REAL = 1

def get_key(value):
    return [k for k, v in SIG_TABLE_DICT.items() if v == value]