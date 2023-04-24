from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.models import Base, CastMember, Character, Play, Scene, User

if __name__ == "__main__":
    print("Hello World - api")

    DATABASE_URL = "postgresql://postgres:dramatize@db:5432/dramatize"

    engine = create_engine(DATABASE_URL, echo=True)
    meta = Base.metadata
    meta.drop_all(bind=engine)
    meta.create_all(bind=engine)

    with Session(engine) as session:
        play1 = Play(name="TBOM", description="TBOM", performance_dates=[1, 2, 3])
        play2 = Play(name="Primos", description="Primos", performance_dates=[1, 2, 3])
        user1 = User(name="John", age=30)
        session.add_all([play1, play2, user1])
        session.flush()

        director1 = CastMember(roles=["DIRECTOR"], user_id=user1.id, play_id=play1.id)
        actor1 = CastMember(user_id=user1.id, play_id=play2.id)
        actor_fake = CastMember(user_id=user1.id, play_id=play2.id)
        session.add_all([director1, actor1, actor_fake])
        session.flush()

        ch1 = Character(name="John", play_id=play1.id)
        ch2 = Character(name="Mary", play_id=play1.id)
        ch3 = Character(name="Felix", play_id=play1.id)
        session.add_all([ch1, ch2, ch3])
        session.flush()

        scene1 = Scene(name="Scene 1", play_id=play1.id, characters=[ch1, ch2])
        scene2 = Scene(name="Scene 2", play_id=play1.id, characters=[ch2, ch3])
        session.add_all([scene1, scene2])
        session.commit()
        print("#### Created successfully ####")
