extern printf, atol ;déclaration des fonctions externes
global main ; declaration main
section .data ; section des données
long_format: db '%lld',10, 0 ; format pour les int64_t
argc : dq 0 ; copie de argc
argv : dq 0 ; copie de argv
x: dq 0
fy: dq 0
z: dq 0
piA: dq 0
section .text ; instructions
main :push rbp; Set up the stack. Save rbp
mov [argc], rdi
mov [argv], rsi
mov rbx, [argv]
mov rdi, [rbx + 8]
xor rax, rax
call atol
mov [x], rax
mov rbx, [argv]
mov rdi, [rbx + 16]
xor rax, rax
call atol
mov [fy], rax
mov rbx, [argv]
mov rdi, [rbx + 24]
xor rax, rax
call atol
mov [z], rax
mov rbx, [argv]
mov rdi, [rbx + 32]
xor rax, rax
call atol
mov [piA], rax
mov [fy], rax
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
mov [z], rax
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
mov [piA], rax
mov [piA], rax
mov [piA], rax
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
pop rbp
xor rax, rax
ret
