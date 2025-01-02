from src.app import create_app
from src.domain.athlete.value_objects import Gender
from src.infrastructure.database.models.athlete import Athlete
from src.infrastructure.database.models.group import Group
from datetime import date

def init_test_data(app):
    with app.app_context():
        with app.db.session() as session:
            # Create some test groups
            u16_football = Group(
                name="U16 Football",
                type="natural",
                sport="Football",
                gender="male",
                age_range={"min": 14, "max": 16},
                is_custom=False
            )
            session.add(u16_football)

            # Create some test athletes
            athlete = Athlete(
                first_name="John",
                last_name="Doe",
                birthdate=date(2008, 1, 1),
                gender="male",
                sport="Football",
                email="john@example.com"
            )
            session.add(athlete)

            # Add athlete to group
            athlete.groups.append(u16_football)

            session.commit()

if __name__ == "__main__":
    app = create_app('default')
    
    # Create tables
    app.db.create_database()
    
    # Initialize test data
    init_test_data(app)
    
    print("Database initialized successfully!")