extern printf

section .data
hello: db "Hello world", 10, 0 ; en c, équivalent d'un char *hello="Hello world"

section .text
global main

main:
    push rbp
    cmp rdi,1
    jne fin
    mov rdi, hello
    mov rsi,42
    mov rax,0
    call printf
fin:
    pop rbp
    ret

;dans le terminal, on execute avec nasm -f elf64 hum.asm
; et ensuite, gcc -no-pie hum.o