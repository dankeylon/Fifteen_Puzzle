# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 10:23:32 2017

@author: Gothmog
"""

"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
Written for Coursera Class: Principles of Computing 2, by Rice University.
Combination of Instructor written and Student Written code.  See 
"#Phase One" For the beginning of student written code: ~141.
"""
#poc_fifteen_gui depends on custom Python module developed for Coursera course:
#Principle of Computing (1&2)
#import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]
    
        self._ref_solution = [[col + puzzle_width * row
               for col in range(self._width)]
               for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
       #Checks that zero tile is at expected position
        if self._grid[target_row][target_col] != 0:
            return False
        #Checks that rows below are solved
        elif self._grid[target_row + 1:] != self._ref_solution[target_row +1:]:
            return False
        #Checks that columns to the right are solved
        elif self._grid[target_row][target_col+1:] != self._ref_solution[target_row][target_col+1:]:
            return False
        else:
            return True
    
    def _interior_early_fin_test(self, target_row, target_col):
        """
        Detects if the target tile is located at (target_row, target_col).  If
        it is, then check to see if the zero tile needs to be moved "left-down"
        in order to prepare for the next tile to solve.  Returns a movement 
        string and a logical value in an array [mov_string, Log].  The logical
        value tells the method that calls this method whether or not it can exit.
        """
        curr_row, curr_col = self.current_position(target_row, target_col)
        target_tup = (target_row, target_col)
        curr_tup = (curr_row, curr_col)
        mov_string = ""
        
        if curr_tup == target_tup:
            zero_row, zero_col = self.current_position(0,0)
            if self.lower_row_invariant(zero_row, zero_col):
                return [mov_string, True]
            else:
                mov_string = mov_string + "ld"
                self.update_puzzle("ld")
                #print self.clone()
                zero_row, zero_col = self.current_position(0,0)
                assert(self.lower_row_invariant(zero_row, zero_col))
                return [mov_string, True]
            
        return [mov_string, False]
    
    def _place_0_for_pos_row(self, target_row, target_col):
        """
        Puts the zero tile in the optimum position to be used by
        the _position_row method.  Returns a mov_string.  Updates 
        the puzzle
        """
        _, curr_col = self.current_position(target_row, target_col)
        zero_row, zero_col = self.current_position(0,0)
        
        mov_string = ""
        if zero_row == 0:
            if zero_col > curr_col:
                mov_string = mov_string + "dlu"
                self.update_puzzle("dlu")
                return mov_string
            elif zero_col < curr_col:
                mov_string = mov_string + "dru"
                self.update_puzzle("dru")
                return mov_string
        else:
            if zero_col > curr_col:
                mov_string = mov_string + "ul"
                self.update_puzzle("ul")
                return mov_string
            elif zero_col < curr_col:
                mov_string = mov_string + "ur"
                self.update_puzzle("ur")
                return mov_string
            
        return mov_string

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        mov_string = ""
        target_tup = (target_row, target_col)
        
        #Phase 1: Get 0 to target tile's current position
        mov_string = mov_string + self._go_to_tile(target_tup)
        
        #Test for early completion
        ld_mov, log = self._interior_early_fin_test(target_row, target_col)
        if log == True:
            return mov_string + ld_mov

        #Phase 2: Cycle target tile to correct column and prep for next phase
        mov_string = mov_string + self._position_col(target_tup, target_tup)
        
        #Test for Early Completion
        ld_mov, log = self._interior_early_fin_test(target_row, target_col)
        if log == True:
            return mov_string + ld_mov
        
        #Puts zero tile into optimal position for next step 
        mov_string = mov_string + self._place_0_for_pos_row(target_row, target_col)
                
        #Test for early completion
        ld_mov, log = self._interior_early_fin_test(target_row, target_col)
        if log == True:
            return mov_string + ld_mov
                
        #Phase 3: Cycle target tile to correct row
        mov_string = mov_string + self._position_row(target_tup, target_tup)
        mov_string = mov_string + "ld"
        self.update_puzzle("ld")
        
        #Test the puzzle is in a solved state
        zero_row, zero_col = self.current_position(0,0)
        assert(self.lower_row_invariant(zero_row, zero_col))

        return mov_string
    
    def _position_row(self, target_tup, dest_tup):
        """
        Takes a cloned puzzle board that has the target tile in the correct
        column with the zero tile directly above it.  Recursive. for use
        with solve_interior_tile.
        """
        target_row, target_col = target_tup
        dest_row, dest_col = dest_tup
        curr_row, curr_col = self.current_position(target_row, target_col)
        assert(curr_col == dest_col)
        
        if curr_row == dest_row:
            return ""
        elif curr_row < dest_row:
            mov_down = "lddru"
            self.update_puzzle(mov_down)
            return mov_down + self._position_row(target_tup, dest_tup)
            
    def _go_to_tile(self, target_tup):
        """
        Takes zero tile and moves it the current location of target tile
        """
        mov_string = ""
        target_row = target_tup[0]
        target_col = target_tup[1]
        curr_row, curr_col = self.current_position(target_row, target_col)
        zero_row, zero_col = self.current_position(0,0)
        
        row_dist = zero_row - curr_row
        col_dist = curr_col - zero_col
        
        #Traverses grid to destination
        for dummy_i in range(0,abs(row_dist)):
            if row_dist > 0:
                mov_string = mov_string + "u"
            elif row_dist < 0:
                mov_string = mov_string + "d"
                
        for dummy_j in range(0,abs(col_dist)):
            if col_dist > 0:
                mov_string = mov_string + "r"
            elif col_dist < 0:
                mov_string = mov_string + "l"
        
        self.update_puzzle(mov_string)
        return mov_string
            
    def _position_col(self, target_tup, dest_tup):
        """
        Takes a cloned puzzle board that has the target tile in a
        row with the zero tile directly to the side of it.  Recursive. For use
        with solve_interior_tile.  Returns a move string and updates the puzzle.
        """
        target_row, target_col = target_tup
        dest_col = dest_tup[1]
        curr_row, curr_col = self.current_position(target_row, target_col)
        
        if curr_col == dest_col:

            return ""
        elif curr_col > dest_col:
            if curr_row == 0:
                #Use down cyclic action
                mov_left = "dllur"
                self.update_puzzle(mov_left)
                return mov_left + self._position_col(target_tup, dest_tup)
            else:
                #Use up cyclic action
                mov_left = "ulldr"
                self.update_puzzle(mov_left)
                return mov_left + self._position_col(target_tup, dest_tup)
        elif curr_col < dest_col:
            if curr_row == 0:
                #Use down cyclic action
                mov_right = "drrul"
                self.update_puzzle(mov_right)
                return mov_right + self._position_col(target_tup, dest_tup)
            else:
                #Use up cyclic action
                mov_right = "urrdl"
                self.update_puzzle(mov_right)
                return mov_right + self._position_col(target_tup, dest_tup)
            
    def _carriage_return(self, target_row):
        """
        Performs a carriage return, moving the zero tile to the right
        until lower_row_invariant returns True.  Returns a movement string
        and updates the puzzle.
        """
        mov_string = ""
        
        while self.lower_row_invariant(target_row-1,self._width - 1) is not True:
            mov_string = mov_string + "r"
            self.update_puzzle("r")
            
        return mov_string
        

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert(self.lower_row_invariant(target_row, 0))
        # replace with your code
        mov_string = ""
        magic_string = "ruldrdlurdluurddlur"
        
        #Moves 0 tile to default position
        mov_string = mov_string + "u"
        self.update_puzzle("u")
        
        #Checks to see if tile is solved
        if self.current_position(target_row,0) == (target_row, 0):
            mov_string = mov_string + self._carriage_return(target_row)
            return mov_string
        
        mov_string = mov_string + "r"
        self.update_puzzle("r")

        dest_tup = (target_row - 1, 1)
        target_tup = (target_row, 0)
        mov_string = mov_string + self._go_to_tile(target_tup)
        
        #Test for solved state
        curr_tup = self.current_position(target_row,0)
        zero_tup = self.current_position(0,0)
        if curr_tup == (target_row - 1, 1) and zero_tup == (target_row - 1, 0):
            mov_string = mov_string + magic_string
            self.update_puzzle(magic_string)
            mov_string = mov_string + self._carriage_return(target_row)
            return mov_string
        
        #Navigates tile to necessary column
        mov_string = mov_string + self._position_col(target_tup, dest_tup)
        
        #Puts zero tile into optimal position for position_row 
        mov_string = mov_string + self._place_0_for_pos_row(target_row, 0)
        
        #Applies position_row, to cycle target tile into the correct row        
        mov_string = mov_string + self._position_row(target_tup, dest_tup)  
        
        assert(self.current_position(target_row, 0) == dest_tup)
        mov_string = mov_string + "ld"
        self.update_puzzle("ld")
        
        #Check for solvable puzzle state
        curr_tup = self.current_position(target_row,0)
        zero_tup = self.current_position(0,0)
        if curr_tup == (target_row - 1, 1) and zero_tup == (target_row - 1, 0):
            mov_string = mov_string + magic_string
            self.update_puzzle(magic_string)
            mov_string = mov_string + self._carriage_return(target_row)
            return mov_string
        
        return mov_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        #Is zero at correct position?
        if self._grid[0][target_col] != 0:
            return False
        #Are columns to the right solved?
        elif self._grid[0:1][target_col+1:]!= self._ref_solution[0:1][target_col+1:]:
            return False
        #Are rows below solved
        elif self._grid[2:]!= self._ref_solution[2:]:
            return False
        #Is slot below solved?
        elif self._grid[1][target_col]!=self._ref_solution[1][target_col]:
            return False
        else:
            return True

        

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Test this
        
        #Does lower_row_invariant hold?
        if self.lower_row_invariant(1, target_col) == False:
            return False
        #Are columns to the right solved?
        elif self._grid[0:1][target_col + 1:] != self._ref_solution[0:1][target_col + 1:]:
            return False
        else:
            return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        mov_string = ""
        magic_string = "urdlurrdluldrruld"
        dest_tup = (1, target_col - 1)
        target_tup = (0, target_col)
        #Moves 0 tile to default position
        mov_string = mov_string + "ld"
        self.update_puzzle("ld")
        
        #Checks to see if tile is solved
        if self.current_position(0,target_col) == (0, target_col):
            
            return mov_string

        mov_string = mov_string + self._go_to_tile(target_tup)
        
        #Test for solved state
        curr_tup = self.current_position(0,target_col)
        zero_tup = self.current_position(0,0)
        if curr_tup == dest_tup and zero_tup == (1, target_col - 2):
            mov_string = mov_string + magic_string
            self.update_puzzle(magic_string)
            return mov_string
        
        #Navigates tile to necessary column
        mov_string = mov_string + self._position_col(target_tup, dest_tup)
        
        #Puts zero tile into optimal position for position_row 
        mov_string = mov_string + self._place_0_for_pos_row(0, target_col)

        #Applies position_row, to cycle target tile into the correct row        
        mov_string = mov_string + self._position_row(target_tup, dest_tup)  
        
        assert(self.current_position(0, target_col) == dest_tup)
        mov_string = mov_string + "ld"
        self.update_puzzle("ld")
        
        #Check for solvable puzzle state
        curr_tup = self.current_position(0,target_col)
        zero_tup = self.current_position(0,0)
        if curr_tup == dest_tup and zero_tup == (1, target_col - 2):
            mov_string = mov_string + magic_string
            self.update_puzzle(magic_string)
            return mov_string
        
        return mov_string
    
    def _row1_early_fin_test(self, target_row, target_col):
        """
        Detects if solve_row1_tile has solved for the current tile correctly.
        If so, it updates the puzzle accordingly to set up for the next tile.
        Returns a movement string and a logical value in an array:
        [mov_string, Log].
        """
        curr_row, curr_col = self.current_position(target_row, target_col)
        target_tup = (target_row, target_col)
        curr_tup = (curr_row, curr_col)
        
        if curr_tup == target_tup:
            zero_row, zero_col = self.current_position(0,0)
            if zero_row == target_row-1 and zero_col == target_col:
                return ["", True]
            elif zero_row == target_row and zero_col == target_col - 1:
                self.update_puzzle("ur")
                return ["ur", True]
            elif zero_row == target_row - 1 and zero_col == target_col - 1:
                self.update_puzzle("r")
                return ["r", True]
            
        return ["", False]

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """        
        mov_string = ""
        target_row = 1
        target_tup = (target_row, target_col)
        
        #Phase 1: Get 0 to target tile's current position
        mov_string = mov_string + self._go_to_tile(target_tup)
        
        #Test for early completion
        place_mov, log = self._row1_early_fin_test(target_row, target_col)
        if log == True:
            return mov_string+place_mov

        #Phase 2: Cycle target tile to correct column and prep for next phase
        mov_string = mov_string + self._position_col(target_tup, target_tup)
        
        #Test for Early Completion
        place_mov, log = self._row1_early_fin_test(target_row, target_col)
        if log == True:
            return mov_string+place_mov
        
        #Puts zero tile into optimal position for next step 
        mov_string = mov_string + self._place_0_for_pos_row(target_row, target_col)
                
        #Test for early completion
        place_mov, log = self._row1_early_fin_test(target_row, target_col)
        if log == True:
            return mov_string+place_mov
                
        #Phase 3: Cycle target tile to correct row
        mov_string = mov_string + self._position_row(target_tup, target_tup)
        
        place_mov, log = self._row1_early_fin_test(target_row, target_col)
        if log == True:
            return mov_string+place_mov
        
        return mov_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        mov_string = ""
        early_stop_iter = 0
        if self.current_position(0,0) == (0,0):
            while self.lower_row_invariant(0,0)==False:
                self.update_puzzle("drul")
                mov_string = mov_string + "drul"
                early_stop_iter = early_stop_iter + 1
                if early_stop_iter > 24:
                    return ""
        elif self.current_position(0,0) == (1, 0):
            self.update_puzzle("u")
            mov_string = mov_string + "u"
            
            while self.lower_row_invariant(0,0)==False:
                self.update_puzzle("drul")
                mov_string = mov_string + "drul"
                early_stop_iter = early_stop_iter + 1
                if early_stop_iter > 24:
                    return ""
        
        elif self.current_position(0,0) == (0, 1):
            self.update_puzzle("l")
            mov_string = mov_string + "l"
            
            while self.lower_row_invariant(0,0)==False:
                self.update_puzzle("drul")
                mov_string = mov_string + "drul"
                early_stop_iter = early_stop_iter + 1
                if early_stop_iter > 24:
                    return ""
                
        elif self.current_position(0,0) == (1,1):
            self.update_puzzle("ul")
            mov_string = mov_string + "ul"
            
            while self.lower_row_invariant(0,0)==False:
                self.update_puzzle("drul")
                mov_string = mov_string + "drul"
                early_stop_iter = early_stop_iter + 1
                if early_stop_iter > 24:
                    return ""

            return mov_string  
        
    def _go_to_end(self):
        """
        Takes the 0 tile to the end of the rainbow.
        """
        curr_row, curr_col = self.current_position(0,0)
        curr_tup = (curr_row, curr_col)
        
        if curr_tup == (self._height - 1, self._width-1):
            return ""
        elif curr_row < self._height-1:
            self.update_puzzle("d")
            return "d" + self._go_to_end()
        elif curr_col < self._width-1:
            self.update_puzzle("r")
            return "r" + self._go_to_end()

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        mov_string = ""
        mov_string = mov_string + self._go_to_end()

        assert(self.current_position(0,0) == (self._height-1,self._width-1))

        #Solves the lower row>1 tiles
        for row_iter in reversed(range(2, self._height)):
            for col_iter in reversed(range(0, self._width)):
                zero_row, zero_col = self.current_position(0,0)
                if self.lower_row_invariant(row_iter, col_iter):
                    if col_iter > 0:
                        mov_string = mov_string + self.solve_interior_tile(row_iter,col_iter)
                    elif col_iter == 0:
                        mov_string = mov_string + self.solve_col0_tile(row_iter)
                elif self.lower_row_invariant(zero_row, zero_col):
                    #Necessary Nothing
                    #Checks for if the solver has gotten lucky
                    #And the puzzle has had multiple tiles "solve themselves"
                    mov_string = mov_string + ""
                else:
                    assert(self.lower_row_invariant(row_iter, col_iter))
                
        #Checks for Early solution of puzzle
        zero_row, zero_col = self.current_position(0,0)
        if zero_row in range(0, 2) and zero_col in range(0,2):    
            mov_string = mov_string + self.solve_2x2()
            return mov_string
        
        #Solves columns in row 1 and row 0
        for col_iter in reversed(range(2, self._width)):
            for row_iter in reversed(range(0, 2)):

                if row_iter == 1:
                    assert(self.row1_invariant(col_iter))
                    mov_string = mov_string + self.solve_row1_tile(col_iter)
                elif row_iter == 0:
                    assert(self.row0_invariant(col_iter))
                    mov_string = mov_string + self.solve_row0_tile(col_iter)
                print self.clone()
        #Solves the final 2x2 grid of values.  If the 2x2 isn't solvable,
        #just returns the state of the puzzle after attempt to solve.
        mov_string = mov_string + self.solve_2x2()

        
        return mov_string

# Start interactive simulation
#Depends on custom Python modules developed for the Coursera course.
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


