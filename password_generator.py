import random
import string
import streamlit as st
import pyperclip
import os

# === Funzione: Genera password ===
def generate_password(length=12):
    excluded_chars = {'"', "'", '\\', '`', ' ', '/', '<', '>', '|', '&', 'O', '0', 'I', 'l'}
    
    letters = [c for c in string.ascii_letters if c not in excluded_chars]
    digits = [c for c in string.digits if c not in excluded_chars]
    symbols = [c for c in string.punctuation if c not in excluded_chars]

    # Assicura almeno un carattere per tipo
    password = [
        random.choice([c for c in letters if c.islower()]),
        random.choice([c for c in letters if c.isupper()]),
        random.choice(digits),
        random.choice(symbols)
    ]

    all_chars = letters + digits + symbols
    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    
    return ''.join(password)

# === Funzione: Valuta forza password ===
def check_strength(password):
    score = sum([
        len(password) >= 12,
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])
    
    if score <= 2:
        return "🔴 Weak"
    elif score == 3:
        return "🟠 Medium"
    else:
        return "🟢 Strong"

# === UI Streamlit ===
st.title("🔐 Password Generator")
length = st.slider("Choose password length:", 8, 32, 14)

# Inizializza stato
if 'password' not in st.session_state:
    st.session_state.password = ""

# Generazione
if st.button("Generate Password"):
    st.session_state.password = generate_password(length)

# Mostra risultato
if st.session_state.password:
    password = st.session_state.password
    st.code(password)
    st.write("💡 Password strength:", check_strength(password))

    if st.button("📋 Copy to clipboard"):
        pyperclip.copy(password)
        st.success("Password copied to clipboard!")

# === Chiusura App ===
st.markdown("---")
if st.button("❌ Close App"):
    st.warning("Closing application...")
    os._exit(0)
