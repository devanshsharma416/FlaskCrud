from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Create the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = True)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Videos(name = {self.name}, views = {self.views}, likes = {self.likes}"

# Because we dont want to override the existing database.
# db.create_all()
# names = {"Devansh": {"age": 19, "Gender": "Male"},
#             "Abhinay": {"age": 30, "Gender": "Male"}}

video_put_args = reqparse.RequestParser()

video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer,
}

# videos = {}

# def abort_if_id_notexist(video_id):
#     if video_id not in videos:
#         abort(404, message = "Video id is not valid...")

# def abort_if_id_exist(video_id):
#     if video_id in videos:
#         abort(409, message = "Video already Exists with That ID")

# class HelloWorld(Resource):
#     def get(self, name):
#         return names[name], 200

# class Video(Resource):
#     def get(self, video_id):
#         abort_if_id_notexist(video_id)
#         return videos[video_id]

#     def post(self, video_id):
#         abort_if_id_exist(video_id) # Don't create videos already exists
#         args = video_put_args.parse_args()  # Get all the defined arguments
#         videos[video_id] = args
#         return videos[video_id], 201

#     def delete(self, video_id):
#         abort_if_id_notexist(video_id)
#         del videos[video_id]
#         return '', 204

class Video(Resource):
    # it is used to serialize the returned instance
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video is not available")
        return result

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id is already taken")
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'])
        # Temporarily Adding to database
        db.session.add(video)
        # Permanently Commit to database
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "Can't find so not able to update'")

        if args['name']:
            result.name = args["name"]
        if args['views']:
            result.views = args["views"]
        if args['likes']:
            result.likes = args["likes"]
        
        db.session.commit()
        return result, 204
        

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).delete()
        db.session.commit()
        return '', 201

# api.add_resource(HelloWorld, '/helloworld/<string:name>')
api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
    app.run(debug=True)

