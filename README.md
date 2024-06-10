# advancedCompilation
Advanced Compilation project

Pour compiler : 

python3 main1.py hello1.c hello1.asm

nasm -f elf64 hello1.asm

gcc -no-pie hello1.o

./a.out 10 12
