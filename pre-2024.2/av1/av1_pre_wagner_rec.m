clear all; close all; clc;

N = 1000000;  % Número de realizações

% Simulação dos resultados do dado (valores de 1 a 6)
U = randi(6, 1, N); % Simula números inteiros entre 1 e 6
X = zeros(1, N);

% Definição das variáveis aleatórias baseadas no valor de U
idx1 = (U == 1); % Caso U = 1 -> X = -5
idx2 = (U == 2 | U == 3); % Caso U = 2 ou 3 -> X ~ Unif([-8, 2])
idx3 = (U == 4 | U == 5); % Caso U = 4 ou 5 -> X ~ Unif([-2, 8])
idx4 = (U == 6); % Caso U = 6 -> X = 5

% Atribuição de valores para cada caso
X(idx1) = -5; % U = 1
X(idx2) = -8 + (2 + 8) * rand(1, sum(idx2)); % Unif([-8, 2])
X(idx3) = -2 + (8 + 2) * rand(1, sum(idx3)); % Unif([-2, 8])
X(idx4) = 5; % U = 6

% Definição do intervalo de x para a simulação
dx = 0.1; x = -10 : dx : 10;

% Cálculo da PDF simulada
pdfX_sim = hist(X, x) / (N * dx);

% Cálculo da PDF teórica (sem os impulsos de Dirac)
pdfX_teo = (1/30) .* (-8 <= x & x <= 2) + ... % Região Unif([-8, 2])
           (1/30) .* (-2 <= x & x <= 8);      % Região Unif([-2, 8])

% Cálculo da CDF simulada
cdfX_sim = cumsum(pdfX_sim) * dx;

% Cálculo da CDF teórica
cdfX_teo = (0) .* (x < -8) + ...  % Antes de -8
           ((x + 8) / 30) .* (-8 <= x & x < -5) + ... % Entre -8 e -5
           (1/6 + (x + 5) / 30) .* (-5 <= x & x < -2) + ... % Entre -5 e -2
           (1/6 + (x + 2) / 30) .* (-2 <= x & x < 2) + ... % Entre -2 e 2
           (2/6 + (x - 2) / 30) .* (2 <= x & x < 5) + ... % Entre 2 e 5
           (3/6 + (x - 5) / 30) .* (5 <= x & x < 8) + ... % Entre 5 e 8
           1 .* (x >= 8); % Após 8

% Cálculo da probabilidade P(5 <= X <= 10)
prob_sim = sum(X >= 5 & X <= 10) / N;

% Exibição da probabilidade simulada
fprintf('Probabilidade simulada de 5 <= X <= 10: %g\n', prob_sim);

% Plotagem das PDFs
figure;

subplot(2, 1, 1); hold on; grid on;
bar(x, pdfX_sim, 'y'); % Histograma da PDF simulada
plot(x, pdfX_teo, 'b', 'LineWidth', 4); % PDF teórica

% Representando os impulsos:
plot([-5, -5], [0, 1/6], 'b', 'LineWidth', 4);
plot(-5, 1/6, 'b^', 'MarkerSize', 12, 'MarkerFaceColor', 'b');
plot([5, 5], [0, 1/6], 'b', 'LineWidth', 4);
plot(5, 1/6, 'b^', 'MarkerSize', 12, 'MarkerFaceColor', 'b');

% Limites e rótulos do gráfico de PDF
xlim([-10 10]); ylim([-0.1, 0.2]);
xlabel('x'); ylabel('f_X(x)');

% Plotagem das CDFs
subplot(2, 1, 2); hold on; grid on;
plot(x, cdfX_sim, 'y', 'LineWidth', 4);
plot(x, cdfX_teo, 'b--', 'LineWidth', 2);

% Limites e rótulos do gráfico de CDF
xlim([-10 10]); ylim([-0.1, 2]);
xlabel('x'); ylabel('F_X(x)');

% Exibindo valores esperados (média)
fprintf('Sim: E[X] = %g\n', mean(X));

