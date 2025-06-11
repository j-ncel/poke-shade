import streamlit as st
import random
import time

from pokemon_fetcher import get_pokemon
from image_masker import mask_image


def main():
    st.set_page_config(page_title="PokeShade",
                       page_icon="🔴", layout="wide")

    # Initialize session state for Pokemon
    if "pokemon_name" not in st.session_state:
        st.session_state.pokemon_img_url, st.session_state.pokemon_name, st.session_state.pokemon_desc = get_pokemon()

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

        h2 {
            font-family: 'Luckiest Guy', cursive;
            text-shadow: -2px -2px 0 white, 2px -2px 0 white, -2px 2px 0 white, 2px 2px 0 white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns(3)
    with center_col:
        with st.container(border=True):
            _, center_col, _ = st.columns([1, 8, 1])
            with center_col:
                whos_that = st.markdown("<h2 style='font-family: Luckiest Guy; color: #4E92CF;'>Who's That Pokémon?</h2>",
                                        unsafe_allow_html=True)
                pokemon_masked_img, pokemon_orig_img = mask_image(
                    st.session_state.pokemon_img_url)
                pokemon_img_placeholder = st.image(
                    pokemon_masked_img, width=500)

            result_placeholder = st.empty()
            hint_button_col, hint_col = st.columns([1, 4.5])
            hint_button = hint_button_col.button("Show Hint")
            if hint_button:
                try:
                    hint_col.info(random.choice(st.session_state.pokemon_desc))
                except Exception:
                    hint_col.error(":orange-background[No hint available.]")

            # --- User Guess Form ---
            with st.form(key="pokemon_guess", border=False, clear_on_submit=True, enter_to_submit=False):
                # Text input for user's guess (hidden label for cleaner UI)
                guess = st.text_input(
                    "Enter Pokemon name:",
                    key="guess",
                    placeholder="Guess here",
                    label_visibility="collapsed",
                    autocomplete="off"
                )
                submit_button = st.form_submit_button("SUBMIT", type="primary")

            # --- Guess Validation and Feedback ---
            if submit_button and not guess.strip():
                result_placeholder.warning("Please enter your guess.")
            elif submit_button:
                # If guess is correct
                if guess.lower() == st.session_state.pokemon_name.lower():
                    st.balloons()
                    result_placeholder.success(
                        f"Your guess is correct. It's {guess.title()}")
                else:
                    # If guess is incorrect
                    result_placeholder.error(
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
