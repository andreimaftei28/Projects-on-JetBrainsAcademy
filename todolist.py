"""Program creates a to-do-list and stores data into a database
using sqlalchemy module"""

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

#  create database engine
todo = input("Enter your name:\n").lower()
engine = create_engine(f"sqlite:///{todo}.db?check_same_thread=False")

Base = declarative_base()


class Table(Base):
    """Initiating table"""
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String(32), default="task")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}"


#  creating database table
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

session = Session()


def today_tasks():
    """function prints to-do tasks on the current day"""
    today = datetime.today()
    tasks = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(tasks) == 0:
        print(f"\nToday: {today.day} {today.strftime('%b')}:")
        print("Nothing to do!\n")
    else:
        print(f"Today: {today.day} {today.strftime('%b')}")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task}")
        print()


def week_tasks():
    """function used to print to-do tasks on a week time from the current date"""
    weeks_day = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
                 4: "Friday", 5: "Saturday", 6: "Sunday"}
    today = datetime.today()
    week = [today.date() + timedelta(days=x) for x in range(7)]
    for dato in week:
        tasks = session.query(Table).filter(Table.deadline == dato).all()
        print(f"\n{weeks_day[dato.weekday()]} {dato.day} {dato.strftime('%b')}:")
        if len(tasks) == 0:
            print("Nothing to do!\n")
        else:
            for i, task in enumerate(tasks):
                print(f"{i + 1}. {task}")


def all_tasks():
    """function is used to print all to-do tasks from database ordered by date"""
    tasks = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")
    print()


def missed_tasks():
    """function is used to print all to-do tasks older then current date"""
    today = datetime.today()
    m_tasks = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
    if len(m_tasks) == 0:
        print("Nothing is missed!\n")
    else:
        print("Missed tasks:")
        for i, m_task in enumerate(m_tasks):
            print(f"{i + 1}. {m_task}. {m_task.deadline.day} {m_task.deadline.strftime('%b')}")
        print()


def delete_task():
    """function is used to delete a to-do task older then the current date"""
    today = datetime.today()
    d_tasks = session.query(Table).filter(Table.deadline <= today.date()).order_by(Table.deadline).all()
    if len(d_tasks) == 0:
        print("Nothing to delete!\n")
    else:
        print("Choose the number of the task you want to delete:")
        for i, d_task in enumerate(d_tasks):
            print(f"{i + 1}. {d_task}. {d_task.deadline.day} {d_task.deadline.strftime('%b')}")
        to_delete = int(input())
        session.delete(d_tasks[to_delete - 1])
        session.commit()
        print("The task has been deleted!\n")


def add_task():
    """function is used to add a to-do task to database"""
    task = Table()
    task.task = input("\nEnter task\n")
    deadline = input("Enter deadline\n")
    task.deadline = datetime.strptime(deadline, "%Y-%m-%d")
    session.add(task)
    session.commit()
    print("The task has been added\n")


def main():
    """function prints a menu and performs tasks according to user input"""
    while True:
        message = input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n""")
        if message == "1":
            today_tasks()
        elif message == "2":
            week_tasks()
        elif message == "3":
            all_tasks()
        elif message == "4":
            missed_tasks()
        elif message == "5":
            add_task()
        elif message == "6":
            delete_task()
        elif message == "0":
            print("\nBye!")
            break
        else:
            print("No such option!Try again!")
    session.close()


if __name__ == "__main__":
    main()