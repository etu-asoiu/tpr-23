 clc; clear all; clf;
 printf("����� ������ ���������\n");

 q = 0.2;
 timeSlotsAmount = 5000;
 maxVolume = 20; 

 lambda = [0.25 0.7];

 p = [0.65 0.99];

 nextV = zeros(maxVolume, 2);
 nextV(2:end, 1) = p(1);
 nextV(2:end, 2) = p(2);

 function res = Vt(nextV, p, q, lambda)
   res = zeros(rows(nextV), columns(nextV));
   for i = 1:columns(nextV)

     res(1, i) = 0;
     for j = 2:rows(nextV)

       res(j, i) = p(i) + q * lambda(i) * nextV(j, 2) + ...
                          q * (1 - lambda(i)) * nextV(j, 1) + ...
                          (1 - q) * lambda(i) * nextV(j - 1, 2) + ...
                          (1 - q) * (1 - lambda(i)) * nextV(j - 1, 1);
     endfor
   endfor
 endfunction


 function res = Vd(nextV, p, q, lambda)
   res = zeros(rows(nextV), columns(nextV));
   for i = 1:columns(nextV)

     res(rows(nextV), i) = (1 - q) * lambda(i) * nextV(rows(nextV), 2) + ...
                           (1 - q) * (1 - lambda(i)) * nextV(rows(nextV), 1);
     for j = 1:(rows(nextV) - 1)

       res(j, i) = q * lambda(i) * nextV(j + 1, 2) + ...
                   q * (1 - lambda(i)) * nextV(j + 1, 1) + ...
                   (1 - q) * lambda(i) * nextV(j, 2) + ...
                   (1 - q) * (1 - lambda(i)) * nextV(j, 1);
     endfor
   endfor
 endfunction

 function [value, valueIndex] = maxMatrix (input1, input2)
   value = zeros(rows(input1), columns(input1));
   valueIndex = zeros(rows(input1), columns(input1));
   for j = 1:columns(input1)
     for i = 1:rows(input1)
       [value(i, j), valueIndex(i, j)] = max([input1(i, j) input2(i, j)]);
     endfor
   endfor
 endfunction

 
 printf("���������� �������������� ��������...\n");
## ����������� ���������� ��������.
 for k = 1:timeSlotsAmount
   [nextV, nextVi] = maxMatrix(Vt(nextV, p, q, lambda), ...
                               Vd(nextV, p, q, lambda));
   if (k == 1000)
##     �������� ����������� ��������� �� 1000-� �����.
     nVi_1 = nextVi;
   elseif (k == 5000)
##     �������� ����������� ��������� �� 5000-� �����.
     nVi_2 = nextVi;
   endif
 endfor
## ����� ���������� �� �����.
 printf("�������������� �������� ���������� ���������� ������� �� \n");
 printf("5000 ��������� ������ ��� ���������� ����������� ���������:\n");
 printf("(���� ����������� ��� �������, ������� ����� �������� ��������\n");
 printf("1 - ��������, 2 - ��������)\n");
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
## ��������� ��������������� ����������� ���������.
 tmpr = nVi_1 == nVi_2;
## ������ ��������� � ����� ���������� �� �����.
 if (rem(sum(sum(tmpr)), maxVolume * 2) == 0)
   printf("����������� ��������� �� 1000-� � 5000-� ���������\n");
   printf("������ ��������� (1 - ��������, 2 - ��������):\n");
   disp(nVi_1);
 else
   printf("����������� ��������� �� 1000-� � 5000-� ���������\n");
   printf("������ �� ��������� (1 - ��������, 2 - ��������):\n")
   for i = 1:rows(tmpr)
     for j = 1:columns(tmpr)
       if (tmpr(i, j) == 0)
         printf("�� 1000-� ����� = \n");
         disp(nVi_1);
         printf("�� 5000-� ����� = \n");
         disp(nVi_2);
       endif
     endfor
   endfor
 endif 

 t = zeros(1, 9);
 printf("���������� �������� ��� �������...\n");
 for q = 1:1:9
   nextV = zeros(maxVolume, 2);
   nextV(2:end, 1) = p(1);
   nextV(2:end, 2) = p(2);
   for k = 1:timeSlotsAmount
     nextV = max(Vt(nextV, p, (q / 10), lambda), ...
                 Vd(nextV, p, (q / 10), lambda));
   endfor

   t(q) = sum(sum(nextV)) / (timeSlotsAmount * 2 * maxVolume);
 endfor
 q = 0.1:0.1:0.9;
 newq = 0.1:0.01:9;

 newt = interp1 (q, t, newq);
 printf("����� �������...\n");
 figure(1);
 plot(newq, newt, "b:", "linewidth", 2, ...
      q, t, "ob", "markersize", 8);

 hold on;
 grid on;
 axis ([0 1 0 1]);
 xlabel("q");
 ylabel("Throughput");
 saveas(1, "graph3.png");
 printf("���������� ������ ���������\n");
