from app import app, db
from flask import request, jsonify
from models import User


# Get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    result = [user.to_json() for user in users]
    return jsonify(result)


# Create a friend
@app.route("/api/users", methods=["POST"])
def create_friend():
    try:
        data = request.json

        # Validations
        required_fields = ["name", "gender"]
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({"error": f'Missing required field: {field}'}), 400

        name = data.get("name")
        gender = data.get("gender")
        score = data.get("score")

        # Fetch avatar image based on gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_user = User(name=name,gender=gender, score=score,  img_url=img_url)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_json()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
