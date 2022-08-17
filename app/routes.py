from datetime import datetime

from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.user import User
from app.models.place import Place
from app.models.history import History

users_bp = Blueprint("users_bp", __name__, url_prefix="/user")
places_bp = Blueprint("places_bp", __name__, url_prefix="/places")
histories_bp = Blueprint("history_bp", __name__, url_prefix="/histories")

def date_str_to_int(s):
    try:
        date_int = int(datetime.strptime(s, "%B %d %Y").timestamp())
        return date_int
    except:
        return None

def date_int_to_str(i):
    return datetime.fromtimestamp(i).strftime("%B %d %Y")

def validate_user_id(user_id):
    try:
        user_id = int(user_id)
    except:
        return abort(make_response(jsonify({"message": f"Invalid user {user_id} "}), 400))

    user = User.query.get(user_id)

    if user is None:
        return abort(make_response(jsonify({"message": f"user {user_id} not found"}), 404))

    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_place_or_abort(place_id):
    try:
        place_id = int(place_id)
    except ValueError:
        response = {"details": "Invalid data!"}
        abort(make_response(jsonify(response), 400))

    chosen_place = Place.query.get(place_id)

    if chosen_place is None:
        response = {"message": f"place {place_id} not found"}
        abort(make_response(jsonify(response), 404))
    
    return chosen_place

def get_history_or_abort(history_id):
    try:
        history_id = int(history_id)
    except ValueError:
        response = {"details": "Invalid data!"}
        abort(make_response(jsonify(response), 400))

    history = History.query.get(history_id)

    if history is None:
        response = {"message": f"history {history_id} not found"}
        abort(make_response(jsonify(response), 404))
    
    return history

#CREATE ONE NEW USER
@users_bp.route("", methods=["POST"])
def create_one_user():
    request_body = request.get_json()

    username = request_body["username"]
    password_hash = request_body["password_hash"]
    first_name = request_body["first_name"]
    last_name = request_body["last_name"]

    user = get_user_by_username(username)
    if not user is None:
        return {"message": f"Username {username} already exists"}, 400

    new_user = User(
        username=username,
        password=password_hash,
        first_name=first_name,
        last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    return {
        "user_id": new_user.user_id,
        "username": new_user.username,
        "message": f"Successfully created username {new_user.username}"
    }, 201

#READ (GET) ONE USER
@users_bp.route("<username>", methods=["POST"])
def get_one_user(username):
    request_body = request.get_json()
    password_hash = request_body["password_hash"]

    user = get_user_by_username(username)
    if user is None:
        return {
            "message": f"User {username} not found"
        }, 404

    if user.password != password_hash:
        return {"message": "Incorrect password"}, 403

    response = {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    return jsonify(response), 200

#READ (GET) ALL USERS
@users_bp.route("", methods=["GET"])
def read_all_users():
    users = User.query.all()
    users_response = []

    for user in users:
        users_response.append({
            "id": user.user_id,
            "username": user.username
        })
    
    return jsonify(users_response), 200

#DELETE ONE USER
@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = validate_user_id(user_id)
    db.session.delete(user)
    db.session.commit()

    return {
        "details": f"place {user.user_id} successfully deleted"
    }, 200

#CREATE ONE PLACE AT USER ID
@places_bp.route("", methods=["POST"])
def create_one_place():
    request_body = request.get_json()

    user_id = request_body["user_id"]
    maps_place_id = request_body["maps_place_id"]
    name = request_body["name"]
    lat = request_body["lat"]
    lon = request_body["lon"]

    user = validate_user_id(user_id)

    for place in user.places:
        if place.maps_place_id == maps_place_id:
            return {
                "message": f"Place {maps_place_id} already exists"
            }, 400

    maps_place_id = request_body["maps_place_id"]

    new_place = Place(
        name = name,
        lat = lat,
        lon = lon,
        maps_place_id = maps_place_id,
        user_id = user_id
    )

    db.session.add(new_place)
    db.session.commit()

    return {
        "place_id": new_place.place_id,
        "maps_place_id": new_place.maps_place_id,
        "message": f"Successfully created place_id {new_place.place_id}"
    }, 201

#READ ALL FAVOURITE PLACES FROM ONE USER
@users_bp.route("/<user_id>/places", methods=["GET"])
def read_places_of_one_user(user_id):
    user = validate_user_id(user_id)

    places_response = []

    for place in user.places:
        places_response.append({
            "place_id": place.place_id,
            "maps_place_id": place.maps_place_id,
            "name": place.name,
            "lat": place.lat,
            "lon": place.lon,
        }
    )

    return jsonify({
        "id": user.user_id,
        "username": user.username,
        "places": places_response
    }), 200

#READ ALL PROGRESS FROM ONE USER
@users_bp.route("/<user_id>/histories", methods=["GET"])
def read_all_progress(user_id):
    user = validate_user_id(user_id)

    histories = []

    for history in user.histories:
        histories.append({
            "history_id": history.history_id,
            "place_name": history.place_name,
            "date": date_int_to_str(history.date),
            "time_spent": history.time_spent,
            "mood": history.mood,
            "comments": history.comments
        })

    return jsonify({
        "id": user.user_id,
        "username": user.username,
        "histories": histories
    }), 200

#DELETE PLACE
@places_bp.route("", methods=["DELETE"])
def delete_place():
    request_body = request.get_json()

    print(request_body)

    user_id = request_body["user_id"]
    place_id = request_body["place_id"]

    user = validate_user_id(user_id)
    place = get_place_or_abort(place_id)

    found = False
    for p in user.places:
        if p.place_id == place_id:
            found = True
            break

    if not found:
        return {"message": f"Place id {place_id} not found"}, 404

    db.session.delete(place)
    db.session.commit()

    return {
        "message": f"Place id {place_id} successfully deleted"
    }, 200

# CREATE HISTORY AT USER ID
@histories_bp.route("", methods=["POST"])
def enter_progress():
    request_body = request.get_json()

    user_id = request_body["user_id"]
    place_name = request_body["place_name"]
    date = request_body["date"]
    time_spent = request_body["time_spent"]
    mood = request_body["mood"]
    comments = request_body["comments"]

    date_int = date_str_to_int(date)
    if date_int is None:
        return {"message": f"Invalid date {date}."}, 400

    validate_user_id(user_id)

    new_history = History(
        place_name = place_name,
        date = date_int,
        time_spent = time_spent,
        mood = mood,
        comments = comments,
        user_id = user_id
    )

    db.session.add(new_history)
    db.session.commit()

    return {
        "history_id": new_history.history_id,
        "message": f"Successfully created history_id {new_history.history_id}"
    }, 201

#DELETE HISTORY
@histories_bp.route("", methods=["DELETE"])
def delete_progress():
    request_body = request.get_json()

    user_id = request_body["user_id"]
    history_id = request_body["history_id"]

    user = validate_user_id(user_id)
    history = get_history_or_abort(history_id)

    found = False
    for h in user.histories:
        if h.history_id == history_id:
            found = True
            break

    if not found:
        return {"message": f"History id {history_id} not found"}, 404

    db.session.delete(history)
    db.session.commit()

    return {
        "message": f"History id {history} successfully deleted"
    }, 200