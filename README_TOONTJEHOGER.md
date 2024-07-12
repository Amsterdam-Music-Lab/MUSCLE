### Experiment config of ToontjeHoger experiments

Set the following experiment values in the admin:

| Experiment | Slug         | Rounds |
| ---------- | ------------ | ------ |
| home       | toontjehoger | 0      |

## Experiment blocks

The ToontjeHoger experiment block rules can be found in:

```
backend/experiment/rules/toontjehoger_1_mozart.py
backend/experiment/rules/toontjehoger_2_preverbal.py
backend/experiment/rules/toontjehoger_3_plink.py
backend/experiment/rules/toontjehoger_4_absolute.py
backend/experiment/rules/toontjehoger_5_tempo.py
backend/experiment/rules/toontjehoger_6_relative.py
```

-   These rules contain all textual content that is shown during the block

**Per block config**

Set the following per-block values in the admin:

| Block | Slug                     | Rounds |
| ---------- | ------------------------ | ------ |
| 1          | toontjehoger_1_mozart    | 2      |
| 2          | toontjehoger_2_preverbal | 2      |
| 3          | toontjehoger_3_plink     | 10     |
| 4          | toontjehoger_4_absolute  | 5      |
| 5          | toontjehoger_5_tempo     | 5      |
| 6          | toontjehoger_6_relative  | 2      |

### Block images

Images for the ToontjeHoger experiments can be found in:

```
frontend/public/images/experiments/toontjehoger/*
```

### Block information pages

The information pages are shown after each experiment can be found in:

```
backend/templates/info/toontjehoger/experiment1.html
backend/templates/info/toontjehoger/experiment2.html
backend/templates/info/toontjehoger/experiment3.html
backend/templates/info/toontjehoger/experiment4.html
backend/templates/info/toontjehoger/experiment5.html
backend/templates/info/toontjehoger/experiment6.html
```

## Playlists

Each block uses a playlist with additional information in the tag/group field.

### Block 1

The group field contains the round.

```
"Tomaso Albinoni","Adagio in G mineur (uitgevoerd door het Prague Baroque Orchestra, onder leiding van Trevor Pinnock)",0,26.0,"/toontjehoger/mozart/fragment_a.mp3",0,0,1
"Wolfgang Amadeus Mozart","Sonate voor twee pianos in D groot, KV 448 (uitgevoerd door Lucas en Arthur Jussen)",0,28.0,"/toontjehoger/mozart/fragment_b.mp3",0,0,2
```

### Block 2

The group field contains the round.

```
AML,Mens,0,1,/toontjehoger/preverbal/1_mens.mp3,0,c,1
AML,Walvis,0,1,/toontjehoger/preverbal/2_walvis.mp3,0,b,1
AML,Trompet,0,1,/toontjehoger/preverbal/3_trompet.mp3,0,a,1
AML,Franse baby,0,1,/toontjehoger/preverbal/5_franse_baby.mp3,0,a,2
AML,Duitse baby,0,1,/toontjehoger/preverbal/4_duitse_baby.mp3,0,b,2
```

### Block 3

The group field contains a semi-colon separated list of time-period and emotion, e.g. 70s;vrolijk

