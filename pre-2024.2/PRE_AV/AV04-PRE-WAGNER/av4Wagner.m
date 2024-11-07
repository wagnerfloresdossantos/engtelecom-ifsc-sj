% Wagner Santos - Questão 7

% ----------------------------------------------------------------------------

% a) Vetor média e matriz de covariância de Y

clc; close all; clear all;

N = 100000;  % Número de experimentos probabilísticos

X1 = zeros(1, N);
X2 = zeros(1, N);
Y1 = zeros(1, N);
Y2 = zeros(1, N);
Y3 = zeros(1, N);

i = 1;
while i <= N
  % Geração de X1 e X2 com distribuição uniforme em [-2, 1]
  X1(i) = -2 + (1 + 2) * rand();  % X1 ~ Unif([-2, 1])
  X2(i) = -2 + (1 + 2) * rand();  % X2 ~ Unif([-2, 1])

  % Definir Y1, Y2, e Y3
  Y1(i) = X1(i)^2;
  Y2(i) = X2(i)^2;
  Y3(i) = X1(i) * X2(i);

  i = i + 1;
end

% Vetor média de Y
muY_sim = mean([Y1; Y2; Y3], 2)
muY_teo = [1, 1, 1/4]'

% Matriz de covariância de Y
covY_sim = cov([Y1; Y2; Y3]')
covY_sim = [6/5 0 0; 0 6/5 0; 0 0 15/16]
% ----------------------------------------------------------------------------

% b) Vetor média e matriz de covariância de Z

Z1 = Y1;
Z2 = Y1 + Y2;
Z3 = Y1 + Y2 + Y3;

% Vetor média de Z
muZ_sim = mean([Z1; Z2; Z3], 2)
muZ_teo = [1 2 9/4]'

% Matriz de covariância de Z
covZ_sim = cov([Z1; Z2; Z3]')
covZ_teo = [6/5 6/5 6/5; 6/5 12/15 12/5; 6/5 12/5 15/5]
