#!/usr/bin/env python3
import collections
import sys
import csv
from typing import List, Dict

#Functions
def dpll(c: int, v: int, clauses: List[List[int]]) -> bool:
    variables = [None for _ in range(v)] #initiate variables to all be null
    decision_stack = []  # Stack to hold decisions and backtrack

    # Repeat until we either satisfy the problem or determine it's unsatisfiable
    while True:
        # First try unit propagation
        unit_result = unit_clause_prop(clauses, variables)
        
        if not unit_result:
            # If unit propagation fails, try pure literal elimination
            pure_result = pure_literal(clauses, variables)
            
            if not pure_result:
                # If both unit propagation and pure literal fail, we backtrack
                while decision_stack:
                    print("entered dicision stack loop!")
                    last_decision, last_value = decision_stack.pop()
                    if last_value:  # If True failed, now try False
                        decision_stack.append((last_decision, False))
                        variables[last_decision - 1] = False
                        clauses = reduce_clauses(clauses, -last_decision)  # Reverse decision
                        break
                    else:
                        variables[last_decision - 1] = None  # Backtrack further
                if not decision_stack:
                    return False  # If no more decisions, the problem is unsatisfiable

        else:
            # If unit propagation succeeds, move to pure literal elimination
            pure_literal(clauses, variables)

        # If all clauses are satisfied, return True
        if not clauses:
            return True

        # Find an unassigned variable to make a decision
        var_to_assign = next((i + 1 for i in range(v) if variables[i] is None), None)
        if var_to_assign is None:
            break  # No unassigned variables left

        # Make a decision: try True first
        decision_stack.append((var_to_assign, True))
        variables[var_to_assign - 1] = True

        clauses = reduce_clauses(clauses, var_to_assign)


    

def unit_clause_prop(clauses: List[List[int]], variables: list) -> bool:
    changed = False
    while True:

        unit_clauses = []
        for c in clauses:
            if len(c) == 1: unit_clauses.append(c[0])
        if not unit_clauses: 
            return changed
        
        changed = True
        for unit in unit_clauses:
            var = abs(unit)
            if unit > 0:
                value = True
            else:
                value = False
            if variables[var - 1] is not None and variables[var - 1] != value:
                return False #conflict
            
            variables[var-1] = value

            for clause in clauses:
                if unit in clause:
                    clauses.remove(clause)
            for clause in clauses:
                if -unit in clause:
                    clause.remove(-unit)
    

def pure_literal(clauses: List[List[int]], variables: list) -> bool:
    literal_count = {}
    changed = False

    # Step 1: Count occurrences of each literal
    for clause in clauses:
        for literal in clause:
            if literal in literal_count:
                literal_count[literal] += 1
            else:
                literal_count[literal] = 1


    # Step 2: Identify pure literals that appear more than once
    pure_literals = set()
    for literal in literal_count:
        if literal_count[literal] > 1 and -literal not in literal_count: #MAYBE CHECK THIS
            pure_literals.add(literal)
    
    
    # Step 3: Remove clauses containing pure literals
    for pure in pure_literals:
        var = abs(pure)
        variables[var - 1] = pure > 0  # Assign the pure literal
        clauses[:] = [clause for clause in clauses if pure not in clause]
        changed = True
    
    return changed

def reduce_clauses(clauses: List[List[int]], assignment: int) -> List[List[int]]:
    """
    Reduce clauses based on the assignment of a variable.
    assignment > 0 means the variable is assigned True
    assignment < 0 means the variable is assigned False
    """
    new_clauses = []
    for clause in clauses:
        if assignment in clause:
            continue  # Clause is satisfied
        new_clause = [lit for lit in clause if lit != -assignment]  # Remove the negated literal
        if not new_clause:
            return []  # Conflict: clause became empty
        new_clauses.append(new_clause)
    return new_clauses

    

#Main
def main():

    file_name = "practice_test.csv"
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        clauses = []
        c = 0

        for line in csvFile:
            if line[0] == 'c':
                problemNum = line[1]
                print(f"Problem:{problemNum}")
            elif line[0] == 'p':
                varNum = int(line[2])
                clauseNum = int(line[3])
            else:
                clause = [int(num) for num in line[:-2]]  #ignore 0 at end 
                clauses.append(clause)
                c += 1
                if c == int(clauseNum):
                    #call dpll function
                    if dpll(clauseNum, varNum, clauses):
                        print("Satisfiable")
                    else:
                        print("Unsatisfiable")
                    c = 0
                    clauses = []
                
                    
if __name__ == '__main__':
    main()