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
from master.models import issues, cars
from master.auth import checkAdmin, checkStaff
import master.validation as validate
import simplejson as json

parser_new = reqparse.RequestParser(bundle_errors=True)
parser_new.add_argument(
    'car_number', type=inputs.regex(r'^[A-Za-z0-9]{1,6}$'), required=True
)
parser_new.add_argument('description', type=inputs.regex(r'(.*?)'), required=True)

parser_update = reqparse.RequestParser(bundle_errors=True)
parser_update.add_argument('issue_id', type=inputs.positive, required=True)
parser_update.add_argument(
    'description', type=inputs.regex(r'^[A-Za-z0-9-_ ]{1,1000}$')
)
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
                car_number=car_number, description=description
            )
            new_issue.save_to_db()
            return (
                {
                    'message': 'Issue ID {} for Car {} submitted.'.format(
                        new_issue.issue_id, new_issue.car_number
                    )
                },
                201,
            )
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
            return (
                {
                    "issue_id": result.issue_id,
                    "car_number": result.car_number,
                    "description": result.description,
                    "status": result.status,
                },
                200,
            )
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class AllIssues(Resource):
    @jwt_required
    def get(self):
        """
        **Admin and Engineer access.**
        """
        current_user = get_jwt_identity()
        role = current_user['role']
        checkStaff(role)

        try:
            all_issues_by_car = []
            car_list = (
                issues.IssueModel.query.with_entities(issues.IssueModel.car_number)
                .group_by(issues.IssueModel.car_number)
                .all()
            )
            for i in car_list:
                car_item = {}
                car_result = cars.CarModel.query.filter_by(
                    car_number=i.car_number
                ).first()
                if car_result:
                    car_item['car_number'] = car_result.car_number
                    car_item['make'] = car_result.make
                    car_item['body_type'] = car_result.body_type
                    car_item['seats'] = car_result.seats
                    car_item['colour'] = car_result.colour
                    car_item['cost_per_hour'] = json.dumps(
                        car_result.cost_per_hour, use_decimal=True
                    )
                    car_item['latitude'] = json.dumps(
                        car_result.latitude, use_decimal=True
                    )
                    car_item['longitude'] = json.dumps(
                        car_result.longitude, use_decimal=True
                    )
                    car_item['lock_status'] = car_result.lock_status

                    issue_result = issues.IssueModel.query.filter_by(
                        car_number=i.car_number
                    ).all()
                    issue_list = list(
                        map(
                            lambda item: {
                                'issue_id': item.issue_id,
                                'description': item.description,
                                'status': item.status,
                            },
                            issue_result,
                        )
                    )
                    car_item['issues'] = issue_list
                    all_issues_by_car.append(car_item)

            return all_issues_by_car, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


api.add_resource(NewIssue, '/issues/new')
api.add_resource(UpdateIssue, '/issues/update')
api.add_resource(AllIssues, '/issues/all')
