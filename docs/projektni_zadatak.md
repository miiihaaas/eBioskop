# Opšte informacije

## Izrada backend-a
- Programski jezik: Python
- Framework: Flask

## Izrada frontend-a
- Frontend okvir: HTML, CSS
- Dizajnerski alat: Figma

## Baza podataka
- Sistem upravljanja bazama podataka: MySQL

# Opis projekta

Portal eBioskop namenjen je prikazivačima i distributerima sa jedne strane, kako bi lakše organizovali rad i međusobnu komunikaciju, kao i krajnjim korisnicima, koji će putem portala pristupati predviđenom setu informacija prethodno unešenih od strane prikazivača i distributera.

Portal ima jedan jezik - srpski i jedno pismo - latinicu. Pristup portalu moguć je direktnim linkom ili putem veb sajta www.cinemanetwork.rs, putem linka koji će stajati u zaglavlju pomenutog veb sajta.

Registracija na portalu nije omogućena, već samo logovanje. Grupe korisnika koje se mogu logovati na administrativni i korisnički deo portala dobijaju pristup od strane administratora portala.

# Grupe korisnika

Postoji 5 grupa korisnika portala. Deo njih imaće pristup administrativnom delu portala, a drugi deo isključivo korisničkom delu portala.

## Grupe korisnika sa administrativnim pristupom

Grupe korisnika koje će imati pristup administrativnom delu portala su:
- Administratori
- Prikazivači
- Distributeri

### Administratori
Korisnici sa najvišim nivoom ovlašćenja na administrativnom delu portala. Imaju pristup svim potrebnim informacijama i opcijama na portalu. Mogu menjati i dodavati određene informacije u korist prikazivača i distributera.

### Prikazivači
Korisnici koji predstavljaju prikazivača odnosno bioskop. Nivo ovlašćenja koji im je dodeljen omogućava im različite vrste unosa podataka o ustanovi, tehničkoj opremljenosti i slično, kao i podatke o prikazivanju filmova, gledanosti i prihodu. Pored unosa imaju opciju da eksportuju unete podatke za potrebe različitih institucija koje zahtevaju podatke od prikazivača.

### Distributeri
Korisnici koji predstavljaju distributere filmova. Nivo ovlašćenja koji im je dodeljen omogućava im različite vrste unosa podataka o kompaniji kao i podatke o filmova. Distributerima je omogućen i unos datuma starta prikazivanja filmova koje distribuiraju u jedinstveni kalendar, dostupan i drugim distributerima i prikazivačima.

## Grupe korisnika sa pristupom korisničkom delu portala

### Korisnici sa proširenim pravima pristupa
Korisnici sa proširenim pravima pristupa (Ministarstvo, Filmski centar Srbije…) su korisnici koji putem logovanja na portal dobijaju u korisničkom delu portala pristup dodatnim informacija koje nisu vidljive za obične korisnike. Ovoj grupi korisnika naloge kreira administrator.

### Korisnici
Korisnici portala imaju pristup isključivo korisničkom delu portala i informacijama koje su javno vidljive.

## Strane na korisničkom delu portala

Na korisničkom delu portala vidljive su sledeće strane:
- Početna
- Prikazivači
- Distributeri
- Box office
- FAQ
- Kontakt

### Korisničke stranice

Korisnici imaju pristup sledećim stranicama:
- Početna
- Prikazivači
- Distributeri
- Box office
- FAQ
- Kontakt

### Početna strana
U hederu početne strane nalazi se opcija za logovanje.

### Prikazivači
Na strani Prikazivači izlistani su svi prikazivači koji se nalaze na portalu eBioskop. Klikom na dugme **OPŠIRNIJE** otvara se modal za prikazivanje detalja konkretnog prikazivača.

Na modalu pojedinačnog prikazivača nalaze se sledeći podaci:
- Naziv
- Adresa
- Mesto
- Telefon
- Mejl
- Veb sajt
- Linkovi ka društvenim mrežama
- Broj sala
- Ukupan broj mesta
- Slika bioskopa (ukoliko nije unešena postaviti generičku sliku)

