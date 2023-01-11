import streamlit as st
import pandas as pd
import numpy as np
import random as rd

st.title('Spion')

no_player = st.number_input('Anzahl an Mitspielern', min_value=3, step=1)
st.write('The current number is ', no_player)

no_spy = st.number_input('Anzahl an Spionen', min_value=1, max_value=no_player-1, step=1)
st.write('The current number is ', no_spy)

cathegories = st.multiselect(
    "Kathegorien",
    ["Länder", "Orte", "Verkehrsmittel"],
    ["Länder", "Orte", "Verkehrsmittel"]
)
countries = ["Deutschland", "Schweiz", "Österreich", 
             "Frankreich", "Belgien", "Niederlande", 
             "England"]

cities = ["Wien", "London", "Paris", "Berlin", "Zürich", "Hamburg"]

vehicles = ["Auto", "Zug", "Straßenbahn", "Flugzeug", "Schiff", "Luftschiff", "Hubschrauber"]

words = []
if "Länder" in cathegories:
    words += countries
if "Orte" in cathegories:
    words += cities
if "Verkehrsmittel" in cathegories:
    words += vehicles

print(words)
if len(words) > 0:
    game_word = rd.choice(words)

    print(game_word)
    start = st.button("Start")