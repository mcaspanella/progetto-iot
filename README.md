Progetto IOT Based Smart System - Timestamping su Blockchain di un file contenente dati provenienti da Arduino YUN

1. Primo passo - Configurazione Arduino YUN
Per la realizzazione del progetto, abbiamo configurato la board Arduino YUN sulla nostra rete WIFI: tramite lo sketch in allegato, abbiamo inviato dei dati numerici random (che rappresentano la temperatura rilevata in 24 ore) ad un nostro server Flask, che provvederà alla creazione del timestamp.

2. Secondo Passo - Creazione Timestamp del file tramite Opentimestamps Client
Cos'è OpenTimestamps:
OpenTimestamps è un progetto open-source che permette la creazione e la verifica di timestamp di file, utilizzando la blockchain Bitcoin. Il concetto principale è quello di utilizzare una blockchain come un registro pubblico e immutabile per convalidare l'istante temporale (timestamp) in cui un determinato file è stato creato o modificato.
Questo può essere utile in vari contesti, come la prova di esistenza di un documento in un momento specifico o la verifica dell'integrità di dati digitali nel tempo.

Le caratteristiche principali di OpenTimestamps sono:
-Open-Source: Il progetto è open-source, quindi il codice sorgente è disponibile pubblicamente a tutti, per cui chiunque può ispezionare il codice e contribuire al progetto.
-Decentralizzato: OpenTimestamps consente gratuitamente a chiunque di creare timestamp utilizzando la blockchain Bitcoin, senza la necessità di avere un'autorità esterna che confermi la transazione.
-Interoperabilità: Gli orari generati da OpenTimestamps sono indipendenti dalla blockchain e possono essere verificati persino offline.
-Flessibilità: È possibile utilizzare OpenTimestamps per creare timestamp di dati di qualsiasi tipo, inclusi file, documenti, transazioni Bitcoin e altro ancora.
-Immutabilità: Una volta registrato un timestamp sulla blockchain, esso non può più essere modificato o cancellato, il che fornisce una prova pubblica dell'istante di tempo in cui i dati sono stati convalidati.

Per poter utilizzare OpenTimestamps, è necessario un client OpenTimestamps: nel nostro caso, abbiamo creato un server tramite Flask che, ricevuti dei dati da Arduino YUN, genera un file.txt con i suddetti dati e lo invia ad Opentimestamps.

Opentimestamps utilizza quattro Calendar gratuiti per la gestione delle transazioni sulla blockchain.
I Calendar disponibili sono i seguenti:
-   Alice : <a href="https://alice.btc.calendar.opentimestamps.org/" target="_blank">https://alice.btc.calendar.opentimestamps.org/</a>
-   Bob : <a href="https://bob.btc.calendar.opentimestamps.org/" target="_blank">https://bob.btc.calendar.opentimestamps.org/</a>
-   Finney : <a href="https://finney.calendar.eternitywall.com/" target="_blank">https://finney.calendar.eternitywall.com/</a>
-   Catallaxy : <a href="https://ots.btc.catallaxy.com/" target="_blank">https://ots.btc.catallaxy.com/</a>

## Come eseguire il Timestamping
Il Server, una volta ricevuti i dati da Arduino, genera un file.txt (nel nostro caso 'data_2023-11-05_17-04-22.txt') ed esegue il timestamping utilizzando il comando:

```bash
ots stamp data_2023-11-05_17-04-22.txt
```

Il comando riprodurrà in output su terminale le seguenti informazioni:

```
Submitting to remote calendar https://a.pool.opentimestamps.org
Submitting to remote calendar https://b.pool.opentimestamps.org
Submitting to remote calendar https://a.pool.eternitywall.com
Submitting to remote calendar https://ots.btc.catallaxy.com
```

A questo punto viene eseguito un algoritmo di `"hashing"` (sha256) sul file originale, il quale riproduce in output una stringa di lunghezza fissa (64 caratteri in esadecimale) chiamata `"hash"`, che rappresenta un'impronta digitale univoca del file.<br>
Per registrare il timestamp su una transazione sulla blockchain Bitcoin, viene generato un file con estensione `.ots`, che contiene le informazioni riguardo il timestamp.<br>
Successivamente, con il comando:

```bash
ots verify data_2023-11-05_17-04-22.txt.ots
```

è possibile verificare lo stato attuale del `Timestamping` nei quattro Calendar.

Nel nostro caso, sul serever è presente una route che, dato il nome del file, ne verifica lo stato.
Inizialmente lo stato dell'operazione è `"Pending confirmation in Bitcoin blockchain"`, infatti compariranno le seguenti informazioni:

```
Calendar https://finney.calendar.eternitywall.com: Pending confirmation in Bitcoin blockchain
Calendar https://btc.calendar.catallaxy.com: Pending confirmation in Bitcoin blockchain
Calendar https://bob.btc.calendar.opentimestamps.org: Pending confirmation in Bitcoin blockchain
Calendar https://alice.btc.calendar.opentimestamps.org: Pending confirmation in Bitcoin blockchain
```

La conferma del timestamp sulla blockchain Bitcoin richiede alcune ore, perché Opentimestamps non esegue una transazione per timestamp, bensì combina un numero illimitato di timestamp in un unica transazione.<br>
Quando la transazione viene inclusa in un blocco valido e confermata sulla blockchain, il timestamp è considerato ufficialmente convalidato. 
(Nel nostro caso, abbiamo visto che il blocco creato era il seguente: Bitcoin block height 815461)

Infine, con il comando:

```bash
ots info data_2023-11-05_17-04-22.txt.ots
```

vengono mostrate ulteriori informazioni sul timestamp:

```
File sha256 hash: 48a0dff891f56a43e6adf74e95b3673581f85c5635cced1ffa360df97647d5c7
Timestamp:
append 2bbdc3ef8776b33864db28001bd37278
sha256
 -> append 29303b824f84e5ccbb6d1b3a40fef9be
    sha256
    prepend 6547bd07
    append 8b49e1d3abedff35
    verify PendingAttestation('https://btc.calendar.catallaxy.com')
 -> append a2dbced7be00e813e0169fda5df5a571
    sha256
    prepend 6547bd07
    append c615c1be6492a926
    verify PendingAttestation('https://bob.btc.calendar.opentimestamps.org')
 -> append b80ba3e215d9fb8cd22c8027afdd144e
    sha256
    append eab17a72d2a60f1bc0e5c581242fb6221ec68218c677b942e4eb70ca4eec08f2
    sha256
    prepend 6547bd07
    append 2a4f85afd0c60036
    verify PendingAttestation('https://alice.btc.calendar.opentimestamps.org')
 -> append ba6cb39fc910b4f27bda9f7b454e3437
    sha256
    prepend 7f99017a63c36a248412bacf2628d7dd0905328cbccb07ed0fe847ed769cf6af
    sha256
    prepend 6547bd06
    append b9845c6d941be973
    verify PendingAttestation('https://finney.calendar.eternitywall.com')

```

Quando il timestamp verrà confermato dalla blockchain, compariranno anche le informazioni sul blocco e sulla transazione.