### Distributeri
Na strani Distributeri izlistani su svi distributeri koji se nalaze na portalu eBioskop. Klikom na dugme **OPŠIRNIJE** otvara se modal za konkretnog distributera.

Na strani pojedinačnog distributera nalaze se sledeći podaci:
- Naziv
- Adresa
- Mesto
- Telefon
- Mejl
- Veb sajt
- Linkovi ka društvenim mrežama
- Logotip distributera (ukoliko nije unešen postaviti logotip eBioskop)

### Box office
Na strani Box office nalazi se javno dostupna tabela koja pruža uvid u gledanost i zaradu 20 filmova sa najvećom zaradom u tekućoj bioskopskoj nedelji. Iznad tabele se nalazi filter putem koga je moguće izabrati bioskopsku nedelju i godinu.

#### Tabela sadrži sledeće kolone:
- Redni broj - RB
- Promenu pozicije filma na tabeli označenu ikonicama (NOVI, - , ↑ ili  ↓) u odnosu na prethodnu bioskopsku nedelju -  (NOVI, - , ↑ ili  ↓)
- Lokalni naziv filma    -  film
- Svetski distributer -  distr.
- Lokalni distributer - local distr
- Broj nedelja prikazivanja We. No.
- Broj bioskopa koji prikazuju film - NO
- Nedeljni Box office (zarada) - za tekuću bioskopsku nedelju- we B.O.
- Nedeljna prodaja ulaznica - za tekuću bioskopsku nedelju - We. admiss.
- % promena - Promena zarade u odnosu na prethodnu bioskopsku nedelju prikazana u procentima, zaokružena na dve decimale -% INC/DEC
- B.O. (Box office) za prethodnu bioskopsku nedelju - Last We B.O.
- Prodaja ulaznica za prethodnu nedelju - Last We Admiss.
- Ukupni B.O. - Cum B.O.
- Ukupna prodaja ulaznica - Cum. Admiss

Isto kao i na hrvatskom sajtu

DISTR.
LOCAL DISTR.
We No.
NO.
WE B.O.
WE ADMISS.
% INC/DEC
LAST WE B.O.
LAST WE ADMISS.
CUM. B.O.
CUM ADMISS

Ispod tabele izračunate su sume za poslednjih 7 kolona (počevši od kolone Nedeljni B.O.)

### FAQ
Strana sa najčešće postavljenim pitanjima i odgovorima vezanim za rad portala i pojedine delove portala i informacije koje portal pruža.

### Kontakt
Na kontakt strani nalaze se kontakt podaci predstavnika portala, kao i kontakt forma putem koje se krajnji korisnici mogu obratiti administratoru portala.

## Korisnici sa proširenim pravima pristupa

Imaju sledeće stranice:
- Početna
- Prikazivači
- Distributeri
- Box office
- FAQ
- Kontakt
- Lične karte bioskopa
- Podaci o projekcijama

### Lične karte bioskopa
nalazi se tabela sa sledećim kolonama:
- Naziv bioskopa
- Mesto
- Da li je član MKS - DA ili NE
- Da li je član Europa Cinemas - DA ili NE
- Sistem prodaje elektronskih karata - DA ili NE
- Da li je bioskop digitalizovan - DA ili NE
- Dugme za preuzimanje kompletne lične karte bioskopa. Lična karta predstavlja sve podatke koje je prikazivač uneo u sledećim sekcijama: Podaci o pravnom licu, Podaci o zastupnicima, Podaci o bioskopu, Podaci o salama i Kontakti u bioskopu. Nije potrebno da preuzimaju podatke o projekcijama. Lična karta bioskopa se preuzima u PDF formatu.

### Podaci o projekcijama
Na ovoj stranici nalazi se lista svih prikazivača. Klikom na dugme 'Prikaži projekcije' pored svakog prikazivača, otvara se nova stranica sa detaljnim pregledom projekcija za izabrani bioskop.

