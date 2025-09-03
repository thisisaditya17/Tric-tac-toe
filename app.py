import streamlit as st
from game_logic import TricTacToe
from ai_player import TricTacToeAI

# Session state setup
if "game" not in st.session_state:
    st.session_state.game = TricTacToe()
if "ai" not in st.session_state:
    st.session_state.ai = TricTacToeAI(depth=7)
if "message" not in st.session_state:
    st.session_state.message = "Your turn (X)."

game = st.session_state.game
ai = st.session_state.ai

def get_symbol(value):
    return "❌" if value == 1 else ("⭕" if value == -1 else "")

def reset_game():
    st.session_state.game = TricTacToe()
    st.session_state.message = "Your turn (X)."

def handle_move(pos):
    if game.game_over:
        return
    
    if game.make_move(pos):
        if game.game_over:
            st.session_state.message = "You win! 🎉" if game.winner == 1 else "AI wins! 🤖"
        else:
            ai_move = ai.get_move(game)
            if ai_move is not None:
                game.make_move(ai_move)
                if game.game_over:
                    st.session_state.message = "AI wins! 🤖"
                else:
                    st.session_state.message = "Your turn (X)."
        st.rerun() 
    else:
        st.session_state.message = "Invalid move. Try again."
        st.rerun()  

# Page title
st.markdown(
    "<h1 style='text-align: center; font-size: 4em;'>🎮 TricTacToe</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; font-size: 3em;'>Game Instructions</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; font-size: 2em;'> You (❌) vs 🤖 AI (⭕). After 6 moves, the oldest move is removed!</h3>",
    unsafe_allow_html=True
)

# Inject CSS for square buttons
st.markdown(
    """
    <style>
    div[data-testid="stButton"] button {
        height: 100px;
        width: 100px;
        font-size: 100px;
        border-radius: 15px;
        margin: 5px;
        background-color: #f8f9fa;
        border: 2px solid #ccc;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #e3e3e3;
        border-color: #666;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Game status
st.subheader(st.session_state.message)

# Game board layout (3x3 grid)
rows = [st.columns(3) for _ in range(3)]
for i in range(9):
    with rows[i // 3][i % 3]:
        button_label = get_symbol(game.board[i]) or " "
        if st.button(button_label, key=f"btn_{i}"):
            handle_move(i)

st.markdown(
    f"<h4 style='text-align: center; font-size: 2em;'>Moves until first removal: {game.moves_until_removal()}</h4>",
    unsafe_allow_html=True
)

# Reset button
cols = st.columns([1.5, 2, 1])
with cols[1]:
    st.button("New Game", on_click=reset_game)

