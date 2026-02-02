# Project: Cutset Conditioning for CSP

Questo progetto implementa un solver per problemi di soddisfacimento di vincoli (CSP) basato sulla tecnica del *cutset conditioning*.  
Sono incluse istanze di map coloring e di criptoaritmetica per testare il corretto funzionamento dell’algoritmo.

---

## Ruolo dei file

- **csp.py**  
  Definisce la classe `CSP`, che rappresenta un problema di soddisfacimento di vincoli con variabili, domini e vincoli.

- **tree_solver.py**  
  Implementa un risolutore basato su backtracking per CSP ad albero.

- **cutset.py**  
  Implementa la tecnica del cutset conditioning: identifica il cutset, costruisce i vincoli residui e risolve il problema.

- **mapcolor.py**  
  Contiene i generatori di istanze di colorazione di mappe (Australia, Europa semplificata, USA semplificata).

- **cryptarithmetic.py**  
  Contiene i generatori di istanze di criptoaritmetica (`T+T=EE`, `SEND+MORE=MONEY`, `TWO+TWO+TWO=SIX`).

- **main.py**  
  Main che esegue la risoluzione di tutte le istanze e salva i risultati di ogni istanza in diversi file all'interno della cartella `logs_of_istances`.

---

## Riproduzione dei risultati

Per riprodurre i risultati sperimentali:

1. Copiare tutti i file Python nella stessa directory.  
2. E' preferibile avere installata l’ultima versione di **Python 3** (non sono richieste librerie esterne).  
3. Eseguire il comando:  

   ```bash
   python3 main.py

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

This project implements a solver for constraint satisfaction problems (CSP) based on the *cutset conditioning* technique.  
Map coloring and cryptarithmetic instances are included to test the correct functioning of the algorithm.

---

## Role of files

- **csp.py**  
  Defines the `CSP` class, which represents a constraint satisfaction problem with variables, domains, and constraints.

- **tree_solver.py**  
  Implements a backtracking-based solver for tree CSPs.

- **cutset.py**  
  Implements the cutset conditioning technique: identifies the cutset, constructs the residual constraints, and solves the problem.

- **mapcolor.py**  
  Contains map coloring instance generators (Australia, simplified Europe, simplified USA).

- **cryptarithmetic.py**  
  Contains cryptarithmetic instance generators (`T+T=EE`, `SEND+MORE=MONEY`, `TWO+TWO+TWO=SIX`).

- **main.py**  
  Main program that solves all instances and saves the results of each instance in different files within the `logs_of_instances` folder.

---

## Reproducing the results

To reproduce the experimental results:

1. Copy all Python files to the same directory.  
2. It is preferable to have the latest version of **Python 3** installed (no external libraries are required).  
3. Run the command:

```bash
   python3 main.py