Na stranici projekcija izabranog bioskopa nalazi se tabela odigranih filmova. Tabela inicijalno prikazuje podatke za tekući kalendarski mesec. U tabeli se prikazuju sledeće kolone:
- Datum
- Vreme
- Lokalni naziv filma
- Verzije filma: originalno, titlovano ili sinhronizovano (različite verzije istog filma su posebni redovi u tabeli)
- Projekcioni format: 2D ili 3D (različiti formati istog filma su posebni redovi u tabeli)
- Broj prodatih ulaznica
- Zarada

Iznad tabele nalaze se opcije za filtriranje podataka:
- Izbor filma - Padajući meni koji prikazuje sve filmove iz podešenog opsega datuma, uključujući i filmove koji su označeni oznakom "završeno prikazivanje" od strane distributera. Različite instance (verzija i format) jednog filma prikazuju se kao jedna stavka u filteru.
- Datum (od-do) - Mogućnost izbora perioda po mesecu i godini, bez mogućnosti izbora dana
- Format - Filter za izbor projekcionog formata
- Verzija - Filter za izbor verzije filma

Nakon izbora pojedinačnog filma u filteru "Izbor filma", prikazuje se modal sa dodatnim podacima za izabrani film:
- Broj nedelja prikazivanja - Ukupan broj bioskopskih nedelja (od četvrtka do četvrtka - bioskopska nedelja) u kojima je film imao bar jednu projekciju, računato od početka prikazivanja do današnjeg datuma, nezavisno od izabranog perioda u filteru
- Broj prikazivanja - Ukupan broj projekcija filma od početka prikazivanja do današnjeg datuma, nezavisno od izabranog perioda u filteru

## Strane na administrativnom delu portala

Na administrativnom delu portala različitim grupama korisnika vidljive su različite strane, zavisno od dodeljenih privilegija.

### Administratori
Administratori imaju dostupne sledeće sekcije:

- DISTRIBUTERI
- PRIKAZIVAČI
- ČLANOVI MKS
- LISTA FILMOVA
- KALENDAR
- PROJEKCIJE

#### DISTRIBUTERI
Na strani distributera nalazi se lista unešenih distributera sa opcijom za dodavanje novog distributera i editovanje postojećih distributera.

#### PRIKAZIVAČI
Na strani prikazivači nalazi se lista unešenih prikazivača sa opcijom za dodavanje novog prikazivača i editovanje postojećih prikazivača.

#### ČLANOVI MKS
*Napomena: samo administrator može da ažurira*

Na ovoj strani administrator može da doda fizička lica koji su članovi MKS. Administrator unosi i edituje sledeće podatke:

- Ime i prezime
- Adresa
- Mesto
- Prikazivač kod koga je zaposlen MKS (izbor jednog od postojećih pravnih lica bioskopa)
- Prikazivač kod koga je zaposlen NOT MKS (ako nije MKS: naziv pravnog lica bioskopa koji nije član MKS)
- Radno mesto
- Mejl (može se uneti do 2 mejla)
- Telefon (može se uneti do 2 broja telefona)

Administrator može izabrati jednu od 3 opcije za člana:
- Aktivan
- Neaktivan
- Počasni

U listi članova prikazuju se uneti podaci i status članova.

#### PROJEKCIJE
Na strani se nalaze tabele za svakog prikazivača ponaosob. U tabelama su prikazani podaci po projekcijama:
- Naziv filma
- Distributer
- Verzija filma
- Projekcioni format
- Broj projekcija
- Broj nedelja prikazivanja (od četvrtka do četvrtka - bioskopska nedelja)
- Broj prodatih karata
- Prihod

*Napomena: Default prikaz je aktuelna bioskopska nedelja. Postoji filter po datumu.*

### Prikazivači
Potrebno je imati sekcije u kojoj bioskop unosi sledeće podatke:

#### PODACI O PRAVNOM LICU
*Napomena: samo administrator može da ažurira*

Obavezna polja su označena sa *

