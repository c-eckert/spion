import random
import streamlit as st
import json

@st.experimental_singleton
def get_words():
    with open('words.json') as file:
        return json.load(file)

def generate_wordlist(categories, player_count, spy_count):
    # select word
    selected_words = []
    words = get_words()
    for category in categories:
        selected_words += words[category]
    selected_word = random.choice(selected_words)
    # create list
    word_list = ['Spion'] * spy_count + [selected_word] * (player_count - spy_count)
    random.shuffle(word_list)
    return word_list

# callback functions
def cb_open():
    st.session_state['state_assignment'] = "open"

def cb_hide():
    st.session_state['state_assignment'] = "hidden"
    if st.session_state['current_player'] >= len(st.session_state['word_list']):
        st.session_state['state_global'] = "done"
    else:
        st.session_state['current_player'] += 1

def cb_start():
    st.session_state['player_count'] = player_count
    st.session_state['spy_count'] = spy_count
    st.session_state['state_assignment'] = "hidden"
    st.session_state['state_global'] = "assign"
    st.session_state['current_player'] = 1
    st.session_state['word_list'] = generate_wordlist(categories, player_count, spy_count)

def cb_new_game():
    st.session_state['state_global'] = "config"

st.set_page_config(
    page_title="Spion", 
    page_icon="🕵️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# initialize session_states
if 'state_global' not in st.session_state:
    st.session_state['state_global'] = "config" # config --> assign --> done

if 'state_assignment' not in st.session_state:
    st.session_state['state_assignment'] = "hidden" # hidden --> open

if 'current_player' not in st.session_state:
    st.session_state['current_player'] = 0

if 'player_count' not in st.session_state:
    st.session_state['player_count'] = 0

if 'spy_count' not in st.session_state:
    st.session_state['spy_count'] = 0

if 'word_list' not in st.session_state:
    st.session_state['word_list'] = []

st.title('Spion - das Spiel 🕵️')

if st.session_state['state_global'] == 'config':
    with st.sidebar:
        st.json(get_words())
    st.info("Jetzt mit Babtisten-Kategorie!!")
    with st.expander("Spielregeln"):
        st.markdown("""
        ### 🏁 Ziel
        **Spion** ist ein Partyspiel ab 3 Personen. Im Spiel geht es um ein bestimmtes Wort, welches einigen Spielern bekannt und anderen unbekannt ist. Diese 2 Gruppen von Spielern spielen gegeneinander.
        Die **Spione**, die das Ziel haben, das *Wort* herauszufinden. Die **anderen** haben das Ziel, die **Spione** zu identifizieren. 

        ### ⚙️ Vorbereitung
        Vor Beginn des Spiels wird ein Handy reihum gegeben, wodurch jeder Spieler seine Rolle zugewiesen bekommnt und das Wort festgelegt wird. 
        1. ``aufdecken`` drücken 
        2. Wort merken oder Rolle merken, wenn "Spion"
        3. ``zudecken`` drücken
        4. Handy weitergeben

        ### 🧐 Spiel
        Danach können sich alle Spieler gegenseitig Fragen zu dem Wort stellen, um die Rolle oder das Wort herauszufinden. 
        Jeder Spion hat *eine* Möglichkeit das Wort zu erraten. Alternativ kann eine Abstimmung durchgeführt werden, in welcher alle Spione gleichzeitig bestimmt werden. Liegt die Gruppe falsch, haben die Spione gewonnen.

        ### 🥳 Spielende
        Das Spiel endet, wenn das Wort durch einen Spion erraten wurde oder wenn alle Spione in *einer* Abstimmung erraten wurden.
        """)

    col1, col2 = st.columns(2)
    with col1:
        player_count = st.number_input('Wie viele Spieler nehmen teil?', min_value=3, max_value=100, value=8)
    with col2:
        spy_count = st.number_input('Wie viele Spione gibt es?', min_value=1, max_value=player_count, value=3)
    categories = st.multiselect('Wählen Sie die Kategorien von Wörtern aus', options=get_words().keys(), default=get_words().keys())
    st.button('Spiel starten', on_click=cb_start)

    
elif st.session_state['state_global'] == "assign":
    st.button('Neues Spiel beginnen', on_click=cb_new_game)
    st.header(f"Rollenzuteilung - Spieler {st.session_state['current_player']} von {st.session_state['player_count']}")

    if st.session_state['state_assignment'] == "hidden":
        st.info("Klicke auf 'aufdecken' um dein Wort zu sehen.")
        st.button("aufdecken", on_click=cb_open)
        
    elif st.session_state['state_assignment'] == "open":
        word = st.session_state['word_list'][st.session_state['current_player'] - 1]
        if word == "Spion":
            st.error(word)
        else:
            st.success(word)
        st.button("zudecken und weitergeben", on_click=cb_hide)
    
elif st.session_state['state_global'] == "done":
    st.success(f"Das Spiel kann los gehen! Es gibt {st.session_state['spy_count']} Spione und {st.session_state['player_count']} Spieler.")
    st.button('Neues Spiel', on_click=cb_new_game)
    st.balloons()