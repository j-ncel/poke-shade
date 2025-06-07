import streamlit as st
import random
import time

from pokemon_fetcher import get_pokemon
from image_masker import mask_image


def main():
    st.set_page_config(page_title="PokeShade",
                       page_icon="🔴", layout="centered")

    # Initialize session state for Pokemon
    if "pokemon_name" not in st.session_state:
        try:
            st.session_state.pokemon_img_url, st.session_state.pokemon_name, st.session_state.pokemon_desc = get_pokemon()
        except Exception as e:
            st.error(f"Failed to fetch Pokémon data: {e}")
            st.stop()

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

        h1 {
            font-family: 'Luckiest Guy', cursive;
            text-shadow: -2px -2px 0 blue, 2px -2px 0 blue, -2px 2px 0 blue, 2px 2px 0 blue;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left_space_, center, right_space_ = st.columns([1, 5, 1])

    with center:
        whos_that = st.markdown("<h1 style='font-family: Luckiest Guy; color: gold;'>Who's That Pokémon?</h1>",
                                unsafe_allow_html=True)

        try:
            pokemon_masked_img, pokemon_orig_img = mask_image(
                st.session_state.pokemon_img_url)
        except Exception as e:
            st.error(f"Failed to process Pokémon image: {e}")
            st.stop()
        pokemon_img_placeholder = st.image(pokemon_masked_img, width=500)

    hint_button_col, hint_col = st.columns([1, 5])
    if hint_button_col.button("Show Hint"):
        try:
            hint_col.write(
                f":orange-background[{random.choice(st.session_state.pokemon_desc)}]")
        except Exception:
            hint_col.write(":orange-background[No hint available.]")

    # --- User Guess Form ---
    with st.form(key="pokemon_guess", border=False, clear_on_submit=True, enter_to_submit=False):
        # Text input for user's guess (hidden label for cleaner UI)
        guess = st.text_input(
            "Enter Pokemon name:",
            key="guess",
            placeholder="Guess here",
            label_visibility="hidden",
        )

        submit_button = st.form_submit_button("SUBMIT", type="primary")

    # --- Guess Validation and Feedback ---
    if submit_button and not guess.strip():
        # Warn if input is empty
        st.warning("Please enter your guess.")
    elif submit_button:
        # If guess is correct
        if guess.lower() == st.session_state.pokemon_name.lower():
            st.balloons()
            st.success(
                f"Your guess is correct. It's {guess.title()}")
        else:
            # If guess is incorrect
            st.error(
                f"Your guess is incorrect. It's {st.session_state.pokemon_name.title()}")
        # Reveal the correct Pokemon name and original image
        whos_that.markdown(f"<h1 style='font-family: Luckiest Guy; color: gold;'>{st.session_state.pokemon_name}</h1>",
                           unsafe_allow_html=True)
        pokemon_img_placeholder.image(pokemon_orig_img, width=500)
        time.sleep(1)
        # Remove current Pokemon from session and rerun for a new round
        del st.session_state.pokemon_name
        st.rerun()


if __name__ == "__main__":
    main()
