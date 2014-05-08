import copy

DEBUG = True
REVERSE_TASK = False

inf = float('Inf')

def print_matr(matr, system_of_nulls = None, quouted_zeros = None):
    if system_of_nulls == None:
        system_of_nulls = []
    for i in range(0, len(matr)):
        for j in range(0, len(matr)):
            if matr[i][j] == 0 and ((i, j) in system_of_nulls):
                print('*', end=' ')
            if (quouted_zeros is not None) and matr[i][j] == 0 and ((i, j) in quouted_zeros):
                print('\'', end=' ')
            else:
                print(matr[i][j], end=' ')
        print()
    print()

def debug_print(outp, system_of_nulls = None, quoted_zeros = None):
    if DEBUG:
        if isinstance(outp, str):
            print(outp)
        else:
            print_matr(outp, system_of_nulls, quoted_zeros)

def matrix_preparation(matr):
    for j in range(0, len(matr)):
        if not REVERSE_TASK:
            min_elem = matr[0][j]
        else:
            max_elem = matr[0][j]
        for i in range(0, len(matr)):
            if not REVERSE_TASK:
                min_elem = matr[i][j] if matr[i][j] < min_elem else min_elem
            else:
                max_elem = matr[i][j] if matr[i][j] > max_elem else max_elem
        for i in range(0, len(matr)):
            if not REVERSE_TASK:
                matr[i][j] -= min_elem
            else:
                matr[i][j] = max_elem - matr[i][j]
    for i in range(0, len(matr)):
        min_elem = min(matr[i])
        matr[i] = list(map(lambda x: x - min_elem, matr[i]))

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
                return ret, (i, j), old_z

def select_and_take(zeros, coord_type, coord, l_line, first_iteration):
    if not first_iteration:
        try:
            found = [z for z in zeros if (z[coord_type] == coord) and z not in l_line][0]
        except IndexError:
            return False
    else:
        found = zeros[len(zeros) - 1]
    l_line.append(found)
    return True


def build_l_line(stared_zeros, quoted_zeros):
    l_line = []
    first_iteration = True
    while True:
        coord = l_line[len(l_line) - 1][0] if len(l_line) > 0 else 0
        result = select_and_take(quoted_zeros, 0, coord,l_line, first_iteration)
        if not result:
            break
        first_iteration = False
        coord = l_line[len(l_line) - 1][1]
        select_and_take(stared_zeros, 1, coord,l_line, first_iteration)
    return l_line

def calc_func(original_matr, solution):
    result = 0
    for i in range(0, len(solution)):
        for j in range(0, len(solution)):
            if original_matr[i][j] == inf:
                continue
            result += solution[i][j] * original_matr[i][j]
    return result

matr = [[inf, 9, 1, 7, 8],
        [7, inf, 10, 6, 0],
        [1, 6, inf, 7, 9],
        [7, 0, 8, inf, 8],
        [8, 6, 9, 2, inf]]

def vengrian(original_matr):
    matr = copy.deepcopy(original_matr)
    matrix_preparation(matr)
    system_of_nulls = find_independent_nulls(matr)
    iteration_num = 0
    while len(system_of_nulls) < len(matr):
        marked_columns = [system_of_nulls[i][1] for i in range(0, len(system_of_nulls))]
        marked_rows = []
        quoted_zeros = []
        cont = True
        while cont:
            if not is_any_unmarked_nulls(matr, marked_columns, marked_rows):
                create_unmarked_nulls(matr, marked_columns, marked_rows)
            (cont, new_z, old_z) = row_contains_marked_and_unmarked_nulls(matr, marked_columns, marked_rows, system_of_nulls)
            if cont:
                marked_columns.remove(old_z[1])
                marked_rows.append(new_z[0])
            quoted_zeros.append(new_z)
        l_line = build_l_line(system_of_nulls, quoted_zeros)
        for i in range(0, len(l_line)):
            if i % 2 == 1:
                system_of_nulls.remove(l_line[i])
            else:
                system_of_nulls.append(l_line[i])
    result = [[1 if (i, j) in system_of_nulls else 0 for j in range(0, len(matr))] for i in range(0, len(matr))]
    return (result, calc_func(original_matr, result))

def get_loops(solution):
    not_used_nums = [i for i in range(0, len(solution))]
    cycles = []
    while len(not_used_nums) > 0:
        cycle = []
        num = not_used_nums.pop(0)
        cycle.append(num)
        cont = True
        while cont:
            for j in range(0, len(solution)):
                if solution[num][j] == 1:
                    if j in not_used_nums:
                        num = j
                        cycle.append(num)
                        not_used_nums.remove(num)
                    else:
                        cont = False
                    break
        cycles.append(cycle[:])
    return cycles

def get_min_loop(solution):
    cycles = get_loops(solution)
    mincycle = cycles[0]
    for cycle in cycles:
        if len(cycle) < len(mincycle):
            mincycle = cycle
    return mincycle

def salesman_solver(matr):
    debug_print("Preparation step")
    evaluate_path = [[1 if j == (i + 1) % len(matr) else 0 for j in range(0, len(matr))] for i in range(0, len(matr))]
    evaluate_len = calc_func(matr, evaluate_path)
    debug_print("Preparation path:")
    debug_print(evaluate_path)
    debug_print("Preparation path len %d" % evaluate_len)
    tasks_list = []
    debug_print("Adding initial task to tasklist")
    debug_print(matr)
    tasks_list.append(copy.deepcopy(matr))
    iter_number = 0
    while len(tasks_list) != 0:
        iter_number = iter_number + 1
        debug_print("Starting iteration %d. %d tasks in list" % (iter_number, len(tasks_list)))
        new_task = tasks_list.pop(0)
        debug_print("Solving task:")
        debug_print(new_task)
        (new_solution, new_solution_len) = vengrian(new_task)
        debug_print("Solution is:")
        debug_print(new_solution)
        debug_print("Path len of solution %d" % new_solution_len)
        if new_solution_len >= evaluate_len:
            debug_print("New solution is longer then current. Continue to new iteration")
            continue
        min_loop = get_min_loop(new_solution)
        debug_print("Min loop is %s" % str(min_loop))
        if len(min_loop) == len(matr):
            debug_print("Fool loop found. Updating values")
            evaluate_path = new_solution
            evaluate_len = new_solution_len
            continue
        for ind in range(0, len(min_loop)):
            task_to_add = copy.deepcopy(new_task)
            i = min_loop[ind]
            j = min_loop[(ind + 1) % len(min_loop)]
            task_to_add[i][j] = inf
            debug_print("Adding task to tasklist")
            debug_print(task_to_add)
            tasks_list.append(task_to_add)
    debug_print("No more tasks in tasklist")
    return (evaluate_path, evaluate_len)

if __name__ == '__main__':
    print("Input task is:")
    print_matr(matr)
    (evaluate_path, evaluate_len) = salesman_solver(matr)
    print('Result path:')
    print_matr(evaluate_path)
    print('Path len: %d' %evaluate_len)