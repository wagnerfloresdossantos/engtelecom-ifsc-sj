% PRE029006 - PROCESSOS ESTOCÁSTICOS (2024 .2 - T01)
% Avaliação 8
% Aluno: Wagner Santos

clear all; close all; clc;

% Parâmetros da simulação
N = 10000;  % Número de realizações (experimentos)
Na = 100;   % Número de amostras no tempo
ns = 1 : Na;  % Vetor dos tempos (discreto)
maxlag = 10;  % Atraso máximo
ells = -maxlag : maxlag;  % Eixo dos atrasos (discreto)

% Gerar o processo estocástico X[n] ~ N(0,4)
X = sqrt(4) * randn(N, Na);

% ------------------------------------------------------------------------------
% (a) A função autocovariância de 𝑋[𝑛]. Esboce.
% ------------------------------------------------------------------------------

% Calcular a média teórica e simulada
muX_teo = zeros(1, Na);  % Média teórica (zero para todo n)
muX_sim = mean(X);        % Média estimada

% Cálculo da autocovariância teórica e simulada
CX_teo = 4 * (ells == 0);  % Impulso unitário escalado por 4
CX_sim = cov(X(:, Na/2), X(:, Na/2 + ells)); % Estimativa empírica

% Comparação da autocovariância simulada vs teórica
figure;
hold on; grid on;
stem(ells, CX_sim, 'g', 'LineWidth', 6);
stem(ells, CX_teo, 'b', 'LineWidth', 2);
xlabel('ℓ'); ylabel('C_X[ℓ]');
title('Autocovariância de X[n]: Simulada vs Teórica');
legend('Simulada', 'Teórica');

% ------------------------------------------------------------------------------
% (b) A função autocovariância de 𝑌 [𝑛], sem utilizar análise no domínio da frequência. Esboce.
% ------------------------------------------------------------------------------

% Construir Y[n] = 4X[n] - 3X[n-1]
Y = zeros(N, Na);
Y(:, 1) = 4 * X(:, 1);  % Primeiro termo sem X[n-1]
for n = 2 : Na
  Y(:, n) = 4 * X(:, n) - 3 * X(:, n-1);
end

% Cálculo da média teórica e simulada
muY_teo = zeros(1, Na);  % Média teórica (zero para todo n)
muY_sim = mean(Y);        % Média estimada

% Cálculo da autocovariância teórica
CX_teo = 4 * (ells == 0);  % C_X[ℓ] = 4δ[ℓ]
CY_teo = 25 * CX_teo - 12 * [CX_teo(2:end), 0] - 12 * [0, CX_teo(1:end-1)];

% Cálculo da autocovariância simulada
CY_sim = zeros(1, length(ells));
for i = 1 : length(ells)
    CY_sim(i) = cov(Y(:, Na/2), Y(:, Na/2 + ells(i)));
end

% Comparação da autocovariância simulada vs teórica
figure;
hold on; grid on;
stem(ells, CY_sim, 'g', 'LineWidth', 6);
stem(ells, CY_teo, 'b', 'LineWidth', 2);
xlabel('ℓ'); ylabel('C_Y[ℓ]');
title('Autocovariância de Y[n]: SEM análise no domínio da frequência');
legend('Simulada', 'Teórica');

% ------------------------------------------------------------------------------
% (c) A função autocovariância de 𝑌 [𝑛], utilizando análise no domínio da frequência.
% ------------------------------------------------------------------------------

% Cálculo da autocovariância teórica de Y[n] no domínio da frequência
CY_teofreq = 100 * (ells == 0) - 48 * (ells == -1) - 48 * (ells == 1);

% Cálculo da autocovariância simulada de Y[n]
CY_simfreq = cov(Y(:, Na/2), Y(:, Na/2 + ells));

% Plotando os resultados
figure;
stem(ells, CY_simfreq, 'g', 'LineWidth', 6); hold on; grid on;
stem(ells, CY_teofreq, 'b', 'LineWidth', 2);
xlabel('ℓ'); ylabel('C_Y[ℓ]');
legend('Simulado', 'Teórico');
title('Autocovariância de Y[n] - Análise no domínio da frequência');

% ------------------------------------------------------------------------------
% (d) A função densidade de probabilidade de 𝑌 [5].
% ------------------------------------------------------------------------------

% Gerar Y[5] = 4X[5] - 3X[4]
Y5 = 4 * X(:,5) - 3 * X(:,4);

% Parâmetros teóricos
mu_Y5 = 0;                % Média de Y[5]
var_Y5 = 100;             % Variância de Y[5]
sigma_Y5 = sqrt(var_Y5);  % Desvio padrão

% Estimativa da PDF via histograma normalizado
[y_counts, y_bins] = hist(Y5, 50); % 50 bins para suavizar
bin_width = y_bins(2) - y_bins(1);
pdf_sim = y_counts / (N * bin_width); % Normalização

% PDF teórica de Y[5]: f_Y(y) = (1 / (10 * sqrt(2π))) * exp(-y^2 / 200)
y_teo = linspace(min(Y5), max(Y5), 100);
pdf_teo = (1 / (sigma_Y5 * sqrt(2 * pi))) * exp(- (y_teo .^ 2) / (2 * var_Y5));

% Plotando a densidade de probabilidade
figure; hold on; grid on;
bar(y_bins, pdf_sim, 'FaceColor', [0.7 0.7 1], 'EdgeColor', 'b'); % Simulação
plot(y_teo, pdf_teo, 'r', 'LineWidth', 2); % Teórica
xlabel('y'); ylabel('f_Y(y)');
legend('Monte Carlo', 'Teórico');
title('Densidade de Probabilidade de Y[5]');

% ------------------------------------------------------------------------------
% (e) A covariância entre 𝑌 [5] e 𝑌 [6].
% ------------------------------------------------------------------------------

% Definir Y[5] e Y[6]
Y5 = 4 * X(:,5) - 3 * X(:,4);
Y6 = 4 * X(:,6) - 3 * X(:,5);

% Estimativa de covariância via Monte Carlo
C_Y_sim = cov(Y5, Y6)

% Covariância teórica
C_Y_teo = -48

% ------------------------------------------------------------------------------
% (f) Pr[𝑌 [5] > 0 | 𝑌 [3] = 1]
% ------------------------------------------------------------------------------

% Definir Y[3] e Y[5]
Y3 = 4 * X(:,3) - 3 * X(:,2);
Y5 = 4 * X(:,5) - 3 * X(:,4);

% Selecionar apenas as amostras onde Y[3] = 1 (aproximado)
tolerancia = 0.1;
idx = abs(Y3 - 1) < tolerancia;

% Calcular a fração de casos onde Y[5] > 0, dado Y[3] ≈ 1
P_Y5_dado_Y3 = sum(Y5(idx) > 0) / sum(idx)

% Resultado teórico
P_Y5_teo = 0.5

