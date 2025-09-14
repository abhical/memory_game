import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import time

def create_card_face(text, color, size=(120, 120)):
    try:
        img = Image.new('RGB', size, color)
        draw = ImageDraw.Draw(img)
        
        # Draw border
        border_color = '#2C3E50'
        draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline=border_color, width=2)
        
        # Draw text
        try:
            font = ImageFont.truetype('arial.ttf', 48)
        except:
            # Fallback to default font if arial.ttf is not available
            font = ImageFont.load_default()
            
        # Center text
        w, h = draw.textbbox((0, 0), text, font=font)[2:]
        draw.text(((size[0]-w)/2, (size[1]-h)/2), text, fill='#2C3E50', font=font)
        
        # Convert to base64 for display
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        st.error(f"Error creating card: {str(e)}")
        return None

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
    if 'matched_cards' not in st.session_state:
        st.session_state.matched_cards = set()

def reset_game():
    st.session_state.cards = list(range(8)) * 2
    random.shuffle(st.session_state.cards)
    st.session_state.flipped = []
    st.session_state.attempts = 0
    st.session_state.matches = 0
    st.session_state.game_over = False
    st.session_state.matched_cards = set()

def main():
    st.set_page_config(
        page_title="Memory Game",
        page_icon="🎮",
        layout="centered",
        initial_sidebar_state="collapsed"
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
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #D0D0D0;
            transform: scale(1.05);
        }
        .main {
            background-color: #F5F5F5;
        }
        .stSuccess {
            background-color: #2ECC71;
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        div[data-testid="stImage"] {
            width: 120px;
            height: 120px;
            margin: 0 auto;
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
            if i in st.session_state.matched_cards or i in st.session_state.flipped:
                # Show card face
                card_value = st.session_state.cards[i]
                card_image = create_card_face(str(card_value + 1), colors[card_value])
                if card_image:
                    st.image(card_image, use_container_width=True)
            else:
                # Show card back
                card_back = create_card_face("?", "#E0E0E0")
                if card_back:
                    if st.button("", key=f"card_{i}"):
                        if len(st.session_state.flipped) < 2 and i not in st.session_state.flipped and i not in st.session_state.matched_cards:
                            st.session_state.flipped.append(i)
                            
                            if len(st.session_state.flipped) == 2:
                                st.session_state.attempts += 1
                                idx1, idx2 = st.session_state.flipped
                                
                                if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
                                    # Match found
                                    st.session_state.matches += 1
                                    st.session_state.matched_cards.update([idx1, idx2])
                                    st.session_state.flipped = []
                                    
                                    if st.session_state.matches == 8:
                                        st.session_state.game_over = True
                                else:
                                    # No match, flip cards back after a delay
                                    time.sleep(1)
                                    st.session_state.flipped = []
                                
                                st.rerun()
    
    # Game over message
    if st.session_state.game_over:
        st.success(f"🎉 Congratulations! You completed the game in {st.session_state.attempts} attempts!")
        if st.button("Play Again"):
            reset_game()
            st.rerun()
    
    # Reset button
    if st.button("Reset Game"):
        reset_game()
        st.rerun()

if __name__ == "__main__":
    main() 