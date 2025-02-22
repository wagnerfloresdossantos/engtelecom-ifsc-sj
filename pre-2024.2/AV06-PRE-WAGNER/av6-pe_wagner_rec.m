% Avaliação 06 - REC - PRE 2024.2 Wagner Santos

clear all; close all; clc;

N = 10000;  % Número de realizações
dt = 0.1; t = -5 : dt : 20;  % Vetor dos tempos com resolução ajustada
Nt = length(t);

% (a) Determine e esboce todas as possíveis funções-amostra de 𝑋(𝑡).

% Funções rect(t) deslocadas
rect = @(t) (abs(t) <= 0.5); % Definição da função retângulo
rect1 = @(t) rect((t - 2) / 4);   % rect deslocado e escalado
rect2 = @(t) rect((t - 4) / 8);   % rect deslocado e escalado
rect3 = @(t) rect((t - 6) / 12);  % rect deslocado e escalado

% Simulação de Monte Carlo para as realizações de X(t)
Xt = zeros(N, Nt);
for i = 1 : N
    A = rand < 0.25; % Bernoulli(1/4)
    B = rand < 0.25; % Bernoulli(1/4)
    C = rand < 0.25; % Bernoulli(1/4)
    Xt(i, :) = A * rect1(t) + B * rect2(t) + C * rect3(t);
end

% Esboço de todas as possíveis funções amostra de X(t)
figure; hold on; grid on;
xlabel('t'); ylabel('X(t)');
title('Realizações de X(t) (Possíveis funções-amostra)');
for i = 1 : 8
    % Todas as combinações de A, B, C (2^3 = 8 combinações possíveis)
    A = bitget(i - 1, 1);
    B = bitget(i - 1, 2);
    C = bitget(i - 1, 3);
    stairs(t, A * rect1(t) + B * rect2(t) + C * rect3(t), 'LineWidth', 2);
    pause(0.5);
end

% (b) Determine e esboce a função densidade de probabilidade de primeira ordem de 𝑋(𝑡).

Na = 12;  % Número total de amostras temporais (correspondente a 0 < t < 12)
Xa = zeros(N, Na);

% Gerar as realizações de A, B, C (Bernoulli com p=1/4)
for i = 1:N
    A = rand < 0.25;  % Bernoulli(1/4)
    B = rand < 0.25;  % Bernoulli(1/4)
    C = rand < 0.25;  % Bernoulli(1/4)

    Xa(i, 1:4) = A + B + C;    % Intervalo 0 < t < 4
    Xa(i, 5:8) = B + C;        % Intervalo 4 < t < 8
    Xa(i, 9:12) = C;           % Intervalo 8 < t < 12
end

% Função densidade de probabilidade (PDF) para cada intervalo
interval_1 = Xa(:, 1:4);
interval_2 = Xa(:, 5:8);
interval_3 = Xa(:, 9:12);

values_1 = [0, 1, 2, 3];
values_2 = [0, 1, 2];
values_3 = [0, 1];

% Cálculo das frequências
freq_1 = hist(interval_1(:), values_1) / (N * 4);
freq_2 = hist(interval_2(:), values_2) / (N * 4);
freq_3 = hist(interval_3(:), values_3) / (N * 4);

% Valores teóricos para comparação
freq_1_teo = [27/64, 27/64, 9/64, 1/64];
freq_2_teo = [9/16, 6/16, 1/16];
freq_3_teo = [3/4, 1/4];

% Plotagem
figure;
subplot(3, 1, 1); hold on; grid on;
bar(values_1, freq_1, 'r'); stem(values_1, freq_1_teo, 'b');
title('0 < t < 4'); xlabel('X(t)'); ylabel('P(X(t))'); legend('Simulado', 'Teórico');

subplot(3, 1, 2); hold on; grid on;
bar(values_2, freq_2, 'r'); stem(values_2, freq_2_teo, 'b');
title('4 < t < 8'); xlabel('X(t)'); ylabel('P(X(t))'); legend('Simulado', 'Teórico');

subplot(3, 1, 3); hold on; grid on;
bar(values_3, freq_3, 'r'); stem(values_3, freq_3_teo, 'b');
title('8 < t < 12'); xlabel('X(t)'); ylabel('P(X(t))'); legend('Simulado', 'Teórico');

