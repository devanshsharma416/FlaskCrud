from email import message
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort


app = Flask(__name__)
api = Api(app)


employee_args = reqparse.RequestParser()
employee_args.add_argument("name", type=str, help="Name of the Employee", required=True)
employee_args.add_argument("address", type=str, help="Address of the Employee", required=True)
employee_args.add_argument("mobile", type=str, help="Mobile Number of the Employee", required=True)
employee_args.add_argument("designation", type=str, help="Name of the Designation", required=True)

employee_update_args = reqparse.RequestParser()
employee_update_args.add_argument("name", type=str, help="Name of the Employee")
employee_update_args.add_argument("address", type=str, help="Address of the Employee")
employee_update_args.add_argument("mobile", type=str, help="Mobile Number of the Employee")
employee_update_args.add_argument("designation", type=str, help="Name of the Designation")


employee = {}

def abort_if_id_notexist(self, emp_id):
    if emp_id not in employee:
        abort(404, message="Employee does not exist")

def abort_if_exist(self, emp_id):
    if emp_id in employee:
        abort(404, message="Employee already exists")


class Employee(Resource):
    def get(self, emp_id):
        abort_if_id_notexist(emp_id)
        return employee[emp_id]

    def post(self, emp_id):
        abort_if_exist(emp_id)
        args = employee_args.parse_args()
        employee[emp_id] = args
        return employee[emp_id], 201


    def patch(self, emp_id):
        abort_if_id_notexist(emp_id)
        args = employee_update_args.parse_args()
        new_value = employee[emp_id]
        if args["name"]:
            new_value["name"] = args["name"]
        if args["address"]:
            new_value["address"] = args["address"]
        if args["mobile"]:
            new_value["mobile"] = args["mobile"]
        if args["designation"]:
            new_value["designation"] = args["designation"]

        return employee[emp_id]

    def delete(self, emp_id):
        abort_if_id_notexist(emp_id)
        del employee[emp_id]
        return {'Message': "Successfully deleted"}


api.add_resource(Employee, '/employee/<int:emp_id>')

if __name__ == '__main__': 
    app.run(debug=True)


