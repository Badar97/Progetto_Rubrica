## Progetto Rubrica
#### Ali Waqar Badar

### Inizio
Realizzare	un	progetto in Java o Python	che rappresenti	una	rubrica telefonica,	un software	che	gestisca i contatti.

Il	software deve	avere	una	classe	`Persona` che	contenga le	informazioni di	uno	dei	contatti	della	rubrica. Lo stesso software deve contenere	una	lista di	oggetti	di tipo	persona.	Deve	permettere la	creazione, la	modifica e l’eliminazione	delle	persone	esistenti.

La	persona	deve mantenere le seguenti	informazioni:
```zsh 
- nome: stringa
- conome: stringa
- indirizzo: stringa
- telefono: stringa
- eta: intero
```

### Interfaccia grafica
Nell’interfaccia	 dell’applicazione ci	 deve	essere	una	finestra	principale,	che	mostra	una	tabella	con	una	riga	per	ogni	persona.	Le	colonne	devono	mostrare	solo	`nome`,	`cognome`	e	`telefono`.	In	basso	ci	devono	essere	tre	bottoni:
- `nuovo`:	serve	per	creare	una	nuova	persona
- `modifica`:	serve	per	modificare	una	persona	esistente
- `elimina`:	serve	per	eliminare	una	persona	esistente

I tasti	 nuovo	 e	 modifica	 devono	 portare	 all’apertura	 di	 una	 seconda	 finestra,	 chiamata	 editor-persona,	che	serve	per	inserire	e modificare	i	dati	di	una	persona.	Questa	finestra	deve	avere	una	serie	 di	 campi,	 divisi	 per	 riga,	 nomeCampo	– valoreCampo,	 per	 ogni	 dato	 della	 persona. Questa	 finestra	 è	 sostanzialmente	 un	 modulo	 di	 inserimento	 dati	 per	 un	elemento	Persona.	Questa	finestra	deve	avere	due	bottoni:	`salva`	e	`annulla`.	

### Persistenza
Procederemo	 alla	 realizzazione	 della	 persistenza	 mediante	 salvataggio	 su	 file. Tramite	 la	 classe	`Scanner`	leggeremo	da	file	e	tramite	la	classe	`PrintStream`	scriveremo	su	file.	Nel file inseriremo il contenuto dei dati delle persone seguendo la seguente codifica:
```zsh 
Steve;Jobs;via Cupertino 13;0612344;56
Bill;Gates;via Redmond 10;06688989;60
Babbo;Natale;via del Polo Nord;00000111;99
```

Esportare il programma in un file `.exe` con il nome `Rubrica.exe`
  
 
