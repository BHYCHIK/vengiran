DEBUG = True

def print_matr(matr):
    for i in range(0, len(matr)):
        print(matr[i])
    print()

def debug_print(matr):
    if DEBUG:
        print_matr(matr)

def matrix_preparation(matr):
    for j in range(0, len(matr)):
        min_elem = matr[0][j]
        for i in range(0, len(matr)):
            min_elem = matr[i][j] if matr[i][j] < min_elem else min_elem
        for i in range(0, len(matr)):
            matr[i][j] -= min_elem
    for i in range(0, len(matr)):
        min_elem = min(matr[i])
        matr[i] = list(map(lambda x: x - min_elem, matr[i]))
    debug_print(matr)

def check_null(system_of_nulls, a, b):
    for i in range(0, len(system_of_nulls)):
        if system_of_nulls[i][0] == a:
            return False
        if system_of_nulls[i][1] == b:
            return False
    return True

def find_independent_nulls(matr):
    system_of_nulls = []
    for i in range(0, len(matr)):
        for j in range(0, len(matr)):
            if (matr[i][j] == 0) and check_null(system_of_nulls, i, j):
                system_of_nulls.append((i, j))
    return system_of_nulls

def is_any_unmarked_nulls(matr, marked_columns, marked_rows):
    umarked_columns = set(range(0, len(matr))) - set(marked_columns)
    umarked_rows = set(range(0, len(matr))) - set(marked_rows)
    for i in umarked_rows:
        for j in umarked_columns:
            if matr[i][j] == 0:
                return True
    return False

def create_unmarked_nulls(matr, marked_columns, marked_rows):
    umarked_columns = set(range(0, len(matr))) - set(marked_columns)
    umarked_rows = set(range(0, len(matr))) - set(marked_rows)
    min_elem = min([matr[i][j] for i in umarked_rows for j in umarked_columns])
    for i in umarked_rows:
        for j in range(0, len(matr)):
            matr[i][j] -= min_elem
    for i in range(0, len(matr)):
        for j in marked_columns:
            matr[i][j] += min_elem
    return False

def row_contains_marked_and_unmarked_nulls(matr, marked_columns, marked_rows, system_of_nulls):
    umarked_columns = set(range(0, len(matr))) - set(marked_columns)
    umarked_rows = set(range(0, len(matr))) - set(marked_rows)
    for i in umarked_rows:
        for j in umarked_columns:
            if matr[i][j] == 0:
                ret = False
                old_z = None
                for z in system_of_nulls:
                    if z[0] == i:
                        ret = True
                        old_z = z
                        break
                yield ret, (i, j), old_z

def select_and_take(zeros, coord_type, coord, l_line, first_iteration, other_zeros):
    if not first_iteration:
        try:
            found = [z for z in zeros if (z[coord_type] == coord) and z not in l_line][0]
        except IndexError:
            return False
    else:
        found = zeros[0]
        for z1 in zeros:
            for z2 in other_zeros:
                if z1[1] == z2[1]:
                    found = z1
    l_line.append(found)
    return True


def build_l_line(stared_zeros, quoted_zeros):
    l_line = []
    first_iteration = True
    while True:
        coord = l_line[len(l_line) - 1][0] if len(l_line) > 0 else 0
        result = select_and_take(quoted_zeros, 0, coord,l_line, first_iteration, stared_zeros)
        if not result:
            break
        first_iteration = False
        coord = l_line[len(l_line) - 1][1]
        select_and_take(stared_zeros, 1, coord,l_line, first_iteration, quoted_zeros)
    return l_line

matr = [[5, 6, 7, 1],[10, 4, 6, 7], [8, 5, 3, 5], [12, 5, 9, 8]]
matrix_preparation(matr)
system_of_nulls = find_independent_nulls(matr)
while len(system_of_nulls) < len(matr):
    marked_columns = [system_of_nulls[i][1] for i in range(0, len(system_of_nulls))]
    marked_rows = []
    quoted_zeros = []
    while True:
        if not is_any_unmarked_nulls(matr, marked_columns, marked_rows):
            create_unmarked_nulls(matr, marked_columns, marked_rows)
        new_marked_columns = marked_columns[:]
        new_marked_rows = marked_rows[:]
        cont = False
        for (ret, new_z, old_z) in row_contains_marked_and_unmarked_nulls(matr, marked_columns, marked_rows, system_of_nulls):
            if ret:
                new_marked_columns.remove(old_z[1])
                new_marked_rows.append(new_z[0])
            quoted_zeros.append(new_z)
            cont = cont or ret
        marked_columns = new_marked_columns[:]
        marked_rows = new_marked_rows[:]
        if not cont:
            break
    l_line = build_l_line(system_of_nulls, quoted_zeros)
    for i in range(0, len(l_line)):
        if i % 2 == 1:
            system_of_nulls.remove(l_line[i])
        else:
            system_of_nulls.append(l_line[i])

result = [[1 if (i, j) in system_of_nulls else 0 for j in range(0, len(matr))] for i in range(0, len(matr))]
print(result)