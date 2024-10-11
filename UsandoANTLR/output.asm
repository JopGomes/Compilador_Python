main:
push ebp
mov ebp, esp
sub esp, 4  ;
sub esp, 4  ;
sub esp, 4  ;
mov eax, 3  ;
mov [ebp-12], eax  ; 
mov eax, 4  ;
mov [ebp-12], eax  ; 
mov eax, cateto_1*cateto_1+cateto_2*cateto_2  ;
mov [ebp-12], eax  ; 
mov esp, ebp
pop ebp
ret