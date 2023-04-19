## Задача 3
##
## Очистка командного окна и переменных
 clc; clear all; clf;
 printf("Старт работы программы\n");
## Вероятность получения аккумулятором единицы
## энергии в каждый временной слот.
 q = 0.2;
## Количество слотов времени.
 timeSlotsAmount = 5000;
## Объём аккумулятора в единицах энергии.
 maxVolume = 20;
## Вероятность смены состояния канала.
## 1 = неблагоприятное состояние,
## 2 = благоприятное состояние.
## 1 - переход из 1 в 2,
## 2 - переход из 2 в 2.
 lambda = [0.2 0.7];
## Вероятность успешной доставки пакета данных в
## зависимости от состояния канала.
## 1 - состояние 1.
## 2 - состояние 2.
 p = [0.55 0.99];
## Формирование выигрыша для заключительного шага.
## Т.к. шаг последний - учитываем только вероятности
## успешной доставки.
 nextV = zeros(maxVolume, 2);
 nextV(2:end, 1) = p(1);
 nextV(2:end, 2) = p(2);
 ## Выигрыш (мат. ожидание) в случае, если выбрано
## действие T: осуществить передачу данных.
## E - количество единиц энергии в данном состоянии.
## S - состояние канала.
 function res = Vt(nextV, p, q, lambda)
   res = zeros(rows(nextV), columns(nextV));
   for i = 1:columns(nextV)
##     Если в аккумуляторе нет энергии, то выигрыш нулевой.
     res(1, i) = 0;
     for j = 2:rows(nextV)
##       Заполняем оставшиеся ячейки матрицы по формуле.
       res(j, i) = p(i) + q * lambda(i) * nextV(j, 2) + ...
                          q * (1 - lambda(i)) * nextV(j, 1) + ...
                          (1 - q) * lambda(i) * nextV(j - 1, 2) + ...
                          (1 - q) * (1 - lambda(i)) * nextV(j - 1, 1);
     endfor
   endfor
 endfunction

 ## Выигрыш (мат. ожидание) в случае, если выбрано
## действие D: отложить передачу данных.
 function res = Vd(nextV, p, q, lambda)
   res = zeros(rows(nextV), columns(nextV));
   for i = 1:columns(nextV)
##     Если аккумулятор полный, то не учитываем вариант с его пополнением.
     res(rows(nextV), i) = (1 - q) * lambda(i) * nextV(rows(nextV), 2) + ...
                           (1 - q) * (1 - lambda(i)) * nextV(rows(nextV), 1);
     for j = 1:(rows(nextV) - 1)
##       Заполняем оставшиеся ячейки матрицы по формуле.
       res(j, i) = q * lambda(i) * nextV(j + 1, 2) + ...
                   q * (1 - lambda(i)) * nextV(j + 1, 1) + ...
                   (1 - q) * lambda(i) * nextV(j, 2) + ...
                   (1 - q) * (1 - lambda(i)) * nextV(j, 1);
     endfor
   endfor
 endfunction

 ## Вычисление максимального значения для каждой пары ячеек двух матриц
## и возвращение индекса матрицы, в которой найдено наибольшее значение.
## input1, input2 - две сравниваемые матрицы n на m.
## value - матрица n на m, которая хранит наибольшие значения.
## valueIndex - матрица n на m, которая индексы матриц.
 function [value, valueIndex] = maxMatrix (input1, input2)
   value = zeros(rows(input1), columns(input1));
   valueIndex = zeros(rows(input1), columns(input1));
   for j = 1:columns(input1)
     for i = 1:rows(input1)
       [value(i, j), valueIndex(i, j)] = max([input1(i, j) input2(i, j)]);
     endfor
   endfor
 endfunction


 printf("Вычисление математических ожиданий...\n");
## Итеративное вычисление выигрыша.
 for k = 1:timeSlotsAmount
   [nextV, nextVi] = maxMatrix(Vt(nextV, p, q, lambda), ...
                               Vd(nextV, p, q, lambda));
   if (k == 1000)
##     Фиксация оптимальной стратегии на 1000-м слоте.
     nVi_1 = nextVi;
   elseif (k == 5000)
##     Фиксация оптимальной стратегии на 5000-м слоте.
     nVi_2 = nextVi;
   endif
 endfor
## Вывод информации на экран.
 printf("Математическое ожидание количества переданных пакетов за \n");
 printf("5000 временных слотов при реализации оптимальной стратегии:\n");
 printf("(ниже представлен вид таблицы, которой будут выведены значения\n");
 printf("1 - передать, 2 - отложить)\n");
 printf("        |S = 1|S = 2\n");
 printf("-------- ----- -----\n");
 printf("E = 0   |.....|.....\n");
 printf("-------- ----- -----\n");
 printf("E = 1   |.....|.....\n");
 printf("-------- ----- -----\n");
 printf("E = ... |.....|.....\n");
 printf("-------- ----- -----\n");
 printf("E = 20  |.....|.....\n\n");
 disp(nextV);
 printf("\n");
## Сравнение зафиксированных оптимальных стратегий.
 tmpr = nVi_1 == nVi_2;
## Анализ сравнения и вывод информации на экран.
 if (rem(sum(sum(tmpr)), maxVolume * 2) == 0)
   printf("Оптимальные стратегии на 1000-м и 5000-м временных\n");
   printf("слотах идентичны (1 - передать, 2 - отложить):\n");
   disp(nVi_1);
 else
   printf("Оптимальные стратегии на 1000-м и 5000-м временных\n");
   printf("слотах не идентичны (1 - передать, 2 - отложить):\n")
   for i = 1:rows(tmpr)
     for j = 1:columns(tmpr)
       if (tmpr(i, j) == 0)
         printf("на 1000-м слоте = \n");
         disp(nVi_1);
         printf("на 5000-м слоте = \n");
         disp(nVi_2);
       endif
     endfor
   endfor
 endif
## Формирование значений для вывода графика.
 t = zeros(1, 9);
 printf("Вычисление значений для графика...\n");
 for q = 1:1:9
   nextV = zeros(maxVolume, 2);
   nextV(2:end, 1) = p(1);
   nextV(2:end, 2) = p(2);
   for k = 1:timeSlotsAmount
     nextV = max(Vt(nextV, p, (q / 10), lambda), ...
                 Vd(nextV, p, (q / 10), lambda));
   endfor
##   Вычисление пропускной способности для заданной вероятности q.
   t(q) = sum(sum(nextV)) / (timeSlotsAmount * 2 * maxVolume);
 endfor
 q = 0.1:0.1:0.9;
 newq = 0.1:0.01:9;
## Интерполяция полученных значений для вывода линейного графика.
 newt = interp1 (q, t, newq);
 printf("Вывод графика...\n");
 figure(1);
 plot(newq, newt, "b:", "linewidth", 2, ...
      q, t, "ob", "markersize", 8);
## "Фиксация" выведенного графика.
 hold on;
## Демонстрация линий сетки.
 grid on;
## Задание пределов осей.
 axis ([0 1 0 1]);
## Задание подписей осей.
 xlabel("q");
 ylabel("Throughput");
## Сохранение графика отдельным файлом.
 saveas(1, "graph3.png");
 printf("Завершение работы программы\n");
