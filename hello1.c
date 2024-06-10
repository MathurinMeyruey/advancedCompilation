main(x,fy,z,piA){
    fy = fy+1.0;
    printf(fy);
    z=1;
    printf(z);
    *piA=3;
    piA=&x;
    *piA=*piA+1;
    printf(x);
    return (fy);
}