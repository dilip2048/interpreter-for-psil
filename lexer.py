import sys
import re

# Standardised token names for easy referencing
SYM     = 'SYMBOL'
NUM     = 'NUMBER'
VAR     = 'VARIABLE'

# Bunch of regular expressions for detecting each type of atom
token_exprs = [
    (r'\+',                    SYM),
    (r'\-',                    SYM),
    (r'\*',                    SYM),
    (r'\/',                    SYM),
    (r'bind',                  SYM),
    (r'frac',                  SYM),
    (r'[0-9]+',                NUM),
    (r'[A-Za-z][A-Za-z0-9_]*', VAR),
]

# Cleans the input code by removing all whitespaces and then splits into tokens
# Input : Entire multiline input string
# Returns : a list of tokens which includes parentheses '(' and ')'
def segment(characters):
    return characters.replace('(',' ( ').replace(')',' ) ').strip(' \t\n\r').split()

# Decides which token belongs to what type and returns a tuple containing the value and token type
# Input : a single token (string) and the regex mapping for every token type
# Returns : tuple containing value and token type
def categorize(token, token_exprs):
    for token_expr in token_exprs:
        pattern, tag = token_expr
        regex = re.compile(pattern)
        if regex.match(token):
            return (token, tag)

# Builds a generalised tree type structure based on parentheses levels
# Input : takes a list of tokens including the parenteses ( and )
# Returns : Dynamic list with structured set of {token : token type} tuples
def lex(characters):
    if len(characters)==0:
        raise SyntaxError('No more tokens!')
    token = characters.pop(0)
    if token=='(':
        stack = []
        while characters[0] != ')':
            stack.append(lex(characters))
        characters.pop(0) # pop off ')'
        return stack
    elif ')' == token:
        raise SyntaxError('extra )')
    else:
        return categorize(token, token_exprs)

# Lex deals with one Parentheses block at a time. Superlex allows it to group all such pairs.
def superlex(characters):
    token_list=[]
    while len(characters)>0:
        token_list.append(lex(characters))
    return token_list
