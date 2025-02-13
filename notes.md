Db-info i config-fil (eg config.py) eller miljøvariabel (.env) for bedre sikkerhet, fleksibilitet og orden.
* disse filene bør da utelates fra repo med .gitignore
* miljøvariabler er "best" fordi disse lagres på OS-nivå
* krever lib 'python-dotenv'
* .env er bare key/value, helt fritt

CTRL + NUM for å bytte vindu i Code - lager også ny vindu

Lurt å kjøre Flask i ekstern terminal fordi..
* bedre logging, miljøvariabler, kombinere med andre CLI-verktøy, nærmere produksjonsoppsett
* men mister Code-fordeler som breakpoints og logpoints
* og debug må settes i .env, tror app.run() ignorerer elns
* og flask run > python app.py pga Flask CLI-funksjoner :)

Filer i .gitignore blir greyed out i filutforskeren i Code

Jinja
* "include 'foo.html'" for enkel importering og direkte bruk av hele modul foo
* hvis man definerer en block kan denne erstattes av filer som "extends"
* innrykk og linjeskift er ikke meningsbærende

url_for heller enn statisk lenking pga fleksibilitet, unngår caching, og tryggere å flytte

Egt bedre å bruke Flasks egen 'logging' bibliotek i stedet for print

Anbefalt å spesifisere kolonner i INSERT-statements i tilfelle tabellen senere får andre kolonner
SQLite foretrekker INTEGER > INT, og TEXT > VARCHAR
* SQLite håndhever uansett ikke lengdebegresninger på VARCHAR

Med en with-kontekst (eg with foo.connect('bar') as conn: ) vil forbindelsen automatisk lukkes når konteksten avsluttes.

bcrypt er en treig og relativt sikker hashe-algoritme. generer en ny saltverdi for hvert passord - dvs at samme passord generer ulike hasher for to brukere. passord + salt = hash
* hashet inneholder saltet... Men det er visst helt trygt hmmm

Trenger ikke conn.commit() ved SELECT?

Flask-sessions krever en app.secret_key for å signere data, og import av lib session
* session["foo"]="bar"
* session.pop("foo")
* session.set?

Flashe via session med lib flash sin flash("foo", "category"). Vises i Jinja via get_flashed_messages(). Flash()-meldinger vises kun en gang.

Sende statuskode manuelt ved å legge det til som argument i return-statemen
* definere custom reaksjon på statuskoder med @app.errorhandler(int)

En dekoratør er en funksjon som "pakker inn" en annen funksjon og legger til ekstra funksjonalitet, uten å endre selve funksjonen. Eg brukes @app.route() for å knytte en funksjon til en route ig

Kan tvinge logging med 'flask run --debug'. Åja, men bruk enten "flask run" eller debug=True, ikke begge hmm

HTTP/1.1 viser versjonen av HTTP-protokollen som ble brukt i forespørselen

Optional Default Parameter: 
data = {"navn": "Ola"}
print(data.get("navn", "Ukjent"))  >> "Ola"
print(data.get("alder", "Ukjent"))  >> "Ukjent" (istedenfor KeyError)

Flasks innebygde webserver er ikke egnet til prod pga: treig (single-threaded), ustabil, utrygg
Nginx: ligger mellom klienten og webserveren. Tilbyr omvendt proxy for sikkerhet (flask eksponeres ikke direkte), og gjør lastbalansering hvis du skalerer opp til flere Flask-servere samtidig
Waitress eller Gunicorn: bedre webserver enn den innebgyde, kanskje primært fordi de er multi-threaded

"En omvendt proxy er en server som tar imot forespørsler fra klienter (nettlesere) og sender dem videre til en intern server, for eksempel en Flask-applikasjon."

"AJAX (Asynchronous JavaScript and XML) lar nettleseren hente og sende data til en server uten å laste inn hele siden på nytt."
HTMX er et mer moderne bibliotek med samme funksjon

PHPMyAdmin er bare en webbasert GUI for å administrere MariaDB/MySQL
* Men PHPMyAdmin krever en webserver som Apache og at PHP er installert tror jeg, så det er litt stress

MariaDb og Postgres er DBMS. MySQL Workbench og PHPMyAdmin er GUI-verktøy for å styre DBMSer. 
Workbench kan: skrive sql (for deg), generere modeller og tilhørende kode, administrere bruker, overvåke - og sikkert mer

I Windows er en service ("tjeneste") et program som kjører i bakgrunnen, vanligvis uten et GUI. == daemon i Linux.

mysql.connector er Oracle-eid - pymysql er open source og med bedre støtte for mariadb. men forskjellen er minimal egt.  

migrere fra sqlite -> mariadb: oppdatere miljøvariabel for db_info og bytte funksjon fra sqlite3.connect(db_info) til pymysql.connect(db_info)
* men også endringer i koden... AUTOINCREMENT -> AUTO_INCREMENT, ? -> %s, må eksplisitt commite() selv med with-kontekst, kanskje TEXT -> VARCHAR, 
* så man migrerer gjerne ikke manuelt
* da bruker man heller et abstraksjonslag i mellom kode og db, eller en ORM som SQLAlchemy

Abstraksjonslag er rett og slett if db_type="sqlite": do sqlite3
* men må også håndtere sql-forskjeller. passe all sql gjennom en funksjon som konverterer ved behov

SQLA bruker db-agnostiske spørringer og tilpasser disse basert på db-tilkoblingene
Og tabeller opprettes som Python-klasser

"schema" og "database" er synonymer i MySQL/MariaDB. (Men ikke i Postgres)