- Naziv bioskopa*
- Zemlja*
- Adresa*
- Poštanski broj*
- Mesto* (npr. Rudnik - koji se nalazi u opštini Gornji Milanovac)
- Opština* (padajući meni sa svim opštinama u Srbiji, uključujući Kosovo)
- Imejl* (Lista mejlova)
- Telefon*
- Oblik pravnog lica* (padajući meni: javna ustanova, kompanija)
- PIB*
- MB*
- Vebsajt
- Linkovi društvenih mreža (YouTube, Facebook, Instagram, TikTok)
- Da li je član MKS?*
- Da li je član Europa Cinemas?*

#### PODACI O ZASTUPNIKU
*Napomena: samo administrator može da ažurira*

Obavezna polja su označena sa *

- Ime*
- Prezime*
- Pozicija*
- Imejl*
- Telefon*
- Fotografija

#### PODACI O BIOSKOPU
Obavezna polja su označena sa *

- Lokacija bioskopa* (padajući meni: centar grada / širi centar grada / periferija)
- Broj stanovnika mesta (grad)*
- Broj stanovnika mesta sa okolinom (opština)*
- Sistem elektronske prodaje karata* (DA/NE)
  - Ako je DA, navesti koji sistem
- Način promocije bioskopa i reklamiranja filmskog programa* (do 500 karaktera)
- Način programiranja u bioskopu* (do 500 karaktera)
- Da li ste istovremeno i distributer?* (DA/NE)
- Fotografije (mogućnost dodavanja 2 fotografije)

#### PODACI O SALAMA

##### DODAVANJE SALE
Obavezna polja su označena sa *

- Naziv sale*
- Broj sedišta*
- Radni dani bioskopa* (izbor dana od ponedeljka do nedelje)
- Broj zaposlenih u bioskopu
- Godina izgradnje*
- Dimenzije sale* (a x b x c - metri, format 0.00)
- Udaljenost kino kabine od projekcionog ekrana*
- Obezbeđeno mrežno napajanje audio i projekcione opreme* (DA/NE)
- Opis sedišta u sali* (do 300 karaktera)
- Obezbeđena klimatizacija sale* (DA/NE)
- Obezbeđeno grejanje sale* (DA/NE)
- Akustička obrada sale* (DA/NE)
- Akustička obrada iza projekcionog ekrana* (DA/NE)
- Projektna dokumentacija enterijera sale* (DA/NE)
- Projektna dokumentacija za tehnološku opremu sale* (DA/NE)
- Veličina projektnog platna (a x b)
- Zvuk (opcije: mono / stereo / dolby / digital standard)
- Da li je sala digitalizovana? (čekboks)

#### KONTAKTI U BIOSKOPU
Može se dodati više kontakata koji ujedno: uređuju podatke o bioskopu, bioskopskim salama, administriraju projekcije, kreiraju/edituju dodatne profile kontakata u bioskopu.

- Ime*
- Prezime*
- Pozicija* (padajući meni: kinooperater, urednik filmskog programa)
- Imejl*
- Telefon*
- Fotografija

#### LISTA FILMOVA
Lista filmova predstavlja tabelu sa informacijama o filmovima koje su svi distributeri već uneli. Kolone u tabeli su:

- Lokalni naziv i originalni naziv
- Režiser i glumci
- Detalji - trajanje, verzije i format
- Kompanija i godina
- Distributer
- Datum starta filma
- Žanr
- Starosna preporuka
- Status (u prikazivanju, završeno prikazivanje, planirano prikazivanje)
- Opširnije (Prikazivači bi trebalo da imaju opciju da kliknu na dugme opširnije i da dobiju kompletne informacije koje je distributer uneo.)

Iznad tabele nalaze se filteri:
- Distributer
- Status filma (u prikazivanju, završeno prikazivanje, planirano prikazivanje)

#### PROJEKCIJE
Na strani projekcije nalazi se tabela odigranih filmova koje je prikazivač prikazao u svom bioskopu. Tabela inicijalno prikazuje podatke za tekući kalendarski mesec. U tabeli se nalaze sledeće kolone:

