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

i = 1
for row in parents:
    print(f"O{i} = {row}")
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

counter = 0
pokoleniye = 0
print("##########################################CROSSOVER##########################################")
while counter < z:
    first_individual = parents[random.randint(0, n - 1)]
    second_individual = parents[random.randint(0, n - 1)]

    while first_individual == second_individual:
        first_individual = parents[random.randint(0, n - 1)]
        second_individual = parents[random.randint(0, n - 1)]
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

                new_childrens = check_intervals(intervals, first_individual_new, first_individual_new_phenotypes, n)

                print("ALL - ", new_childrens)

                print(f"O{i + 1} childrens = {new_childrens}, sum = {sum(new_childrens)}")

                if sum(new_childrens) < best_individual:
                    best_individual = sum(new_childrens)
                    print(
                        f"############################НОВАЯ ЛУЧШАЯ ОСОБЬ - {best_individual}############################")
                    counter = 0
                    pokoleniye += 1
                    print(
                        f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ПОКОЛЕНИЕ - {pokoleniye}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    with open("pokoleniya.txt", 'w') as f:
                        f.write(f"Pokoleniye: {pokoleniye}\n")
                    continue

                if sum(new_childrens) == best_individual:
                    counter += 1
                    print(f"############################COUNTER = {counter}############################")

                    pokoleniye += 1
                    print(
                        f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ПОКОЛЕНИЕ - {pokoleniye}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    with open("pokoleniya.txt", 'w') as f:
                        f.write(f"Pokoleniye: {pokoleniye}\n")
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

                    new_childrens = check_intervals(intervals, second_individual_new,
                                                    second_individual_new_phenotypes,
                                                    n)

                    print("ALL - ", new_childrens)

                    print(f"O{i + 1} childrens = {new_childrens}, sum = {sum(new_childrens)}")

                    if sum(new_childrens) < best_individual:
                        best_individual = sum(new_childrens)
                        print(
                            f"############################НОВАЯ ЛУЧШАЯ ОСОБЬ - {best_individual}############################")
                        counter = 0
                        pokoleniye += 1
                        print(
                            f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ПОКОЛЕНИЕ - {pokoleniye}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                        with open("pokoleniya.txt", 'w') as f:
                            f.write(f"Pokoleniye: {pokoleniye}\n")
                        continue

                    if sum(new_childrens) == best_individual:
                        counter += 1
                        print(f"############################COUNTER = {counter}############################")
                        pokoleniye += 1
                        print(
                            f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ПОКОЛЕНИЕ - {pokoleniye}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                        with open("pokoleniya.txt", 'w') as f:
                            f.write(f"Pokoleniye: {pokoleniye}\n")
                else:
                    print("############################МУТАЦИЯ НЕ УДАЛАСЯ############################")

    else:
        print("############################КРОССОВЕР НЕ УДАЛСЯ############################")
