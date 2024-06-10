import lark

grammaire = """
%import common.INT
%import common.WS
%ignore WS

INT_VARIABLE : /(?!f)[a-zA-Z_][a-zA-Z 0-9]*/
FLOAT_VARIABLE : /f[a-zA-Z_][a-zA-Z0-9]*/
ENTIER : INT
FLOAT : /-?\d+\.\d+/
POINTEUR : /p[a-zA-Z_][a-zA-Z 0-9]*/
OPBINAIRE: /[+*\/&><]/|">="|"-"|">>"  //lark essaie de faire les tokens les plus long possible

lhs: INT_VARIABLE -> lhs_int_variable
| FLOAT_VARIABLE -> lhs_float_variable
| POINTEUR -> lhs_pointeur
|"*" POINTEUR -> lhs_pointeur_dereference

expression: exp_binaire_int -> exp_bin_int
| exp_binaire_float -> exp_bin_float
| "&" VARIABLE -> exp_adresse
| "*" VARIABLE -> exp_dereferencement
| "malloc" "(" expression ")" -> exp_malloc
| lhs -> exp_lhs

exp_binaire_int : INT_VARIABLE -> exp_int_variable
| ENTIER -> exp_entier
| exp_binaire_int OPBINAIRE exp_binaire_int -> exp_bin_rec

exp_binaire_float : FLOAT_VARIABLE -> exp_float_variable
| FLOAT -> exp_float
| expression OPBINAIRE exp_binaire_float -> exp_bin_float_rec

commande : lhs "=" expression ";"-> com_asgt //les exp entre "" ne sont pas reconnues dans l'arbre syntaxique
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
                    fy = fy+1.0;
                    printf(fy);
                    }
                  z=1;
                  printf(z);
                 *pA=3;
                 pA=&x;
                 *pA=*pA+1;
                 printf(x);
                 return (fy);
                }
                 """)
print(t)


def pretty_printer_liste_var(t):
    if t.data == "liste_vide" :
        return ""
    return ", ".join([u.value for u in t.children])    
    
def pretty_printer_lhs(t):
    if t.data in ("lhs_int_variable", "lhs_float_variable","lhs_pointeur"):
        return t.children[0].value
    return "*"+t.children[0].value

def pretty_printer_expression(t):
    if t.data in ("exp_entier", "exp_int_variable", "exp_float", "exp_float_variable"):
        return t.children[0].value
    elif t.data in ("exp_bin_int", "exp_bin_float"):
        return pretty_printer_expression(t.children[0])
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
