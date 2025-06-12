import streamlit as st
import random
import time

from pokemon_fetcher import get_pokemon
from pokemon_fetcher import get_all_pokemon_names
from image_masker import mask_image


def main():
    st.set_page_config(page_title="PokeShade",
                       page_icon="🔴", layout="wide")

    # Initialize session state for Pokemon
    if "pokemon_name" not in st.session_state:
        st.session_state.pokemon_img_url, st.session_state.pokemon_name, st.session_state.pokemon_desc = get_pokemon()
        pokemon_samples = st.session_state.all_pokemon_names
        pokemon_samples.remove(st.session_state.pokemon_name)
        st.session_state.wrong_choices = random.sample(pokemon_samples, 3)
        st.session_state.guessed = False

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

    _, center_col, _, right_col, _ = st.columns([1, 2, .1, 2, 1])

    with right_col:
        st.markdown("<h3 style='font-family: Luckiest Guy; color: #4E92CF;'>Guessed Pokemon</h3>",
                    unsafe_allow_html=True)

        if "correct_count" not in st.session_state:
            st.session_state.correct_count = 0
        if "incorrect_count" not in st.session_state:
            st.session_state.incorrect_count = 0

        correct_count = st.session_state.correct_count
        incorrect_count = st.session_state.incorrect_count
        total_count = 1 if correct_count + \
            incorrect_count == 0 else correct_count + incorrect_count
        col1, col2, col3 = st.columns(3)
        col1.metric("Correct Guess",
                    correct_count, border=True)
        col2.metric("Incorrect Guess",
                    incorrect_count, border=True)
        col3.metric("Correct Guess Rate",
                    (f"{round((st.session_state.correct_count / (total_count)) * 100, 2)}%"), border=True)

        guessed_pokemon = st.session_state.get("given_pokemons", [])
        cols = st.columns(3)
        for idx, pokemon in enumerate(guessed_pokemon):

            pokemon_name = pokemon["name"]
            pokemon_img_url = pokemon["img_url"]

            # Apply masking logic
            pokemon_masked_img, pokemon_orig_img = mask_image(pokemon_img_url)

            # Assign each Pokémon to the correct column
            with cols[idx % 3]:
                st.write(pokemon_name.title() if st.session_state.pokemon_name !=
                         pokemon_name else "? " * len(pokemon_name))
                st.image(pokemon_orig_img if st.session_state.pokemon_name !=
                         pokemon_name else pokemon_masked_img, width=80)

    with center_col:
        with st.container(border=True):
            _, center_col, _ = st.columns([1, 10, 1])
            with center_col:
                whos_that = st.markdown("<h2 style='font-family: Luckiest Guy; color: #4E92CF;'>Who's That Pokémon?</h2>",
                                        unsafe_allow_html=True)
                pokemon_masked_img, pokemon_orig_img = mask_image(
                    st.session_state.pokemon_img_url)
                pokemon_img_placeholder = st.image(
                    pokemon_masked_img, width=500)

            result_placeholder = st.empty()
            with st.form("hint_form", border=False):
                hint_button_col, hint_col = st.columns([1, 4])
                hint_button = hint_button_col.form_submit_button("Show Hint")
            if hint_button:
                try:
                    hint_col.info(random.choice(st.session_state.pokemon_desc))
                except Exception:
                    hint_col.error(":orange-background[No hint available.]")

            # Custom CSS for button styling
            st.markdown("""
            <style>
            div.stButton > button {
                background-color: #4E92CF;
                width: 150px;
                color: white; 
                font-size: 14px;
                font-weight: bold;
                padding: 10px 10px;
                border-radius: 10px;
                border: none;
                cursor: pointer;
                display: block;
                margin: 0 auto; /* Centers the button */
            }
            div.stButton > button:hover {
                background-color: #3572A5;
                color: white;   
            }
            div.stButton > button:active {
                background-color: transparent;
                color: white !important;
            }
            div.stButton > button:focus {
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)

            # --- Multiple Choice ---
            wrong_choices = st.session_state.wrong_choices

            choices = [wrong_choices[0],
                       wrong_choices[1],
                       wrong_choices[2],
                       pokemon_name]
            random.shuffle(choices)
            cols = st.columns(2)
            with cols[0]:  # Left column
                if st.button(choices[0].title()):
                    if not st.session_state.get("guessed", False):
                        check_answer(choices[0], result_placeholder, whos_that,
                                     pokemon_img_placeholder, pokemon_orig_img)
                if st.button(choices[1].title()):
                    if not st.session_state.get("guessed", False):
                        check_answer(choices[1], result_placeholder, whos_that,
                                     pokemon_img_placeholder, pokemon_orig_img)

            with cols[1]:  # Right column
                if st.button(choices[2].title()):
                    if not st.session_state.get("guessed", False):
                        check_answer(choices[2], result_placeholder, whos_that,
                                     pokemon_img_placeholder, pokemon_orig_img)
                if st.button(choices[3].title()):
                    if not st.session_state.get("guessed", False):
                        check_answer(choices[3], result_placeholder, whos_that,
                                     pokemon_img_placeholder, pokemon_orig_img)


def check_answer(guess, result_placeholder, whos_that, pokemon_img_placeholder, pokemon_orig_img):
    st.session_state.guessed = True
    # If guess is correct
    if guess.lower() == st.session_state.pokemon_name.lower():
        st.session_state.correct_count += 1
        st.balloons()
        result_placeholder.success(
            f"Your guess is correct. It's {guess.title()}")
    else:
        # If guess is incorrect
        st.session_state.incorrect_count += 1
        result_placeholder.error(
            f"Your guess is incorrect. It's {st.session_state.pokemon_name.title()}")
    # Reveal the correct Pokemon name and original image
    whos_that.markdown(f"<h1 style='font-family: Luckiest Guy; color: gold;'>{st.session_state.pokemon_name}</h1>",
                       unsafe_allow_html=True)
    pokemon_img_placeholder.image(pokemon_orig_img, width=500)
    # Remove current Pokemon from session and rerun for a new round
    del st.session_state.pokemon_name
    time.sleep(1)
    st.rerun()


if __name__ == "__main__":
    main()
