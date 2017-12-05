#!/usr/bin/env python

'''
	Contains defines of base JPath tokens and rules of their parsing
'''

# Define metadata
__version__ 	= '1.0.0'
__author__ 		= 'Vladimir Saltykov'
__copyright__ 	= 'Copyright 2017, Vladimir Saltykov'
__email__ 		= 'vowatchka@mail.ru'
__license__ 	= "MIT"
__date__ 		= '2017-12-04'

# Import modules and packages
import jpathpy.utils as utils

# Define token names
tokens = (
			'ROOT',
			'SIMPLESELECTOR',
			'DEEPSELECTOR',
			'STRING',
			'LPAREN',
			'RPAREN',
			'LSQUAREPAREN',
			'RSQUAREPAREN',
			'FUNCNAME',
			'DELIMPARAMS',
			'SLICE',
			'MINUS',
			'PLUS',
			'MULT',
			'DIV',
			'MOD',
			'NOT',
			'EQ',
			'NE',
			'LT',
			'LE',
			'GT',
			'GE',
			'AND',
			'OR',
			'INT',
			'FLOAT',
			'TRUE',
			'FALSE',
			'NULL',
			'UNION'
		)

# Define token values
t_ROOT 				= r'\$'
t_SIMPLESELECTOR 	= r'\.'
t_DEEPSELECTOR 		= r'\.{2}'
t_STRING 			= r'"([\u0020-\u0021\u0023-\u005B\u005D-\uFFFF]|\\(["\\\/bfnrt]|u[0-9ABCDEF]{4}))*"'
t_LPAREN 			= r'\('
t_RPAREN 			= r'\)'
t_LSQUAREPAREN 		= r'\['
t_RSQUAREPAREN 		= r'\]'
t_FUNCNAME 			= r'[a-zA-Z][a-zA-Z0-9_]*'
t_DELIMPARAMS 		= r','
t_SLICE 			= r':'
t_MINUS 			= r'\-'
t_PLUS 				= r'\+'
t_MULT 				= r'\*'
t_DIV 				= r'\/'
t_MOD 				= r'%'
t_NOT 				= r'!'
t_EQ 				= r'='
t_NE 				= r'!='
t_LT 				= r'\<'
t_LE 				= r'\<='
t_GT 				= r'\>'
t_GE 				= r'\>='
t_UNION 			= r'\|'

def t_AND(t):
	r'[aA][nN][dD]'
	t.value = t.value.lower()
	return t
	
def t_OR(t):
	r'[oO][rR]'
	t.value = t.value.lower()
	return t

# t_FLOAT must be defined early than t_INT
def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t
	
def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t
	
def t_TRUE(t):
	r'[tT][rR][uU][eE]'
	t.value = t.value.lower()
	return t
	
def t_FALSE(t):
	r'[fF][aA][lL][sS][eE]'
	t.value = t.value.lower()
	return t
	
def t_NULL(t):
	r'[nN][uU][lL]{2}'
	t.value = t.value.lower()
	return t

# Define ignored tokens
t_ignore = ' \t'

# Define token rule
def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
   
# Define error rule
def t_error(t):
	if t == None:
		raise utils.JLexicalError('Unexpected end of JPath query')
	else:
		if t.value[0] == '\\' and t.value[1] != '\\':
			message = 'Unescaped char "' + t.value[0] + '"'
		else:
			message = 'Invalid syntax'
		raise utils.JLexicalError(message, t.lineno, t.lexpos)
	t.lexer.skip(1)