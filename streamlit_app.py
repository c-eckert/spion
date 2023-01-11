import random
import streamlit as st

WORDS = {
        'Berufe': ["Arzt", "Ingenieur", "Lehrer", "Manager", "Polizist", "Krankenschwester", 
            "Bauarbeiter", "Schauspieler", "Verkäufer", "Rechtsanwalt", "Koch", "Erzieher", 
            "Architekt", "Journalist", "Informatiker"],
        'Länder': ["Afghanistan", "Albanien", "Algerien", "Argentinien", "Australien",
            "Bangladesch", "Belgien", "Bolivien", "Brasilien", "Bulgarien", "Uruguay", 
            "Kanada", "China", "Kroatien", "Kuba", "Zypern", "Tschechien", "Dänemark", 
            "Deutschland", "Ägypten", "Estland", "Äthiopien", "Finnland", "Frankreich", 
            "Griechenland", "Ungarn", "Island", "Österreich", "Israel"],
        "Orte im Haus" : ["Wohnzimmer", "Küche", "Schlafzimmer", "Bad", "Gästezimmer",
            "Arbeitszimmer", "Flur", "Balkon", "Garage", "Garten", "Keller", "Dachboden", 
            "Abstellraum", "Waschküche", "Treppe", "Fenster", "Tür", "Pool"],
        "Sehenswürdigkeiten" : ["Pyramide", "Taj Mahal", "Kolosseum in Rom", "Chinesische Mauer", 
            "Niagarafälle", "Schiefe Turm von Pisa", "Freiheitsstatue", "Mount Everest", 
            "Great Barrier Reef", "Eiffelturm", "Big Ben", "Central Park", "Zugspitze"],
        "Transport" : ["Auto", "Bus", "Zug", "Flugzeug", "Fahrrad", "Straßenbahn", "Motorrad",
            "Schiff", "Kanu", "Segelboot", "Surfbrett", "Skateboard", "Inlineskates", "Schlitten",
            "Snowboard", "Ski", "Helikopter", "Heißluft-Ballon", "Einrad", "E-Bike", "E-Scooter"],
        "Sport" : ["Fußball", "Basketball", "Tennis", "Volleyball", "Schwimmen", "Laufen", "Boxen",
            "Golf", "Eishockey", "Handball", "Wrestling", "Klettern", "Surfen", "Segeln", "Marathon", 
            "American Football", "Dart", "Billard", "Tischtennis", "Schach"],
        "Einrichtung" : ["Schule", "Universität", "Krankenhaus", "Bibliothek", "Feuerwehr",
            "Gefängnis", "Museum", "Theater", "Kino", "Fitnessstudio", "Einkaufszentrum", "Supermarkt",
            "Bank", "Postamt", "Tankstelle", "Hotel", "Restaurant", "Schwimmbäd", "Sauna", "Flughafen", 
            "Bahnhof"]
    }

# Funktion, um das Wort auszuwählen
def select_word(categories):
    selected_words = []
    for category in categories:
        selected_words += WORDS[category]

    return random.choice(selected_words)

def cb_seeing():
    st.session_state['mini_state'] = "seeing"

def cb_done():
    st.session_state['mini_state'] = "done"
    st.session_state['current_player'] += 1
    if st.session_state['current_player'] > len(st.session_state['players']):
        st.session_state['gamestate'] = "done"
    else:
        st.session_state['mini_state'] = "waiting"

def cb_disable():
    st.session_state['disabled'] = True

def cb_new_game():
    st.session_state['disabled'] = False
    st.session_state['gamestate'] = "ready"

def main():
    # initialize states
    if 'gamestate' not in st.session_state:
        st.session_state['gamestate'] = "ready"

    if 'current_player' not in st.session_state:
        st.session_state['current_player'] = 0

    if 'mini_state' not in st.session_state:
        st.session_state['mini_state'] = "init"

    if 'player_count' not in st.session_state:
        st.session_state['player_count'] = 0

    if 'spy_count' not in st.session_state:
        st.session_state['spy_count'] = 0
    
    if 'disabled' not in st.session_state:
        st.session_state['disabled'] = False

    st.title('Spion - das Spiel')

    player_count = st.number_input('Wie viele Spieler nehmen teil?', min_value=3, max_value=100, value=8, disabled=st.session_state["disabled"])
    spy_count = st.number_input('Wie viele Spione gibt es?', min_value=1, max_value=player_count, value=3, disabled=st.session_state["disabled"])
    categories = st.multiselect('Wählen Sie die Kategorien von Wörtern aus', options=WORDS.keys(), default=WORDS.keys(), disabled=st.session_state["disabled"])

    if st.session_state['gamestate'] == 'ready':
        if st.button('Spiel starten', on_click=cb_disable):
            selected_word = select_word(categories)
            players = ['Spion'] * spy_count + [selected_word] * (player_count - spy_count)
            random.shuffle(players)
            st.session_state['players'] = players
            st.session_state['gamestate'] = "started"
            st.session_state['current_player'] = 1
            st.session_state['mini_state'] = "waiting"
            st.session_state['player_count'] = player_count
            st.session_state['spy_count'] = spy_count

    else:
        st.button('Neues Spiel', on_click=cb_new_game)


    if st.session_state['gamestate'] == "started":
        player_count = st.empty()
        st.header("Rollenzuteilung")
        st.subheader(f"Spieler {st.session_state['current_player']} von {st.session_state['player_count']}")
        player_word = st.empty()

        if st.session_state['mini_state'] == "waiting":
            player_word.info("Klicke auf 'aufdecken' um dein Wort zu sehen.")
            st.button("aufdecken", on_click=cb_seeing)
            
        if st.session_state['mini_state'] == "seeing":
            word = st.session_state['players'][st.session_state['current_player'] - 1]
            if word == "Spion":
                player_word.error(word)
            else:
                player_word.success(word)
            st.button("zudecken", on_click=cb_done)
        
    elif st.session_state['gamestate'] == "done":
        player_word = st.empty()
        st.success(f"Das Spiel kann los gehen! Es gibt {spy_count} Spione und {player_count} Spieler.")
        st.session_state['disabled'] = False


if __name__ == '__main__':
    main()