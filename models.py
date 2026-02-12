from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint

# ------------------------------------------------------------------
# MODELLO 1: L'UTENTE (User)
# ------------------------------------------------------------------
class User(SQLModel, table=True, extend_existing=True):
    # ID univoco generato automaticamente dal DB (Primary Key)
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Username: deve essere unico (non possono esserci due "Mario")
    username: str = Field(index=True, unique=True)
    
    # Password: Qui salveremo la versione criptata (hash), non in chiaro!
    password: str 
    
    # RELAZIONE: Un utente può avere MOLTI esami.
    # "back_populates" dice: "Guarda la variabile 'user' nella classe Exam per collegarti"
    exams: List["Exam"] = Relationship(back_populates="user")

    # Questa non è una colonna reale nel DB! 
    # È un "ponte virtuale" di SQLAlchemy. 
    # Ti permette di scrivere user.exams nel codice Python e ottenere automaticamente 
    # la lista di tutti i voti di quell'utente senza scrivere query SQL manuali.

# ------------------------------------------------------------------
# MODELLO 2: L'ESAME (Exam)
# Rappresenta un singolo voto preso.
# ------------------------------------------------------------------
class Exam(SQLModel, table=True, extend_existing=True):
    # Aggiungiamo il vincolo: la combinazione di nome e user_id deve essere unica
    __table_args__ = (UniqueConstraint("name", "user_id", name="unique_subject_user"),)

    # ID univoco dell'esame
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Dati dell'esame
    name: str                   # Nome materia (es. "Analisi 1")
    grade: int                  # Voto (es. 28)
    credits: int                # CFU (es. 9)
    date: datetime              # Data di registrazione (automatica)
    
    # CHIAVE ESTERNA (Foreign Key):
    # Questo campo dice: "A quale utente appartiene questo esame?"
    # Collega questo esame all'ID della tabella User.
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # RELAZIONE INVERSA:
    # Permette di risalire all'oggetto Utente partendo dall'Esame.
    user: Optional[User] = Relationship(back_populates="exams")