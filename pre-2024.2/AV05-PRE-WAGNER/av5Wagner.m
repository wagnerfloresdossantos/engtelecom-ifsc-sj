% Wagner - Questão: 5

close all; clear all; clc;

pkg load statistics

N = 10000000;

mu = [0; 0; 0];  % Vetor média

C = [5 0 2 ;
     0 4 0;       % Matriz covariância
     2 0 3];

vetX = mvnrnd(mu, C, N);  % Gera uma matriz com o vetor média e a matriz covariância fornecidos
X1 = vetX(:, 1)';           % O vetor X1, terá os valores da primeira coluna de vetX
X2 = vetX(:, 2)';           % O vetor X2, terá os valores da segunda coluna de vetX
X3 = vetX(:, 3)';           % O vetor X3, terá os valores da terceira coluna de vetX


% ----------------------------------------------------------------------------

% (a) Pr[2 ≤ X1 ≤ 3].


Pr_a_sim = mean((2 <= X1) & (X1 <= 3))
Pr_a_teo = normcdf(3 / sqrt(5)) - normcdf(2 / sqrt(5))

% ----------------------------------------------------------------------------

% (b) Pr[2 ≤ X1 ≤ 3 | X2 = 2].


X_b_cond = X1(abs(X2 - 2) < 0.1);

Pr_b_sim = mean((2 <= X_b_cond) & (X_b_cond <= 3))
Pr_b_teo = normcdf(3 / sqrt(5)) - normcdf(2 / sqrt(5))

% ----------------------------------------------------------------------------

% (c) Pr[2 ≤ X1 ≤ 3 | X2 = 2 e X3 = 3].

X_c_cond = X1(abs(X2 - 2) < 0.1 & abs(X3 - 3) < 0.1);

Pr_c_sim = mean((2 <= X_c_cond) & (X_c_cond <= 3))
Pr_c_teo = normcdf((3 - 2) / sqrt(11/3)) - normcdf((2 - 2) / sqrt(11/3))

% ----------------------------------------------------------------------------

% (d) Pr[X1 − X3 > 4].

Pr_d_sim = mean((X1 - X3) > 4)
Pr_d_teo = 1 - normcdf((4-0)/sqrt(4))
