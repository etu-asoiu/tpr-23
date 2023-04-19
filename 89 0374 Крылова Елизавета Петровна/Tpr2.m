cost = [150, 150, 350, 200, 100];
lim = [0 1 1 0 0;
0 1 1 1 0; 
0 1 1 1 0;
1 1 1 1 1;
1 0 1 1 0;
1 0 1 1 1;
1 1 1 1 1;
1 0 1 1 0;
1 0 0 1 1;
1 0 1 1 1;
1 0 1 1 1;
0 0 1 1 1];

vec = [1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1];

ctype = "LLLLLLLLLLLL";
vartype = "IIIII";
sense = 1;
[xmin, Fmin, error_code, extra]=glpk(cost, lim, vec, [0; 0; 0; 0; 0], [1; 1; 1; 1; 1], ctype, vartype, sense)