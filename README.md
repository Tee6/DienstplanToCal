### Dienstplan-To-Calendar
----
Im Zivildienst bekomme ich jeden Monat einen Dienstplan. Diesen wollte ich automatisiert in meine Kalender-App einfügen. Dafür habe ich dieses Skript geschrieben.
Anfangs wollte ich mit OpenCV und Tesseract die Schichten aus dem Bild des Dienstplans herausfiltern. Doch das funktionierte nicht. Auch mit ChatGPT habe ich versucht, 
den Dienstplan in die richtige Form für mein Skript zu bekommen, jedoch ebenfalls vergeblich.

Nun müssen die Schichten manuell in die folgende Form gebracht werden, jedoch wird der Rest automatisch grün in meinen Kalender eingetragen, was für mich persönlich eine große 
Erleichterung im Alltag darstellt.

```
kalender_map = {
    "ZT": {
        'days': [5,6,7,8,11,12,21,22,25,26,27,28], # Wochentage an denen ich Tagdienst habe
        'start_time': [7, 30], 
        'end_time': [16, 30]
    },
    "Z2": {
        'days': [1,2,3,9,23], # WochenendTage, an denen ich Tagdienst habe
        'start_time': [8, 0], 
        'end_time': [14, 0],
    },
    "Z3": {
        'days': [14,15,18], # Wochentage an denen ich Spätdienst habe
        'start_time': [15, 30], 
        'end_time': [23, 0],
    },
    "Z4": {
        'days': [16,17,30], # Wochenendtage an denen ich Spätdienst habe
        'start_time': [18, 0], 
        'end_time': [23, 0],
    },
}
```
