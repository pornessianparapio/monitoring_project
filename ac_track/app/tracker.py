import time
# import win32gui
from threading import Thread
from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import db, Activity
from . import create_app

app = create_app()

tracking = False
current_activity = None

def get_active_window_title():
    meow = 'meowmeowmeowmeowmeowmeow'
    return  meow
    # hwnd = win32gui.GetForegroundWindow()
    # return win32gui.GetWindowText(hwnd)

def track_activity(user_id):
    global tracking, current_activity
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)

    while tracking:

        with app.app_context():
            window_title = get_active_window_title()
            session = Session()
            try:
                if current_activity is None or current_activity.activity != window_title:
                    if current_activity is not None:
                        current_activity.end_time = datetime.utcnow()
                        session.add(current_activity)
                        session.commit()
                    new_activity = Activity(user_id=user_id, start_time=datetime.utcnow(), activity=window_title)
                    session.add(new_activity)
                    session.commit()
                    current_activity = new_activity
                    print(current_activity)
            finally:
                session.remove()
        time.sleep(1)

def start_tracking(user_id):
    global tracking
    tracking = True
    tracker_thread = Thread(target=track_activity, args=(user_id,))
    tracker_thread.start()

def stop_tracking():
    global tracking, current_activity
    tracking = False
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)
    with app.app_context():
        session = Session()
        try:
            if current_activity is not None:
                current_activity.end_time = datetime.utcnow()
                session.add(current_activity)
                session.commit()
                current_activity = None
        finally:
            session.remove()

