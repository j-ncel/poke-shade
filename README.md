# PokeShade

A fun "Who's That Pokémon?" guessing game built with Streamlit.  
Players are shown a masked silhouette of a random Pokémon and must guess its name. Hints are available, and the game keeps track of Pokémon already shown in the session.

## Try It Here

**[PokeShade](https://poke-shade.streamlit.app/)**

## Features

- Randomly selects a Pokémon from the first 151 (Kanto region).
- Displays a masked (silhouette) image of the Pokémon.
- Accepts user guesses and provides feedback.
- Option to show a hint.
- Reveals the answer and original image after each guess.
- Avoids repeating Pokémon in a single session.

## Project Structure

```
pokeshade/
│
├── main.py              # Streamlit app and UI logic
├── pokemon_fetcher.py   # Functions for fetching Pokemon data (Name and Image URL) and hints
├── image_masker.py      # Functions for masking Pokemon images
└── README.md            # This file
```

---

## How it Works

- **main.py**: Handles the Streamlit UI, user input, and game flow.
- **pokemon_fetcher.py**: Fetches Pokemon data from the PokéAPI, manages session state for already-shown Pokemon.
- **image_masker.py**: Masks the Pokemon image to create a silhouette effect, also return the original image.

---

## Credits

- Pokémon data and images from [PokéAPI](https://pokeapi.co/).
- Built with [Streamlit](https://streamlit.io/).
