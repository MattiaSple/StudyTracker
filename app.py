import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from auth import signup, login
from crud import create_exam, get_exams_by_user, delete_exam

# ------------------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------
st.set_page_config(page_title="Study Tracker", page_icon="🎓", layout="wide")

# ------------------------------------------------------------------
# 2. GESTIONE SESSIONE (Lo "Stato" dell'app)
# Streamlit resetta le variabili a ogni refresh. st.session_state no.
# Qui salviamo se l'utente è loggato.
# ------------------------------------------------------------------
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
    st.session_state["username"] = None

# ==================================================================
# FUNZIONI DI INTERFACCIA (UI Components)
# ==================================================================

def show_login_page():
    """Gestisce la schermata di ingresso (Login/Registrazione)."""
    st.title("🔐 Study Tracker")
    st.write("Il tuo libretto universitario nel cloud.")
    
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    
    # --- TAB LOGIN ---
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Entra")
            
            if submitted:
                # Usiamo la nuova funzione login() di auth.py
                user = login(username, password)
                
                if user:
                    st.session_state["user_id"] = user.id
                    st.session_state["username"] = user.username
                    st.success(f"Bentornato {user.username}!")
                    st.rerun()
                else:
                    st.error("Credenziali non valide.")

    # --- TAB REGISTRAZIONE ---
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Scegli Username")
            new_pass = st.text_input("Scegli Password", type="password")
            confirm_pass = st.text_input("Conferma Password", type="password")
            submitted = st.form_submit_button("Crea Account")
            
            if submitted:
                if new_pass != confirm_pass:
                    st.error("Le password non coincidono.")
                elif len(new_pass) < 4:
                    st.error("Scegli una password più lunga (min 4 caratteri).")
                else:
                    # Usiamo la funzione signup() di auth.py
                    user = signup(new_user, new_pass)
                    if user:
                        st.success("Account creato con successo! Ora puoi accedere.")
                    else:
                        st.error("Errore: lo username potrebbe essere già occupato.")