- Datum
- Vreme
- Lokalni naziv filma
- Verzije filma: originalno, titlovano ili sinhronizovano (različite verzije istog filma su posebni redovi u tabeli)
- Projekcioni format: 2D ili 3D (različiti formati istog filma su posebni redovi u tabeli)
- Broj prodatih ulaznica
- Zarada

Iznad tabele nalaze se opcije za fitriranje:

- Izbor filma - Mogu se izabrati samo filmovi iz podešenog opsega datuma. Potrebno je da se vide i filmovi koji su označeni oznakom “završeno prikazivanje” od strane distributera. Različite instance (verzija i format) jednog filma su jedna stavka u filteru.
- Datum (od-do) - u kome se može birati mesec i godina, ne i dan.
- Format
- Verzija

U slučaju odabira pojedinačnog filma putem filtera “Izbor filma”, pojavljuje se modal sa dva dodatna podatka samo za izabrani film: Ovaj modal prikazuje sledeće podatke:
- Broj nedelja prikazivanja - ovaj podatak se prikazuje nezavisno od filtera datuma, odnosno za čitav period od starta prikazivanja do današnjeg datuma. Uzeti u obzir da bioskopska nedelja traje od četvrtka do četvrtka. Bioskopska nedelja se broji u broj nedelja prikazivanja ukoliko je u toj nedelji bila jedna ili više projekcija.
- Broj prikazivanja - ovaj podatak se prikazuje nezavisno od filtera datuma, odnosno za čitav period od starta prikazivanja do današnjeg datuma. Uzeti u obzir da bioskopska nedelja traje od četvrtka do četvrtka.

Iznad tabele se nalazi i dugme DODAJ PROJEKCIJU. Klikom na dugme otvara se modal za unos sledećih podataka:

- Datum
- Vreme
- Lokalni naziv filma - izbor od postojećih filmova unetih od strane distributera.
- Verzije filma: originalno, titlovano ili sinhronizovano (izbor iz padajućeg menija jedne od opcija)
- Projekcioni format: 2D ili 3D (izbor iz padajućeg menija jedne od opcija)
- Broj prodatih ulaznica
- Zarada

Dodavanjem filma, šalje se mejl distributeru nadležnom za taj film, sa podacima vezanim za konkretnu projekciju.

Ispod tabele nalaze se opcije za izvoz podataka u XML formatu.
Potrebno je da postoji izvoz za sledeće institucije:
- Filmski centar Srbije - Period za koji se izvozi je jedna kalendarska godina, a potrebno je da svaka projekcija u tabeli bude zasebno prikazana.
- Sokoj - Period za koji se izvozi je jedan kalendarski mesec, a potrebno je da svaka projekcija u tabeli bude zasebno prikazana.
- Europa Cinemas - Period za koji se izvozi je jedna kalendarska godina, a potrebno je da svaki film u tabeli bude zasebno prikazan.

### Distributeri
Distributeri imaju dostupne sledeće sekcije:

- O PRAVNOM LICU
- LISTA FILMOVA
- KALENDAR DISTRIBUCIJE
- PROJEKCIJE

#### O PRAVNOM LICU
U sekciji o pravnom licu unose se sledeći podaci:

- Naziv kompanije*
- Zemlja*
- Adresa*
- Poštanski broj*
- Mesto*
- Imejl* (Može i više mejlova)
- Telefon*
- PIB*
- MB*
- Ovlašćeno lice*
- Vebsajt
- Linkovi društvenih mreža (Padajući meni: YouTube, Facebook, Instagram, TikTok)
- Zastupnik distributera - Opcija za izbor svetskih distributera sa kojima imaju potpisan ugovor, a koji će se kasnije pojavljivati u padajućem meniju pri unosu filmova. Jedan svetski distributer može da radi samo sa jednim distributerom. Jedan distributer može da radi sa više svetskih distributera. Konačan spisak distributera: Paramount, Universal, Warner Bros, Columbia/Sony, Disney, 20th Century Studios, Drugi, Lokalna produkcija. Više distributera može izabrati opcije “Drugi” i “Lokalna produkcija”.

