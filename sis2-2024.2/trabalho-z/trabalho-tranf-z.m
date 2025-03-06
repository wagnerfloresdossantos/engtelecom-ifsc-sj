clear all; close all; clc;

% Trabalho Transformada Z
% Acesso núvem: ssh nome@191.36.8.56 -XC


% 1.2) Diagrama de polos e zeros
b = [1];
a = [1 1 0.21];

figure;
zplane(b, a);
title('1.2 - Diagrama de Polos e Zeros');
grid on;

% Raízes
disp('Raízes do denominador (polos):');
roots(a)

disp('Raízes do numerador (zeros):');
roots(b)

% 1.3) Decomposição em frações parciais
[r, p, k] = residuez(b, a);


% 1.4) Resposta ao impulso
n = 20;
h = impz(b, a, n);

figure;
stem(0:n-1, h, 'filled', 'LineWidth', 1.5);
title('1.4 - Resposta ao Impulso');
grid on;

% 1.6) Resposta em frequência
w = 0:pi/100:pi;
[H, w] = freqz(b, a, w);

figure;
subplot(2,1,1);
plot(w, abs(H));
title('1.6 - Módulo da Resposta em Frequência');
grid on;

subplot(2,1,2);
plot(w, angle(H));
title('1.6 - Fase da Resposta em Frequência');
grid on;

% 1.7) Sinal de entrada
n = 0:20;
x = (1 - 0.8.^n);

figure;
stem(n, x, 'filled', 'LineWidth', 1.5);
title('1.7 - Sinal de Entrada');
grid on;

% 1.8) Transformada Z do sinal de entrada
syms n z;
x = (1 - 0.8^n); % Corrigido parêntese ausente
X_Z = ztrans(x, n, z);
disp('1.8 - Transformada Z do sinal de entrada:');
pretty(X_Z);

% 1.9) Representação do sinal de entrada no plano Z
a = poly([1 0.8]);
b = [0 0.2];

figure;
zplane(b, a);
title('1.9 - Sinal de Entrada no Plano Z');
grid on;

% 1.10) TZ da resposta do sistema ao sinal de entrada
a = poly([-0.3, -0.7, 1, 0.8]);
b = [0 0.2];

figure;
zplane(b, a);
title('1.10 - Resposta do Sistema no Plano Z');
grid on;

% 1.11) Resolução da TZ da resposta ao sinal de entrada
a = poly([-0.3, -0.7, 1, 0.8]);
b = [0 0.2];

[r, p, k] = residuez(b, a);
syms z;
disp('1.11 - Transformada inversa:');
iztrans(r(1)/(1 - p(1)*z.^(-1)) - r(2)/(1 - p(2)*z.^(-1)) + r(3)/(1 - p(3)*z.^(-1)) + r(4)/(1 - p(4)*z.^(-1)))

% 1.14) Representação da resposta completa
n = 20;
vec = 0:(n-1);
x = 0.03146 * (-0.3).^vec - 0.09607 * (-0.7).^vec + 0.45248 - 0.38787 * (0.8).^vec;

figure;
stem(vec, x, 'filled', 'LineWidth', 1.5);
title('1.14 - Resposta Completa');
grid on;

% 1.15) Resposta ao sinal de entrada usando filter
n = 20;
vec = 0:(n-1);
a = [1 1 0.21];
b = [1];
x = 1 - 0.8.^(vec);

y = filter(b, a, x);

figure;
stem(vec, y, 'filled', 'LineWidth', 1.5);
title('1.15 - Resposta ao Sinal de Entrada com filter');
grid on;

% 1.16) Resposta às condições iniciais usando filtic
a = [1 1 0.21];
b = [1];
y = [1 1];
r = filtic(b, a, y);
disp('1.16 - Resposta às Condições Iniciais com filtic:');
disp(r);

% 1.18) Transformada inversa da resposta às condições iniciais
a = [1, 1, 0.21];
b = [-1.21 -0.21];

[r, p, k] = residuez(b, a);
syms z;

disp('1.18 - Transformada inversa:');
iztrans(r(1)/(1 - p(1)*z.^(-1)) + r(2)/(1 - p(2)*z.^(-1)))

% 1.20) Resposta completa às condições iniciais
n = 20;
vec = 0:(n-1);
x = 0.413 * (-0.3).^vec - 1.688*(-0.7).^vec + 0.452 - 0.387 * (-0.8).^vec;

figure;
stem(vec, x, 'filled', 'LineWidth', 1.5);
title('1.20 - Resposta Completa às Condições Iniciais');
grid on;

% 1.21) Resposta ao sinal de entrada considerando condições iniciais
n = 20;
vec = 0:(n-1);
a = [1 1 0.21];
b = [1];
c = [1 1];

x = 1 - 0.8.^(vec);
xic = filtic(b, a, c);
y = filter(b, a, x, xic);

figure;
stem(vec, y, 'filled', 'LineWidth', 1.5);
title('1.21 - Resposta ao Sinal de Entrada com Condições Iniciais');
grid on;
