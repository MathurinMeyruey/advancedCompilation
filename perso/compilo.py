import lark 

grammaire = """
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
//%ignore /[ ]/
OPBINAIRE : /[+*\/&|<>]/|">="|"-"|">>" // on met des backslash avant le - et le /, car sinon ils seraient interpretes par la machine
VARIABLE : /[a-zA-Z_][a-zA-Z_0-9]*/
NOMBRE : SIGNED_NUMBER // remplace grosso modo :/[1-9][0-9]*/
expression : VARIABLE -> exp_variable
//lhs : VARIABLE|...
| NOMBRE -> exp_nombre
| expression OPBINAIRE expression -> exp_binaire
commande: VARIABLE "=" expression ";" -> com_asgt // toutes les expressions qui sont entre guillemets dans les regles disparaissent des arbres, ce sont simplement deds mots clefs.
|"printf" "(" expression ")" ";" -> com_printf
| commande+ -> com_sequence
|"while" "(" expression ")" "{" commande "}" -> com_while
|"if" "(" expression ")" "{" commande "}" "else" "{" commande "}" ->com_if
liste_var : -> liste_vide
|VARIABLE ("," VARIABLE)* -> liste_normale
programme : "main" "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}"
"""

parser = lark.Lark(grammaire, start="liste_var")



t= parser.parse("""X,Y

""")
print(t)
"""
print(t.data)
u = t.children[0]
print(u.value)
print(u.type)"""