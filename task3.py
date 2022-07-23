# На языке Python реализовать функцию, которая быстрее всего (по процессорным тикам) отсортирует данный ей массив чисел.
# Массив может быть любого размера со случайным порядком чисел (в том числе и отсортированным).
# Объяснить почему вы считаете, что функция соответствует заданным критериям.

# Так как массив может быть любого размера и содержать уже отсортированные данные,
# то может быть худший случай для quick_sort, значит такой алгоритм уже не подходит.

# Для указанных условий подходит алгоритм Timsort, так как его идея заключается в некоторой адаптивности под данные.
# Эта адаптивность заключается в достаточно сложных модификациях стандартных алгоритмов сортировки.
# Например, gallop mode для merge sort, которая при продолжительном выборе элементов одного из сливаемых массивов
# сравнивает элементы не по порядку, а с увеличивающимся шагом, что позволительно вследствие упорядоченности массивов.
# Также данные подготавливаются на этапе разбиения исходного массива на run'ы, чтобы insertion sort отрабатывала быстрее.
# Эти модификации позволяют на некоторых видах данных проводить меньше операций сравнения и присваивания, что занимает
# несколько тактов по времени

# Далее приведён код без этих модификаций, так как мне не удалось в полной мере разобраться в их устройстве.

# вычисление минимальной длины run'а в соответствии с требуемыми условиями
def find_minrun_length(n):
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r

# стандартная сортировка вставкой
def insertion_sort(array, left, right):
    for i in range(left + 1, right + 1):
        element = array[i]
        j = i - 1
        while element < array[j] and j >= left:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = element
    return array

# стандартная сортировка слиянием без gallop mode
def merge(array, l, m, r):
    array_length1 = m - l + 1
    array_length2 = r - m
    left = []
    right = []
    for i in range(0, array_length1):
        left.append(array[l + i])
    for i in range(0, array_length2):
        right.append(array[m + 1 + i])

    i = 0
    j = 0
    k = l

    while j < array_length2 and i < array_length1:
        if left[i] <= right[j]:
            array[k] = left[i]
            i += 1

        else:
            array[k] = right[j]
            j += 1

        k += 1

    while i < array_length1:
        array[k] = left[i]
        k += 1
        i += 1

    while j < array_length2:
        array[k] = right[j]
        k += 1
        j += 1

# Timsort без предварительной подготовки run'ов для сортировки вставкой
def tim_sort(array):
    n = len(array)
    min_run = find_minrun_length(n)

    for left in range(0, n, min_run):
        right = min(left + min_run - 1, n - 1)
        insertion_sort(array, left, right)

    size = min_run
    while size < n:

        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            merge(array, left, mid, right)

        size = 2 * size
