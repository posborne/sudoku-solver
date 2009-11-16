import sys
import array
import copy
import time

# TODO: possible optimizations
#  * Keep running track of available table instead of calculating each
#    and every time.

def pprint_puzzle(puzzle, empty='.'):
    """Given a puzzle, pretty print it."""
    ROWSEP = ' +' + '-' * (2 * len(puzzle[0]) + 5) + '+'
    i = 0
    print ROWSEP
    for rowset in (puzzle[:3], puzzle[3:6], puzzle[6:]):
        for row in rowset:
            for colset in (row[:3], row[3:6], row[6:]):
                sys.stdout.write(' | ' + ' '.join(('%s' % i if i > 0 else empty for i in colset)))
            print ' |'
        print ROWSEP

def nums_available(puzzle, i, j):
    """Return all numbers available given a puzzle and i, j position"""
    jrange = int(j / 3) * 3
    irange = int(i / 3) * 3
    colset = set((row[j] for row in puzzle))
    rowset = set(puzzle[i])
    gridset = set()
    for row in (row[jrange:jrange + 3] for row in (colset for colset in puzzle[irange:irange + 3])):
        gridset.update([x for x in row])
    return set(xrange(1, 10)) - colset - rowset - gridset
#    used_set = set()
#    jrange = int(j / 3) * 3
#    irange = int(i / 3) * 3
#    for element in (row[j] for row in puzzle):
#        used_set.add(element)
#    for element in puzzle[i]:
#        used_set.add(element)
#    for row in (row[jrange:jrange + 3] for row in (colset for colset in puzzle[irange:irange + 3])):
#        used_set.update([x for x in row])
#    return set(range(1,10)) - used_set

def solve_puzzle(puzzle):
    """Do it now!"""
    res = solve_puzzle_helper(puzzle, 0, 0)
    if isinstance(res, tuple):
        return res[1]
    else:
        return False # no solutions found

def solve_puzzle_helper(puzzle, i, j):
    """Recursion, Oh Yeah"""
    next = (i, j + 1) if j < 8 else (i + 1, 0)
    mypuzzle = copy.deepcopy(puzzle)
    if not eliminate_naked_singles(mypuzzle):
        return False # elimination detected a bad path
    available = nums_available(mypuzzle, i, j)
    if i == 8 and j == 8:
        if len(available) == 1 or mypuzzle[i][j] != 0:
            if (len(available) == 1):
                mypuzzle[i][j] = list(available)[0]
            eliminate_naked_singles(mypuzzle)
            return True, mypuzzle
        else:
            return False
    elif mypuzzle[i][j] != 0:
        res = solve_puzzle_helper(puzzle, *next)
        if isinstance(res, tuple):
            return res
    elif len(available) == 0 and mypuzzle[i][j] == 0:
        return False
    else:
        for num in available:
            mypuzzle[i][j] = num
            res = solve_puzzle_helper(mypuzzle, *next)
            if isinstance(res, tuple):
                return res
    return False

def eliminate_naked_singles(puzzle, istart=0, jstart=0):
    """Eliminate all naked singles"""
    for i in xrange(istart, 9):
        for j in xrange(jstart, 9):
            if puzzle[i][j] == 0:
                avail = nums_available(puzzle, i, j)
                if len(avail) == 0:
                    return False
                elif len(avail) == 1:
                    puzzle[i][j] = list(avail)[0]
                    # on average, faster without
                    #eliminate_naked_singles(puzzle)
    return True

if __name__ == '__main__':
    puzzle = \
    [[0, 0, 5, 0, 0, 0, 0, 0, 1,],
     [0, 0, 0, 9, 1, 0, 4, 0, 0,],
     [0, 8, 0, 0, 0, 4, 0, 0, 0,],
     [0, 0, 2, 0, 0, 7, 9, 0, 4,],
     [0, 3, 0, 0, 0, 0, 0, 6, 0,],
     [8, 0, 7, 2, 0, 0, 3, 0, 0,],
     [0, 0, 0, 3, 0, 0, 0, 4, 0,],
     [0, 0, 6, 0, 9, 5, 0, 0, 0,],
     [4, 0, 0, 0, 0, 0, 2, 0, 0,]]
#    puzzle = [ [0,0,0,8,0,0,0,0,0],
#            [9,3,0,0,2,0,0,0,8],
#            [0,0,4,0,0,6,2,9,3],
#            [5,4,0,0,0,8,6,0,2],
#            [0,2,3,0,0,0,5,8,0],
#            [8,0,9,2,0,0,0,4,7],
#            [2,6,8,4,0,0,9,0,0],
#            [3,0,0,0,8,0,0,7,5],
#            [0,0,0,0,0,3,0,0,0] ]
#
#    puzzle =[ [0,0,9,8,0,1,0,0,0],
#            [6,0,3,0,0,0,0,9,0],
#            [0,2,0,0,0,5,0,0,0],
#            [9,4,0,0,0,0,0,0,0],
#            [0,2,3,0,0,0,0,0,0],
#            [0,0,0,2,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,8,0,0,0,0],
#            [0,0,0,0,0,3,0,0,0] ]
    newpuz = []
    for row in puzzle:
        newpuz.append(array.array('B', row))
    puzzle = newpuz
    pprint_puzzle(puzzle)
    print '-' * 20 + ' SOLVING ' + '-' * 20
    stime = time.clock()
    puzzle = solve_puzzle(puzzle)
    print "Time: %s" % (time.clock() - stime)
    pprint_puzzle(puzzle)
