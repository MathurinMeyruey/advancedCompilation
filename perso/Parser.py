import lark
 
grammaire = """
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
 
    //%ignore /[ ]/
    //OPBINAIRE : /[+\-\/*&<>]/
    // NOMBRE: /[1-9][0-9]*/
 
    VARIABLE : /[a-zA-Z_][a-zA-Z_0-9]*/
 
    OPBINAIRE : "+" | "-" | "*" | "/" | "&" | "<" | ">" | "<=" | ">=" | "<<" | ">>"
 
    NOMBRE: SIGNED_NUMBER
 
    liste_var : VARIABLE ("," VARIABLE)* -> liste_var_seq
                | -> liste_var_vide
 
    expression: VARIABLE    -> exp_var
                | NOMBRE    -> exp_nb
                | expression OPBINAIRE expression -> exp_add
 
    commande :  VARIABLE "=" expression ";"-> com_asgt
                | "printf" "(" expression ")" ";" -> com_printf
                | commande + -> com_seq
                | "while" "(" expression ")" "{" commande "}" -> com_while
                | "if" "(" expression ")" "{" commande "}" "else" "{" commande "}" -> com_if
 
    programme : "main" "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}" -> prog_main
"""
# main : symbole de départ.
# VARIABLE : une suite de lettres et de chiffres.
# main : VARIABLE : la règle de production de main est VARIABLE.
# expression : VARIABLE | NOMBRE : la règle de production de expression est VARIABLE ou NOMBRE
#               ou expression '+' expression qui définit une addition.
 
def pretty_printer(program, indent_level = 0):
    return "main (%s) {\n%sreturn (%s);\n}" % (pretty_printer_var(program.children[0], 0),
                                              pretty_printer_command(program.children[1], 1),
                                              pretty_printer_expression(program.children[2], 0))
 
def pretty_printer_command(command, indent_level = 0):
    if command.data == "com_asgt":
        return "\t" * indent_level + f"{command.children[0].value} = {pretty_printer_expression(command.children[1])};\n"
    elif command.data == "com_printf":
        return "\t" * indent_level + f"printf ({pretty_printer_expression(command.children[0])});\n"
    elif command.data == "com_seq":
        return "\t" * indent_level + f"{pretty_printer_command(command.children[0])}{pretty_printer_command(command.children[1])}"
    elif command.data == "com_while":
        return "\t" * indent_level + f"while ({pretty_printer_expression(command.children[0])}) {{\n{pretty_printer_command(command.children[1])}}}\n"
    elif command.data == "com_if":
        return ("\t" * indent_level +
                f"if ({pretty_printer_expression(command.children[0])}) "
                f"{{ {pretty_printer_command(command.children[1])} }} "
                f"else {{ {pretty_printer_command(command.children[2])} }}")
    else:
        return "\t" * indent_level + pretty_printer_command(command.children[0])
 
 
def pretty_printer_var(variable, indent_level = 0):
    if variable.data == "liste_var_vide":
        return ""
    return "\t" * indent_level + ", ".join([u.value for u in variable.children])
 
def pretty_printer_expression(expression, indent_level = 0):
    if expression.data in ["exp_var", "exp_nb"]:
        return expression.children[0].value
    else:
        return ("\t" * indent_level +
                f"{pretty_printer_expression(expression.children[0])} "
                f"{expression.children[1].value} "
                f"{pretty_printer_expression(expression.children[2])}")
        

        
parser = lark.Lark(grammaire, start='programme')
tree = parser.parse("""
 
main(X,Y) {
    while(X) {
        X = X- 1;
        Y = Y + 1;
    }
    return(X+Y);
}
 
""")
print(pretty_printer(tree))
print(tree)
print(tree.data)