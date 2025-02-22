% Avaliação 07 - PRE - 2024.2 - Wagner Santos - Questão 3

clear all; close all; clc;

% Parâmetros
N = 1000;  % Número de realizações
dt = 0.01; t = 0 : dt : 10;  % Vetor de tempo
Nt = length(t);

lambda1 = 1.5;  % Taxa do processo X1
lambda2 = 1.0;  % Taxa do processo X2
lambda = lambda1 + lambda2;  % Taxa total do processo X(t)

% Simulação do processo Poisson combinado X(t)
X = zeros(N, Nt);
for i = 1 : N
  T = 0;
  while T < t(end)
    DELTA = rande() / lambda;
    T += DELTA;
    X(i, :) += t > T;
  end
end

% (a) Determine e esboce a função média do processo estocástico 𝑋(𝑡).
muX_teo = lambda * t;  % Teórico
muX_sim = mean(X);     % Simulado

figure; hold on; grid on;
for i = 1 : 100
  stairs(t, X(i, :));
end
plot(t, muX_sim, 'm', 'LineWidth', 6);
plot(t, muX_teo, 'b', 'LineWidth', 3);
xlabel('t (s)'); ylabel('X(t)');

%(b) Determine a probabilidade de ocorrer pelo menos três eventos
%entre 4 e 5 s, dado que ocorreram exatamente dois eventos entre 2 e 3 s.

t1 = 4; t2 = 5; t3 = 2; t4 = 3;  % Intervalos
idx1 = round((t1 - t(1)) / dt) + 1;
idx2 = round((t2 - t(1)) / dt) + 1;
idx3 = round((t3 - t(1)) / dt) + 1;
idx4 = round((t4 - t(1)) / dt) + 1;

X24 = X(:, idx4) - X(:, idx3);  % Eventos entre 2 e 3
X15 = X(:, idx2) - X(:, idx1);  % Eventos entre 4 e 5
P_cond_sim = mean(X15(X24 == 2) >= 3)
P_cond_teo = 1 - exp(-lambda) - lambda * exp(-lambda) - (lambda^2 / 2) * exp(-lambda)

% (c) Determine a probabilidade de que o tempo decorrido entre o
% quinto evento e o sexto evento seja maior que 0,5 s.

ev1 = 5; ev2 = 6;  % Eventos
T5 = zeros(1, N);
T6 = zeros(1, N);
for i = 1 : N
  idx5 = find(X(i, :) >= ev1, 1);
  idx6 = find(X(i, :) >= ev2, 1);
  T5(i) = t(idx5);
  T6(i) = t(idx6);
end
P_gap = mean((T6 - T5) > 0.5)

% d) Determine a matriz covariância do vetor aleatório [𝑋(4) 𝑋(7)] 𝖳 .

tA = 4; tB = 7;  % Instantes de tempo
idxA = round((tA - t(1)) / dt) + 1;
idxB = round((tB - t(1)) / dt) + 1;
X4 = X(:, idxA);
X7 = X(:, idxB);
COV = cov(X4, X7)



