# Results for different alterations done on [Main.qs](./Main.qs)
* Results of testing the consequences of:
    * Reordering gate-application.
    * Movement of for-loops and its surrounding functions.
    * Standard refactoring measures on quantum code.

## What is being tested

### Line Switches
* In this section we are going to focus on line switches, bit limited to the applications of gates, specifically the order of gate applications. 

* 53+54
    * Lines 53 and 54 consists of an X-gate and an H-gate. 
    ```
    X(outputQubit);
    H(outputQubit);
    ```
* 60
    * Line 60 contains the X-gate being applied to every other qubit. 
    ```
    for q in inputQubits[...2...] {
        X(q);
    }
    ```
* 63
    * Line 63 contains an CX gate being applied to all qubits, using a recently created outputQubit.
    ```
    Controlled X(inputQubits, outputQubit);
    ```
* 69
    * Line 69 activates all qubits using the Hadamard Gate.
    ```
    H(q);
    ```
* 74
    * Line 74 contains a CZ gate being applited to all qubits.
    ```
    Controlled Z(Most(inputQubits), Tail(inputQubits));
    ```
* 83
    * Line 83 contains an X-gate being applied to all qubits.
    ```
    X(q);
    ```
    

### For-loop
We have multiple for loops we could test this with to see consequences of a misplaced or misordered for loop. On out main we have loops on:
* Line 27 - 30 (F1)
    * Contains 2 functions with qubits entered as parameter

    ```
        for _ in 1..iterations {
        phaseOracle(qubits);
        ReflectAboutUniform(qubits);
    }
    ```

* Line 59 - 61 (F2)
    * Contains X-gate applications to every other qubit. 
    ```
    for q in inputQubits[...2...] {
        X(q);
    }
    ```
* Line 68 - 70 (F3)
    * Contains H-gate applications
    ```
    for q in inputQubits {
        H(q);
    }
    ```
* Line 82 - 84 (F4)
    * Contains X-gate applications
    ```
    for q in inputQubits {
        X(q);
    }
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

## Testing results

### For Loops

* F1
    * The F1 for loop contains the two functions phaseOracle and ReflectAboutUniform.
    * Switching the two lines makes no difference to the output / results.
    * However, this loop occurs after the PrepareUniform function, if the for loop were to be run prior to PrepareUniform, we would end up with a wrong and randomized result.
    * The altered code with PrepareUniform function being executed after the for-loop can be run from the [F1 file](./for-loop-reorder/F1.qs).

* F2 ---  this is not a for loop. keep regardless for memory info
    * There is not much to do with the F2 loop. It simply checks if requested qubits exceed allocatable qubits, and if so it stops prematurely. 
    * Theoretically, we could test what were to happen if the file was executed using 64 qubits, but the iterations calculation is far too high for a normal signed Interger. Even if we used unsigned Integers, the execution time would be long. Far too long to test. You could also remove the OptimalIterations functions and add a static number, but the memory required to execute the code is not realistic to have on normal computers at this time.
    * A statevector simulation represents the full quantum state using a (large) vector of complex numbers. The size of this vector grow exponentially at 2^N * 16, where N represents a qubit and 16 is the bytes allocated. For a state vector of (just) 20 qubits, we would need approximately 16GB of free memory. For 64 qubits, we would need approximately 295 billion GB of memory.
    * https://pmc.ncbi.nlm.nih.gov/articles/PMC6656884/ to cite

* F2 
    * The third for loop applies the X gate to every other qubit. There is multiple things we can do here:
        * Removing it: Doing this makes all qubits return as 1.
        * Moving it: If we move it to before the X and H gates above, the results do not change, we get the expected result.
    * The results can be viewed from the [F2 file](./for-loop-reorder/F2.qs). Default change is the removal. 

* F3
    * The 4th for-loop is rather simple, it just activates all the qubits using the H-gate. Removing this results in the qubits all returning 0. It is just 1 line, and the consequences of moving it was tested via F1, as the call of the ```PrepareUniform()``` function is dont at the beginning of the file, right before F1 occurs. There is not much else do be done or tested, as the loop only contains the H-gate.
    * The results can be viewed from the [F3 file](./for-loop-reorder/F3.qs).

* F4
    * The last for-loop exists in the ```ReflectAboutUniform()``` function, which like the F3 function ```PrepareUniform()```, is called at the beginning of the file. Removing this for-loop results in the output being randomized. We could also put this for- loop before the line ```Adjoint PrepareUniform(inputQubits);```. This also results in the output becoming randomized and upredictable. 
    * The results can be viewed from the [F4 file](./for-loop-reorder/F4.qs).

### Line Switches
* Lines 53 and 54
    * Line 53 and 54 consists of an X and an H gate application. Switching these two lines results in the output becoming unpredictable and random. 
    * Removing line 53 (X Gate) has the same results. 
    * Removing line 54 (H Gate) has a bigger effect, it crashes the application. The error message that follows is 'Qubit5 released while not in |0⟩ state'.
    * Results can be viewed in the [L53+54 file](./line-switches/L53-54.qs).

* Line 60
    * This is the appliation of the X gate to every other qubit, done in a for-loop. Removing this leads to the output being a consistent 1,1,1,1,1.
    * Results can be viewed in the [L60 file](./line-switches/L60.qs).

* Line 63
    * Line 63 applies a CX gate to all qubits. Prior to this, we configure an output-qubit (being used as comparison to the inputQubits). We apply the X and H gate to this output-qubit, and follow by X-gating every other input-qubit. 
    We then proceed by using the CX gate on the inputQubits using the outputQubit. 
    * Removing this gate results in the results again becoming random and unpredictable.
    * Removing this line also causes the qubits to not be engangled, as they would be after CX-application.
    * Results can be viewed in the [L63 file](./line-switches/L63.qs).

* Line 69
    * Line 69 applies the Hadamard Gate to all qubits. Removing the activation results in all qubits consistently being 0.
    * Results can be viewed in the [L69 file](./line-switches/L69.qs).

* Line 74
    * Line 74 contains a Pauli Z gate. Removing this line results in a randomized and unpredictable result. 
    * Results can be viewed in the [L74 file](./line-switches/L74.qs).

* Line 83
    * Line 83 contains the X gate, which is applied to all qubits. Removing this line results in a randomized and unpredictable result.
    * Results can be viewed in the [L83 file](./line-switches/L83.qs).

### Refactors
* Renaming
    * This refactor does not change functionality, and does not break code if performed correctly. As long dependencies, calls etc are updated alongside the name, nothing should change.
    * Rename of GroverSearch can be viewed in the [renaming.qs file](./classical-refactors/renaming.qs).
    * Not much was changed in file, but the ```operation Grover``` section was renamed ```operation GroverAlgorithm``` and ```ReflectAboutMarked``` was renamed to ```ReflectionAboutMarked```.
* Encapsulate
    * This does
    * Results can be viewed in the [encapsulate file](./classical-refactors/encapsulate.qs).
* Inline
    * Was performed on the ```ReflectAboutAllOnes``` and ```PrepareUniform``` functions. Both calls were replaced with their content.
    * Results can be viewed in the [inline file](./classical-refactors/inline.qs).
    * Lines containing inlined content is 27 - 29 and 95 on the new file.
    * No consequences were noticed ater this change, result remains the same. 
* Extract
    * This does
    * Results can be viewed in the [extract file](./classical-refactors/extract.qs).
