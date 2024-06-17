# advancedCompilation
Advanced Compilation project


POUR COMPILER : 

python3 main1.py hello1.c hello1.asm

nasm -f elf64 hello1.asm

gcc -no-pie hello1.o

./a.out x fy z piA (remplacer par les valeurs souhaitées)

pour l'input 1 1 2 3, on attend l'output 2 1 0 2


EXEMPLE DE CODE : 

Les fichiers hello1.c et hello2.c consistent en des exemples de code pour tester notre compilateur.


AVANCEMENT DU PROJET : 

Actuellement, le pretty printer marche et le fichier Parser1 semble correct. Cependant, l'exécution du fichier Compile1 renvoie des erreurs, probablement au niveau de la gestion des flottants : pour hello1.c on obtient 3 2 2 2 et non pas 2 1 0 2 comme output.
Par contre, pour hello2.c, l'execution fonctionne bien.


NOS PRINCIPES DE COMPILATION :

Nous avons codé dans notre grammaire plusieurs types de bases : INT_VARIABLE, FLOAT_VARIABLE, ENTIER, FLOAT, OPBINAIRE, POINTEUR_INT et POINTEUR_FLOAT.

Les deux types de variables et de pointeurs sont rassemblés dans des surtypes "variable" et "pointeur"

Nos autres types principaux sont programme, liste_var, commande, exp_binaire et lhs.

Une expression peut être une exp_binaire_int, une exp_binaire_float, une exp_binaire_pointeur ou une exp_malloc.

Un lhs peut être une variable, un pointeur ou un lhs_pointeur_dereference.