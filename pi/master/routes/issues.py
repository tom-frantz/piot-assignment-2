"""
RESTful API Routes: `/issues/{endpoint}`
"""

from flask_restful import reqparse, abort, Resource, inputs
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from master import app, api, db
from sqlalchemy.exc import SQLAlchemyError
from master.models import issues
from master.auth import checkAdmin
import master.validation as validate

parser_new = reqparse.RequestParser(bundle_errors=True)
parser_new.add_argument('car_number', type=inputs.regex(r'^[A-Za-z0-9]{1,6}$'), required=True)
parser_new.add_argument('description', type=inputs.regex(r'^[A-Za-z0-9-_ ]{1,1000}$'), required=True)

parser_update = reqparse.RequestParser(bundle_errors=True)
parser_update.add_argument('issue_id', type=inputs.positive, required=True)
parser_update.add_argument('description', type=inputs.regex(r'^[A-Za-z0-9-_ ]{1,1000}$'))
# True: "true", False: "false"
parser_update.add_argument('status', type=inputs.boolean)

class NewIssue(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        role = current_user['role']
        checkAdmin(role)

        try:
            args = parser_new.parse_args()
            car_number = args['car_number']
            description = args['description']
            new_issue = issues.IssueModel(
                car_number = car_number,
                description = description
            )
            new_issue.save_to_db()
            return {
                'message': 'Issue ID {} for Car {} submitted.'.format(new_issue.issue_id, new_issue.car_number)
            }, 201
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

class UpdateIssue(Resource):
    @jwt_required
    def put(self):
        current_user = get_jwt_identity()
        role = current_user['role']
        checkAdmin(role)

        try:
            args = parser_update.parse_args()
            issue_id = args['issue_id']

            result = issues.IssueModel.query.filter_by(issue_id=issue_id).first()
            
            if args['description']:
                result.description = args['description']
            
            if args['status'] is not None:
                result.status = args['status']
            
            db.session.commit()
            return {
                "issue_id": result.issue_id,
                "car_number": result.car_number,
                "description": result.description,
                "status": result.status
            }, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

api.add_resource(NewIssue, '/issues/new')
api.add_resource(UpdateIssue, '/issues/update')
