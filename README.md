# advancedCompilation
Advanced Compilation project


**Pour compiler : **

python3 main1.py hello1.c hello1.asm

nasm -f elf64 hello1.asm

gcc -no-pie hello1.o

./a.out <x> <fy> <z> <piA>10 12



-Exemles de code en nanoc
-nos principes de compilation ("""Gamma(E1), push rax...""")
-limites ou problèmes

main(X, Y){
    while(X){
        X=X-1;
        Y=Y+1;
    }
    return (Y);
}

main(x,fy,z,piA){
    while(x>0) {
        fy = fy+1.0;
        printf(fy);
        x=x-1;
    }
    z=1;
    printf(z);
    *piA=3;
    piA=&x;
    *piA=*piA+1;
    printf(x);
    return (fy);
}