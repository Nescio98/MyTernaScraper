## Repository Fargate

La repository è composta dai seguenti file:

- Ecs: contiene il file cloudformation con le specifiche del task Fargate
  - **Nel caso in cui vadano specificati dei permessi IAM per effettuare determinate operazioni (es. upload su S3), sarà necessario aggiungere i permessi sotto la sezione TaskRole->Properties->AssumeRolePolicyDocument->Statements (utilizzare i permessi già presenti come template)**
- Bitbucket_pipeline_set_env.sh: script che viene eseguito dalla pipeline Bitbucket per settare le variabili d'ambiente con i valori delle variabili del workspace di Bitbucket.
- Bitbucket-pipelines.yml: file che contiene la logica della pipeline Bitbucket
- Dockefile: il Dockerfile per la generazione dell'immagine Docker che verrà utilizzata dal task Fargate.
  - **Inserire inserire una COPY con eventuali nuovi file che saranno utilizzati dall'ecs (che andranno anche aggiunti, come descritto al punti sopra, all'interno della pipeline**
- handler.py: file handler della Lambda, qui sarà specificata la logica python della Lambda
- requirements.txt: il file requirements di python che contiene le dipendenze della Lambda
- shared.py: file shared che contiene metodi utili da utilizzare nell'handler. **Si consiglia di utilizzare questi metodi, se presenti, per effettuare determinate operazioni (es. upload su S3)**. 


## Istruzioni al deploy su BitBucket

- Nella pagina del repository su Bitbucket cliccare sulla scheda "Pipelines".
- Per configurare la pipeline cliccare sul pulsante "set up pipeline e selezionare "custom".
- Aggiungi le istruzioni per la build del tuo progetto nel file bitbucket-pipelines.yml. 
- Salva le modifiche alla  pipeline e Bitbucket eseguirà automaticamente la prima build del  progetto. Puoi monitorare il progresso della build nella scheda "Pipelines".
- Una volta che la  pipeline è stata configurata correttamente, Bitbucket eseguirà automaticamente la build del tuo progetto ogni volta che effettuerai una modifica e pusherai il codice sul repository.
