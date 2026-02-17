import math

# Имя входного файла
input_file = "input.txt"
# Имя выходного файла
output_file = "emitter.txt"

with open(input_file, 'r') as f_in:
    # Читаем первую строку
    header = f_in.readline().strip()
    
    # Парсим заголовок
    parts = header.split()
    if len(parts) == 4 and parts[0] == "ASCII" and parts[2] == "0" and parts[3] == "1":
        N = int(parts[1])
    else:
        raise ValueError("Неверный формат заголовка")
    
    # Читаем все строки с точками
    points = []
    for _ in range(N):
        line = f_in.readline().strip()
        if not line:
            break
        x_str, y_str, z_str, point_id = line.split()
        
        # Преобразуем в float
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)
        
        # Вычисляем potential = sqrt(x^2 + y^2)
        potential = math.sqrt(x*x + y*y)
        
        points.append((x, y, z, point_id, float(potential)))
        
        # Для отладки - выведем считанные значения
        #print(f"Прочитано: x={x}, y={y}, z={z}, id={point_id}, potential={potential}")

# Записываем результат
with open(output_file, 'w') as f_out:
    # Записываем заголовок
    f_out.write(f"ASCII {N} 0 1\n")
    
    # Записываем точки с potential
    for x, y, z, point_id, potential in points:
        f_out.write(f"{x} {y} {z} {point_id} {potential:e}\n")

print(f"Обработано {N} точек. Результат сохранен в {output_file}")