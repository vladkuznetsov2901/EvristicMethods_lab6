import random
import sys


def check_intervals(intervals, parents, parents_phenotype, n):
    children_arr = []
    j = 0
    for interval in intervals:
        children_arr.append([])
        for i in range(len(parents_phenotype)):
            if interval[0] <= parents_phenotype[i] <= interval[1]:
                children_arr[j].append(parents[i])
        j += 1
    print(children_arr)
    _max_children = [0]
    for i in range(len(children_arr)):
        if sum(children_arr[i]) > sum(_max_children):
            _max_children = children_arr[i]
    return _max_children


def array_sort(new_pokolenya, new_pokolenya_phenotypes, new_pokolenya_fitness):
    for i in range(len(new_pokolenya_fitness)):
        for j in range(0, len(new_pokolenya_fitness) - i - 1):
            if new_pokolenya_fitness[j] > new_pokolenya_fitness[j + 1]:
                temp1 = new_pokolenya_fitness[j]
                new_pokolenya_fitness[j] = new_pokolenya_fitness[j + 1]
                new_pokolenya_fitness[j + 1] = temp1

                temp = new_pokolenya[j]
                new_pokolenya[j] = new_pokolenya[j + 1]
                new_pokolenya[j + 1] = temp

                temp2 = new_pokolenya_phenotypes[j]
                new_pokolenya_phenotypes[j] = new_pokolenya_phenotypes[j + 1]
                new_pokolenya_phenotypes[j + 1] = temp2

    return new_pokolenya[0:len(new_pokolenya) // 2], new_pokolenya_phenotypes[
                                                     0:len(new_pokolenya_phenotypes) // 2], new_pokolenya_fitness[0:len(
        new_pokolenya_fitness) // 2]


def best_child(new_pokolenya):
    _min = sys.maxsize
    for i in range(len(new_pokolenya)):
        if sum(new_pokolenya[i]) < _min:
            _min = sum(new_pokolenya[i])

    return _min


def search_best_individual(all_childrens):
    _min_value = sys.maxsize
    for i in range(len(all_childrens)):
        if sum(all_childrens[i]) < _min_value:
            _min_value = sum(all_childrens[i])
    return _min_value


def invert_random_bit(number):
    binary_number = bin(number)[2:]

    random_bit_index = random.randint(0, len(binary_number) - 1)

    inverted_bit = '1' if binary_number[random_bit_index] == '0' else '0'

    new_binary_number = binary_number[:random_bit_index] + inverted_bit + binary_number[random_bit_index + 1:]

    new_number = int(new_binary_number, 2)

    return new_number


file = open("pokoleniya.txt", "w")
m = int(input("Введите кол-во генов: "))
k = int(input("Введите кол-во особей: "))
n = int(input("Введите кол-во процессоров: "))
t1 = int(input("Введите диапазон от: "))
t2 = int(input("Введите диапазон до: "))
z = int(input("Введите кол-во повторений для заврешения: "))
Pk = int(input("Введите вероятность кроссовера: "))
Pm = int(input("Введите вероятность мутации: "))

parents = []

for i in range(k):
    parents.append([])
    for j in range(m):
        parents[i].append(random.randint(t1, t2))

file.write("РОДИТЕЛИ:\n")
i = 1
for row in parents:
    print(f"O{i} = {row}")
    file.write(f"O{i} = {row}\n")
    i += 1

remainder = int(255 / n)
print(f"Remainder: {remainder}")

intervals = []
start = 0
end = start + remainder
for i in range(n):
    intervals.append([])
    for j in range(1):
        intervals[i].append(start)
        intervals[i].append(end)
        start = end + 1
        end += remainder

i = 1
for row in intervals:
    print(f"Interval{i} = {row}")
    i += 1

parents_phenotypes = []

for i in range(k):
    parents_phenotypes.append([])
    for j in range(m):
        parents_phenotypes[i].append(random.randint(0, 255))

for i in range(len(parents)):
    print(f"O{i + 1} = {parents[i]}")
    print(f"parents_fenotype{i + 1} = {parents_phenotypes[i]}")

all_children = []

for i in range(k):
    all_children.append(check_intervals(intervals, parents[i], parents_phenotypes[i], k))

