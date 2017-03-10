from flask import send_from_directory, abort
from flask_restful import Api, Resource
import flask_cors

from models import Call, db, app
import core

api = Api(app)
flask_cors.CORS(app, resources={'/*': {'origins': '*'}})


class CallResource(Resource):
    def get(self):
        data = {
            'data': [
                call.json() for call in db.session.query(Call)
                                                  .order_by(Call.date.desc())
                                                  .all()
            ]
        }
        headers = {'Cache-Control': 'no-cache, must-revalidate'}
        return data, 200, headers


class DevelopmentResource(Resource):
    def get(self, filename):
        engine = core.Engine(app.config['RECORDINGS_DIR'])
        return engine.process_recording(filename, debug=True)


class TranscribeResource(Resource):
    def get(self, filename):
        engine = core.Engine(app.config['RECORDINGS_DIR'])
        return engine.transcribe_recording(filename)


api.add_resource(CallResource, '/calls')
api.add_resource(DevelopmentResource, '/calc/<string:filename>')
api.add_resource(TranscribeResource, '/transcribation_direct_process/<string:filename>')


@app.route('/recordings/<int:call_id>')
def serve_recording(call_id):
    call = db.session.query(Call.recording_filename).filter_by(id=call_id).first()

    if call is None:
        abort(404)

    return serve_recording_from_name(call.recording_filename)


@app.route('/recordings/<string:recording_filename>')
def serve_recording_from_name(recording_filename):
    extension = recording_filename[-4:]
    try:
        mimetype = app.config['MIMETYPES'][extension]
    except KeyError:
        raise RuntimeError(
            'Unsupported recording file extension ({}).'
            .format(recording_filename)
        )
    return send_from_directory(app.config['RECORDINGS_DIR'], recording_filename,
                               mimetype=mimetype)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
