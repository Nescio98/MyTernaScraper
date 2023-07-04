# MyTernaScraper

### EGO Energy
#### Contesto

EGO è leader in Italia nella valorizzazione dell’energia prodotta da fonti rinnovabili e nell'efficienza energetica, acquista l’energia prodotta da circa 1500 impianti di produzione di energia, per poi venderla sul mercato elettrico nazionale. Al fine di ottimizzare la vendita sul mercato dell'energia prodotta dagli impianti dispacciati da EGO, è necessario conoscere la produzione di energia e altre grandezze fisiche e operative degli impianti in tempo reale.


#### Progetto
Il progetto prevede il download di una grande quantità di dati relativi agli impianti di produzione energetica dal sito di Terna, 
che non fornisce API per il download. L'approccio utilizzato prevede l'utilizzo di una funzione Lambda serverless per riempire una coda di messaggi 
che contengono i dati necessari per il download dei dati di un singolo mese relativi ad un particolare impianto. Una volta che la coda è stata riempita, 
una serie di container eseguirà il codice relativo al web-scraper, che si occuperà di eseguire il login sul sito MyTerna e di eseguire il download dei dati 
relativi ai messaggi contenuti nella coda, per poi caricare i risultati nel database di EGO. 

Dettagli aggiuntivi nella [documentazione](https://github.com/mnarizzano/se22-p09/tree/main/docs)
