import streamlit as st
from sqlmodel import SQLModel, create_engine
from models import User, Exam

# ------------------------------------------------------------------
# 1. RECUPERO DELLE CREDENZIALI
# Cerchiamo la password nel file .streamlit/secrets.toml
# ------------------------------------------------------------------
try:
    database_url = st.secrets["DATABASE_URL"]
except Exception:
    # Se non trova i segreti (es. primo avvio senza config), avvisa
    st.error("⚠️ Non ho trovato il file secrets.toml! Controlla la guida.")
    st.stop()

# ------------------------------------------------------------------
# 2. CREAZIONE DEL MOTORE (Engine)
# L'engine è l'oggetto che gestisce effettivamente la connessione al server.
# echo=False -> Non stampa tutte le query SQL nel terminale (più pulito)
# ------------------------------------------------------------------
engine = create_engine(database_url, echo=False)

# ------------------------------------------------------------------
# 3. FUNZIONE DI INIZIALIZZAZIONE
# Questa funzione va chiamata una volta sola all'avvio dell'app.
# Controlla se le tabelle esistono su Supabase. Se no, le crea.
# ------------------------------------------------------------------
def create_db_and_tables():
    # Prende tutti i modelli definiti (User, Exam) e crea le tabelle SQL
    SQLModel.metadata.create_all(engine)

# ------------------------------------------------------------------
# TEST RAPIDO (Solo se lanci questo file direttamente)
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("⏳ Tentativo di connessione al Database...")
    try:
        create_db_and_tables()
        print("✅ Successo! Tabelle create (o già esistenti) su Supabase.")
    except Exception as e:
        print(f"❌ Errore: {e}")