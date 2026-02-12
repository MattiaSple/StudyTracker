from sqlmodel import Session, select
from database import engine
from models import User, Exam
from datetime import datetime

# --- OPERAZIONI UTENTE ---

def create_user(username, hashed_password):
    """Salva fisicamente il nuovo utente nel DB."""
    new_user = User(username=username, password=hashed_password)
    with Session(engine) as session:
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except Exception:
            session.rollback()
            return None

def get_user_by_username(username):
    """Recupera l'utente per il controllo login."""
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

# --- OPERAZIONI ESAMI ---

def create_exam(user_id: int, name: str, grade: int, credits: int, date: datetime):
    """Crea un record esame collegato all'utente."""
    with Session(engine) as session:
        exam = Exam(
            name=name, 
            grade=grade, 
            credits=credits, 
            date=date, 
            user_id=user_id
        )
        session.add(exam)
        session.commit()
        session.refresh(exam)
        return exam

def get_exams_by_user(user_id: int):
    """Prende tutti gli esami dell'utente."""
    with Session(engine) as session:
        statement = select(Exam).where(Exam.user_id == user_id)
        return session.exec(statement).all()

def delete_exam(exam_id: int):
    """Elimina un esame specifico."""
    with Session(engine) as session:
        exam = session.get(Exam, exam_id)
        if exam:
            session.delete(exam)
            session.commit()
            return True
        return False