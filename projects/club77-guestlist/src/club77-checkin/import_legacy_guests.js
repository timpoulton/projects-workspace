const { Event, Guest } = require('./models');

// Legacy guest data from old system
const legacyData = `Club 77: Phil Smart	31/05/2025	Nicolette	Bell
Club 77: Phil Smart	31/05/2025	Rachael	Lambert
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mac	Weily
Club 77: Reenie	24/05/2025	Mac	Weily
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Mac	Weily
Club 77: Phil Smart	31/05/2025	Mac	Weily
Club 77: Phil Smart	31/05/2025	James	Hortle
Club 77: Reenie	24/05/2025	Zelko	Nedic
Club 77: Phil Smart	31/05/2025	Kara	Giardullo
Club 77: Reenie	24/05/2025	Agustina	López Quinteros
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Rachel	Jeffers
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Imogen	power
Club 77: Phil Smart	31/05/2025	Felipe	Cuevas Guerra
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jefry	Moreno
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Emma	Hamilton
Club 77: Reenie	24/05/2025	Maz	Sheehan
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Tyson	Schwarze
Club 77: Phil Smart	31/05/2025	Ashley	Hendriks
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	renata	carrillo
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Eloise	Bennett
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Jessica	Blake
Club 77: Phil Smart	31/05/2025	Annie	Camuglia
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Piper	Oates
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Rachel	Manley
Club 77: Reenie	24/05/2025	Josh	Smith
Club 77: Phil Smart	31/05/2025	Heather	Loudon
Club 77: Phil Smart	31/05/2025	Lara	Gardner
Club 77: Reenie	24/05/2025	Sarah	Burnett
Club 77: Reenie	24/05/2025	Andrew	Brown
Club 77: Reenie	24/05/2025	Dan	Hunt
Club 77: Reenie	24/05/2025	conrad	Mailey
Club 77: Reenie	24/05/2025	Jamie	Reilly
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Mac	Weily
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Mac	Weily
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Mac	Weily
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Jo	Robinson
Club 77: Phil Smart	31/05/2025	Kira	Stubbs
Club 77: Reenie	24/05/2025	Massimo	Willoughby
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Marcus	Rouquet
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Ethan	Procter
Fridays at 77: Ayebatonye, Deepa	09/05/2025	Benjamin	Ruzanskyruzansky
Fridays at 77: Ayebatonye, Deepa	09/05/2025	Jacob	Rieser
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Muhammad Hamza	Rahat
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Monica	Nunn
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Maria	Vivanco
Club 77: Phil Smart	31/05/2025	Albert	Moreno
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Kat	Ru
Fridays at 77: Ayebatonye, Deepa	10/05/2025	Jordan	McBride
Club 77: Phil Smart	31/05/2025	Florencia	Blanco
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Garehn	Kalloghlian
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Benny	Uzoziri
Club 77: Reenie	24/05/2025	Paolo	Colombo
Fridays at 77: Ayebatonye, Deepa	10/05/2025	Lily	Newton
Club 77: Reenie	24/05/2025	Liv	White
Club 77: Phil Smart	31/05/2025	Ilaria	Roggero
Club 77: Reenie	24/05/2025	Michael	Brown
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Tristan	Sela
Club 77: Reenie	24/05/2025	Niki	de Vergara
Club 77: Reenie	24/05/2025	Ilse	Brouwer
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Paola	Ricalde
Club 77: Reenie	24/05/2025	Bente	van Diepen
Club 77: Phil Smart	31/05/2025	Jonathan	Papallo
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Sidnei	Canhedo
Fridays at 77: Ciara, Scruffs	13/06/2025	Mac	Weily
Club 77: Reenie, Goat Spokesperson	14/06/2025	Mac	Weily
Fridays at 77: Ciara, Scruffs	17/05/2025	Joseph	Rizk
Club 77: Phil Smart	31/05/2025	Des Mason	Des Mason
Club 77: Reenie	24/05/2025	A	A
Club 77: Reenie	24/05/2025	Aksharaa	Agarwal
Club 77: Reenie	24/05/2025	Aaron	C
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Sol	Llorente Lucena
Fridays at 77: Ciara, Scruffs	13/06/2025	Tim	Trust
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Veronica	Bull
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Arthur	Morgan
Fridays at 77: Ayebatonye, Deepa	17/05/2025	Kenta	Marsh
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Carola	Riva
Club 77: Phil Smart	31/05/2025	Ellen	Burke
Club 77: Reenie	24/05/2025	Amy	McInnis
Club 77: Reenie	24/05/2025	Jamie	Wood
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Ignacia	Yanez
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Brittany	Cooper
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Amram	Arif
Club 77: Reenie	24/05/2025	Catrina	Coakley-Burns
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Lovisa	Bringemo
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Jay	Nelson
Club 77: Phil Smart	31/05/2025	Jan	Fabricius
Club 77: Phil Smart	31/05/2025	Adam	Leelasorn
Fridays at 77: Ayebatonye, Deepa	06/06/2025	MJ	Yang
Club 77: Reenie	24/05/2025	bella	noble
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Akil	Ergenç
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Arlina	Tusi
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Arlina	Tusi
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Lincoln	Davies
Club 77: Reenie	24/05/2025	Max	Ollerenshaw
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Lance	Sia
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Kiarne	Radecki
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Eilidh	Tippen
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Baila	Hernandez
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Ettienne	Montzka-Caceres
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Dean Jamie	Drieberg
Club 77: Reenie	24/05/2025	Emma	Butler
Fridays at 77: Ayebatonye, Deepa	06/06/2025	MIKU	FUKUDA
Club 77: Reenie	24/05/2025	Melinda	Butterworth
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Chae Hyun	Lee
Club 77: Reenie	24/05/2025	Brendan	Yeates
Club 77: Reenie	24/05/2025	Joanne	Gay
Club 77: Reenie	24/05/2025	Shane	Collard
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Peace	Sinsomboon
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Edan	Porter
Club 77: Reenie, Goat Spokesperson	14/06/2025	Summer	Parry
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Matilda	Breen
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Raghav	Malhotra
Club 77: Phil Smart	31/05/2025	Zaccary	Renford
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Jack	Viscardi
Club 77: Phil Smart	31/05/2025	Jesse	Blaustein
Club 77: Phil Smart	31/05/2025	Jiayi	Chen
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	William	Macleod
Fridays at 77: Ayebatonye, Deepa	17/05/2025	Leo	Jones
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Rashie	Kase
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Venus	Fleck
Club 77: Reenie, Goat Spokesperson	14/06/2025	Michael	Dibiase
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Henry	Vaaler
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Alexander	Sherlock
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Ellie	Woodrow
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Will	McAllister
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Sijin	Lu
Fridays at 77: Ayebatonye, Deepa	17/05/2025	indi	ruppert
Club 77: Reenie	24/05/2025	Sebastian	Darney
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	abhishek	gupta
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Bella	Grant
Club 77: Reenie	24/05/2025	Alice	Stewart
Club 77: Reenie	24/05/2025	Zoe	Vlahos
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Oliver	Sved
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Justin	Lee
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Michael	Codd
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Will	McAllister
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Joshua	Feld
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	William	McAllister
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Alex	Cehak
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Chris	Trevallion
Club 77: Reenie	24/05/2025	Joshua	Rivera
Club 77: Reenie	24/05/2025	Timothy	Poulton
Club 77: Reenie	24/05/2025	Audrey	Flemming
Club 77: Reenie	24/05/2025	Dan	Brandon
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Dane	Gorrel
Club 77: Reenie	24/05/2025	Aksharaa	A
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Matthieu	Landais
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Abbey	Phillips
Club 77: Reenie	24/05/2025	Loïc	Banh
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Tony	Pittaway
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Timothy	Poulton
Fridays at 77: Ciara, Scruffs	13/06/2025	Skye	Hill
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Tim	Poulton
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Timothy	Poulton
Club 77: Phil Smart	31/05/2025	Timothy	Ballface
Fridays at 77: Ciara, Scruffs	13/06/2025	Tester	Trust
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Tester	Poulton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Timothy	Poulton
Fridays at 77: Wavyrager, halalbutch	20/06/2025	Mac	Weily
Club 77: Reenie	24/05/2025	Tim	Poulton
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Deepchild	Poulton
Club 77: Mike Who & Daniel Lupica	21/06/2025	Club	77
Club 77: Mike Who & Daniel Lupica	21/06/2025	Mac	Weily
Club 77: Mike Who & Daniel Lupica	21/06/2025	Troy	Hogan
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Tim	Poulton
Club 77: Reenie	24/05/2025	Tim	Trust
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Club	Trust
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Deepchild	Ballface
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lucas	Andrade
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Juan	Rafael Rico
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Chaitanya	Mistry
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Sharleen	Weerakkody
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Ben	Barnes
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Ben	Barnes
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Adam	Howard
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Adam	Howard
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Ben	Barnes
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Ami	Humphreys
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Siro	Cavaiuolo
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Emil	Kattiya-aree
Fridays at 77: Wavyrager, halalbutch	20/06/2025	Tester	Trust
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	giulia	farigu
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Tim	Poulton
Club 77: Reenie	24/05/2025	Julian	Pellegrini
Club 77: Reenie	24/05/2025	Julia	Mars
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Max	Putman
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Niamh	Youmans
Club 77: Reenie	24/05/2025	Mayra	Altink
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Laura	Janko
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Timotej	Janko
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Maddi	Lindsay
Club 77: Reenie, Goat Spokesperson	14/06/2025	Timothy	Trust
Club 77: Reenie, Goat Spokesperson	14/06/2025	Timothy	Trust
Club 77: Phil Smart	31/05/2025	Timothy	Poulton
Club 77: Phil Smart	31/05/2025	Timothy	Poulton
Club 77: Reenie	24/05/2025	Timothy	Poulton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Tim	Poulton
Club 77: Reenie	24/05/2025	Nick	Ang
Sundays at 77: Barney Kato & Simon Caldwell	07/06/2025	Niamh	Youmans
Fridays at 77: Ciara, Scruffs	13/06/2025	Sophie	McAlpine
Fridays at 77: Ciara, Scruffs	13/06/2025	Sophie	McAlpine
Fridays at 77: Ciara, Scruffs	13/06/2025	Mikaela	Dalgleish
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Leon	Chan
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Merella	Francheska Apuya
Club 77: Reenie	24/05/2025	Sophie	Todd
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Dario	Ishiyama
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Kriti	Chhetri
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Dario	Ishiyama
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Dario	Ishiyama
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Akash	Jadhav
Club 77: Reenie	24/05/2025	Akash	Jadhav
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Timothy	Poulton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	SAURABH	SABHARWAL
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Timothy	Poulton
Club 77: Reenie	24/05/2025	Henry	Faktor
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Tetsuya	Lewis
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	dane	gorrel
Club 77: Reenie	24/05/2025	Tomasz	Michalczyk
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Timothy	Trust
Sundays at 77: Barney Kato & Simon Caldwell	08/06/2025	Deepchild	Trust
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Tim	Poulton
Fridays at 77: Ciara, Scruffs	13/06/2025	Tester	Trust
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Olivia	Diaz Romano
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	maika	dvf
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Oliver	Tazewell
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	SAURABH	SABHARWAL
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Ananya	Srinivas
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Ananya	Srinivas
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Merella Francheska	Apuya
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mila	Altree-Williams
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Imogen	Leese
Club 77: Reenie	24/05/2025	Lukas	Klotz
Club 77: Reenie	24/05/2025	Karolina	Buszczak
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Louis	Kokoura
Club 77: Reenie	24/05/2025	Louis	Kokoura
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Louis	Kokoura
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Federico	Astigarraga
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Francisco	Oreggia
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Alejandro	Moro
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Diego	Picarelli
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lucas	Anchorena
Club 77: Reenie	24/05/2025	Nick	nicholls
Club 77: Phil Smart	31/05/2025	Jason	Malouf
Sundays at 77: Barney Kato & Simon Caldwell	08/06/2025	Amelia	Ruddock
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Martha	Chess Phelps
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Indianna	Jones
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Max	Ohman
Club 77: Reenie	24/05/2025	Oscar	Greville
Club 77: Reenie	24/05/2025	Sebastiaan	Barneveld
Fridays at 77: Ciara, Scruffs	13/06/2025	Timothy	Poulton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Annabel	Smith
Club 77: Reenie, Goat Spokesperson	14/06/2025	Timothy	Trust
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Maddi	Lindsay
Club 77: Phil Smart	31/05/2025	Timothy	Poulton
Fridays at 77: Ayebatonye, Deepa	06/06/2025	Lorenzo	Ignacio
Sundays at 77: Barney Kato & Simon Caldwell	08/06/2025	Timothy	Poulton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jan Marlo	Avenido
Club 77: Phil Smart	31/05/2025	Jan Marlo	Avenido
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Lorenzo	Ignacio
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Timothy	Poulton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Daniel	Merson
Club 77: Reenie	24/05/2025	Mirelle	Lazerson
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Timothy	Poulton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Youssef	Sabir
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Giacomo	Boiero
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Juliet	Ivkovic
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	David	Contreras diaz
Club 77: Reenie	24/05/2025	Alice	Campbell
Club 77: Reenie	24/05/2025	Chloe	Arnold
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Estefania	Triana Parra
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jonathan	Brutman
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mac	Test
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jan Carlos	Builes
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Timothy	Poulton
Club 77: Reenie	24/05/2025	Sophie	Todd
Fridays at 77: Wavyrager, Yemi Sul	23/05/2025	Jaime	Herrera
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jaime	Herrera
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jaime	Herrera
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Aditi	Kapoor
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lucas	Baumann
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Franco	Behm
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Marcos	Manchon
Club 77: Reenie	24/05/2025	Jake	Brown
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Marcos	Manchon
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Marcelo	Gonzalez
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Andrea	Delvecchio
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Andrea	Delvecchio
Club 77: Reenie	24/05/2025	Graeme	Auchterlonie
Club 77: Reenie	24/05/2025	Sam	Brau
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Andrea	Delvecchio
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Andrea	Delvecchio
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jaime	Herrera
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Massimo	Willoughby
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	inty	ligertwood
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Guillaume	BAILHACHE
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jan Carlos	Builes
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Charles	Deconinck
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Bautista	Bustillo
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Bautista	Bustillo
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Zachary	Phillips
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Archie	Hylands
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lauren	Tam
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Kayley	Smith
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Kerry	Martin
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Luke	Anderson
Club 77: Reenie	24/05/2025	Javiera	Bobadilla
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Katelyn	Davidson
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Matthew	Swallow
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jiya	Vander Straaten
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lauren	Tam
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jen	Arana
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Matthew	Swallow
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Samantha	Williams
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lauren	Tam
Sundays at 77: Barney Kato & Simon Caldwell	23/05/2025	Victoria	Mcnabb
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Kyle	Whittard
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Dylan	Upton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Dylan	Upton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Sahara	Hillman
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Cristobal	Gonzalez
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Federico	Tasso
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lydi	Menzies
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	dane	gorrel
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Federico	Tasso
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	dane	gorrel
Club 77: Reenie	24/05/2025	dane	gorrel
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Caitlyn	Burton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	emmma	mcgrath
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	jessica	boulais
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jackson	Macnevin
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Caitlyn	Burton
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Caitlin	Bryce
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Rachel	Murray
Fridays at 77: Wavyrager, Yemi Sul	23/05/2025	Pauline	Schultze
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Pauline	Schultze
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Pauline	Schultze
Club 77: Phil Smart	31/05/2025	Celine	Tay
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Sienna	Davies
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Yacine Riad	Yediou
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mael	Porche
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Edward	England
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Edward	England
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Maite	Diez
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Carolina	Unger
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Rosario	Aguirre
Club 77: Reenie	23/05/2025	Murphy	Pietranski
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Willow	Berry
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Taylah	Simons
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Murphy	Pietranski
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Gema	Martínez
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Marianne	Clifford
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Marianne	Clifford
Club 77: Reenie	23/05/2025	Genevieve	Ward
Fridays at 77: Wavyrager, Yemi Sul	23/05/2025	Sophia	MacKinnon
Club 77: Reenie	24/05/2025	Poppy	Whale
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Daniel	Gardner
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	lachie	brown
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	lily	humberstone
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Gemma	Bolles
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	lily	humberstone
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Pablo	Respaldiza
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Paige	Winter
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lauren	Tam
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Chloe Elizabeth	Conrick
Club 77: Reenie	24/05/2025	Gianluca	Pecora
Club 77: Reenie	24/05/2025	Rafqa	Touma
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Nicholas	bolles
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Rachel	Parks
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mitch	Pratt
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Morgan	Jury
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mitch	Pratt
Fridays at 77: Wavyrager, Yemi Sul	30/05/2025	Toby	Norman
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Javier	Gomez Navarro
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Shrijan	Pradhan
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	August	Willoughby
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Flavian	Schmidt
Fridays at 77: Wavyrager, halalbutch	23/05/2025	Josh	Lamont
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Harry	B
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Niamh	Thompsett
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Josh	Lamont
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	carla	colonna
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	carla	colonna
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Rachel	Parks
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Rachel	Parks
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mael	PORCHE
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Maël	PORCHE
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Lauren	Tam
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Guillaume	BAILHACHE
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Sunny	hoelzle
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	sunny	hoelzle
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	piper	dampney
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jules	Hopkinson
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Luna	Ligertwood
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Max	Williams
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	sunny	hoelzle
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jen	Arana
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Sunny	Hoelzle
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	kyla	bezuidenhout
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Anni	Guo
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Yuxuan	Zhang
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Josie	Newell
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	ava	landers
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Juan	Manuel
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Cameron	Mcintyre
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Philip	Law
Club 77: Reenie	24/05/2025	Ridley	Owens
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Sebastian	Martin
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Philip	Law
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Philip	Law
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Max	Williams
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Jorden	Morl
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Stephanie	Tolentino
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Adam	Huynh
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	sophie	harper
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Daniel	Milgrom
Fridays at 77: Ari Kiko, Jhassic	23/05/2025	Mja	Makepeace
Club 77: Reenie	24/05/2025	Rob	Harley
Club 77: Reenie	24/05/2025	Finten	Davey
Club 77: Reenie	24/05/2025	Harry	Shutes
Club 77: Reenie	24/05/2025	Harry	Shutes
Club 77: Reenie	24/05/2025	Jawad	Ibn Jahangir
Club 77: Reenie	24/05/2025	Sasha	Vulling
Club 77: Reenie	24/05/2025	Giedry	Lande Franco
Club 77: Reenie	24/05/2025	Kyra	Daley
Club 77: Reenie	24/05/2025	Oscar	Greville
Club 77: Reenie	24/05/2025	Olivia	Da Silva
Club 77: Reenie	24/05/2025	Rohanna	Hadlow
Club 77: Reenie	24/05/2025	Indi	Jennings
Club 77: Reenie	24/05/2025	Timothy	Poulton
Club 77: Reenie	24/05/2025	Oscar	Greville
Club 77: Reenie	24/05/2025	Skye	Hill
Club 77: Reenie	24/05/2025	Dylan	Upton
Club 77: Reenie	24/05/2025	Kyle	Whittard
Club 77: Reenie	24/05/2025	Michaela	Kovacs wilson
Club 77: Phil Smart	31/05/2025	Timothy	Poulton
Club 77: Reenie	24/05/2025	Carolina	Jofre
Club 77: Reenie	24/05/2025	Thomas	Morgan
Club 77: Reenie	24/05/2025	Selina	Metzger
Club 77: Reenie	24/05/2025	Dylan	Upton
Club 77: Reenie	24/05/2025	Amy	McInnis
Club 77: Reenie	24/05/2025	Eduardo	Miron
Club 77: Reenie	24/05/2025	Manou	Yu
Club 77: Reenie	24/05/2025	Em	Mason
Club 77: Reenie	24/05/2025	Amy	Hendricks
Club 77: Reenie	24/05/2025	Harry	Campbell
Club 77: Reenie	24/05/2025	Alex	Duce
Club 77: Reenie	24/05/2025	Emily	Mason
Club 77: Reenie	24/05/2025	Liam	Davidson
Club 77: Reenie	24/05/2025	Gemma	Huxley
Club 77: Reenie	24/05/2025	Jemma	Onslow
Club 77: Reenie	24/05/2025	Hannah	Maxwell
Club 77: Reenie	24/05/2025	Georgia	Ryan
Club 77: Reenie	24/05/2025	Camila	Winterton
Club 77: Reenie	24/05/2025	Lily	Littleproud
Club 77: Reenie	24/05/2025	rocco	sinclair
Club 77: Reenie	24/05/2025	Cedar	Petrulis
Club 77: Reenie	24/05/2025	Finley	Watson
Club 77: Reenie	24/05/2025	Flynn	Watts
Club 77: Reenie	24/05/2025	Poppy	Marsh
Club 77: Reenie	24/05/2025	Lili	Batterson
Club 77: Reenie	24/05/2025	Poppy	Marah
Club 77: Reenie	24/05/2025	Sophie	Davies
Club 77: Reenie	24/05/2025	Sebastiaan	Barneveld
Club 77: Reenie	24/05/2025	Zoe	Isgrove
Club 77: Reenie	24/05/2025	Tom	Martin
Club 77: Reenie	24/05/2025	Katarina	Wong
Club 77: Reenie	24/05/2025	em	sexton
Club 77: Reenie	24/05/2025	Ruby	Varndell
Club 77: Reenie	24/05/2025	Gaston	La hoz
Club 77: Reenie	24/05/2025	Alessio	Benamati
Club 77: Reenie	24/05/2025	Antonia	Treuer
Club 77: Reenie	24/05/2025	Casey	O'Regan
Club 77: Reenie	24/05/2025	Laurren	Posey
Club 77: Reenie	24/05/2025	Federica	Baldon
Club 77: Reenie	24/05/2025	Andrea	Montano
Club 77: Reenie	24/05/2025	Rachel	Hoctor
Sundays at 77: Barney Kato & Simon Caldwell	24/05/2025	Della	Daly
Club 77: Reenie	24/05/2025	Franki	Kurlansky
Club 77: Reenie	24/05/2025	James	Leong
Club 77: Reenie	24/05/2025	Ben	Simpson
Club 77: Reenie	24/05/2025	James	Leong
Club 77: Reenie	24/05/2025	Dylan	Upton
Club 77: Reenie	24/05/2025	Todd	Neumann
Club 77: Reenie	24/05/2025	Mimansa	Satam
Club 77: Reenie	24/05/2025	Leanne	Pollard
Club 77: Reenie	24/05/2025	Todd	Neumann
Club 77: Reenie	24/05/2025	Danny	Allul Orozco
Club 77: Reenie	24/05/2025	Leanne	Pollard
Club 77: Reenie	24/05/2025	Remy	Carlson
Club 77: Reenie	24/05/2025	Jandra Leona	Rivera
Fridays at 77: Ciara, Scruffs	24/05/2025	Daniella	Storm
Club 77: Reenie	24/05/2025	Jake	Brown
Club 77: Reenie	24/05/2025	Jake	Brown
Club 77: Reenie	24/05/2025	Sam	Owen
Club 77: Reenie	24/05/2025	Todd	Neumann
Club 77: Reenie	24/05/2025	Andrea	Montano
Club 77: Reenie	24/05/2025	Belind	Rafferty
Club 77: Reenie	24/05/2025	Alex	Phoon
Club 77: Reenie	24/05/2025	Carly	Bugg
Club 77: Reenie	24/05/2025	Belinda	Rafferty
Club 77: Reenie	24/05/2025	Nadisa	Milo
Club 77: Reenie	24/05/2025	Emelia	Barry
Club 77: Reenie	24/05/2025	Louis	Kokoura
Club 77: Reenie	24/05/2025	Agda	Dias de Lima
Club 77: Reenie	24/05/2025	Milagros	Urta
Club 77: Reenie	24/05/2025	Agda	Dias de Lima
Club 77: Reenie	24/05/2025	Taner	Guney
Club 77: Reenie	24/05/2025	Taner	Guney
Club 77: Reenie	24/05/2025	Joel	Kelett
Club 77: Reenie	24/05/2025	Andrea	Montano
Club 77: Reenie	24/05/2025	Dylan	Upton
Club 77: Reenie	24/05/2025	Tasman	Trinder
Club 77: Reenie	24/05/2025	Amram	Arif
Club 77: Reenie	24/05/2025	charlie	Verity
Club 77: Phil Smart	24/05/2025	Xavier	Whiteley
Club 77: Reenie	24/05/2025	Gryffyn	Long
Club 77: Reenie	24/05/2025	Olle	Hearn
Club 77: Reenie	24/05/2025	Gaia	Pattison
Club 77: Reenie	24/05/2025	Gaia	Pattison
Club 77: Reenie	24/05/2025	Luca	Bianchinotti
Club 77: Reenie	24/05/2025	Emily	Mason
Club 77: Reenie	24/05/2025	Gokalp	Akkas
Club 77: Reenie	24/05/2025	Halil	Kamalak
Club 77: Mazzacles, Kate Doherty & Aphasic	07/06/2025	Amelia	Sharples
Club 77: Reenie	24/05/2025	Heath	Kerr
Club 77: Reenie	24/05/2025	bella	noble
Club 77: Reenie	24/05/2025	Jack	Hind
Club 77: Reenie	24/05/2025	Russell	Matthews
Club 77: Reenie	24/05/2025	Beau	Medland
Club 77: Reenie	24/05/2025	John	Larkins
Club 77: Reenie	24/05/2025	mason	connell
Club 77: Reenie	24/05/2025	Lara	Hoelscher
Club 77: Reenie	24/05/2025	Anastasia	Harris
Club 77: Reenie	24/05/2025	India	Pardoel
Club 77: Reenie, Goat Spokesperson	24/05/2025	Nihar	Kengur
Fridays at 77: Ayebatonye, Deepa	24/05/2025	Halil ibrahim	Kamalak
Club 77: Reenie	24/05/2025	James	Harper
Club 77: Reenie	24/05/2025	Natalie	Kehoe
Club 77: Reenie	24/05/2025	Halil	Kamalak
Club 77: Reenie	24/05/2025	Amelia	Sharples
Club 77: Reenie	24/05/2025	Marvin	Bell
Club 77: Reenie	24/05/2025	Asha	Tonkin
Fridays at 77: Wavyrager, halalbutch	24/05/2025	Suaenny	Alvarez
Club 77: Reenie	24/05/2025	Isidora	becerra quezada
Club 77: Reenie	24/05/2025	Karyn	Wee
Club 77: Reenie	24/05/2025	Williams	Quishpe
Club 77: Reenie	24/05/2025	Nicolas	Rey
Club 77: Reenie	24/05/2025	Izzy	Howlett
Club 77: Reenie	24/05/2025	Alvaro	Estrada
Club 77: Reenie	24/05/2025	Evelyn	Carrera
Club 77: Reenie	24/05/2025	Christina	Pearse
Club 77: Reenie	24/05/2025	Nicolas	Rey
Club 77: Reenie	24/05/2025	Isidora	becerra quezada
Club 77: Reenie	24/05/2025	India	Pardoel
Club 77: Reenie	24/05/2025	Anastasia	Harris
Club 77: Reenie	24/05/2025	Gary	Tan
Club 77: Reenie	24/05/2025	Rodolfo	León
Club 77: Reenie	24/05/2025	Caner	Özçevik
Club 77: Reenie	24/05/2025	Fatu	Türkmen
Club 77: Reenie	24/05/2025	sasha	sokolova
Club 77: Reenie	24/05/2025	Vicente	Granda
Club 77: Reenie	24/05/2025	dan	kimmo
Club 77: Reenie	24/05/2025	Alvaro	Lagos Lagos
Club 77: Reenie	24/05/2025	Christina	Eastman
Club 77: Reenie	24/05/2025	rylan	ungaro
Club 77: Reenie	24/05/2025	Mathew	Death
Club 77: Reenie	24/05/2025	antonia	Luna
Club 77: Reenie	24/05/2025	Michele	Cannillo
Club 77: Reenie	24/05/2025	Maya	Pierron
Club 77: Reenie	24/05/2025	antonia	Luna
Club 77: Reenie	24/05/2025	Michele	Cannillo
Club 77: Reenie	24/05/2025	Camilla	Winterton
Club 77: Reenie	24/05/2025	antonia	Luna
Club 77: Reenie	24/05/2025	ADIA	Yazdan-Parast
Club 77: Reenie	24/05/2025	Adia	Yazdan-Parast
Club 77: Reenie	24/05/2025	Rhiannon	Ovia
Club 77: Reenie	24/05/2025	Max	Perkins
Club 77: Reenie	24/05/2025	Gonzalo	Lamas
Club 77: Reenie	24/05/2025	Francisco Teodoro	Da Silva Neto
Club 77: Reenie	24/05/2025	Francisco	Neto
Club 77: Reenie	24/05/2025	Hanisah Binti	Mohmad Sharil
Club 77: Reenie	24/05/2025	Blake	Moy
Club 77: Reenie	24/05/2025	Laura	Bittar
Club 77: Reenie	24/05/2025	leila	weymouth
Club 77: Reenie	24/05/2025	Tahlia	Campagner
Club 77: Reenie	24/05/2025	Meredith	Kelly
Club 77: Reenie	24/05/2025	Jonathan	Reid
Club 77: Reenie	24/05/2025	Heather	O'Sullivan
Club 77: Reenie	24/05/2025	Joel	King
Club 77: Reenie	24/05/2025	Elizabeth	Kerr
Club 77: Reenie	24/05/2025	Harrison	Meares
Club 77: Reenie	24/05/2025	Ronan	Tyler
Club 77: Reenie	24/05/2025	aurora	thirard
Club 77: Reenie	24/05/2025	Amity	Fietz
Club 77: Reenie	24/05/2025	Amaya	Legg
Club 77: Mazzacles, Kate Doherty & Aphasic	24/05/2025	sienna	woodford
Club 77: Reenie	24/05/2025	Alexis	Retamal
Club 77: Reenie	24/05/2025	Amaya	Legg
Club 77: Reenie	24/05/2025	Amelia	Mackadam
Club 77: Reenie	24/05/2025	aurora	thirard
Club 77: Reenie	24/05/2025	Tim	Chapman
Club 77: Reenie	24/05/2025	richardo	antony
Club 77: Reenie	24/05/2025	Levi	Mcgriger
Club 77: Reenie	24/05/2025	Amelia	Mackadam
Club 77: Reenie	24/05/2025	sophia	wood
Club 77: Reenie	24/05/2025	Maemyka Eve	Sulat
Club 77: Reenie	24/05/2025	sophia	wood
Club 77: Reenie	24/05/2025	Alejandro	Sanroman Rodriguez
Club 77: Reenie	24/05/2025	Guillermo	Moreno
Club 77: Reenie	24/05/2025	Guillermo	Moreno
Club 77: Reenie	24/05/2025	sophia	wood
Club 77: Reenie	24/05/2025	Guillermo	Moreno
Club 77: Reenie	24/05/2025	Syukii	Wan
Club 77: Reenie	24/05/2025	Robbie	Mchugh
Club 77: Reenie	24/05/2025	Syukii	Wan
Club 77: Reenie	24/05/2025	Olivia	Heaney
Club 77: Reenie	24/05/2025	James	Mcdonald
Club 77: Reenie	24/05/2025	hussein	ali
Club 77: Reenie	24/05/2025	Georgia	Mackadam
Club 77: Reenie	24/05/2025	Caoimhe	Deering
Club 77: Reenie	24/05/2025	Neve	Clacy
Club 77: Reenie	24/05/2025	Alejandro	Soriano
Club 77: Reenie	24/05/2025	Colin	Hill
Club 77: Reenie	24/05/2025	Harriet	Naismith
Sundays at 77: Barney Kato & Simon Caldwell	24/05/2025	Meredith	Kelly
Club 77: Reenie	24/05/2025	Suaenny	Alvarez
Club 77: Reenie	24/05/2025	Meredith	Kelly
Club 77: Reenie	24/05/2025	Meredith	Kelly
Club 77: Reenie	24/05/2025	Neve	Clacy
Club 77: Reenie	24/05/2025	Divyanna	Padukka
Club 77: Reenie	24/05/2025	Phoebe	Vass
Club 77: Reenie	24/05/2025	Rhiannon	Ovia
Club 77: Reenie	24/05/2025	Grace	Winter
Club 77: Reenie	24/05/2025	Muskan	Shrestha
Club 77: Reenie	24/05/2025	andhita	sarin
Fridays at 77: Ayebatonye, Deepa	24/05/2025	Zoe	Isgrove
Club 77: Mazzacles, Kate Doherty & Aphasic	24/05/2025	Tom	Martin
Club 77: Reenie	24/05/2025	Oscar	Franklin
Club 77: Reenie	24/05/2025	Francisco	Sanchez
Club 77: Reenie	24/05/2025	Zoe	Isgrove
Club 77: Reenie	24/05/2025	Oscar	Franklin
Club 77: Reenie	24/05/2025	Aviad	Cohen
Club 77: Reenie	24/05/2025	Michele	Cannillo
Club 77: Reenie	24/05/2025	Mrigesh	Patel
Club 77: Reenie	24/05/2025	Sarthak	Madan
Club 77: Reenie	24/05/2025	Mimansa	Satam
Club 77: Reenie	24/05/2025	Música	James
Club 77: Reenie	24/05/2025	Eshaa	Tiwari
Club 77: Reenie	24/05/2025	Mimansa	Satam
Club 77: Reenie	24/05/2025	Dylan	Upton
Club 77: Reenie	24/05/2025	Alexis	Retamal
Club 77: Reenie	24/05/2025	Dylan	Upton
Club 77: Reenie	24/05/2025	Tom	Martin
Club 77: Reenie	24/05/2025	Marty	Hynes
Club 77: Reenie	24/05/2025	Aoife	Moore
Club 77: Reenie	24/05/2025	Elisha	matthews
Club 77: Reenie	24/05/2025	Luiza	Vasconcelos de Souza
Club 77: Reenie	24/05/2025	Jade	Touzot
Club 77: Reenie	24/05/2025	David	Haynes
Club 77: Reenie	24/05/2025	Rose	Hess
Club 77: Reenie	24/05/2025	sophie	nicholas
Club 77: Reenie	24/05/2025	Nathan	Liverant
Fridays at 77: Ayebatonye, Deepa	24/05/2025	Aoife	Moore
Club 77: Reenie	24/05/2025	Rose	Hess
Club 77: Reenie	24/05/2025	Aviad	Cohen
Club 77: Reenie	24/05/2025	Aviad	Cohen
Club 77: Reenie	24/05/2025	Michal	Markovič
Club 77: Reenie	24/05/2025	Eamonn	Murphy
Club 77: Reenie	24/05/2025	Lucy	Lobo
Club 77: Reenie	24/05/2025	Harry	Stanley
Club 77: Reenie	24/05/2025	Eamonn	Murphy`;

