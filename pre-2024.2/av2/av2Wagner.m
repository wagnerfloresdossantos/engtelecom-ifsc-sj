% Wagner - Questão 10

% ----------------------------------------------------------------------------

% a) PMF conjunta de X e Y.

close all; clear all; clc;

N = 10000;

X = zeros(1, N);
Y = zeros(1, N);

% Gerando o X e o Y
for i = 1 : N
  B = randi([0 1], 1, 4);   % Sorteia B1, B2, B3, B4 de Unif({0,1})

  X(i) = sum(B);             % Definicao de X como soma de B's
  Y(i) = prod(B);            % Definicao de Y como o produto dos B's
end

x = 0 : 4;          % O 'x' vai de 0 a 4
y = [0, 1];         % O 'y' pode ser 0 ou 1

% Matriz para armazenar as ocorrências conjuntas
histXY = zeros(5, 2);

for i = 1 : 5
  for j = 1 : 2
    histXY(i, j) = sum(X == x(i) & Y == y(j));
  end
end

pmfXY_sim = histXY / N;
pmfXY_teo = [1/16 0;
             4/16 0;
             6/16 0;
             4/16 0;
             0    1/16];

disp('PMF Conjunta Simulada:');
disp(pmfXY_sim);
disp('PMF Conjunta Teórica:');
disp(pmfXY_teo);

% ----------------------------------------------------------------------------

% b) PMFs marginais de X e Y

% PMF marginal de X
pmfX_sim = hist(X, x) / N;
pmfX_teo = [1/16 4/16 6/16 4/16 1/16];

% PMF marginal de Y
pmfY_sim = hist(Y, y) / N;
pmfY_teo = [15/16 1/16];

figure;
subplot(2, 2, 1); hold on; grid on;
bar(x, pmfX_sim, 'y');
stem(x, pmfX_teo, 'b', 'LineWidth', 4);
xlabel('x'); ylabel('p_X(x)');
title('PMF de X');

subplot(2, 2, 2); hold on; grid on;
bar(y, pmfY_sim, 'y');
stem(y, pmfY_teo, 'b', 'LineWidth', 4);
xlabel('y'); ylabel('p_Y(y)');
title('PMF de Y');

% ----------------------------------------------------------------------------

% c) PMFs condicionais de X dado que Y = y, para y ∈ {0, 1}

pmfX_condY_sim = zeros(2, 5);

XcondY = X(Y == 0); % Condicional para Y = 0
pmfX_condY_sim(1, :) = hist(XcondY, x) / sum(Y == 0);

XcondY = X(Y == 1); % Condicional para Y = 1
pmfX_condY_sim(2, :) = hist(XcondY, x) / sum(Y == 1);

% PMFs condicionais teóricas
pmfX_condY_teo = [1/15 4/15 6/15 4/15 0;
                  0 0 0 0 1];

subplot(2, 2, 3); hold on; grid on;
bar(x, pmfX_condY_sim(1, :), 'y');
stem(x, pmfX_condY_teo(1, :), 'b', 'LineWidth', 4);
xlabel('x'); ylabel(sprintf('p_X(x | Y = 0)'));
title('PMF Condicional: X | Y = 0');

subplot(2, 2, 4); hold on; grid on;
bar(x, pmfX_condY_sim(2, :), 'y');
stem(x, pmfX_condY_teo(2, :), 'b', 'LineWidth', 4);
xlabel('x'); ylabel(sprintf('p_X(x | Y = 1)'));
title('PMF Condicional: X | Y = 1');
