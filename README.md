# Progetto: Cutset Conditioning per CSP

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
