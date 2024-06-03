import lark

grammaire = """
%import common.SIGNED_NUMBER  #bibliothèque lark.
%import common.WS
%ignore WS
// %ignore /[ ]/   #ignore les blancs, mais l'arbre ne contient pas l'information de leur existence. problématique du pretty printer. 

VARIABLE : /(?!p)[a-zA-Z_][a-zA-Z 0-9]*/
POINTEUR : /p[a-zA-Z_][a-zA-Z 0-9]*/
NOMBRE : SIGNED_NUMBER
// NOMBRE : /[1-9][0-9]*/
OPBINAIRE: /[+*\/&><]/|">="|"-"|">>"  //lark essaie de faire les tokens les plus long possible

lhs: VARIABLE -> lhs_variable
| POINTEUR -> lhs_pointeur
|"*" POINTEUR -> lhs_pointeur_dereference

expression: VARIABLE -> exp_variable
| NOMBRE         -> exp_nombre
| expression OPBINAIRE expression -> exp_binaire
| "&" VARIABLE -> exp_adresse
| "*" VARIABLE -> exp_dereferencement
| "malloc" "(" expression ")" -> exp_malloc
| lhs -> exp_lhs

commande : lhs "=" expression ";"-> com_asgt //les exp entre "" ne sont pas reconnues dans l'arbre syntaxique
| "printf" "(" expression ")" ";" -> com_printf
| commande+ -> com_sequence
| "while" "(" expression ")" "{" commande "}" -> com_while
| "if" "(" expression ")" "{" commande "}" "else" "{" commande "}" -> com_if

liste_var :                -> liste_vide
| VARIABLE ("," VARIABLE)* -> liste_normale
programme : "main" "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}" -> prog_main // ressemble à une déclaration de fonction
"""

parser = lark.Lark(grammaire, start = "programme")

t = parser.parse("""main(x,y){
                 *pA=3;
                 pA=&x;
                 *pA=*pA+1;
                 printf(x);
                 return (x);
                }
                 """)
print(t)


def pretty_printer_liste_var(t):
    if t.data == "liste_vide" :
        return ""
    return ", ".join([u.value for u in t.children])    
    
def pretty_printer_lhs(t):
    if t.data in ("lhs_variable","lhs_pointeur"):
        return t.children[0].value
    return "*"+t.children[0].value

def pretty_printer_expression(t):
    if t.data in ("exp_variable", "exp_nombre"):
        return t.children[0].value
    elif t.data == "exp_lhs":
        return pretty_printer_lhs(t.children[0])
    elif t.data == "exp_adresse":
        return "&"+ t.children[0].value
    elif t.data == "exp_dereferencement":
        return "*"+t.children[0].value
    elif t.data=="exp-malloc":
        return "malloc(" + pretty_printer_expression(t.children[0]) +")"
    return f"{pretty_printer_expression(t.children[0])} {t.children[1].value} {pretty_printer_expression(t.children[2])}"

def pretty_printer_commande(t):
    if t.data == "com_asgt":
        return f"{pretty_printer_lhs(t.children[0])} = {pretty_printer_expression(t.children[1])} ;"
    if t.data == "com_printf":
        return f"printf ({pretty_printer_expression(t.children[0])}) ;"
    if t.data == "com_while":
        return "while (%s){ %s}" % (pretty_printer_expression(t.children[0]), pretty_printer_commande(t.children[1]))
    if t.data == "com_if":
        return "if (%s){ %s} else { %s}" % (pretty_printer_expression(t.children[0]), pretty_printer_commande(t.children[1]), pretty_printer_commande(t.children[2]))
    if t.data == "com_sequence":
        return "\n".join([pretty_printer_commande(u) for u in t.children])

def pretty_print(t):
    return  "main (%s) { %s return (%s); }" % (pretty_printer_liste_var(t.children[0]), 
                                               pretty_printer_commande(t.children[1]),
                                                pretty_printer_expression( t.children[2]))

print(pretty_print(t))
#print(t)