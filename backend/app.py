from flask import Flask, send_from_directory, abort
from flask_restful import Api, Resource
import flask_cors

import core

app = Flask(__name__)
app.config.from_object('settings')
rest_api = Api(app)
cors = flask_cors.CORS(app, resources={'/*': {'origins': '*'}})


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


rest_api.add_resource(CallResource, '/calls')
rest_api.add_resource(DevelopmentResource, '/calc/<string:filename>')


@app.route('/recordings/<int:call_id>')
def serve_recording(call_id):
    call = db.session.query(Call.recording_filename).filter_by(id=call_id).first()

    if call is None:
        abort(404)

    extension = call.recording_filename[-4:]
    try:
        mimetype = app.config['MIMETYPES'][extension]
    except KeyError:
        raise RuntimeError(
            'Unsupported recording file extension ({}) (call_id={}).'
            .format(call.recording_filename, call_id)
        )

    return send_from_directory(app.config['RECORDINGS_DIR'],
                               call.recording_filename,
                               mimetype=mimetype)


from models import db, Call


if __name__ == '__main__':
    app.run(port=8001, debug=True)
