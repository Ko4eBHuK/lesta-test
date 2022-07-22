# На языке Python (2.7) реализовать минимум по 2 класса РЕАЛИЗУЮЩИХ циклический буфер FIFO. Объяснить плюсы и минусы каждой реализации.

# + общий подход реализации для разных языков
# + присвоение и взятие элемента по индексу работает за константное время
# - требуется начальное выделение памяти на хранение элементов
# - для работе моей реализации возможен вариант когда нулевой по счёту элемент простаивает, что нарушает требуемую логику буфера (add_element_soft без предварительного take_element)
class FifoWithIndices:
    def __init__(self, size):
        self.size = size
        self.data = [None] * size
        self.head = 0
        self.tail = 0

    def add_element_soft(self, element):
        h = self.head + 1
        if h == self.size:
            h = 0
        if h == self.tail:
            return
        self.head = h
        self.data[h] = element

    def add_element_hard(self, element):
        h = self.head + 1
        if h == self.size:
            h = 0
        if h == self.tail:
            self.tail += 1
        self.head = h
        self.data[h] = element

    def take_element(self):
        if self.tail == self.head:
            return
        t = self.tail + 1
        if t == self.size:
            t = 0
        self.tail = t
        return self.data[self.tail]


# + логически корректный алгоритм работы, при инициализации первый элемент попадает в начало
# + алгоритм реализации проще, используются стандартные операции над списками
# - выполнение add_element_hard имеет линейную сложность в случае когда очередь заполнена
# - выполнение take_element равносильно pop(i), что говорит о линейной сложности
class FifoWithSlice:
    def __init__(self, size):
        self.size = size
        self.data = []

    def add_element_soft(self, element):
        if len(self.data) == self.size:
            return
        else:
            self.data.append(element)

    def add_element_hard(self, element):
        if len(self.data) == self.size:
            self.data = self.data[1:] + [element]
        else:
            self.data.append(element)

    def take_element(self):
        if len(self.data) > 0:
            return self.data.pop(0)
        else:
            return
