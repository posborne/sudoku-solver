import puzzles
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
        
def pprint_available(available):
    i = 0
    for i in xrange(9):
        for j in xrange(9):
            sys.stdout.write('%12s' % ','.join(('%d' % x for x in available[i][j])))
        print ''

def nums_available(puzzle, i, j):
    """Return all numbers available given a puzzle and i, j position"""
    if puzzle[i][j] != 0:
        return set()
    jrange = int(j / 3) * 3
    irange = int(i / 3) * 3
    colset = set((row[j] for row in puzzle))
    rowset = set(puzzle[i])
    gridset = set()
    for row in (row[jrange:jrange + 3] for row in (colset for colset in puzzle[irange:irange + 3])):
        gridset.update([x for x in row])
    return set(xrange(1, 10)) - colset - rowset - gridset

def build_available_table(puzzle):
    """Build and return available table for puzzle"""
    availaible = []
    for i in xrange(9):
        row = []
        for j in xrange(9):
            row.append(nums_available(puzzle, i, j))
        availaible.append(row)
    return availaible

def update_from_position(puzzle, available, i, j):
    """Update the available grid for those positions 
    affected by the provided i, j position."""
    num = puzzle[i][j]
    jrange = int(j / 3) * 3 
    irange = int(i / 3) * 3

    # update rows and columns
    for avail in ([row[j] for row in available] + available[i]):
        avail.discard(num)
    
    for row in available[irange:irange + 3]:
        for avail in row[jrange:jrange + 3]:
            avail.discard(num)

    return available

def eliminate_naked_singles(puzzle, available, istart=0, jstart=0):
    """Eliminate all naked singles"""
    for i in xrange(istart, 9):
        for j in xrange(jstart, 9):
            if puzzle[i][j] == 0 and len(available[i][j]) == 1:
                puzzle[i][j] = available[i][j].pop()
                update_from_position(puzzle, available, i, j)
                eliminate_naked_singles(puzzle, available)
    return True

def solve_puzzle(puzzle):
    """Do it now!"""
    available = build_available_table(puzzle)
    res = solve_puzzle_helper(puzzle, available, 0, 0)
    if isinstance(res, tuple):
        return res[1]
    else:
        return False # no solutions found

def solve_puzzle_helper(puzzle, av, i, j):
    """Recursion, Oh Yeah"""
    next = (i, j + 1) if j < 8 else (i + 1, 0)
    available = av[i][j]
    mypuzzle = copy.deepcopy(puzzle)
    if not eliminate_naked_singles(mypuzzle, av):
        return False
    if i == 8 and j == 8:
        if len(available) == 1 or mypuzzle[i][j] != 0:
            if len(available) == 1:
                mypuzzle[i][j] = available.pop()
            return True, mypuzzle
        else:
            return False
    elif mypuzzle[i][j] != 0:
        res = solve_puzzle_helper(mypuzzle, av, *next)
        if isinstance(res, tuple):
            return res
    elif len(available) == 0 and mypuzzle[i][j] == 0:
        return False
    else:
        for num in available:
            locavail = copy.deepcopy(av)
            mypuzzle[i][j] = num
            update_from_position(mypuzzle, locavail, i, j)
            res = solve_puzzle_helper(mypuzzle, locavail, *next)
            if isinstance(res, tuple):
                return res
    return False

def convert_to_array(puzzle):
    puz = []
    for row in puzzle:
        puz.append(array.array('B', row))
    return puz

def solve_and_time(puzzle):
    print ''
    print '~' * 20 + ' PUZZLE ' + '~' * 20
    puzzle = convert_to_array(puzzle)
    pprint_puzzle(puzzle)
    print '-' * 20 + ' SOLVING ' + '-' * 20
    stime = time.clock()
    puzzle = solve_puzzle(puzzle)
    print "Time: %s" % (time.clock() - stime)
    pprint_puzzle(puzzle)

if __name__ == '__main__':
    solve_and_time(puzzles.puzzle0)
    #solve_and_time(puzzles.puzzle1)
    #solve_and_time(puzzles.puzzle2)