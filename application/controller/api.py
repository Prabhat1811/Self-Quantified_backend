from flask_restful import Resource, Api, fields, marshal_with, reqparse, marshal
from application.utils.validation import *
from application.data.database import db
from application.data.models import *
import werkzeug
from flask import abort
from flask_security import auth_required, login_required, auth_token_required, current_user, logout_user
from email_validator import validate_email


output_fields_userAPI = {
    "id": fields.Integer,
    "firstname": fields.String,
    "lastname": fields.String,
    "email": fields.String
}

# create_user_parser = reqparse.RequestParser()
# create_user_parser.add_argument("firstname")
# create_user_parser.add_argument("lastname")
# create_user_parser.add_argument("email")
# create_user_parser.add_argument("password")

update_user_parser = reqparse.RequestParser()
# update_user_parser.add_argument("firstname")
# update_user_parser.add_argument("lastname")
update_user_parser.add_argument("email")


class UserAPI(Resource):

    @auth_required("token")
    def get(self):

        user = db.session.query(User).filter(User.id==current_user.id).first()

        try:
            return marshal(current_user, output_fields_userAPI)
        except:
            raise NotFoundError(status_code=404)

    # @auth_required("token")
    # def put(self):
    #     args = update_user_parser.parse_args()
    #     email = args.get("email", None)

    #     try:
    #         validate_email(email)
    #     except:
    #         raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="Invalid email")
        
    #     user = db.session.query(User).filter(User.email==email).first()
    #     if user:
    #         raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Duplicate email id")
        
    #     user = db.session.query(User).filter(User.id == current_user.id).first()
    #     if user is None:
    #         raise NotFoundError(status_code=404)

    #     user.email = email
    #     db.session.add(user)
    #     db.session.commit()

    #     return "Email changed", 200

    # @auth_required("token")
    # def delete(self):

    #     user = db.session.query(User).filter(User.id==current_user.id).first()
    #     try:
    #         user = db.session.query(User).filter(User.id==current_user.id).first()
    #     except:
    #         raise NotFoundError(status_code=404)
        
    #     # find all trackers and logs and delete them

    #     db.session.delete(user)
    #     db.session.commit()

    #     return "User deleted", 200

    # def post(self):
    #     args = create_user_parser.parse_args()

    #     firstname = args.get("firstname", None)
    #     lastname = args.get("lastname", None)
    #     password = args.get("password", None)
    #     email = args.get("email", None)

    #     if firstname is None:
    #         raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="Firstname is required")

    #     try:
    #         validate_email(email)
    #     except:
    #         raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="Invalid email")

    #     user = db.session.query(User).filter(User.email == email).all()

    #     if user:
    #         raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Duplicate email id")
        
    #     new_user = User(firstname=firstname, lastname=lastname, password=password, email_id=email)
    #     db.session.add(new_user)
    #     db.session.commit()

    #     return "New user created", 200


output_fields_trackerAPI = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "tracker_type": fields.String,
    "settings": fields.String
}

create_tracker_parser = reqparse.RequestParser()
create_tracker_parser.add_argument("user_id")
create_tracker_parser.add_argument("name")
create_tracker_parser.add_argument("description")
create_tracker_parser.add_argument("tracker_type")
create_tracker_parser.add_argument("settings")

delete_tracker_parser = reqparse.RequestParser()
delete_tracker_parser.add_argument("tracker_id")


