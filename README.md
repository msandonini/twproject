# Mediapop
## Librerie/software utilizzati

Per questo progetto sono stati utilizzati i seguenti packages di Python:

- pipenv: pacchetto Python per la gestione di ambienti virtuali
- django: web framework utilizzato come server
- bleach: pacchetto Python per la messa in sicurezza di file HTML e la prevenzione di XSS injection
- pillow: pacchetto Python per la gestione di immagini inserito per garantire il perfetto funzionamento dei campi ImageField dei modelli Django

N.B. I pacchetti si riferiscono alla versione 3.11 di Python. Il sistema è stato programmato e testato con questa versione. Non c'è garanzia che funzioni con versioni differenti del linguaggio.

## Istruzioni per l'esecuzione

### Configurazione dell'ambiente

Controllare che `pipenv` sia installato:

```shell
pipenv --version
```
Se il pacchetto non è installato installarlo:

```shell
pip3 install pipenv
```

Una volta installato entrare nella directory del progetto se già non ci siamo, entrare nell'ambiente virtuale, ed eseguire un'operazione di sincronizzazione dei pacchetti installati:

```shell
cd twproject
pipenv shell
pipenv sync
exit
```

### Esecuzione del server

Una volta installati i pacchetti necessari, avviare il server django da dentro l'ambiente virtuale:

```shell
pipenv shell
python manage.py runserver
```