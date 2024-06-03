import lark

cpt = 0 

def compile(ast):
    asmString = ""
    asmString += "extern printf, atel ;déclaration des fonction externes\n"
    asmString += "global main ; déclaration main \n"
    asmString += "section .data ; section des données\n"
    asmString += "long_format: db '%lld', 10, 0 ;format pour les int_64\n"
    asmString += "argc : dq 0 ; copie de argc"
    asmString += "argv : dq 0 ; copie de argv"
    
    
    return asmString
    
def variable_declaration(ast):
    asmVar = ""
    vars = set()
    if ast.data != "liste_vide":
        for child in ast.children:
            asmVar += f"{child.value}: dq 0\n"
            vars.add(child.value)
    return asmVar, vars

def initMainVar(ast):
    asmVar = ""
    if ast.data != "liste_vide":
        index=0
        for child in ast:
    return asmVar
            
def compilReturn(ast):
    asmVar = compilPrintf(ast)
    return asmVar

def compilCommand(ast):
    asmVar = ""
    if ast.data == "com_while":
        asmVar += compilWhile(ast)
    elif ast.data == "com_if":
        asmVar += compilIf(ast)
    elif ast.data == "com_sequence":
        for child in ast:
            asmVar += compilCommand(child)
    elif ast.data =="com_asgt":
        asmVar+= compilAsgt(ast)
    elif ast.data == "com_printf":
        asmVar += compilPrintf(ast)
    return asmVar

def compilWhile(ast):
    global cpt
    cpt+=1
    return f"""
            loop{cpt} : {compilExpression(ast.children[0])}
                cmp rax, 0
                jz fin{cpt}
                {compilCommand(ast.children[1])}
                jmp loop{cpt}
            fin{cpt} :
        """

def compilIf(ast):
    global cpt
    cpt+=1
    return f"""
            {compilExpression(ast.children[0])}
            cmp rax, 0
            jz fin{cpt}
            {compilCommand(ast.children[1])}
            fin{cpt} :
        """
        
def compilSequence(ast):
    asm =""
    for child in ast.children:
        asm += compilCommand(child)
    return asm

def compilAsgt(ast):
    asm = compilExpression(ast.children[1])
    asm += f"mov [{ast.children[0].value}], rax \n"
    return asm

def compilPrintf(ast):
    asm = compilExpression(ast.children[0])
    asm+= "mov rsi, rax \n"
    asm+= "mov rdi, fmt \n"
    asm+= "xor rax, rax \n"
    asm+= "call printf \n"
    return asm
            
def compilExpression(ast):
    if ast.data =="VARIABLE":
        return f"mov rax, [{ast.children[0].value}]\n"
    elif ast.data == "NOMBRE":
        return f"mov rax, [{ast.children[0].value}]\n"
    elif ast.data == "OPBINAIRE":
        return f"""
                {compilExpression(ast.children[2].value)}
                push rax
                {compilExpression(ast.children[0].value)}
                pop rbx
                add rax, rbx
        """