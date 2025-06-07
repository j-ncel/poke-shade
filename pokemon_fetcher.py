import requests
import random
import re
import streamlit as st

def get_pokemon():
    # Get all valid Pokemon IDs that haven't been shown yet in this session
    valid_pokemon_ids = [i for i in range(
        1, 151) if i not in st.session_state.get("given_pokemon_list", [])]
    # Randomly select one Pokémon ID from the remaining pool
    random_pokemon_id = random.choice(valid_pokemon_ids)

    # Fetch Pokemon data
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon_id}"
    pokemon_response = requests.get(pokemon_url).json()
    pokemon_img_url = pokemon_response["sprites"]["other"]["official-artwork"]["front_default"]
    pokemon_name = pokemon_response["name"]

    # Fetch Pokemon species data (contains descriptions)
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{random_pokemon_id}"
    species_response = requests.get(species_url).json()

    # Extract all English descriptions while replacing Pokemon name and removing special characters
    descriptions = [
        re.sub(rf"\b{pokemon_name}\b", "?", re.sub(
            r"[\n\f]", " ", entry["flavor_text"]), flags=re.IGNORECASE)
        for entry in species_response["flavor_text_entries"]
        if entry["language"]["name"] == "en"
    ]

    # Initialize the list of given Pokemon if it doesn't exist in session state
    if "given_pokemon_list" not in st.session_state:
        st.session_state.given_pokemon_list = []
    # Add the current Pokemon ID to the list to avoid repeats
    st.session_state.given_pokemon_list.append(random_pokemon_id)

    # Return the image URL, name, and descriptions for the selected Pokémon
    return pokemon_img_url, pokemon_name, descriptions