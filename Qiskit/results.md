# Results for different alterations done on [main.py](./main.py)
* Results of testing the consequences of:
    * Reordering gate-application.
    * Movement of for-loops and its surrounding functions.
    * Standard refactoring measures on quantum code.

## What is being tested

### Line Switches
* There are multiple gate applications being executed in the Qiskit implementation. 

* Line 17
    * The first occuring gate is an Hadamard gate, which activates all the qubits. 
    ```
    qc.h(range(n))
    ```

* Line 20
    * On line 20 we apply the CZ gate.
    ```
    oracle.cz(0, 1)
    ```

* Lines 24 - 30
    * Lines 24 to 30 contains many sequential gate applications.
    ```
    diffuser.h(range(n))
    diffuser.x(range(n))
    diffuser.h(1)
    diffuser.cx(0, 1)
    diffuser.h(1)
    diffuser.x(range(n))
    diffuser.h(range(n))
    ```

### Moving For Loops
* There is not a lot of for loops in the Qiskit impementation of Grovers algorithm. The only one occurs on line 33.
* F1 (Lines 33 - 35)
    * Consists of 2 appends acting on the qc variable (QuantumCircuit). The appends are repeated iterations amount of times. 
    ```
    for _ in range(iterations):
        qc.append(oracle_gate, range(n))
        qc.append(diffuser_gate, range(n))
    ```

### Refactors
* Not all refactors guaranteed to work on quantum code, and some may not serve any function at all. Which we are going to find out. We will test the following refactoring methods: 

* Inlining
    * The process of extracting a functions body out of the function (or removing a function call with function content), as its abstraction is no longer required. Mostly used for short functions. 
* Extract
    * Opposite of inlining. This technique moves a code block into its own function or method.
* Rename
    * Self-explanatory
* Encapsulate
    * Process of hiding details of a class and only exposing necessary interfaces. Prevents dependance of details which are subject to change. Example is to enforce access via getters and setters. 
* We are using a more advanced, updated version of the ```main.py``` file for all refactoring tests apart from 'rename', as the 2-qubit method seemed too stable to test a realistic scenario. 

## Results

### Line Switches
* Line 17
    * As mentioned above, line 17 contains the activation of the qubits (Hadamard Gate). 
    * If we were to remove this line, the result would be a consistent 00. 
    * We can not move this line above the QC above, but we may try to move it downwards. 
    * Moving it below the oracle functions (lines 19 - 21) does not change the result.
    * Moving it below the diffuser lines (lines 23 - 31) does not change the result either. 
    * Neither case is suprising, as the qc appends the oracle and diffuser in the for-loop at lines 33-35. Moving the activation below this loop makes the result unpredictable and randomized. 
    * Moving the activation to the beginning of the for loop results in a consistent 11 result, but rather unexpected as the for loop in this case only runs once. 
    * In the [L17 file](./line-switches/L17.py), we have commented out line 17.

* Line 20
    * Line 20 contains a CZ gate being applied it the oracle quantum circuit. 
    * Removing this line causes the result to become randomized and unpredictable.
    * We can not move this line up the file, as it works on the oracle variable being created on line 19.
    * If we were to move the line down the file, it would serve no function, as the oracle gets converted using the ```oracle.to_gate()``` function. Applying cz after this point would be an application to a 'dead' variable, and serves the same purpose as deleting it. 
    * In the [L20 file](./line-switches/L20.py), we have commented out line 20. 

* Lines 24 - 30
    * Lines 24 - 30 contains multiple gate applications the qubits of the diffuser quantum circuit. 
    * Moving these lines above line 23 (where the diffuser is instantiated) would not work, so we are not testing this.
    * Moving these below line 31 would cause the applications to occur after data has been transfered to a new object, making the applications at this point would be to affect a dead object and would result in no actual changes. This is the same effect as moving L20 down the file. 
    * We can restructure the forementioned lines, however, and see what the consequences are for switching the sequence of gate applications on one of the gates in this code.

### Moving For Loops
* F1 (Lines 33 - 35)
    * If the for loop was to not repeat iterations amount of times, but iterations + 1, the result becomes random and unpredictable. 
        * We did not test iterations - 1, as the optimal number of iterations is 1. If we were to change iterations, the result would again be unpredictable, and we would not be able to test changes to F1 loops.
    * If the for loop is missing an append, the result also becomes random and unpredictable, regardless of which statement is removed. 
    * If the for loop were to be moved:
        * The for loop contains variables created on lines 21 (oracle_gate) and 31 (diffuser_gate), so when moving the for loop, we must ensure it remains below those in the code-file. 
        * The ```diffuser_gate``` depends on lines 23-30, and ```oracle_gate``` on line 21 depends on line 19-20. 
        * Moving it down the file would put it below the measurings, leading to measuring at an incomplete state, and the for loop not serving any purpose.
        * In the [F1 file](./for-loop-moving/F1.py), the for-loop is commented out. 


### Applying Existing Refactors
* Encapsulate
    * After performing encapsulation on the file and making the circuit 'hidden', no changes in behaviour occured. Results may have been different depending on what is encapsulated, must test as well. 
    * You can see edits and results using the [encapsulate file](./classical-refactors/encapsulate.py).

* Extract
    * In this test we attempted to extract the code related to ```oracle_gate``` and ```diffuser_gate``` into their own functions. 
    * Results did not differ after this, and appeared consistent and correct.
    * You can see edits and results using the [extract file](./classical-refactors/extract.py).

* Inline
    * In this test we inlined the ```oracle_gate``` and ```diffuser_gate``` functions. Doing this resulted in a random, unpredictable result. 
    * This test was the main reason we extended the code to work with more qubits, as when working with the 2 original qubit count, this test did not fail. 
    * You can see edits and results using the [inline file](./classical-refactors/inline.py).

* Rename
    * This test is simply an example of how renaming can improve readability of a file. While the file looks more 'cluttered' with the longer names, it is more readable and you better understand what exactly is being worked on. 
    * A better example of this is the optimized file, where the better names remain, but the clutterness does not. Read below.
    * You can see edits and results using the [rename file](./classical-refactors/rename.py).

* Optimized
    * This is a file utilizing multiple of the refactoring methods. We extracted the same functions as we did in the extract test, and put the functions in the [helper file](./classical-refactors/helper.py). 
    * The ```calculate_optimal_iterations``` function was inlined.
    * The new, more descriptive names are utilized effectively in this file, as with the extra functions moved to an own file, the file is much shorter and does not feel cluttered.
    * The changes can be viewed in the [optimized](./classical-refactors/optimized.py) and [helper](./classical-refactors/helper.py) files.