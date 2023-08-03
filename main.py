from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class VideoModel(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name= {self.name}, views= {self.views}, likes= {self.likes})"


# arguments to be passed to insert data into database
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)

# arguments to be passed to update data in the database
video_update = reqparse.RequestParser()
video_update.add_argument("name", type=str, help="Name of the video", required=False)
video_update.add_argument("likes", type=int, help="Likes of the video", required=False)
video_update.add_argument("views", type=int, help="Views of the video", required=False)


resource_fields = {
    "_id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}

class Video(Resource):
    @marshal_with(resource_fields)
    def put(self, video_id):
        result = VideoModel.query.filter_by(_id=video_id).first()
        ## to avoid server crash when trying to create an identical video
        if result:
            # throw a 409 error when the video already exists
            abort(409, message="Video already exists")
        args = video_put_args.parse_args()
        video = VideoModel(
            _id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.create_all()
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(_id=video_id).first()
        if not result:
            # show 404 error message if id is not found in database
            abort(404, message="Video not found") 
        return result
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        result = VideoModel.query.filter_by(_id=video_id).first()
        if not result:
            # show 404 error message if id is not found in database
            abort(404, message="Video not found, nothing to update")
        args = video_update.parse_args()

        if args['views']:
            result.likes = args["views"]
        if args['likes']:
            result.likes = args["likes"]
        if args['name']:
            result.name = args["name"]
        
        db.session.commit()
        return result 

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
