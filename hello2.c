main(c,piA,x,y,z){
    piA=&x;
    z=x+y;
    printf(z);
    z=z+1;
    printf(z);
    piA=&x;
    z=z+*piA;
    printf(z);
    *piA=*piA + 1;
    piA=&c;
    x=*piA+1;
    return (x);
}