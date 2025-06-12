import requests
import random
import re
import streamlit as st


def get_pokemon():
    # Get all valid Pokemon IDs that haven't been shown yet in this session
    shown_ids = [entry["id"]
                 for entry in st.session_state.get("given_pokemons", [])]
    valid_pokemon_ids = [i for i in range(1, 152) if i not in shown_ids]
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

    # Initialize the list if it doesn't exist
    if "given_pokemons" not in st.session_state:
        st.session_state.given_pokemons = []
        get_all_pokemon_names()
    # Add the current Pokemon as a dictionary
    st.session_state.given_pokemons.append({
        "id": random_pokemon_id,
        "img_url": pokemon_img_url,
        "name": pokemon_name
    })

    return pokemon_img_url, pokemon_name, descriptions


def get_all_pokemon_names():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url).json()

    # Extract pokemon names
    pokemon_names = [pokemon["name"] for pokemon in response["results"]]
    st.session_state.all_pokemon_names = pokemon_names
