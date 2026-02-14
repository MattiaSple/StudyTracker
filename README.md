# StudyTracker

## Descrizione in italiano

**Cosa fa StudyTracker**:
Il progetto è un'applicazione Web (sviluppata con Streamlit) per studenti, che funge da "libretto universitario virtuale". Ti permette di:
1. Registrare nuovi esami con dettagli come nome, voto, CFU e data.
2. Visualizzare le statistiche accademiche, come la media aritmetica, media ponderata e CFU totali.
3. Simulare come un futuro esame influirà sui tuoi voti.
4. Generare grafici e tabelle per l'andamento dei tuoi esami.

**Funzioni principali**:
- **Login e Registrazione**: Include autenticazione per l’accesso sicuro.
- **Dashboard**: Mostra dati accademici e opzioni per aggiungere/rimuovere esami.
- **Simulatore Numerico**: Calcola proiezioni basate su ipotetici CFU e voti futuri.

### Istruzioni su come utilizzare StudyTracker

1. **Requisiti Minimi**:
   - Python installato (>= 3.7)
   - Streamlit (`pip install streamlit`)
   - Altre dipendenze del progetto (potrebbero essere aggiunte in un file `requirements.txt`).

2. **Clona il progetto sul tuo PC**:
```bash
git clone https://github.com/MattiaSple/StudyTracker.git
cd StudyTracker
```

3. **Configurazione del Database**:
   - Il progetto richiede un database compatibile con SQLModel (ad esempio di Supabase). Configura l'URL nel file `.streamlit/secrets.toml`.

4. **Avvio del server**:
   - Lancia l'app con Streamlit:
```bash
streamlit run app.py
```

5. **Usa l'applicazione**:
   - Apri il browser all’indirizzo fornito da Streamlit (esempio: `http://localhost:8501`).
   - Registrati per creare un account, fai il login e inizia a tracciare i tuoi esami.

---

## Description in English

**What StudyTracker Does**:
StudyTracker is a web application (built with Streamlit) intended for students as a "virtual university transcript". It allows you to:
1. Log new exams with details such as name, grade, credits, and date.
2. View academic statistics, such as arithmetic and weighted averages as well as total credits.
3. Simulate how a future exam will affect your scores.
4. Generate charts and tables tracking your exam progress.

**Key Features**:
- **Login and Registration**: Secure authentication for accessing your personal data.
- **Dashboard**: Displays academic stats and options to add/remove exams.
- **Numeric Simulator**: Calculates projections based on hypothetical grades and credits.

### Instructions for Using StudyTracker

1. **Minimum Requirements**:
   - Installed Python (>= 3.7)
   - Streamlit (`pip install streamlit`)
   - Other dependencies in a `requirements.txt` file may be needed.

2. **Clone the Project to Your PC**:
```bash
git clone https://github.com/MattiaSple/StudyTracker.git
cd StudyTracker
```

3. **Configure the Database**:
   - The project requires a database compatible with SQLModel (e.g., Supabase). Configure the URL in the `.streamlit/secrets.toml` file.

4. **Run the Server**:
   - Use Streamlit Launch:
```bash
streamlit run app.py
```

5. **Use the Application**:
   - Open your browser to the address provided by Streamlit (e.g., `http://localhost:8501`).
   - Register an account, log in, and start tracking your exams.