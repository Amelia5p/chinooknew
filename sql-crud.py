from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select  # For SQLAlchemy 2.0 query syntax

# Suppress SQLAlchemy 2.0 warning (if you intend to use SQLAlchemy 1.x)
import os
os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"  # This silences the deprecation warning

# Database connection URL
db = create_engine("postgresql:///chinook")

# Declare the base class for our model
Base = declarative_base()


# Create a class-based model for the "Programmer" table
class Programmer(Base):
    __tablename__ = "Programmer"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    nationality = Column(String)
    famous_for = Column(String)


# Session setup (with future=True to enable 2.0 behavior)
Session = sessionmaker(db, future=True)

# Create all tables in the database (if not already created)
Base.metadata.create_all(db)


# Create some Programmer instances
ada_lovelace = Programmer(
    first_name="Ada",
    last_name="Lovelace",
    gender="F",
    nationality="British",
    famous_for="First Programmer"
)

alan_turing = Programmer(
    first_name="Alan",
    last_name="Turing",
    gender="M",
    nationality="British",
    famous_for="Modern Computing"
)

grace_hopper = Programmer(
    first_name="Grace",
    last_name="Hopper",
    gender="F",
    nationality="American",
    famous_for="COBOL language"
)

margaret_hamilton = Programmer(
    first_name="Margaret",
    last_name="Hamilton",
    gender="F",
    nationality="American",
    famous_for="Apollo 11"
)

bill_gates = Programmer(
    first_name="Bill",
    last_name="Gates",
    gender="M",
    nationality="American",
    famous_for="Microsoft"
)

tim_berners_lee = Programmer(
    first_name="Tim",
    last_name="Berners-Lee",
    gender="M",
    nationality="British",
    famous_for="World Wide Web"
)

millie_service = Programmer(
    first_name="Millie",
    last_name="Service",
    gender="F",
    nationality="Irish",
    famous_for="Hi"
)


# Add programmers to the session and commit (using a context manager for the session)
with Session() as session:
    # Add each programmer to the session
    session.add_all([
        ada_lovelace, alan_turing, grace_hopper, margaret_hamilton, 
        bill_gates, tim_berners_lee, millie_service
    ])

    # Commit to persist the changes
    session.commit()


# Querying the database to find all programmers
with Session() as session:
    stmt = select(Programmer)  # Create the query
    results = session.execute(stmt).scalars().all()  # Execute and fetch results
    
    # Display the results
    for programmer in results:
        print(
            programmer.id,
            f"{programmer.first_name} {programmer.last_name}",
            programmer.gender,
            programmer.nationality,
            programmer.famous_for,
            sep=" | "
        )
