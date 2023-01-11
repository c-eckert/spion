import random
import streamlit as st
import json

# Funktion, um das Wort auszuwählen
def generate_wordlist(categories, player_count, spy_count):
    # select word
    selected_words = []
    with open('words.json') as file:
        words = json.load(file)
        for category in categories:
            selected_words += words[category]
    selected_word = random.choice(selected_words)
    # create list
    word_list = ['Spion'] * spy_count + [selected_word] * (player_count - spy_count)
    random.shuffle(word_list)
    return word_list

@st.experimental_singleton
def get_words():
    with open('words.json') as file:
        return json.load(file)

def cb_open():
    st.session_state['state_assignment'] = "open"

def cb_hide():
    st.session_state['state_assignment'] = "hidden"
    if st.session_state['current_player'] >= len(st.session_state['word_list']):
        st.session_state['state_global'] = "done"
    else:
        st.session_state['current_player'] += 1

def cb_start():
    st.session_state['state_assignment'] = "hidden"
    st.session_state['state_global'] = "assign"
    st.session_state['disabled'] = True
    st.session_state['current_player'] = 1
    st.session_state['word_list'] = generate_wordlist(st.session_state['categories'], st.session_state['player_count'], st.session_state['spy_count'])

def cb_new_game():
    st.session_state['disabled'] = False
    st.session_state['state_global'] = "config"


def main():
    # initialize states
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

    if 'categories' not in st.session_state:
        st.session_state['categories'] = []
    
    if 'disabled' not in st.session_state:
        st.session_state['disabled'] = False

    if 'word_list' not in st.session_state:
        st.session_state['word_list'] = []

    st.title('Spion - das Spiel')

    player_count = st.number_input('Wie viele Spieler nehmen teil?', min_value=3, max_value=100, value=8, disabled=st.session_state["disabled"])
    spy_count = st.number_input('Wie viele Spione gibt es?', min_value=1, max_value=player_count, value=3, disabled=st.session_state["disabled"])
    categories = st.multiselect('Wählen Sie die Kategorien von Wörtern aus', options=get_words().keys(), default=get_words().keys(), disabled=st.session_state["disabled"])

    if st.session_state['state_global'] == 'config':
        st.session_state['player_count'] = player_count
        st.session_state['spy_count'] = spy_count
        st.session_state['categories'] = categories
        with st.sidebar:
            st.json(get_words())

        st.button('Spiel starten', on_click=cb_start)

    elif st.session_state['state_global'] == "assign":
        st.button('Neues Spiel', on_click=cb_new_game)
        st.header("Rollenzuteilung")
        st.subheader(f"Spieler {st.session_state['current_player']} von {st.session_state['player_count']}")

        if st.session_state['state_assignment'] == "hidden":
            st.info("Klicke auf 'aufdecken' um dein Wort zu sehen.")
            st.button("aufdecken", on_click=cb_open)
            
        elif st.session_state['state_assignment'] == "open":
            word = st.session_state['word_list'][st.session_state['current_player'] - 1]
            if word == "Spion":
                st.error(word)
            else:
                st.success(word)
            st.button("zudecken", on_click=cb_hide)
        
    elif st.session_state['state_global'] == "done":
        st.success(f"Das Spiel kann los gehen! Es gibt {spy_count} Spione und {player_count} Spieler.")
        st.button('Neues Spiel', on_click=cb_new_game)


if __name__ == '__main__':
    main()