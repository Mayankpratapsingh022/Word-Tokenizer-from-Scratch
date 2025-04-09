import streamlit as st
import re
import random

st.set_page_config(page_title="Simple Tokenizer App", layout="wide")

# Title
st.title("Tokenizer Playground")

# Dropdown for tokenizer type
tokenizer_type = st.selectbox("Select Tokenizer Type", ["Word-based", "Character-based"])

# User text input
text_input = st.text_area("Enter your text here:", height=150, value="Hello! I'm learning LLMs.")

# Special tokens
special_tokens = ["<start>", "<end-of-sequence>"]

# Tokenization logic
def word_tokenizer(text):
    tokens = re.findall(r"\b\w+(?:'\w+)?\b|[^\w\s]", text.lower())
    return special_tokens[:1] + tokens + special_tokens[1:]

def char_tokenizer(text):
    return special_tokens[:1] + list(text) + special_tokens[1:]

# Assign unique token IDs
def assign_token_ids(tokens):
    vocab = {}
    token_ids = []
    next_id = 100  # Start from 100 for cleaner visualization

    for token in tokens:
        if token not in vocab:
            vocab[token] = next_id
            next_id += 1
        token_ids.append(vocab[token])
    return token_ids, vocab

# Tokenize
tokens = word_tokenizer(text_input) if tokenizer_type == "Word-based" else char_tokenizer(text_input)
token_ids, vocab = assign_token_ids(tokens)

# Display token count
st.markdown(f"###  Token Count: `{len(tokens)}`")
# Custom color palette
color_palette = [
    "#8ecae6", "#f2e8cf", "#e9ff70", "#edddd4", "#ffa5ab", 
    "#e0b1cb", "#a2d6f9", "#73e2a7", "#fe6d73", "#ffff3f", "#a594f9"
]

# Display colored tokens using custom palette
st.markdown("### Tokens")
colored_html = ""
for i, token in enumerate(tokens):
    color = color_palette[i % len(color_palette)]  # Cycle through colors
    colored_html += f"""
    <span style='
        background-color:{color};
        color:black;
        padding:1px 4px;
        font-size:15px;
        margin:2px;
        display:inline-block;
    '> {token} </span>"""
st.markdown(colored_html, unsafe_allow_html=True)


# Display token IDs
st.markdown("### Token IDs")
text_color = "white"
bg_color = "#1e1e1e"

# Format the token IDs like code
token_id_html = f"""
<div style='
    background-color:{bg_color};
    color:{text_color};
    padding:10px;
    font-size:15px;
    font-family:monospace;
'>
{token_ids}
</div>
"""

st.markdown(token_id_html, unsafe_allow_html=True)

# Optional: show vocab mapping
with st.expander(" View Vocab Dictionary"):
    st.json(vocab)
