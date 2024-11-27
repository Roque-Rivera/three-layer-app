from app import db, Item, app
from dotenv import load_dotenv

def init_database():
    with app.app_context():
        db.create_all()
        
        # Add some sample items
        sample_items = [
            Item(name='Item 1', description='First sample item'),
            Item(name='Item 2', description='Second sample item'),
            Item(name='Item 3', description='Third sample item')
        ]
        
        for item in sample_items:
            db.session.add(item)
        
        db.session.commit()

if __name__ == '__main__':
    load_dotenv()
    init_database()
    print("Database initialized with sample data!")
