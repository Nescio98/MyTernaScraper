## Intervista per web scraper

**Che tipo di applicativo vi serve?**

Servirebbe un web scraper che navighi sul sito di Terna e che sia in grado di scaricare i dati delle curve di carico degli impianti di interesse di Ego Data ed Ego Energy.

**Avete già un software che fa qualcosa del genere?**

Abbiamo già implementato il software che si occupa di questo task, per quanto riguarda il download dei dati non storici funziona abbastanza bene, ma non riusciamo a fargli completare il ciclo di download storico.

**Che differenza c'è tra un download storico e uno non storico?**

La differenza è rispetto alla quantità di dati scaricati, un download di dati non storici si dovrà occupare di scaricare i dati dell'ultimo mese trascoro degli impianti di interesse. Un download storico invece dovrà occuparsi di ottenere tutti i dati contenuti sul sito degli ultimi 5 anni di tutti gli impianti di nostro interesse.

**Dove si trovano i metadati degli impianti che vi interessano?**

Abbiamo tutti i metadati all'interno dei server AWS.

**Cosa fa il software attualmente quando provate a eseguire una run storica?**

Il software arriva alla conclusione dopo circa 16-18 ore ma non abbiamo modo di verificare se sia andato a buon fine o meno e quando andiamo a verificare su S3 se sono stati archiviati correttamente spesso solo una piccola quantità di curve di carico è stata effettivamente scaricata.

**Che differenza c'è tra Ego Data ed Ego Energy?**

Sono due reparti diversi di Ego Energy che si occupano ognuno di impianti differenti, quindi quando dovrete scaricare i dati avrete una lista di impianti di interesse per Ego Data ed una lista differente per Ego Energy. La differenza più grossa è il numero di impianti in quanto la lista di impianti di interesse per Ego Energy è molto più lunga dell'altra.

**Cos'è S3?**

S3 è una tecnologia che fornisce AWS e che permette di salvare dati sotto forma di file.

**Sapete già perchè la run storica non va a buon fine? Se è un problema dell'applicativo o del sito di Terna?**

Crediamo che i problemi siano su entrambi, il sito Terna ha dei crash durante l'esecuzione del flusso e l'applicativo non è in grado di riconoscerli correttamente e agire di conseguenza. Uno dei vostri primi compiti sarà quello di capire quando e perchè il sito Terna crasha.

**Avete detto che una run storica al momento dura circa 16-18 ore, avete dei vincoli temporali da rispettare?**

E' necessario che l'applicativo non superi questo numero di ore perchè lo facciamo partire la sera e ne abbiamo bisogno il giorno successivo.

**Avete necessità di scaricare solo il mese corrente o i 5 anni di tutti gli impianti o volete poter selezionare mesi specifici e impianti specifici?**

Non ci serve poter prendere particolari periodi tremporali o sottoinsiemi di impianti, per le nostre necessità è sufficiente eseguire correttamente la run storica e il mese trascorso.
