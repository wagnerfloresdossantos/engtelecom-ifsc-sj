% Wagner Santos - Questão 9

% ----------------------------------------------------------------------------

% b) Pr[X >= Y]

clc; close all; clear all;

N = 100000;  % Número de experimentos probabilísticos

X = zeros(1, N);
Y = zeros(1, N);

i = 1;
while i <= N
  % Geração de X e Y baseados nas regiões especificadas
  X(i) = 40 * rand() -10;  % -10 <= X <= 30
  Y(i) = 20 * rand();       % 0 <= Y <= 20

  % Condição para definir a região de suporte
  if (X(i) >= -10 && X(i) <= 30 && Y(i) >= 0 && Y(i) <= 20)!= (0 <= X(i) && X(i) <= 20 && 0 <= Y(i) && Y(i) <= 10)
    i = i + 1;
  end
end

PrX_maior_igual_Y_sim = mean(X >= Y)
PrX_maior_igual_Y_teo = 0.417  % Valor teórico calculado previamente


% ----------------------------------------------------------------------------

% c) PDF marginal de Y

y = 0 : 0.5 : 20;

histY = hist(Y, y);
pdfY_sim = histY / trapz(y, histY);  % Normalização pelo trapézio
pdfY_teo = (1 / 30) * (y >= 0 & y <= 10) + (1 / 15) * (y > 10 & y <= 20);

figure
subplot(3, 1, 1); grid on; hold on;
bar(y, pdfY_sim, 'y');  % Histograma da simulação
plot(y, pdfY_teo, 'b', 'LineWidth', 4);  % Curva teórica
xlabel('y'); ylabel('f_Y(y)');
title('PDF marginal de Y');

% ----------------------------------------------------------------------------

% d) CDF marginal de Y

cdfY_sim = cumsum(histY) / N;  % CDF a partir da PDF simulada
cdfY_teo = (y / 30) .* (y >= 0 & y <= 10) + (1 / 3 + (y - 10) / 15) .* (y > 10 & y <= 20);

subplot(3, 1, 2); grid on; hold on;
plot(y, cdfY_sim, 'g', 'LineWidth', 4);  % Simulação
plot(y, cdfY_teo, 'b--', 'LineWidth', 2);  % Curva teórica
xlabel('y'); ylabel('F_Y(y)');
xlim([0 20]);
title('CDF marginal de Y');

% ----------------------------------------------------------------------------

% e) PDF condicional de Y dado que X = 5.

idx = (X >= 5 - 1) & (X <= 5 + 1);  % Pegar valores de X próximos de 5
histY_condX = hist(Y(idx), y);
pdfY_condX_sim = histY_condX / trapz(y, histY_condX);  % Normalização
pdfY_condX_teo = (1 / 10) * (y >= 10 & y <= 20);

subplot(3, 1, 3); grid on; hold on;
bar(y, pdfY_condX_sim, 'y');
plot(y, pdfY_condX_teo, 'b', 'LineWidth', 4);
xlabel('y'); ylabel('f_{Y|X=5}(y)');
title('PDF condicional de Y dado X=5');

% ----------------------------------------------------------------------------

% f) Covariância entre X e Y

E_X = 10;  % Valor esperado de X calculado previamente
E_Y = 35 / 3;  % Valor esperado de Y calculado previamente
E_XY = 116.667;  % Valor esperado de XY calculado previamente

% f) Covariância entre X e Y

rhoXY_sim = cov(X, Y) / sqrt(var(X) * var(Y))
covXY_teo = E_XY - E_X * E_Y
covXY_sim = cov(X, Y)

