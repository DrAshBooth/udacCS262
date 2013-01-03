'''
Created on Jan 2, 2013

@author: Ash Booth
'''

if __name__ == '__main__':
    
    webpage = "hello <!-- a comment --> all"

    import ply.lex as lex
    
    tokens = ('LANGLE', # <
              'LANGLESLASH', # </
              'RANGLE', # >
              'EQUAL', # =
              'STRING', # "hello"
              'WORD', # Welcome!
              )
    
    states = (
              ('htmlcomment','exclusive'),
              )
    
    t_ignore = ' ' # shortcut for whitespace
    
    # html
    def t_htmlcomment(token):
        r'<!--'
        token.lexer.begin('htmlcomment')
        
    def t_htmlcomment_end(token):
        r'-->'
        token.lexer.lineno += token.value.count('\n')
        token.lexer.begin('INITIAL')
        
    def t_htmlcomment_error(token):
        token.lexer.skip(1)
        
    def t_newline(token):
        r'\n'
        token.lexer.lineno += 1
        pass
    
    def t_LANGLESLASH(token):
        r'</'
        return token
    
    def t_LANGLE(token):
        r'<'
        return token
    
    def t_RANGLE(token):
        r'>' 
        return token
    
    def t_EQUAL(token):
        r'='
        return token
    
    def t_STRING(token):
        r'"[^"]*"'
        token.value = token.value[1:-1]
        return token
    
    def t_WORD(token):
        r'[^ <>\n]+'
        return token
    
    def t_error(token):
        pass
    
    # JavaScript
    
    def t_NUMBER(token):
        r'-?[0-9]+(?:\.[0-9]*)?'
        token.value = float(token.value)
        return token
    
    def t_eolcomment(token):
        r'//[^\n]*'
        pass
    
    # Grammar stuff
    grammar = [
               ("exp", ["exp", "+", "exp"]),
               ("exp", ["exp", "-", "exp"]),
               ("exp", ["(", "exp", ")"]),
               ("exp", ["num"]),
               ]
    
    def expand(tokens, grammar):
        for pos in range(len(tokens)): # for every token
            for rule in grammar: # compare for every rule in the grammar
                if tokens[pos]==rule[0]:
                    yield tokens[0:pos] + rule[1] + tokens[pos+1:]
        
    htmllexer = lex.lex()
    htmllexer.input(webpage)
    while True:
        tok = htmllexer.token()
        if not tok: break
        print tok
    
    