% (c) Determine e esboce a função média de 𝑋(𝑡).

muX_sim = mean(Xt, 1);
muX_teo = zeros(1, Nt);
muX_teo(t > 0 & t <= 4) = 0.75;  % Intervalo 0 < t < 4
muX_teo(t > 4 & t <= 8) = 0.5;   % Intervalo 4 < t < 8
muX_teo(t > 8 & t <= 12) = 0.25; % Intervalo 8 < t < 12

% Plotagem da função média
figure; hold on; grid on;
plot(t, muX_sim, 'r', 'LineWidth', 2); % Média simulada
plot(t, muX_teo, 'b--', 'LineWidth', 2); % Média teórica
xlabel('t'); ylabel('\mu_X(t)');
title('Função Média de X(t)');
legend('Simulada', 'Teórica');

% (d) Determine a função densidade de probabilidade de segunda ordem de 𝑋(𝑡), considerando
% apenas valores 𝑡1 e 𝑡2 satisfazendo de 0 < 𝑡1 < 4 e −∞ < 𝑡2 < ∞. (Não é necessário esboçar.)
% Valores possíveis de X(t1) e X(t2)

% Função auxiliar para imprimir tabela
function print_joint_prob_table(x_vals_1, x_vals_2, joint_probs, title_text)
    fprintf('\n%s\n', title_text);
    fprintf('    x2 = ');
    fprintf('%6d ', x_vals_2);
    fprintf('\n');
    for i = 1:length(x_vals_1)
        fprintf('x1 = %d ', x_vals_1(i));
        for j = 1:length(x_vals_2)
            fprintf('%7.4f ', joint_probs(i, j));
        end
        fprintf('\n');
    end
    fprintf('\nSoma = %.4f\n', sum(joint_probs(:)));
end

% Caso 0 < t1 < 4 e 0 < t2 < 4, x(t) = A + B + C
x_vals_ABC = 0:3; % Valores possíveis de X(t)
p_x = [27/64, 27/64, 9/64, 1/64]; % Probabilidades marginais
joint_prob_ABC = zeros(4, 4);
for i = 1:length(x_vals_ABC)
    for j = 1:length(x_vals_ABC)
        joint_prob_ABC(i, j) = p_x(i) * p_x(j);
    end
end
print_joint_prob_table(x_vals_ABC, x_vals_ABC, joint_prob_ABC, 'Caso 0 < t1 < 4 e 0 < t2 < 4, x(t) = A + B + C');

% Caso 4 < t1 < 8 e 0 < t2 < 4, x(t1) = B + C, x(t2) = A + B + C
x_vals_BC = 0:2; % Valores possíveis de X(t1)
p_x1_BC = [9/16, 6/16, 1/16]; % Probabilidades marginais para t1
joint_prob_BC_ABC = zeros(3, 4);
for i = 1:length(x_vals_BC)
    for j = 1:length(x_vals_ABC)
        joint_prob_BC_ABC(i, j) = p_x1_BC(i) * p_x(j);
    end
end
print_joint_prob_table(x_vals_BC, x_vals_ABC, joint_prob_BC_ABC, 'Caso 4 < t1 < 8 e 0 < t2 < 4, x(t1) = B + C, x(t2) = A + B + C');

% Caso 8 < t1 < 12 e 0 < t2 < 4, x(t1) = C, x(t2) = A + B + C
x_vals_C = 0:1; % Valores possíveis de X(t1)
p_x1_C = [3/4, 1/4]; % Probabilidades marginais para t1
joint_prob_C_ABC = zeros(2, 4);
for i = 1:length(x_vals_C)
    for j = 1:length(x_vals_ABC)
        joint_prob_C_ABC(i, j) = p_x1_C(i) * p_x(j);
    end
end
print_joint_prob_table(x_vals_C, x_vals_ABC, joint_prob_C_ABC, 'Caso 8 < t1 < 12 e 0 < t2 < 4, x(t1) = C, x(t2) = A + B + C');

% Caso t1 > 12 e t2 > 12, x(t) = 0
joint_prob_zero = zeros(1, 1);
joint_prob_zero(1, 1) = 1; % Probabilidade de x1=0 e x2=0 é 1
print_joint_prob_table([0], [0], joint_prob_zero, 'Caso t1 > 12 e t2 > 12, x(t) = 0');
