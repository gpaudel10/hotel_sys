# init_db.py
from app import create_app, db
from app.auth.models import User
from app.booking.models import Room, Booking
from sqlalchemy.exc import IntegrityError

def init_db():
    app = create_app()
    with app.app_context():
        
        # creating the tables
        #for debugging case
        
        print("Dropping existing tables...")
        db.drop_all()
        
        print("table is creating..")
        db.create_all()
        
        # some room data
        default_rooms = [
            Room(
                room_number='101',
                room_type='single',
                price_per_night=1000.0,
                description='best room for single person',
                is_available=True
            ),
            Room(
                room_number='102',
                room_type='single',
                price_per_night=1200.0,
                description='single room with mountain view',
                is_available=True
            ),
            Room(
                room_number='103',
                room_type='double',
                price_per_night=1500.0,
                description='double room with garden view and queen size bed',
                is_available=True
            ),
            Room(
                room_number='104',
                room_type='double',
                price_per_night=2000.0,
                description='double room with balcony',
                is_available=True
            ),
            Room(
                room_number='105',
                room_type='suite',
                price_per_night=2500.0,
                description='luxury room with living room and kitchen',
                is_available=True
            )
        ]
        
        try:
            # to check if rooms already exist or not
            
            existing_rooms = Room.query.count()
            if not existing_rooms:
                #for debugging
                print("adding sample rooms")
                
                for room in default_rooms:
                    db.session.add(room)
                db.session.commit()
                print(f"added {len(default_rooms)} rooms successfully.")
            else:
                print(f"Database already contains {existing_rooms} rooms. Skipping..")
                
        except IntegrityError as e:
            db.session.rollback()
            print("error: could not add sample rooms (they may already exist)")
            print(str(e))
        except Exception as e:
            db.session.rollback()
            print("error while initializing database:")
            print(str(e))
            
        print("database initialization is completed")

if __name__ == '__main__':
    init_db()