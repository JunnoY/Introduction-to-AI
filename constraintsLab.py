#!/usr/bin/env python3
from constraint import Problem, AllDifferentConstraint, ExactSumConstraint


# Task 1
def addTravellerConstraint(problem, traveller, time):
    problem.addConstraint(lambda x: (x == time), ["t_" + traveller])


def Travellers(List):
    problem = Problem()
    people = ["claude", "olga", "pablo", "scott"]
    times = ["2:30", "3:30", "4:30", "5:30"]
    destinations = ["peru", "romania", "taiwan", "yemen"]
    t_variables = list(map(lambda x: "t_" + x, people))
    d_variables = list(map(lambda x: "d_" + x, people))
    problem.addVariables(t_variables, times)
    problem.addVariables(d_variables, destinations)
    problem.addConstraint(AllDifferentConstraint(), t_variables)
    problem.addConstraint(AllDifferentConstraint(), d_variables)
    # comment out the first constraint
    for person in people:
        # problem.addConstraint((lambda x,y,z: (y != "yemen") or ((x == "4:30") and (z == "2:30")) or ((x == "5:30") and (z == "3:30"))),["t_"+person , "d_"+person , "t_olga"])
        problem.addConstraint((lambda z: (z == "2:30") or (z == "3:30")), ["t_claude"])
        problem.addConstraint((lambda x, y: ((x == "2:30") and (y == "peru"))
                                            or ((x != "2:30") and (y == "romania"))
                                            or ((x != "2:30") and (y == "taiwan"))
                                            or ((x != "2:30") and (y == "yemen"))), ["t_" + person, "d_" + person])
        problem.addConstraint((lambda x, y: ((x != "yemen") and (y != "2:30") and (y != "3:30"))),
                              ["d_pablo", "t_pablo"])
    # The person flying from Yemen is leaving earlier than the person flying from Taiwan.
    for person_1 in people:
        for person_2 in people:
            if person_1 != person_2:
                problem.addConstraint((lambda x, y, q, z:
                                       ((q == "yemen") and (z == "taiwan") and (x < y)) or
                                       ((q != "yemen") and (z == "taiwan")) or
                                       ((q == "yemen") and (z != "taiwan")) or
                                       ((q != "yemen") and (z != "taiwan"))
                                       ), ["t_" + person_1, "t_" + person_2, "d_" + person_1, "d_" + person_2])
    for pair in List:
        traveller = pair[0]
        time = pair[1]
        addTravellerConstraint(problem, traveller, time)
    solns = problem.getSolutions()
    return solns


# print(Travellers([["olga", "2:30"]]))


# Task 2
def CommonSum(n):
    magic_constant = n * (n ** 2 + 1) // 2
    return magic_constant


# Task 3
def add_pairList_constraints(problem, v, i):
    problem.addConstraint(lambda x: (x == i), [v])


def msqList(m, pairList):
    problem = Problem()
    problem.addVariables(range(0, m * m), range(1, m * m + 1))  # contains numbers from 1 to n^2
    problem.addConstraint(AllDifferentConstraint(),
                          range(0, m * m))  # each square contains different values from the range of 1 to n*n
    for row in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [row * m + i for i in range(m)])
    for col in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [j * m + col for j in range(m)])
    # implement diagonal
    # left to right diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(m)), [i * (m + 1) for i in range(m)])
    # right to left diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(m)), [i * (m - 1) for i in range(1, m + 1)])
    # pairlist
    if len(pairList) != 0:
        for pair in pairList:
            v = pair[0]
            i = pair[1]
            if 0 <= v < m ** 2 and 1 <= i <= m ** 2:
                add_pairList_constraints(problem, v, i)
    solns = problem.getSolutions()
    # for i in range(len(solns)):
    #     print(solns[i])
    return solns


# print(msqList(3, []))
# print(msqList(4,[[0,13],[1,12],[2,7]]))


# Task 4
def pmsList(m, pairList):
    problem = Problem()
    problem.addVariables(range(0, m * m), range(1, m * m + 1))  # contains numbers from 1 to n^2
    problem.addConstraint(AllDifferentConstraint(),
                          range(0, m * m))  # each square contains different values from the range of 1 to n*n
    for row in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [row * m + i for i in range(m)])
    for col in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), [j * m + col for j in range(m)])
    # implement broken diagonal and normal diagonal
    dd = []
    dd_item_main_lr = []
    dd_item_main_rl = []
    # left to right main diagonal
    # method 1: add constraint directly
    # problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i * (n + 1) for i in range(n)])
    # or
    for i in range(m):
        dd_item_main_lr.append(i * (m + 1))
    dd.append(dd_item_main_lr)
    # right to left main diagonal
    # method 1: add constraint directly
    # problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i * (n - 1) for i in range(1, n + 1)])
    # or
    for i in range(1, m + 1):
        dd_item_main_rl.append(i * (m - 1))
    dd.append(dd_item_main_rl)
    # left to right broken diagonal
    for i in range(1, m):
        dd_item_broken_lr = []
        for j in range(i, (m - i) * m, m + 1):
            dd_item_broken_lr.append(j)
            if j == (m - i) * m - 1 and len(dd_item_broken_lr) < m:
                for extra in range(j + 1, ((j + 1) + (m + 1) * (m - len(dd_item_broken_lr))), m + 1):
                    dd_item_broken_lr.append(extra)
        dd.append(dd_item_broken_lr)
    # right to left broken diagonal
    for i in range(m - 1):
        dd_item_broken_rl = []
        for j in range(i, i * m + 1, m - 1):
            dd_item_broken_rl.append(j)
            if j == i * m and len(dd_item_broken_rl) < m:
                for extra in range(j + (2 * m - 1), ((j + (2 * m - 1)) + (m - 1) * (m - len(dd_item_broken_rl))),
                                   m - 1):
                    dd_item_broken_rl.append(extra)
        dd.append(dd_item_broken_rl)
    for i in range(len(dd)):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), dd[i])
    # pairlist
    if len(pairList) != 0:
        for pair in pairList:
            v = pair[0]
            i = pair[1]
            if 0 <= v < m ** 2 and 1 <= i <= m ** 2:
                add_pairList_constraints(problem, v, i)
    solns = problem.getSolutions()
    # for i in range(len(solns)):
    #     print(solns[i])
    return solns

# print(pmsList(3,[]))
# print(pmsList(4, [[0, 13], [1, 12], [2, 7]]))

# Debug
if __name__ == '__main__':
    print("debug run...")
