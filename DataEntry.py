# Let us create empty grid
class InputGrid(object):
    def inputgrid(self):
        inputrow = input("Please enter first row with spaces: ")
        grid = inputrow.split(' ')
        ## now check for each number to be less than 9 and total of 9 are entered.
        if len(grid) != 9 :
            print(f"Please enter 9 numbers. You entered {len(grid)} numbers")
            exit(1)
        count = 0
        while count < 9:
            gridnumber = int(grid[count])
            if gridnumber < 0 or gridnumber >9:
                print(f"Enter numbers 0 to 9 only. You entered {gridnumber} at {count} position")
            count = count + 1
        ## check for duplicates
        count = 0
        while count < 9:
            passcount = 0
            while passcount < 9:
                if grid[count] == grid[passcount] and grid[count] != '0' and count < passcount:
                    print(f"You have duplicate at position {passcount} for number {grid[count]}")
                passcount = passcount + 1
            count = count + 1
        return grid

# check for naked singles, naked pairs, naked triplets and naked quds
class GenerateCandidates(object):

    def generate(self, grid):
        self.grid = grid
        candidates = [[],[],[],[],[],[],[],[],[]]
        sortedgrid = grid.copy()
        sortedgrid.sort()
        ## Remove leading zeros from the sorted list
        count = 0
        while count < len(sortedgrid):
            if sortedgrid[count] == '0':
                sortedgrid.pop(count)
            else:
                count = count + 1
        print(sortedgrid)
        count = 0
        while count < 9:

            if grid[count] != '0':
                candidates[count].append(grid[count])

            else:
                passcount = 0
                index = 0
                while passcount < 9:

                    if index < len(sortedgrid):
                        if (passcount+1) != int(sortedgrid[index]):
                            candidates[count].append(str(passcount+1))
                        else:
                            index = index +1
                    else:
                        candidates[count].append(str(passcount+1))
                    passcount = passcount + 1
            count = count + 1
        return candidates

## Now count the number of squares where the number may first

    def countfreq(self, grid, candidates):
        self.grid = grid
        self.candidates = candidates
        freqlist = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}
        print("Freq:",freqlist)
        count = 0
        while count < 9:
            passcount = 0
            while passcount < len(candidates[count]):
                freqlist[candidates[count][passcount]] += 1
                passcount += 1
            count += 1

        return freqlist
## this super class contains all possible Suggestions



grid = InputGrid()
griddata = grid.inputgrid()
print("Grid: ", griddata)
candidates = GenerateCandidates()
candidatelist = candidates.generate(griddata)
print("Candidates: ",candidatelist)
freqlist = candidates.countfreq(griddata, candidatelist)
print("Freq: ", freqlist)