```
Queen,Bohemian Rhapsody,0,1,/toontjehoger/plink/2021-001.mp3,0,0,70s;vrolijk
Danny Vera,Roller Coaster,0,1,toontjehoger/plink/2021-002.mp3,0,0,10s;vrolijk
Procol Harum,A Whiter Shade Of Pale,0,1,toontjehoger/plink/2021-003.mp3,0,0,60s;vrolijk
Eagles,Hotel California,0,1,toontjehoger/plink/2021-004.mp3,0,0,70s;vrolijk
Billy Joel,Piano Man,0,1,toontjehoger/plink/2021-005.mp3,0,0,70s;vrolijk
Golden Earring,Radar Love,0,1,toontjehoger/plink/2021-006.mp3,0,0,70s;vrolijk
Led Zeppelin,Stairway To Heaven,0,1,toontjehoger/plink/2021-007.mp3,0,0,70s;vrolijk
Metallica,Nothing Else Matters,0,1,toontjehoger/plink/2021-008.mp3,0,0,90s;vrolijk
Pearl Jam,Black,0,1,toontjehoger/plink/2021-009.mp3,0,0,90s;vrolijk
Boudewijn de Groot,Avond,0,1,toontjehoger/plink/2021-010.mp3,0,0,90s;vrolijk
Coldplay,Fix You,0,1,toontjehoger/plink/2021-011.mp3,0,0,00s;vrolijk
Queen,Love Of My Life,0,1,toontjehoger/plink/2021-012.mp3,0,0,70s;vrolijk
Pink Floyd,Wish You Were Here,0,1,toontjehoger/plink/2021-013.mp3,0,0,70s;vrolijk
Di-rect,Soldier On,0,1,toontjehoger/plink/2021-014.mp3,0,0,20s;vrolijk
Deep Purple,Child In Time,0,1,toontjehoger/plink/2021-015.mp3,0,0,70s;vrolijk
Bruce Springsteen,The River,0,1,toontjehoger/plink/2021-016.mp3,0,0,80s;vrolijk
Guns N' Roses,November Rain,0,1,toontjehoger/plink/2021-017.mp3,0,0,90s;vrolijk
Dire Straits,Brothers In Arms,0,1,toontjehoger/plink/2021-018.mp3,0,0,80s;vrolijk
Disturbed,The Sound Of Silence,0,1,toontjehoger/plink/2021-019.mp3,0,0,10s;vrolijk
Miss Montreal,Door De Wind,0,1,toontjehoger/plink/2021-020.mp3,0,0,20s;vrolijk
Prince & The Revolution,Purple Rain,0,1,toontjehoger/plink/2021-021.mp3,0,0,80s;vrolijk
Pink Floyd,Comfortably Numb,0,1,toontjehoger/plink/2021-022.mp3,0,0,70s;vrolijk
Toto,Africa,0,1,toontjehoger/plink/2021-023.mp3,0,0,80s;vrolijk
David Bowie,Heroes,0,1,toontjehoger/plink/2021-024.mp3,0,0,70s;vrolijk
Dire Straits,Sultans Of Swing,0,1,toontjehoger/plink/2021-025.mp3,0,0,70s;vrolijk
```

### Block 4

The tag field contains indicates if the section pitch is original (a) or it it changed (b,c).
The group field contains a song identifier.

