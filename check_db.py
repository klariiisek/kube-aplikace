from app import app, db, User
with app.app_context():
    print("Users in database:", [u.id for u in User.query.all()])
