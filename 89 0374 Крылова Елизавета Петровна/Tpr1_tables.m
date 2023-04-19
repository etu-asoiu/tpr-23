tr = [9 5 10 7 9; 9 8 5 10 5; 6 8 8 6 6];
sp = [36 45 29 32 56];
ra = [0.5 0.3 0.5 0.4 0.3; 0.4 0.2 0.3 0.4 0.2; 0.3 0.1 0.2 0.3 0.1];


printf('Таблица транспортные расходы:\n')
for i=1:size(tr,1)
  printf(" ")
  for j=1:size(tr,2)
    fprintf("%.0f ", tr(i,j))
  end
  fprintf("\n")
end
printf("\n");

printf('Таблица спрос:\n')
for i=1:size(sp,1)
  printf(" ")
  for j=1:size(sp,2)
    fprintf("%.0f ", sp(i,j))
  end
  fprintf("\n")
end
printf("\n");

printf('Таблица эффективности рекламных акций:\n')
for i=1:size(ra,1)
  printf(" ")
  for j=1:size(ra,2)
    fprintf("%.1f ", ra(i,j))
  end
  fprintf("\n")
end
