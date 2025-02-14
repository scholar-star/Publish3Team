from sqlmodel import Session, create_engine, select, SQLModel

db_file_name="blog.db"
db_url = f"sqlite:///{db_file_name}"
db_conn_args = {"check_same_thread": False}
db_engine = create_engine(db_url, connect_args=db_conn_args)

def get_db_session():
    with Session(db_engine) as session:
        yield session
    # db 생성

def create_db_and_tables():
    #print("생성될 테이블 목록:", SQLModel.metadata.tables.keys())
    SQLModel.metadata.create_all(db_engine)