def show_dashboard():
    """La schermata principale con grafici e dati."""
    
    # --- SIDEBAR (Input Dati) ---
    with st.sidebar:
        st.write(f"👤 Ciao, **{st.session_state['username']}**")
        if st.button("Esci (Logout)"):
            st.session_state["user_id"] = None
            st.rerun()
            
        st.divider()
        st.header("➕ Nuovo Esame")
        
        with st.form("add_exam"):
            nome = st.text_input("Materia (es. Analisi 1)")
            voto = st.number_input("Voto", 18, 31, 24, help="Usa 31 per la Lode")
            cfu = st.number_input("CFU", 1, 30, 6)
            data_esame = st.date_input("Data Verbalizzazione", datetime.today())
            
            if st.form_submit_button("Salva"):
                if nome:
                    try:
                        # Proviamo a creare l'esame
                        create_exam(st.session_state["user_id"], nome, voto, cfu, data_esame)
                        st.success(f"Esame di {nome} salvato!")
                        st.rerun()
                    except Exception:
                        # Se il DB blocca il duplicato, entriamo qui
                        st.error(f"Hai già inserito un voto per '{nome}'. Modifica quello esistente o usa un nome diverso.")
                else:
                    st.warning("Inserisci il nome della materia.")

    # --- AREA PRINCIPALE (Output Dati) ---
    st.title("📊 La tua Carriera")

    # 1. Scarichiamo i dati dal DB
    exams = get_exams_by_user(st.session_state["user_id"])
    
    if not exams:
        st.info("👋 Benvenuto! Inizia aggiungendo il tuo primo esame dalla barra laterale.")
        return

    # 2. Creiamo il DataFrame (Tabella Excel in memoria)
    # Convertiamo la lista di oggetti DB in un formato facile per i grafici
    df = pd.DataFrame([{
        "ID": e.id,
        "Materia": e.name, 
        "Voto": e.grade, 
        "CFU": e.credits, 
        "Data": e.date
    } for e in exams])

    # 3. Calcolo KPI (Indicatori Chiave)
    # Gestione Lode: per la media il 31 vale 30
    df["Voto_Calcolo"] = df["Voto"].apply(lambda x: 30 if x > 30 else x)
    
    media_aritmetica = df["Voto_Calcolo"].mean()
    # Formula Media Ponderata: Σ(voto*cfu) / Σ(cfu)
    media_ponderata = (df["Voto_Calcolo"] * df["CFU"]).sum() / df["CFU"].sum()
    base_laurea = (media_ponderata * 110) / 30
    cfu_totali = df["CFU"].sum()

    # Mostriamo le metriche in 4 colonne
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Media Aritmetica", f"{media_aritmetica:.2f}")
    kpi2.metric("Media Ponderata", f"{media_ponderata:.2f}")
    kpi3.metric("Proiezione Laurea", f"{base_laurea:.1f}")
    kpi4.metric("CFU Acquisiti", cfu_totali)

    st.divider()

    # 4. Grafici e Tabelle
    tab_chart, tab_data = st.tabs(["📈 Analisi Grafica", "📝 Libretto"])

    with tab_chart:
        # Grafico Temporale
        # Converti a datetime e ordina in modo crescente (cronologico)
        df['Data'] = pd.to_datetime(df['Data'])
        df_sorted = df.sort_values("Data", ascending=True).reset_index(drop=True)
        fig = px.line(df_sorted, x="Data", y="Voto", markers=True, title="Andamento Voti")
        # Aggiunge una linea rossa tratteggiata per la media
        fig.add_hline(y=media_ponderata, line_dash="dash", line_color="red", annotation_text="Media")
        st.plotly_chart(fig, use_container_width=True)

    with tab_data:
        # Mostriamo la tabella pulita (senza ID e colonne di calcolo)
        st.dataframe(df[["Materia", "Voto", "CFU", "Data"]], use_container_width=True)
        
        # Sezione Cancellazione
        st.subheader("Gestione")
        exam_to_delete = st.selectbox("Seleziona un esame da eliminare:", df["Materia"].tolist())
        if st.button("🗑️ Elimina Esame"):
            # Recuperiamo l'ID nascosto corrispondente al nome
            raw_id = df[df["Materia"] == exam_to_delete]["ID"].values[0]
            exam_id = int(raw_id)
            delete_exam(exam_id)
            st.warning("Esame eliminato.")
            st.rerun()

    show_numeric_simulator(df, media_aritmetica, media_ponderata, cfu_totali)

def show_numeric_simulator(df, media_aritmetica, media_ponderata, cfu_totali):
    st.divider()
    st.header("🔢 Tabella voto esame futuro")
    st.write("Analisi dell'impatto del prossimo esame sui tuoi indicatori correnti.")

    voti_simulazione = list(range(18, 32)) # Mettiamo 32 per includere il 31 (Lode)
    rows = []

    for v in voti_simulazione:
        # Per la media, la lode (31) conta come 30
        v_effettivo = 30 if v == 31 else v
        
        # --- IPOTESI 6 CFU ---
        nuova_pond_6 = ((media_ponderata * cfu_totali) + (v_effettivo * 6)) / (cfu_totali + 6)
        
        # --- IPOTESI 9 CFU ---
        nuova_pond_9 = ((media_ponderata * cfu_totali) + (v_effettivo * 9)) / (cfu_totali + 9)
        
        rows.append({
            "Voto Futuro": "30L" if v == 31 else str(v),
            "Media Ponderata (6CFU)": round(nuova_pond_6, 2),
            "Media Ponderata (9CFU)": round(nuova_pond_9, 2)
        })

    sim_df = pd.DataFrame(rows)
    
    # Formatta tutti i numeri con 2 decimali
    formato = {col: "{:.2f}" for col in sim_df.columns if col != "Voto Futuro"}
    
    st.dataframe(
        sim_df.style.format(formato)
                   .highlight_max(axis=0, color="#0e1117")
                   .highlight_min(axis=0, color="#0e1117"),
        use_container_width=True,
        hide_index=True
    )


# ==================================================================
# MAIN (Il semaforo)
# ==================================================================
if st.session_state["user_id"]:
    show_dashboard()
else:
    show_login_page()