```
AML,Star Wars,0,1,/toontjehoger/absolute/4_Toonhoogte_Item1_a.mp3,0,a,1
AML,Star Wars,0,1,/toontjehoger/absolute/4_Toonhoogte_Item1_b.mp3,0,b,1
AML,Star Wars,0,1,/toontjehoger/absolute/4_Toonhoogte_Item1_c.mp3,0,c,1
AML,Viva la vida van Coldplay,0,1,/toontjehoger/absolute/4_Toonhoogte_Item2_a.mp3,0,a,2
AML,Viva la vida van Coldplay,0,1,/toontjehoger/absolute/4_Toonhoogte_Item2_b.mp3,0,b,2
AML,Viva la vida van Coldplay,0,1,/toontjehoger/absolute/4_Toonhoogte_Item2_c.mp3,0,c,2
AML,De wereld draait door,0,1,/toontjehoger/absolute/4_Toonhoogte_Item3_a.mp3,0,a,3
AML,De wereld draait door,0,1,/toontjehoger/absolute/4_Toonhoogte_Item3_b.mp3,0,b,3
AML,De wereld draait door,0,1,/toontjehoger/absolute/4_Toonhoogte_Item3_c.mp3,0,c,3
AML,Friends,0,1,/toontjehoger/absolute/4_Toonhoogte_Item4_a.mp3,0,a,4
AML,Friends,0,1,/toontjehoger/absolute/4_Toonhoogte_Item4_b.mp3,0,b,4
AML,Friends,0,1,/toontjehoger/absolute/4_Toonhoogte_Item4_c.mp3,0,c,4
AML,Game of Thrones,0,1,/toontjehoger/absolute/4_Toonhoogte_Item5_a.mp3,0,a,5
AML,Game of Thrones,0,1,/toontjehoger/absolute/4_Toonhoogte_Item5_b.mp3,0,b,5
AML,Game of Thrones,0,1,/toontjehoger/absolute/4_Toonhoogte_Item5_c.mp3,0,c,5
AML,Sesamstraat,0,1,/toontjehoger/absolute/4_Toonhoogte_Item6_a.mp3,0,a,6
AML,Sesamstraat,0,1,/toontjehoger/absolute/4_Toonhoogte_Item6_b.mp3,0,b,6
AML,Sesamstraat,0,1,/toontjehoger/absolute/4_Toonhoogte_Item6_c.mp3,0,c,6
AML,NOS Studio Sport,0,1,/toontjehoger/absolute/4_Toonhoogte_Item7_a.mp3,0,a,7
AML,NOS Studio Sport,0,1,/toontjehoger/absolute/4_Toonhoogte_Item7_b.mp3,0,b,7
AML,NOS Studio Sport,0,1,/toontjehoger/absolute/4_Toonhoogte_Item7_c.mp3,0,c,7
AML,het NOS Journaal,0,1,/toontjehoger/absolute/4_Toonhoogte_Item8_a.mp3,0,a,8
AML,het NOS Journaal,0,1,/toontjehoger/absolute/4_Toonhoogte_Item8_b.mp3,0,b,8
AML,het NOS Journaal,0,1,/toontjehoger/absolute/4_Toonhoogte_Item8_c.mp3,0,c,8
AML,Stranger Things,0,1,/toontjehoger/absolute/4_Toonhoogte_Item9_a.mp3,0,a,9
AML,Stranger Things,0,1,/toontjehoger/absolute/4_Toonhoogte_Item9_b.mp3,0,b,9
AML,Stranger Things,0,1,/toontjehoger/absolute/4_Toonhoogte_Item9_c.mp3,0,c,9
AML,Wie is de Mol,0,1,/toontjehoger/absolute/4_Toonhoogte_Item10_a.mp3,0,a,10
AML,Wie is de Mol,0,1,/toontjehoger/absolute/4_Toonhoogte_Item10_b.mp3,0,b,10
AML,Wie is de Mol,0,1,/toontjehoger/absolute/4_Toonhoogte_Item10_c.mp3,0,c,10
AML,ER,0,1,/toontjehoger/absolute/4_Toonhoogte_Item11_a.mp3,0,a,11
AML,ER,0,1,/toontjehoger/absolute/4_Toonhoogte_Item11_b.mp3,0,b,11
AML,ER,0,1,/toontjehoger/absolute/4_Toonhoogte_Item11_c.mp3,0,c,11
AML,The Walking Dead,0,1,/toontjehoger/absolute/4_Toonhoogte_Item12_a.mp3,0,a,12
AML,The Walking Dead,0,1,/toontjehoger/absolute/4_Toonhoogte_Item12_b.mp3,0,b,12
AML,The Walking Dead,0,1,/toontjehoger/absolute/4_Toonhoogte_Item12_c.mp3,0,c,12
AML,Breaking Bad,0,1,/toontjehoger/absolute/4_Toonhoogte_Item13_a.mp3,0,a,13
AML,Breaking Bad,0,1,/toontjehoger/absolute/4_Toonhoogte_Item13_b.mp3,0,b,13
AML,Breaking Bad,0,1,/toontjehoger/absolute/4_Toonhoogte_Item13_c.mp3,0,c,13
```

### Block 5

The tag field contains an identifier. The group field shows if it is an original (or) or changed (ch) track.

