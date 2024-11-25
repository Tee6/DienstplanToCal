import datetime
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Google Calendar API Setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authentifizierung und Service erstellen
def authenticate_google_account():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

# Funktion zum Erstellen von Events
def create_calendar_events(service, year, month, key, days, start_time, end_time):
    for day in days:
        event_start = datetime.datetime(year, month, day, start_time[0], start_time[1])  # Startzeit
        event_end = datetime.datetime(year, month, day, end_time[0], end_time[1])  # Endzeit
        
        event = {
            'summary': key,  # Event Name (z.B. "ZT")
            'start': {
                'dateTime': event_start.isoformat(),
                'timeZone': 'Europe/Berlin',
            },
            'end': {
                'dateTime': event_end.isoformat(),
                'timeZone': 'Europe/Berlin',
            },
            'colorId': '2'  # Farbe des Events (2 = Grün)
        }

        # Erstelle das Event im Google Kalender
        service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event für {key} am {event_start.strftime('%d.%m.%Y')} von {event_start.strftime('%H:%M')} bis {event_end.strftime('%H:%M')} wurde erstellt.")


# Authentifizieren und Kalender-Service erhalten
service = authenticate_google_account()

# Arbeitszeiten Definieren nach Dienstplan
Jahr = 2024
Monat = 12

kalender_map_okt = { # Oktober 2024
    "ZT": {
        'days': [1,2,3,4,15,16,17,18,21,22,23,24,25,28,29,30], # Wochentage an denen ich Tagdienst habe
        'start_time': [7, 30], 
        'end_time': [16, 30]
    },
    "Z2": {
        'days': [5], # WochenendTage, an denen ich Tagdienst habe
        'start_time': [8, 0], 
        'end_time': [14, 0],
    },
    "Z3": {
        'days': [9,10,11], # Wochentage an denen ich Spätdienst habe
        'start_time': [15, 30], 
        'end_time': [23, 0],
    },
    "Z4": {
        'days': [12,13], # Wochenendtage an denen ich Spätdienst habe
        'start_time': [18, 0], 
        'end_time': [23, 0],
    },
}

kalender_map_nov = { # November 2024
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

kalender_map_dez = { # Dezember 2024
    "ZT": {
        'days': [4,5,6,10,11,12,13,30,31], # Wochentage an denen ich Tagdienst habe
        'start_time': [7, 30], 
        'end_time': [16, 30]
    },
    "Z2": {
        'days': [14], # WochenendTage, an denen ich Tagdienst habe
        'start_time': [8, 0], 
        'end_time': [14, 0],
    },
    "Z3": {
        'days': [16,17,18,19,20,27], # Wochentage an denen ich Spätdienst habe
        'start_time': [15, 30], 
        'end_time': [23, 0],
    },
    "Z4": {
        'days': [1,7,8,23,24,25,26], # Wochenendtage an denen ich Spätdienst habe
        'start_time': [18, 0], 
        'end_time': [23, 0],
    },
}

kalender_map = kalender_map_dez

input = input("Events erstellen (e) oder Arbeitszeit berechnen (b)?")
Tagesstunden = 40/7
if input == "b":
    # Arbeitszeiten berechnen
    total_hours = 0
    for key, data in kalender_map.items():
        total_shift_hours = 0
        for day in data['days']:
            start_time = datetime.datetime(Jahr, Monat, day, data['start_time'][0], data['start_time'][1])
            end_time = datetime.datetime(Jahr, Monat, day, data['end_time'][0], data['end_time'][1])
            diff = end_time - start_time
            if key == "ZT":
                diff -= datetime.timedelta(hours=0.5)  # Pause abziehen
            total_shift_hours += diff.total_seconds() / 3600
        print(f"Arbeitszeit für {key}: {total_shift_hours} Stunden")
        total_hours += total_shift_hours
    print(f"Gesamte Arbeitszeit: {total_hours} Stunden. Sollwert: ", round(Tagesstunden*31))
    print(f"Überstunden: {round(total_hours - Tagesstunden*31)} Stunden")
if input == "e":
    # Events erstellen
    for key, data in kalender_map.items():
        create_calendar_events(service, Jahr, Monat, key, data['days'], data['start_time'], data['end_time'])
