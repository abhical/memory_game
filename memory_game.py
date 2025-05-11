import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont
import io
import base64

def create_card_face(text, color, size=(120, 120)):
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    border_color = '#2C3E50'
    draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline=border_color, width=2)
    
    # Draw text
    try:
        font = ImageFont.truetype('arial.ttf', 48)
    except:
        font = ImageFont.load_default()
        
    # Center text
    w, h = draw.textbbox((0, 0), text, font=font)[2:]
    draw.text(((size[0]-w)/2, (size[1]-h)/2), text, fill='#2C3E50', font=font)
    
    # Convert to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def initialize_game():
    if 'cards' not in st.session_state:
        st.session_state.cards = list(range(8)) * 2
        random.shuffle(st.session_state.cards)
    if 'flipped' not in st.session_state:
        st.session_state.flipped = []
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'matches' not in st.session_state:
        st.session_state.matches = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

def reset_game():
    st.session_state.cards = list(range(8)) * 2
    random.shuffle(st.session_state.cards)
    st.session_state.flipped = []
    st.session_state.attempts = 0
    st.session_state.matches = 0
    st.session_state.game_over = False

def main():
    st.set_page_config(
        page_title="Memory Game",
        page_icon="🎮",
        layout="centered"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            width: 120px;
            height: 120px;
            padding: 0;
            margin: 2px;
            border: none;
            background-color: #E0E0E0;
        }
        .stButton>button:hover {
            background-color: #D0D0D0;
        }
        .main {
            background-color: #F5F5F5;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize game state
    initialize_game()
    
    # Title
    st.title("Memory Game")
    st.markdown("Find matching pairs of cards!")
    
    # Game stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Attempts", st.session_state.attempts)
    with col2:
        st.metric("Matches", f"{st.session_state.matches}/8")
    
    # Card colors
    colors = [
        '#FFB3BA',  # Soft pink
        '#BAFFC9',  # Soft green
        '#BAE1FF',  # Soft blue
        '#FFFFBA',  # Soft yellow
        '#FFB3FF',  # Soft purple
        '#FFD4B3',  # Soft orange
        '#B3FFE6',  # Soft turquoise
        '#E6B3FF'   # Soft lavender
    ]
    
    # Create game board
    cols = st.columns(4)
    for i in range(16):
        col_idx = i % 4
        with cols[col_idx]:
            if i in st.session_state.flipped:
                # Show card face
                card_value = st.session_state.cards[i]
                card_image = create_card_face(str(card_value + 1), colors[card_value])
                st.image(card_image, use_column_width=True)
            else:
                # Show card back
                card_back = create_card_face("?", "#E0E0E0")
                if st.button("", key=f"card_{i}"):
                    if len(st.session_state.flipped) < 2 and i not in st.session_state.flipped:
                        st.session_state.flipped.append(i)
                        
                        if len(st.session_state.flipped) == 2:
                            st.session_state.attempts += 1
                            idx1, idx2 = st.session_state.flipped
                            if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
                                st.session_state.matches += 1
                                if st.session_state.matches == 8:
                                    st.session_state.game_over = True
                            else:
                                st.session_state.flipped = []
    
    # Game over message
    if st.session_state.game_over:
        st.success(f"🎉 Congratulations! You completed the game in {st.session_state.attempts} attempts!")
        if st.button("Play Again"):
            reset_game()
            st.experimental_rerun()
    
    # Reset button
    if st.button("Reset Game"):
        reset_game()
        st.experimental_rerun()

if __name__ == "__main__":
    main() 