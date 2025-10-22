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
    * To alter runs / iterations in Q#, you simply specify how many qubits you wish to test on (line 8), then the 'CalculateOptimalIterations' function will do the rest
    * You can not alter iterations in the Qiskit implementation of Grover (yet).
 
### What causes different results, and what changes:
* Manually changing iterations in Q#
    * Manually altering iterations in Q# to the 'unoptimal' causes results to differ. The result becomes both unpredictable and inconsistent.

* Switching sequence of gate-applications
    * In Q#, you can switch line 58 and 59 to reorder the application of the X and H gates. Switching these lines produces unpredictable results. This can be tested with the 'main-altered.qs' file.

    * In Qiskit, you can switch line 16 and all following lines until 23 (lines 16-22). Switching lines 18 and 19 will produce inconsistent results, while switching 16 and 17 will produce a consistent, but flipped result. Switching 21 and 22 will also produce flipped results. This can be tested with the 'main-altered.py' file.
 