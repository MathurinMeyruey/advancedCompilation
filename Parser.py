import lark

grammaire = """
%import common.INT  #bibliothèque lark.
%import common.WS
%ignore WS

INT_VARIABLE : /(?!f)[a-zA-Z_][a-zA-Z 0-9]*/
FLOAT_VARIABLE : /f[a-zA-Z_][a-zA-Z0-9]*/
ENTIER : INT
FLOAT : /-?\d+\.\d+/
OPBINAIRE: /[+*\/&><]/|">="|"-"|">>"  //lark essaie de faire les tokens les plus longs possible

expression: exp_binaire_int -> exp_bin_int
| exp_binaire_float -> exp_bin_float

exp_binaire_int : INT_VARIABLE -> exp_int_variable
| ENTIER -> exp_entier
| exp_binaire_int OPBINAIRE exp_binaire_int -> exp_bin_rec

exp_binaire_float : FLOAT_VARIABLE -> exp_float_variable
| FLOAT -> exp_float
| expression OPBINAIRE exp_binaire_float -> exp_bin_float_rec

commande : INT_VARIABLE "=" expression ";"-> com_asgt //les exp entre "" ne sont pas reconnues dans l'arbre syntaxique
| FLOAT_VARIABLE "=" expression ";" -> com_float_asgt
| "printf" "(" expression ")" ";" -> com_printf
| commande+ -> com_sequence
| "while" "(" expression ")" "{" commande "}" -> com_while
| "if" "(" expression ")" "{" commande "}" "else" "{" commande "}" -> com_if

liste_var :                -> liste_vide
| (INT_VARIABLE |FLOAT_VARIABLE) ("," (INT_VARIABLE | FLOAT_VARIABLE))* -> liste_normale

programme : "main" "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}" -> prog_main // ressemble à une déclaration de fonction
"""

parser = lark.Lark(grammaire, start = "programme")

t = parser.parse("""main(x,fy,z){
                 while(x) {
                    fy = fy + 1.0;
                    printf(fy);
                 }
                z = 1;
                 printf(z);
                 return (fy);
                }
                 """)

def pretty_printer_liste_var(t):
    if t.data == "liste_vide" :
        return ""
    return ", ".join([u.value for u in t.children])

def pretty_printer_expression(t):
    if t.data in ("exp_entier", "exp_int_variable", "exp_float", "exp_float_variable"):
        return t.children[0].value
    elif t.data in ("exp_bin_int", "exp_bin_float"):
        return pretty_printer_expression(t.children[0])
    return f"{pretty_printer_expression(t.children[0])} {t.children[1].value} {pretty_printer_expression(t.children[2])}"

def pretty_printer_commande(t):
    if t.data in ("com_asgt", "com_float_asgt"):
        return f"{t.children[0].value} = {pretty_printer_expression(t.children[1])} ;"
    if t.data == "com_printf":
        return f"printf({pretty_printer_expression(t.children[0])}) ; \n"
    if t.data == "com_while":
        return "while (%s){\n %s}" % (pretty_printer_expression(t.children[0]), pretty_printer_commande(t.children[1]))
    if t.data == "com_if":
        return "if (%s){\n %s \n} \nelse {\n %s}" % (pretty_printer_expression(t.children[0]), pretty_printer_commande(t.children[1]), pretty_printer_commande(t.children[2]))
    if t.data == "com_sequence":
        return "\n".join([pretty_printer_commande(u) for u in t.children])

def pretty_print(t):
    return  "main (%s) { %s return (%s); }" % (pretty_printer_liste_var(t.children[0]), 
                                               pretty_printer_commande(t.children[1]),
                                                pretty_printer_expression( t.children[2]))

print(t)
print(pretty_print(t))