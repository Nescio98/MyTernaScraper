### User Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154


**VERSION : 1.0**

**Authors**  
Simone Palladino  
Edoardo Bianco

**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 14-01-2023 | Simone Palladino, Edoardo Bianco | First Draft |
| 1.1 | 28-01-2023 | Simone Palladino | Second Draft |
| 1.2 | 11-03-2023 | Simone Palladino | Third Draft |
| 1.3 | 24-03-2023 | Simone Palladino | Final Draft |


# Table of Contents

1. [Introduzione](#p1)
	1. [Document Scope](#sp1.1)
	2. [Definitios and Acronym](#sp1.2) 
	3. [References](#sp1.3)
2. [System Description](#p2)
	1. [Context and Motivation](#sp2.15)
	2. [Project Objectives](#sp2.2)
3. [Requirement](#p3)
 	1. [Stakeholders](#sp3.1)
 	2. [Functional Requirements](#sp3.2)
 	3. [Non-Functional Requirements](#sp3.3)
  
  

<a name="p1"></a>

## 1. Introduzione
Il documento presente descrive i requisiti funzionali e non-funzionali di un sistema che vuole poter scaricare una grossa quantità di dati dal sito di Terna, un operatore di reti per l'energia elettrica in Italia, e salvarli in maniera ordinata nel database dell'azienda.
<a name="sp1.1"></a>

### 1.1 Document Scope
Il documento descrive le funzionalità del sistema, spiegando i servizi forniti e i vincoli sotto i quali deve operare.
<a name="sp1.2"></a>

### 1.2 Definitios and Acronym


| Acronym				| Definition | 
| ------------------------------------- | ----------- | 
|AWS|Amazon web services|
|S3|Amazon Simple Storage Service|
|SQS|Amazon Simple Queue Service|
|ECS|Amazon Elastic Container Service|


<a name="sp1.3"></a>

### 1.3 References
[Amazon Simple Storage Service](https://aws.amazon.com/it/s3/)

[Amazon Simple Queue Service](https://aws.amazon.com/it/sqs/)

[Amazon Elastic Container Service](https://aws.amazon.com/it/ecs/)

[Sito myTerna](https://myterna.terna.it/portal/portal/myterna)


<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>

### 2.1 Context and Motivation
EGO è leader in Italia nella valorizzazione dell’energia prodotta da fonti rinnovabili e nell'efficienza energetica, acquista l’energia prodotta da circa 1500 impianti di produzione di energia, per poi venderla sul mercato elettrico nazionale. Al fine di ottimizzare la vendita sul mercato dell'energia prodotta dagli impianti dispacciati da EGO, è necessario conoscere la produzione di energia e altre grandezze fisiche e operative degli impianti in tempo reale. L'applicativo vuole facilitare la gestione e il salvataggio dei dati forniti da Terna riguardanti le curve di carico per ogni impianto dispacciato da Ego, al fine di poter calcolare i conguagli fino a cinque anni indietro.
<a name="sp2.2"></a>

### 2.2 Project Obectives 
Il software deve accedere al portale myTerna, un grosso database privo di api, e attraverso un web scraper deve poter fare due tipi di download in base all'input ricevuto, **mensile** o **storico**:

* Il download **mensile** consiste nello scaricare tutti i dati riguardanti le curve di carico per ogni impianto attualmente dispacciato da Ego. Il download mensile si riferisce al mese precedente a quello corrente.
* Il download **storico** consiste nello scaricare tutti i dati riguardanti le curve di carico per ogni impianto attualmente dispacciato da Ego, ma sull'arco temporale degli ultimi 5 anni. Questo tipo di operazione serve per scansionare l'intero database di terna e scaricare eventuali file persi dall'operazione mensile, in quanto Terna può caricare o aggiornare versioni differenti dello stesso file a distanza di massimo 5 anni.

I file scaricati da queste operazioni devono essere caricati su S3, una soluzione di archivazione dati offerta da AWS.
Infine il sistema deve inviare una notifica contenente il nome dei file scaricati.

<a name="p3"></a>

## 3. Requirements

| Priorità | Significato | 
| --------------- | ----------- | 
| M | **Mandatory:**   |
| D | **Desiderable:** |
| O | **Optional:**    |
| E | **future Enhancement:** |

<a name="sp3.1"></a>
### 3.1 Stakeholders
Matteo Fattore - Chief Information Officer </br>
Fabio Garagiola - Software Architect </br>
Stefano Balboni - Responsabile Database </br>
EGO Energy S.R.L </br>
EGO Data S.R.L </br>
Terna S.P.A </br>

<a name="sp3.2"></a>
### 3.2 Functional Requirements 

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| f1 | Il sistema dovrebbe essere in grado di prendere in input la compagnia che dispaccia gli impianti di cui si vogliono scaricare le curve di carico |M|
| f2 | Il sistema dovrebbe essere in grado di prendere in input il tipo di operazione da eseguire, tra mensile o storica  |M|
| f3 | Il sistema dovrebbe accedere a dati fino a 5 anni nel passato |M|
| f4 | Il sistema dovrebbe gestire problematiche di time out causate dal sito di Terna |M|
| f5 | Il sistema di lettura all'interno del sito di Terna dovrebbe poter essere parallelizzabile |D|
| f6 | Il sistema dopo aver scaricato i dati dovrebbe salvarli su s3 con una struttura ben definita |D|
| f7 | Il sistema dovrebbe essere predisposto a poter inviare in futuro  una notifica via mail specificando di quali impianti sono state scaricate le curve di carico |E|



<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| nf1 | Il sistema dovrebbe terminare l'operazione di lettura e scrittura dei 5 anni di dati in meno di 18 ore |D|
| nf2 | Il sistema dovrebbe essere robusto a eventuali problematiche del sito di Terna e terminare le operazioni soltanto dopo aver scaricato tutti i file richiesti dall'operazione |M|
| nf3 | Il sistema dovrebbe essere incapsulato all'interno di un docker per essere facilmente integrato negli altri servizi dell'azienda |M|
