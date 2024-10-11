grammar Grammar;

program         : lde;
lde             : lde de | de;
de              : df | dt;

df              : 'function' idd '(' lp ')' ':' t b;
dt              : 'type' idd '=' 'array' '[' NUM ']' 'of' t
                | 'type' idd '=' 'struct' '{' dc '}'
                | 'type' idd '=' t;
dc              : dc ';' li ':' t | li ':' t;
lp              : lp ',' idd ':' t | idd ':' t;
b               : '{' ldv ls '}';
ldv             : ldv dv | dv;
ls              : ls s | s;
dv              : 'var' li ':' t ';';
li              : li ',' idd | idd;
s               : 'if' '(' e ')' s
                | 'if' '(' e ')' s 'else' s
                | 'while' '(' e ')' s
                | 'do' s 'while' '(' e ')' ';'
                | b
                | lv '=' e ';'
                | 'break' ';'
                | 'continue' ';';
e               : e '&&' l
                | e '||' l
                | l;
l               : l '<' r
                | l '>' r
                | l '<=' r
                | l '>=' r
                | l '==' r
                | l '!=' r
                | r;
r               : r '+' y
                | r '-' y
                | y;
y               : y '*' f
                | y '/' f
                | f;
f               : lv
                | '++' lv
                | '--' lv
                | lv '++'
                | lv '--'
                | '(' e ')'
                | idu '(' le ')'
                | '-' f
                | '!' f
                | TRUE
                | FALSE
                | CHR
                | STR
                | NUM;
le              : le ',' e | e;
lv              : lv '.' Id
                | lv '[' e ']'
                | idu;
idd             : Id;
idu             : Id;

t               : 'integer'
                | 'char'
                | 'boolean'
                | 'string'
                | idu; 

TRUE            : 'true';
FALSE           : 'false';
CHR             : '\'' . '\'';
STR             : '"' .*? '"';
NUM             : [0-9]+;
Id              : [a-zA-Z_][a-zA-Z_0-9]*;

WS              : [ \t\r\n]+ -> skip;
