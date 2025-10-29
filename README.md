# Testing enviroment - Behavioral changes of quantum applycations after refactoring and line reordering

### Tools used in project:
* Python 3.13.5
    * Pip, v25.2
    * Qiskit, v2.2.1
    * Qiskit-aer, v0.17.2
    * Matplotlib, v3.10.7
* Visual Studio Code, v1.103.2
    * Azure Quantum Development Kit, v1.21.0


### Procedure:

#### Q#:
* Run in Visual Studio Code using Azure QKD

#### Qiskit:
* Run 'python3 main.py' in terminal
    * Replace python version with locally installed, may for instance be 'python main.py'

 
### Instructions:
* Altering runs:
    * Iterations in Q# are optimally calculated on line 9. The result of the function can be overwritten if a value is assigned after the function has been called, or by replacing the function call itself with a value. 
    
    * Iterations in Qiskit are optimally calculated, just as in Q#. This function can be ignored by manually writing number of iterations on line 14 (replacing function call), or by overwriting value after calling function. 
 
### What causes different results, and what changes:
* Manually changing iterations in
    * Manually altering iterations to the 'unoptimal' causes results to differ. The result becomes both unpredictable and inconsistent.

* Switching sequence of gate-applications
    * In Q#, you can switch line 53 and 54 to reorder the application of the X and H gates. Switching these lines produces unpredictable results. This can be tested with the 'main-altered.qs' file.

    * In Qiskit, you can switch line 25 and all following lines until 32 (lines 25-31). Switching lines 27 and 28 will produce inconsistent results, while switching 25 and 26 will produce a consistent, but flipped result. Switching 30 and 31 will also produce flipped results. This can be tested with the 'main-altered.py' file.
 