## Creazione e esecuzione container ECS

Per creare manualmente un container ECS, andare nella pagina del microservizio AWS ECS e selezionare sotto la voce **Task Definition** la build precedentemente caricata.
Inserire i parametri:
* AWS_DEFAULT_REGION : la regione dell'utenza AWS
* DESTINATION_BUCKET: Il nome identificativo del bucket S3 di destinazione, dove verranno caricate le curve di carico scaricate da MyTerna
* QUEUE_NAME: Il nome della coda SQS, da istanziare nella pagina AWS sotto il servizio Simple Queue Service
* ENVIRONMENT: L'ambiente in cui si vuole eseguire la task,  "prod" per la produzione o "stag" per lo staging
* COMPANY: Il nome della compagnia per cui vogliamo scaricare le curve di carico
* HISTORICAL: true se vogliamo eseguire un'esecuzione storica, false per un'esecuzione mensile

![input](https://github.com/mnarizzano/se22-p09/assets/101431140/1b408a65-e884-4aee-9ee3-bcac2c056244)

## Visualizzare i risultati
* Si possono visualizzare i log del software nella pagina CloudWatch del microservizio AWS
* I risultati si possono visualizzare nella pagina S3 del microservizio AWS, nel bucket indicato come DESTINATION_BUCKET nella creazione del container.




![s3](https://github.com/mnarizzano/se22-p09/assets/101431140/6c9373bd-38b1-4515-a175-ac44ae21d7a7)
