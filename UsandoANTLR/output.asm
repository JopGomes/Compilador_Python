main:
push ebp
mov ebp, esp
sub esp, 4  ; alocando vari�vel cateto_1
sub esp, 4  ; alocando vari�vel cateto_2
sub esp, 4  ; alocando vari�vel hipotenusa_quadrado
mov eax, 3  ; carrega valor ou vari�vel simples
mov [ebp-12], eax  ; atribui a cateto_1
mov eax, 4  ; carrega valor ou vari�vel simples
mov [ebp-12], eax  ; atribui a cateto_2
mov eax, cateto_1*cateto_1+cateto_2*cateto_2  ; carrega valor ou vari�vel simples
mov [ebp-12], eax  ; atribui a hipotenusa_quadrado
mov esp, ebp
pop ebp
ret