#### LISTA FILMOVA
Lista filmova predstavlja tabelu sa informacijama o filmovima koje je distributer već uneo. Kolone u tabeli koje su:

- Lokalni naziv
- Režiser
- Godina produkcije
- Trajanje
- Kompanija
- Dan, mesec i godina starta filma
- Žanr
- Starosna preporuka
- Status (u prikazivanju, završeno prikazivanje, planirano prikazivanje)
- Uredi

Iznad tabele se nalazi dugme za dodavanje novog filma.

Kod unosa filmova distributeri popunjavaju sledeća polja:
- Originalni naziv filma*
- Lokalni naziv filma*
- Režiser*
- Glumci*
- Zemlja produkcije filma (lista svih zemalja)*
- Kompanija*
- Godina produkcije*
- Trajanje*
- Verzije filma* - check polja (može se izabrati više): originalno, titlovano i sinhronizovano
- Projekcioni format* - check polja (može se izabrati više): 2D i 3D
- Starosna preporuka - selekt meni sa opcijama
  - bez ograničenja
  - 5+
  - 6+
  - 7+
  - 12+
  - 15+
  - 16+
  - 18+
- Plakat*
- 3 slike (16x9)
- Link ka trejleru
- Sinopsis*
- Žanr - check polja (može se izabrati više):
  - Avanturistički
  - Akcioni
  - Arthaus
  - Animirani
  - Biografski
  - Vestern
  - Domaći
  - Dečji
  - Dokumentarni
  - Drama
  - Istorijski
  - Komedija
  - Kriminalistički
  - Misterija
  - Mjuzikl
  - Naučna fantastika
  - Nezavisni
  - Porodični
  - Psihološki triler
  - Ratni
  - Romantična komedija
  - Sportski
  - Tinejdžerski
  - Triler
  - Horor
- Datum starta filma*

Kada Distributer unese i sačuva podatke o filmu, film postaje vidljiv Prikazivačima na strani Projekcije pri opciji dodavanja nove projekcije sa svim unetim podacima i opcijama iz check polja koja se Prikazivačima prikazuju u vidu padajućeg menija.

Pored toga uneti podatak o datumu starta filma se prikazuje u Kalendaru distribucije. Ostalim distributerima i svim prikazivačima stiže mejl o unetom startu filma ili o načinjenoj izmeni vezanoj za start filma.

#### KALENDAR DISTRIBUCIJE
Kalendar distribucije predstavlja stranu na kojoj su prikazani startovi filmova svih distributera koji imaju pristup softveru. Svi distributeri vide sve unete filmove sa datumom starta prikazivanja. Potrebno je da filmovi različitih distributera na neki način budu obeleženi različitim bojama u kalendaru. Potrebno je u kalendaru prikazati naziv filma i naziv distributera.

Filmovi se prikazuju u formi liste sa akordionom, zasebno za svaki dan za koji je zakazan start distribucije barem jednog filma. Predefinisano se prikazuje lista sa datumom koji je dve nedelje u nazad od trenutnog datuma. (Ako može, dobro bi bilo da protekli datumi budu zasenčeni). U vrhu strane nalazi se filter datuma (koji se ponaša kao sticky menu) pomoću koga se mogu prikazati i raniji startovi filmova. Lista prikazuje sve zakazane filmove bez obzira koliko su oni u budućnosti zakazani.

#### PROJEKCIJE
Distributer na strani projekcije ima uvid u podatke o prikazivanju filmova koje on distribuira kod različitih prikazivača. Podaci su prikazani u tabelama, svaki prikazivač koji ima saradnju sa tim distributerom ima zasebnu tabelu. U tabli su prikazani podaci u sledećim kolonama:
- Naziv filma
- Verzija filma
- Projekcioni format
- Broj projekcija
- Broj nedelja prikazivanja (od četvrtka do četvrtka - bioskopska nedelja)
- Broj prodatih karata
- Prihod

Postoji filter po datumu. Default prikaz je aktuelna bioskopska nedelja.
