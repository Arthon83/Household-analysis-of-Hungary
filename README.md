# Household-analysis-of-Hungary

Az emberi élet különböző szakaszait társadalmi, gazdasági és kulturális és egyéni tényezők formálják, amelyek hatással vannak arra, hogy milyen élethelyzeteket tapasztalunk meg.

Az egyik ilyen tényező a családi struktúra vagyis háztartáson belüli kapcsolatok rendszere. Az, hogy valaki gyermekével, szüleivel, párjával vagy vegyes közösségben él nem csak egyéni döntések, hanem társadalmi és gazdasági folyamatok eredménye. Ezek az élethelyzetek feltérképezése különösen fontos lehet mind a szociológiai, mind a gazdasági kutatások számára, hiszen többek között tükrözi a család szerepét, a gyermekvállalás körülményeit és az életkori mintázatokat.

Ebben a repo-ban egy olyan adat átalakítási algoritmust mutatok be, amelynek célja, hogy éves szinten elkülönített adatkészltekből, egy olyan előkészített adatrendszer jöjjön létre, amely megkönnyíti különböző családi struktúrák területi, életkorbeli és nem szerinti összehasonlítását.

main.py:  
Ez a fő szkript vezérli az adatelemzési folyamatot, amely betölti a forrásadatokat, feldolgozza azokat, és paraméterezhető módon hoz létre átmeneti mátrixokat. Az azonosítókat, dimenziókat és vizsgált attribútumokat rugalmasan lehet megadni, a végeredményt pedig külön fájlokban menti el.

moduls.py:  
Ez a modul biztosítja az adatok betöltéséhez és feldolgozásához szükséges osztályokat:

-   Loader: Adatok betöltése, korcsoportok és települési jellemzők hozzárendelése.
    
-   Simulation: Két időszak adatai közötti átmenetek modellezése és az átmeneti mátrixok létrehozása.
    

postprocessing.py:  
Az utófeldolgozás modulja, amely az eredményfájlokat összefűzi, tisztítja, és előkészíti Power BI elemzésekhez. Kiszámítja az évek közötti változásokat és pivot táblákat generál, majd az eredményeket tisztított formában exportálja.

### Első gyerek vállalás valószínűségének elemzése

Az elemzés célja, hogy megmutassam, milyen típusú következtetéseket lehet levonni az adatrendszer segítségével. Kb. a populáció 20%-ánál figyelhető meg évről évre valamilyen változás a háztartási struktúrában, ami jól jelzi a társadalmi dinamika állandó jelenlétét.

