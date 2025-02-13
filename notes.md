To dataset i første omgang: 
1) temperatur i Oslo siste måneden (*c + dato) -> l
2) nedbør, i kategorier, sist måneden -> pie chart og/eller histogram

SQLite har innebygd CSV-import. Python Pandas har samme funksjonalitet, og kan også lese .xlsx direkte
* pandas er nok bedre her for det går rett i koden

CSV (Comma-Separated Values) is a simple text format for storing tabular data, where each row represents a record, and values are separated by commas.
Rainbow CSV er en super extension :)

df = DataFrame, konsept i Pandas som ligner veldig på SQL. "Tabular data structure"

sender dataen til sqlite heller enn å bruke csven direkte for spørringer
og konverter sql-dataen til DF for databehandling

trenger defer attribut i script tag

chart.js er raskere, enklere, og interaktivt, men krever en web-frontend. Matplotlib er mye mer brukt i data science. 
dropper matplotlib! blir en mer naturlig fordeling, og er mye gøyere og enklere. + callback.
beholder pandas: filtrering og aggregering uten sql. kall en gang fra db, bruk pandas til å manipulere. men si at må ikke gjøre det - kan gjøre mange db kall. 
* og pandas dukker opp overalt i APIer, automatisering, web scarping etc etc. CV-mat!

Tror vi kjører .csv som bonus. Start med bare .sql tenker jeg.

ref API-kall i frontend vs backend:
* enklere og raskere i frontend, men usikkert hvis keys og kan bli blokkert av CORS restriksjoner
* backend er tryggere 

Server-side rendering (SSR) med Jinja - tryggere, potensielt raskere. men statisk og kan bare gjøre ett "pull" per side.
Client-side rendering (CSR) med JS fetch() - dynamisk og kan gjøre flere kall
Vanlig å bruke Jinja for første load, og så oppdatere med fetch

// noen APIer krever både en "base url" og en "JSON request payload"