// Event mapping - match legacy event names to current database events
const eventMapping = {
  // Exact matches
  'Club 77: Phil Smart': 6,
  'Fridays at 77: Wavyrager, Yemi Sul': 5,
  'Fridays at 77: Ayebatonye, Deepa': 7,
  'Club 77: Mazzacles, Kate Doherty & Aphasic': 8,
  'Sundays at 77: Barney Kato & Simon Caldwell': 9,
  'Fridays at 77: Ciara, Scruffs': 10,
  'Club 77: Reenie, Goat Spokesperson': 11,
  'Fridays at 77: Wavyrager, halalbutch': 12,
  'Club 77: Mike Who & Daniel Lupica': 13,
  
  // Events that don't match current system (will be skipped)
  'Club 77: Reenie': null, // No "Club 77: Reenie" event in current system
  'Fridays at 77: Ari Kiko, Jhassic': null, // No "Fridays at 77: Ari Kiko, Jhassic" event
  'Fridays at 77: Jhassic, Kiminza': 14, // This matches the current event
};

async function importLegacyGuests() {
  try {
    console.log('Starting legacy guest import...');
    
    const lines = legacyData.trim().split('\n');
    let imported = 0;
    let skipped = 0;
    let errors = 0;
    const skippedEvents = new Set();
    
    for (const line of lines) {
      try {
        const parts = line.split('\t');
        if (parts.length !== 4) {
          console.log(`Skipping malformed line: ${line}`);
          errors++;
          continue;
        }
        
        const [eventName, dateStr, firstName, lastName] = parts;
        
        // Check if we have a mapping for this event
        const eventId = eventMapping[eventName];
        
        if (eventId === null) {
          skippedEvents.add(eventName);
          skipped++;
          continue;
        }
        
        if (!eventId) {
          console.log(`Unknown event: ${eventName}`);
          skippedEvents.add(eventName);
          skipped++;
          continue;
        }
        
        // Convert date from DD/MM/YYYY to YYYY-MM-DD
        const [day, month, year] = dateStr.split('/');
        const eventDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        
        // Create guest record
        await Guest.create({
          event_id: eventId,
          first_name: firstName.trim(),
          last_name: lastName.trim(),
          email: `legacy_${firstName.toLowerCase()}_${lastName.toLowerCase()}@placeholder.com`, // Placeholder email
          dob: null, // No DOB in legacy data
          checked_in: false
        });
        
        imported++;
        
        if (imported % 50 === 0) {
          console.log(`Imported ${imported} guests so far...`);
        }
        
      } catch (error) {
        console.error(`Error processing line: ${line}`, error.message);
        errors++;
      }
    }
    
    console.log('\n=== IMPORT SUMMARY ===');
    console.log(`Total guests imported: ${imported}`);
    console.log(`Total guests skipped: ${skipped}`);
    console.log(`Total errors: ${errors}`);
    
    if (skippedEvents.size > 0) {
      console.log('\nSkipped events (not in current system):');
      skippedEvents.forEach(event => console.log(`- ${event}`));
    }
    
    console.log('\nImport completed successfully!');
    
  } catch (error) {
    console.error('Import failed:', error);
  } finally {
    process.exit(0);
  }
}

// Run the import
importLegacyGuests(); 