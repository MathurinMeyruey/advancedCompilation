# advancedCompilation
Advanced Compilation project


**Pour compiler : **

python3 main1.py hello1.c hello1.asm

nasm -f elf64 hello1.asm

gcc -no-pie hello1.o

./a.out <x> <fy> <z> <piA>
pour l'input 1 1 2 3, on attend l'output 2 1 0 2


Le fichier hello1.c consiste en un exemple de code pour tester notre compilateur.


Actuellement, le pretty printer marche et le fichier Parser1 semble correct. Cependant, l'exécution du fichier Compile1 renvoie des erreurs : on obtinet 3 2 2 2 et non pas 2 1 0 2 comme output.


-nos principes de compilation ("""Gamma(E1), push rax...""")