```
Glenn Gould,"J. S. Bach, English Suite No. 3, BWV 808, Allemande",0,1,/toontjehoger/tempo/C1_P1_CH_70.mp3,0,C1_P1_CH,ch
Sviatoslav Richter,"J. S. Bach, English Suite No. 3, BWV 808, Allemande",0,1,/toontjehoger/tempo/C1_P1_OR_70.mp3,0,C1_P1_OR,or
Sviatoslav Richter,"J. S. Bach, English Suite No. 3, BWV 808, Allemande",0,1,/toontjehoger/tempo/C1_P2_CH_87.mp3,0,C1_P2_CH,ch
Glenn Gould,"J. S. Bach, English Suite No. 3, BWV 808, Allemande",0,1,/toontjehoger/tempo/C1_P2_OR_87.mp3,0,C1_P2_OR,or
Glenn Gould,"J. S. Bach, WTC II, BWV 880, Fugue 11",0,1,/toontjehoger/tempo/C2_P1_CH_102.mp3,0,C2_P1_CH,ch
Rosalyn Tureck,"J. S. Bach, WTC II, BWV 880, Fugue 11",0,1,/toontjehoger/tempo/C2_P1_OR_102.mp3,0,C2_P1_OR,or
Rosalyn Tureck,"J. S. Bach, WTC II, BWV 880, Fugue 11",0,1,/toontjehoger/tempo/C2_P2_CH_135.mp3,0,C2_P2_CH,ch
Glenn Gould,"J. S. Bach, WTC II, BWV 880, Fugue 11",0,1,/toontjehoger/tempo/C2_P2_OR_135.mp3,0,C2_P2_OR,or
Arthur Rubinstein,"L. v. Beethoven, Piano Sonata No. 14, Op. 17, no. 2. Allegretto",0,1,/toontjehoger/tempo/C3_P1_CH_75.mp3,0,C3_P1_CH,ch
Vladimir Ashkenazy,"L. v. Beethoven, Piano Sonata No. 14, Op. 17, no. 2. Allegretto",0,1,/toontjehoger/tempo/C3_P1_OR_75.mp3,0,C3_P1_OR,or
Vladimir Ashkenazy,"L. v. Beethoven, Piano Sonata No. 14, Op. 17, no. 2. Allegretto",0,1,/toontjehoger/tempo/C3_P2_CH_56.mp3,0,C3_P2_CH,ch
Arthur Rubinstein,"L. v. Beethoven, Piano Sonata No. 14, Op. 17, no. 2. Allegretto",0,1,/toontjehoger/tempo/C3_P2_OR_56.mp3,0,C3_P2_OR,or
Claudio Arrau,"F. Chopin, Grande Valse Brillante, op. 18",0,1,/toontjehoger/tempo/C4_P1_CH_88.mp3,0,C4_P1_CH,ch
Vladimir Ashkenazy,"F. Chopin, Grande Valse Brillante, op. 18",0,1,/toontjehoger/tempo/C4_P1_OR_88.mp3,0,C4_P1_OR,or
Vladimir Ashkenazy,"F. Chopin, Grande Valse Brillante, op. 18",0,1,/toontjehoger/tempo/C4_P2_CH_70.mp3,0,C4_P2_CH,ch
Claudio Arrau,"F. Chopin, Grande Valse Brillante, op. 18",0,1,/toontjehoger/tempo/C4_P2_OR_70.mp3,0,C4_P2_OR,or
Vladimir Horowitz,"R. Schumann, Kinderszenen, Träumerei",0,1,/toontjehoger/tempo/C5_P1_CH_70.mp3,0,C5_P1_CH,ch
Claudio Arrau,"R. Schumann, Kinderszenen, Träumerei",0,1,/toontjehoger/tempo/C5_P1_OR_70.mp3,0,C5_P1_OR,or
Claudio Arrau,"R. Schumann, Kinderszenen, Träumerei",0,1,/toontjehoger/tempo/C5_P2_CH_87.mp3,0,C5_P2_CH,ch
Vladimir Horowitz,"R. Schumann, Kinderszenen, Träumerei",0,1,/toontjehoger/tempo/C5_P2_OR_87.mp3,0,C5_P2_OR,or
Herbie Hancock,Dolphin Dance,0,1,/toontjehoger/tempo/J1_P1_CH_153.mp3,0,J1_P1_CH,ch
Ahmad Jamal,Dolphin Dance,0,1,/toontjehoger/tempo/J1_P1_OR_153.mp3,0,J1_P1_OR,or
Ahmad Jamal,Dolphin Dance,0,1,/toontjehoger/tempo/J1_P2_CH_120.mp3,0,J1_P2_CH,ch
Herbie Hancock,Dolphin Dance,0,1,/toontjehoger/tempo/J1_P2_OR_120.mp3,0,J1_P2_OR,or
Bill Evans,Blue in Green,0,1,/toontjehoger/tempo/J2_P1_CH_55.mp3,0,J2_P1_CH,ch
Miles Davis,Blue in Green,0,1,/toontjehoger/tempo/J2_P1_OR_55.mp3,0,J2_P1_OR,or
Miles Davis,Blue in Green,0,1,/toontjehoger/tempo/J2_P2_CH_67.mp3,0,J2_P2_CH,ch
Bill Evans,Blue in Green,0,1,/toontjehoger/tempo/J2_P2_OR_67.mp3,0,J2_P2_OR,or
Duke Ellington,Caravan,0,1,/toontjehoger/tempo/J3_P1_CH_96.mp3,0,J3_P1_CH,ch
Duke Ellington,Caravan,0,1,/toontjehoger/tempo/J3_P1_OR_96.mp3,0,J3_P1_OR,or
Duke Ellington,Caravan,0,1,/toontjehoger/tempo/J3_P2_CH_114.mp3,0,J3_P2_CH,ch
Duke Ellington,Caravan,0,1,/toontjehoger/tempo/J3_P2_OR_114.mp3,0,J3_P2_OR,or
Phil Woods,Au Privave,0,1,/toontjehoger/tempo/J4_P1_CH_90.mp3,0,J4_P1_CH,ch
Wes Montgomery,Au Privave,0,1,/toontjehoger/tempo/J4_P1_OR_90.mp3,0,J4_P1_OR,or
Wes Montgomery,Au Privave,0,1,/toontjehoger/tempo/J4_P2_CH_113.mp3,0,J4_P2_CH,ch
Phil Woods,Au Privave,0,1,/toontjehoger/tempo/J4_P2_OR_113.mp3,0,J4_P2_OR,or
Bert van de Brink,All the things you are,0,1,/toontjehoger/tempo/J5_P1_CH_140.mp3,0,J5_P1_CH,ch
Keith Jarrett,All the things you are,0,1,/toontjehoger/tempo/J5_P1_OR_140.mp3,0,J5_P1_OR,or
Keith Jarrett,All the things you are,0,1,/toontjehoger/tempo/J5_P2_CH_108.mp3,0,J5_P2_CH,ch
Bert van de Brink,All the things you are,0,1,/toontjehoger/tempo/J5_P2_OR_108.mp3,0,J5_P2_OR,or
Jimi Hendrix,Killing Floor,0,1,/toontjehoger/tempo/R1_P1_CH_156.mp3,0,R1_P1_CH,ch
The Jimi Hendrix Experience,Killing Floor,0,1,/toontjehoger/tempo/R1_P1_OR_156.mp3,0,R1_P1_OR,or
The Jimi Hendrix Experience,Killing Floor,0,1,/toontjehoger/tempo/R1_P2_CH_137.mp3,0,R1_P2_CH,ch
Jimi Hendrix,Killing Floor,0,1,/toontjehoger/tempo/R1_P2_OR_137.mp3,0,R1_P2_OR,or
Muse,Muscle Museum,0,1,/toontjehoger/tempo/R2_P1_CH_161.mp3,0,R2_P1_CH,ch
Muse,Muscle Museum,0,1,/toontjehoger/tempo/R2_P1_OR_161.mp3,0,R2_P1_OR,or
Muse,Muscle Museum,0,1,/toontjehoger/tempo/R2_P2_CH_138.mp3,0,R2_P2_CH,ch
Muse,Muscle Museum,0,1,/toontjehoger/tempo/R2_P2_OR_138.mp3,0,R2_P2_OR,or
Iron Butterfly,In a Gadda da Vida,0,1,/toontjehoger/tempo/R3_P1_CH_140.mp3,0,R3_P1_CH,ch
Slayer,In a Gadda da Vida,0,1,/toontjehoger/tempo/R3_P1_OR_140.mp3,0,R3_P1_OR,or
Slayer,In a Gadda da Vida,0,1,/toontjehoger/tempo/R3_P2_CH_115.mp3,0,R3_P2_CH,ch
Iron Butterfly,In a Gadda da Vida,0,1,/toontjehoger/tempo/R3_P2_OR_115.mp3,0,R3_P2_OR,or
Dread Zeppelin,Stairway to Heaven,0,1,/toontjehoger/tempo/R4_P1_CH_66.mp3,0,R4_P1_CH,ch
Stanley Jordon,Stairway to Heaven,0,1,/toontjehoger/tempo/R4_P1_OR_66.mp3,0,R4_P1_OR,or
Stanley Jordon,Stairway to Heaven,0,1,/toontjehoger/tempo/R4_P2_CH_86.mp3,0,R4_P2_CH,ch
Dread Zeppelin,Stairway to Heaven,0,1,/toontjehoger/tempo/R4_P2_OR_86.mp3,0,R4_P2_OR,or
Iggy Pop,Now I Wanna Be Your Dog,0,1,/toontjehoger/tempo/R5_P1_CH_123.mp3,0,R5_P1_CH,ch
The Stooges,Now I Wanna Be Your Dog,0,1,/toontjehoger/tempo/R5_P1_OR_123.mp3,0,R5_P1_OR,or
The Stooges,Now I Wanna Be Your Dog,0,1,/toontjehoger/tempo/R5_P2_CH_155.mp3,0,R5_P2_CH,ch
Iggy Pop,Now I Wanna Be Your Dog,0,1,/toontjehoger/tempo/R5_P2_OR_155.mp3,0,R5_P2_OR,or
```

### Block 6

The tag field indicates if the section in a, b or c.

```
AML,Fragment A,0,1,/toontjehoger/relative/relative_a.mp3,0,a,0
AML,Fragment B,0,1,/toontjehoger/relative/relative_b.mp3,0,b,0
AML,Fragment C,0,1,/toontjehoger/relative/relative_c.mp3,0,c,0
```
