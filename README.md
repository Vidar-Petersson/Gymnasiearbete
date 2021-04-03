# GA - Havs- och väderundersökningar på ett kostnadseffektivt och demokratiskt sätt
I detta gymnasiearbete studerades möjligheterna att undersöka havstemperaturutveckling i Östersjöområdet med eget mottagna vädersatellitbilder. I denna GitHub presenteras all kod och data associerade med arbetet. 

## Översikt
Databehandlingen i studien bestod i huvudsak av två delar:
* Att utifrån en avkodad SST-bild avläsa pixelvärdena och returnera en havsmedeltemperatur för det avlästa området. 
* Att samla in relevant metadata sparad i de avkodade bilderna.
Den sammanställda havstemperaturen och relevant metadata sammanställdes sedan och sparades i en CSV-fil kallad ```SST.csv```

## Användning
1. Skapa en mapp kallad ```img``` där alla avkodade bilder sparas.
2. Beskär sedan själv alla bilder till det området som önskas avläsas. Förslagsvis med [inbac](https://github.com/weclaw1/inbac).
3. Spara alla beskurna bilder i ```img/crop```.
4. Kör sedan ```python meta.py``` i sin hemmapp.
5. Temperaturen för alla beskurna bilder avläses, metadaten hämtas från de icke-beskurna och all data sammanställs i ```data/SST.csv```

### Observera
* Använd alltid standard paletten för SST i WxToImg, så att temperaturfärgerna motsvarar ```tempscale300.png```.

## Om projektet
* Detta projekt deltog i [Unga Forskares digitala utställning](https://digitala-utstallningen.ungaforskare.se/finalutstallning/) för gymnasiearbeten 2021.
* Kvalade sig vidare till region- och riksfinal. 
* Vann [Yale Science and Engineering Association Award](http://groupspaces.com/YSEA/pages/ysea-science-fair-award) och [Stockholm Junior Water Prize Sweden](https://www.siwi.org/prizes/stockholmjuniorwaterprize/) i finalen.
* Ska delta i Forsknings-VM för vattenfrågor (internationella SJWP-finalen).

## License
[MIT](https://choosealicense.com/licenses/mit/)
