import re
from unicodedata import name
from flask_restful import Resource, abort, fields, marshal_with, Api, reqparse
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class EmployeeData(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable = True)
    address     = db.Column(db.String(200), nullable = True)
    mobile      = db.Column(db.Integer, nullable = True)
    designation = db.Column(db.String(200), nullable = True)

    # def __repr__(self):
    #     return f"EmployeeData(name = {self.name}, address = {self.address}, mobile = {self.mobile}, designation = {self.designation})


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "address": fields.String,
    "mobile": fields.Integer,
    "designation": fields.String,

}

employee_args = reqparse.RequestParser()
employee_args.add_argument("name", type=str, help="Name of the employee", required=True)
employee_args.add_argument("address", type=str, help="Address of the employee", required=True)
employee_args.add_argument("mobile", type=int, help="Mobile of the employee", required=True)
employee_args.add_argument("designation", type=str, help="Designation of the employee", required=True)


employee_update_args = reqparse.RequestParser()
employee_update_args.add_argument("name", type=str, help="Name of the employee")
employee_update_args.add_argument("address", type=str, help="Address of the employee")
employee_update_args.add_argument("mobile", type=int, help="Mobile of the employee")
employee_update_args.add_argument("designation", type=str, help="Designation of the employee")



def abort_if_id_notexist(emp_id):
    abort(404, message = "Employee doesn't exist")

class EmployeeCrud(Resource):
    
    @marshal_with(resource_fields)
    def get(self, emp_id):
        result = EmployeeData.query.filter_by(id=emp_id).first()
        if not result:
            abort_if_id_notexist(emp_id)
        return result
    
    @marshal_with(resource_fields)
    def post(self, emp_id):
        args = employee_args.parse_args()
        result = EmployeeData.query.filter_by(id=emp_id).first()
        if result:
            abort(409, message="Video id is already taken")
        
        employee = EmployeeData(id=emp_id, name=args["name"], address=args["address"], mobile=args["mobile"], designation=args["designation"])
        db.session.add(employee)
        db.session.commit()

        return employee
    @marshal_with(resource_fields)
    def patch(self, emp_id):
        args = employee_update_args.parse_args()
        result = EmployeeData.query.filter_by(id=emp_id).first()
        if not result:
            abort_if_id_notexist(emp_id)

        if args["name"]:
            result.name = args["name"]
        if args["address"]:
            result.address = args["address"]
        if args["mobile"]:
            result.mobile = args["mobile"]
        if args["designation"]:
            result.designation = args["designation"]

        db.session.commit()
        return result
        
    @marshal_with(resource_fields)
    def delete(self, emp_id):
        result = EmployeeData.query.filter_by(id=emp_id).delete()
        del result
        db.session.commit()
        return '', 201
        

api.add_resource(EmployeeCrud, '/employee/<int:emp_id>')

if __name__  == '__main__':
    app.run(debug=True)