class TrackerAPI(Resource):
    
    @auth_required("token")
    def get(self):
        
        tracker = db.session.query(Tracker).filter(Tracker.user_id == current_user.id).all()

        try:
            return marshal(tracker, output_fields_trackerAPI)
        except:
            raise NotFoundError(status_code=404)

    @auth_required("token")
    def put(self):
        pass

    @auth_required("token")
    def delete(self):
        args = delete_tracker_parser.parse_args()

        tracker_id = args.get("tracker_id", None)

        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()

        if tracker is None:
            raise NotFoundError(status_code=404)

        user = db.session.query(Tracker).filter(tracker.user_id == current_user.id).first()

        if user is None:
            raise NotFoundError(status_code=404)

        tracker_log = db.session.query(TrackerLog).filter(tracker.id == TrackerLog.tracker_id).first()

        if tracker_log is not None:
            raise BusinessValidationError(status_code=400, error_code="BE2006", error_message="Tracker contains existing tracker logs")

        db.session.delete(tracker)
        db.session.commit()

        return "Tracker deleted", 200

    @auth_required("token")
    def post(self):
        args = create_tracker_parser.parse_args()

        name = args.get("name", None)
        description = args.get("description", None)
        tracker_type = args.get("tracker_type", None)
        settings = args.get("settings", None)

        if name is None or name == "":
            raise BusinessValidationError(status_code=400, error_code="BE2001", error_message="Name is required")
        
        if tracker_type is None:
            raise BusinessValidationError(status_code=400, error_code="BE2002", error_message="Tracker type is required")
        
        if tracker_type not in ("numerical", "multiple_choice", "time_duration", "boolean"):
            raise BusinessValidationError(status_code=400, error_code="BE2003", error_message="Tracker type is invalid")

        new_tracker = Tracker(user_id=current_user.id, name=name, description=description, tracker_type=tracker_type, settings=settings)
        db.session.add(new_tracker)
        db.session.commit()

        return "New tracker created", 201


output_fields_trackerLogAPI = {
    "id": fields.Integer,
    "tracker_id": fields.Integer,
    # "date_created": fields.String,
    # "time_created": fields.String,
    "timestamp": fields.String,
    "value": fields.String,
    "note": fields.String
}

get_trackerLog_parser = reqparse.RequestParser()
get_trackerLog_parser.add_argument("tracker_id")

create_trackerLog_parser = reqparse.RequestParser()
create_trackerLog_parser.add_argument("tracker_id")
create_trackerLog_parser.add_argument("value")
create_trackerLog_parser.add_argument("note")

delete_trackerLog_parser = reqparse.RequestParser()
delete_trackerLog_parser.add_argument("log_id")

class TrackerLogAPI(Resource):
    
    @auth_required('token')
    def get(self):
        args = get_trackerLog_parser.parse_args()

        tracker_id = args.get("tracker_id", None)

        if tracker_id is None or tracker_id == "":
            raise BusinessValidationError(status_code=400, error_code="BE2004", error_message="tracker_id is required")
        
        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()

        if tracker is None:
            raise NotFoundError(status_code=404)

        user = db.session.query(Tracker).filter(tracker.user_id == current_user.id).first()

        if user is None:
            raise NotFoundError(status_code=404)

        trackerLog = db.session.query(TrackerLog).filter(TrackerLog.tracker_id == tracker_id).all()

        try:
            return marshal(trackerLog, output_fields_trackerLogAPI)
        except:
            raise NotFoundError(status_code=404)

    @auth_required('token')
    def delete(self):
        args = delete_trackerLog_parser.parse_args()

        log_id = args.get("log_id", None)

        tracker_log = db.session.query(TrackerLog).filter(TrackerLog.id == log_id).first()

        if tracker_log is None:
            raise NotFoundError(status_code=404)

        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_log.tracker_id).first()

        if tracker is None:
            raise NotFoundError(status_code=404)

        user = db.session.query(Tracker).filter(tracker.user_id == current_user.id).first()

        if user is None:
            raise NotFoundError(status_code=404)

        db.session.delete(tracker_log)
        db.session.commit()

        return "Tracker Log deleted", 200

    @auth_required('token')
    def post(self):
        args = create_trackerLog_parser.parse_args()

        tracker_id = args.get("tracker_id", None)
        value = args.get("value", None)
        note = args.get("note", None)

        if tracker_id is None or tracker_id == "":
            raise BusinessValidationError(status_code=400, error_code="BE2004", error_message="tracker_id is required")

        if value is None or value == "":
            raise BusinessValidationError(status_code=400, error_code="BE2005", error_message="value is required")
        

        tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()

        if tracker is None:
            raise NotFoundError(status_code=404)

        user = db.session.query(Tracker).filter(tracker.user_id == current_user.id).first()

        if user is None:
            raise NotFoundError(status_code=404)

        new_trackerLog = TrackerLog(tracker_id=tracker_id, value=value, note=note)
        db.session.add(new_trackerLog)
        db.session.commit()

        return "New Log created", 201
