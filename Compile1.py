import lark

cpt = 0

op2asm = {"+": "add rax, rbx", "-": "sub rax, rbx"}

def compile(ast):
    asmString = ""
    asmString = asmString + "extern printf, atol ;déclaration des fonctions externes\n"
    asmString = asmString + "global main ; declaration main\n"
    asmString = asmString + "section .data ; section des données\n"
    asmString = asmString + "long_format: db '%lld',10, 0 ; format pour les int64_t\n"
    asmString = asmString + "argc : dq 0 ; copie de argc\n"
    asmString = asmString + "argv : dq 0 ; copie de argv\n"
    asmVar, vars = variable_declaration(ast.children[0])
    asmString = asmString + asmVar
    asmString = asmString + "section .text ; instructions\n"
    asmString += "main :"
    asmString += "push rbp; Set up the stack. Save rbp\n"
    asmString += "mov [argc], rdi\n"
    asmString += "mov [argv], rsi\n"
    asmString += initMainVar(ast.children[0])
    asmString += compilCommand(ast.children[1])
    asmString += compilReturn(ast.children[2])
    asmString += "pop rbp\n"
    asmString += "xor rax, rax\n"
    asmString += "ret\n"
    return asmString

def variable_declaration(ast) :
    asmVar = ""
    vars = set()
    if ast.data != "liste_vide":
        for child in ast.children:
            if 'f' in child.value:
                asmVar += f"{child.value}: dq 0\n"
            elif 'pi' in child.value or 'pf' in child.value:
                asmVar += f"{child.value}: dq 0\n"
            else:
                asmVar += f"{child.value}: dq 0\n"
            vars.add(child.value)
    return asmVar, vars

def initMainVar(ast):
    asmVar = ""
    if ast.data != "liste_vide":
        index = 0
        for child in ast.children:
            asmVar += "mov rbx, [argv]\n"
            asmVar += f"mov rdi, [rbx + { 8*(index+1)}]\n"
            asmVar += "xor rax, rax\n"
            asmVar += "call atol\n"
            asmVar += f"mov [{child.value}], rax\n"
            index += 1
    return asmVar

def compilReturn(ast):
    asm = compilExpression(ast)
    asm += "mov rsi, rax \n"
    asm += "mov rdi, long_format \n"
    asm += "xor rax, rax \n"
    asm += "call printf \n"
    return asm

def compilCommand(ast):
    asmVar = ""
    if ast.data == "com_while":
        asmVar = compilWhile(ast)
    elif ast.data == "com_if":
        asmVar = compilIf(ast)
    elif ast.data == "com_sequence":
        asmVar = compilSequence(ast)
    elif ast.data == "com_asgt":
        asmVar = compilAsgt(ast)
    elif ast.data == "com_printf":
        asmVar = compilPrintf(ast)
    return asmVar

def compilWhile(ast):
    global cpt
    cpt += 1
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
    cpt += 1
    return f""" 
            {compilExpression(ast.children[0])}
            cmp rax, 0
            jz fin{cpt}
            {compilCommand(ast.children[1])}
            fin{cpt} :
        """

def compilSequence(ast):
    asm = ""
    for child in ast.children :
        asm +=compilCommand(child)
    return asm

def compilAsgt(ast):
    asm = compilExpression(ast.children[1])
    lhs_variable = ast.children[0].children[0]
    variable_name = lhs_variable.children[0].value
    if lhs_variable.data == "lhs_pointeur_dereference":
        asm += f"mov rax, QWORD PTR [{variable_name}]\n"
        asm += f"mov DWORD PTR [rax], edx\n"
    elif lhs_variable.data == "lhs_pointeur":
        asm += f"mov QWORD PTR [{variable_name}], rax\n"
    else:
        asm += f"mov [{variable_name}], rax\n"
    return asm

def compilPrintf(ast):
    asm = compilExpression(ast.children[0])
    asm += "mov rsi, rax \n"
    asm += "mov rdi, long_format \n"
    asm += "xor rax, rax \n"
    asm += "call printf \n"
    return asm

def compilExpression(ast):
    if ast.data == "exp_bin_int":
        return compilBinInt(ast)
    elif ast.data == "exp_bin_float":
        return compilBinFloat(ast)
    elif ast.data == "exp_pointeur":
        return f"mov rax, [{ast.children[0].children[0].value}]\n"
    elif ast.data == "exp_adresse":
        return f"lea rax, [{ast.children[0].children[0].value}]\n"
    elif ast.data == "exp_malloc":
        return f"""
                mov rdi, {ast.children[0].value}
                call malloc
                """    
    return ""

def compilBinInt(ast):
    asm = ""
    if ast.children[0].data == "exp_bin_rec":
        tempoAst = ast.children[0]
        if tempoAst.children[0].data == "exp_int_variable":
            print(tempoAst.children[0].children[0].value)
            asm += f"mov rax, [{tempoAst.children[0].children[0].value}]\n"
        elif tempoAst.children[0].data == "exp_entier":
            asm += f"mov rax, {tempoAst.children[0].children[0].value}\n"
        elif tempoAst.children[0].data == "exp_pointeur_deref_int":
            asm += f"mov rcx, [{tempoAst.children[0].children[0].value}]\n"
            asm += f"mov rax, [rcx]\n"
            asm += f"xor rcx, rcx\n"
        if tempoAst.children[2].data == "exp_int_variable":
            print(tempoAst.children[2].children[0].value)
            asm += f"mov rbx, [{tempoAst.children[2].children[0].value}]\n"
        elif tempoAst.children[2].data == "exp_entier":
            asm += f"mov rbx, {tempoAst.children[2].children[0].value}\n"
        elif tempoAst.children[2].data == "exp_pointeur_deref_int":
            asm += f"mov rcx, [{tempoAst.children[2].children[0].value}]\n"
            asm += f"mov rbx, [rcx]\n"
            asm += f"xor rcx, rcx\n"
        asm += op2asm[tempoAst.children[1].value] + "\n"
    return asm

def compilBinFloat(ast):
    asm = ""
    if ast.children[0].data == "exp_bin_rec":
        tempoAst = ast.children[0]
        if tempoAst.children[0].data == "exp_float_variable":
            print(tempoAst.children[0].children[0].value)
            asm += f"mov rax, [{tempoAst.children[0].children[0].value}]\n"
        elif tempoAst.children[0].data == "exp_float":
            asm += f"mov rax, {tempoAst.children[0].children[0].value}\n"
        elif tempoAst.children[0].data == "exp_pointeur_deref_float":
            asm += f"mov rcx, [{tempoAst.children[0].children[0].value}]\n"
            asm += f"mov rax, [rcx]\n"
            asm += f"xor rcx, rcx\n"
        if tempoAst.children[2].data == "exp_float_variable":
            print(tempoAst.children[2].children[0].value)
            asm += f"mov rbx, [{tempoAst.children[2].children[0].value}]\n"
        elif tempoAst.children[2].data == "exp_float":
            asm += f"mov rbx, {tempoAst.children[2].children[0].value}\n"
        elif tempoAst.children[2].data == "exp_pointeur_deref_float":
            asm += f"mov rcx, [{tempoAst.children[2].children[0].value}]\n"
            asm += f"mov rbx, [rcx]\n"
            asm += f"xor rcx, rcx\n"
        asm += op2asm[tempoAst.children[1].value] + "\n"
    return asm

        