print("ALL - ", all_children)

for i in range(len(all_children)):
    print(f"O{i + 1} childrens = {all_children[i]}, sum = {sum(all_children[i])}")

best_individual = search_best_individual(all_children)

print(f"Лучшая особь: {best_individual}")

file.write(f"Лучшая особь: {best_individual}\n")

counter = 0
counter_pokolenyi = 0
pokoleniye = 0
print("##########################################CROSSOVER##########################################")
new_pokolenya = []
new_pokolenya_phenotypes = []
new_pokolenya_fitness = []
while counter < z:

    while len(new_pokolenya) < (k * 2):
        try:
            first_individual_ind = random.randint(0, len(parents) - 1)
            first_individual = parents[first_individual_ind]
            second_individual_ind = random.randint(0, len(parents) - 1)
            second_individual = parents[second_individual_ind]

            if first_individual == second_individual:
                continue
            if random.randint(0, 100) <= Pk:
                first_phenotypes = parents_phenotypes[parents.index(first_individual)]
                second_phenotypes = parents_phenotypes[parents.index(second_individual)]
                print(f"1 особь(O{parents.index(first_individual) + 1}): {first_individual}")
                print(f"2 особь(O{parents.index(second_individual) + 1}): {second_individual}")
                crossover_ind_1 = random.randint(1, m - 3)
                crossover_ind_2 = random.randint(crossover_ind_1 + 1, m - 1)

                print(f"Индекс кроссовера 1: {crossover_ind_1}")
                print(f"Индекс кроссовера 2: {crossover_ind_2}")

                first_individual_new = first_individual[0:crossover_ind_1] + second_individual[
                                                                             crossover_ind_1:crossover_ind_2] + first_individual[
                                                                                                                crossover_ind_2::]
                second_individual_new = second_individual[0:crossover_ind_1] + first_individual[
                                                                               crossover_ind_1:crossover_ind_2] + second_individual[
                                                                                                                  crossover_ind_2::]
                print(f"1 особь: {first_individual_new}")
                print(f"2 особь: {second_individual_new}")
                first_individual_new_phenotypes = first_phenotypes[0:crossover_ind_1] + second_phenotypes[
                                                                                        crossover_ind_1:crossover_ind_2] + first_phenotypes[
                                                                                                                           crossover_ind_2::]
                second_individual_new_phenotypes = second_phenotypes[0:crossover_ind_1] + first_phenotypes[
                                                                                          crossover_ind_1:crossover_ind_2] + second_phenotypes[
                                                                                                                             crossover_ind_2::]
                print(f"Фенотипы(1): {first_individual_new_phenotypes}")
                print(f"Фенотипы(2): {second_individual_new_phenotypes}")
                for _ in range(2):
                    if random.randint(0, 100) <= Pm:
                        phenotype_ind = random.randint(0, len(first_individual_new_phenotypes) - 1)
                        old_phenotype = first_individual_new_phenotypes[phenotype_ind]
                        print(f"Старый фенотип: {old_phenotype}")
                        new_phenotype = invert_random_bit(old_phenotype)
                        print(f"Новый фенотип: {new_phenotype}")

                        first_individual_new_phenotypes[phenotype_ind] = new_phenotype

                        print(f"Фенотипы: {first_individual_new_phenotypes}")

                        new_pokolenya_fitness.append(
                            sum(check_intervals(intervals, first_individual_new, first_individual_new_phenotypes, n)))

                        new_pokolenya.append(first_individual_new)
                        new_pokolenya_phenotypes.append(first_individual_new_phenotypes)
                        print(f"$$$$$$$$$$$$$$$$$НОВЫЕ ПОКОЛЕНИЯ: {new_pokolenya}$$$$$$$$$$$$$$$$$")

                        # if sum(new_childrens) == best_individual:
                        #     counter += 1
                        #     print(f"############################COUNTER = {counter}############################")
                        #
                        #     pokoleniye += 1
                        #     print(
                        #         f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ПОКОЛЕНИЕ - {pokoleniye}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                        #     with open("pokoleniya.txt", 'w') as f:
                        #         f.write(f"Pokoleniye: {pokoleniye}\n")
                    else:
                        print("############################МУТАЦИЯ НЕ УДАЛАСЯ############################")

                    for _ in range(2):
                        if random.randint(0, 100) <= Pm:
                            phenotype_ind = random.randint(0, len(second_individual_new_phenotypes) - 1)
                            old_phenotype = second_individual_new_phenotypes[phenotype_ind]
                            print(f"Старый фенотип: {old_phenotype}")
                            new_phenotype = invert_random_bit(old_phenotype)
                            print(f"Новый фенотип: {new_phenotype}")

                            second_individual_new_phenotypes[phenotype_ind] = new_phenotype

                            print(f"Фенотипы: {second_individual_new_phenotypes}")

                            new_pokolenya_fitness.append(
                                sum(check_intervals(intervals, second_individual_new, first_individual_new_phenotypes, n)))

                            new_pokolenya.append(second_individual_new)
                            new_pokolenya_phenotypes.append(first_individual_new_phenotypes)
                            print(f"$$$$$$$$$$$$$$$$$НОВЫЕ ПОКОЛЕНИЯ: {new_pokolenya}$$$$$$$$$$$$$$$$$")

                            # if sum(new_childrens) == best_individual:
                            #     counter += 1
                            #     print(f"############################COUNTER = {counter}############################")
                            #     pokoleniye += 1
                            #     print(
                            #         f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ПОКОЛЕНИЕ - {pokoleniye}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                            #     with open("pokoleniya.txt", 'w') as f:
                            #         f.write(f"Pokoleniye: {pokoleniye}\n")
                        else:
                            print("############################МУТАЦИЯ НЕ УДАЛАСЯ############################")

            else:
                print("############################КРОССОВЕР НЕ УДАЛСЯ############################")
        except RecursionError:
            print("Превышено максимальное количество попыток генерации уникальных особей. Продолжаем выполнение.")
            continue
    pokoleniye += 1
    new_pokolenya, new_pokolenya_phenotypes, new_pokolenya_fitness = array_sort(new_pokolenya, new_pokolenya_phenotypes,
                                                                                new_pokolenya_fitness)

    print(f"$$$$$$$$$$$$$$$$$НОВЫЕ ПОКОЛЕНИЯ №{pokoleniye}: {new_pokolenya}$$$$$$$$$$$$$$$$$")
    print(f"$$$$$$$$$$$$$$$$$НОВЫЕ ПОКОЛЕНИЯ ФЕНОТИПЫ №{pokoleniye}: {new_pokolenya_phenotypes}$$$$$$$$$$$$$$$$$")
    print(f"$$$$$$$$$$$$$$$$$НОВЫЕ ПОКОЛЕНИЯ ПРИСПОСОБЛЕННОСТЬ №{pokoleniye}: {new_pokolenya_fitness}$$$$$$$$$$$$$$$$$")

    file.write(f"НОВЫЕ ПОКОЛЕНИЯ №{pokoleniye}: {new_pokolenya}\n")
    file.write(
        f"НОВЫЕ ПОКОЛЕНИЯ ФЕНОТИПЫ №{pokoleniye}: {new_pokolenya_phenotypes}\n")
    file.write(
        f"НОВЫЕ ПОКОЛЕНИЯ ПРИСПОСОБЛЕННОСТЬ №{pokoleniye}: {new_pokolenya_fitness}\n")

    parents = new_pokolenya
    parents_phenotypes = new_pokolenya_phenotypes
    temp = new_pokolenya_fitness[0]
    print(temp)
    if temp == best_individual:
        counter += 1
        print(f"############################COUNTER = {counter}############################")
        file.write(
            f"Лучший потомок: {best_individual}, лучший потомок из поколения №{pokoleniye}: {temp}, кол-во повторений: {counter}\n")
    elif temp < best_individual:
        counter = 0
        best_individual = temp
        print(f"$$$$$$$$$$$$$$$$$НОВЫЙ ЛУЧШИЙ ПОТОМОК: {best_individual}$$$$$$$$$$$$$$$$$")
        file.write(f"НОВЫЙ ЛУЧШИЙ ПОТОМОК: {best_individual}\n")
