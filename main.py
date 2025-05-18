import flask
from flask import Flask, jsonify, make_response, request
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.jobs import Jobs


app = Flask(__name__)
api = Api(app)

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('id',
                                    'team_leader',
                                    'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
                 for item in news]
        }
                   )


@blueprint.route('/api/job/<int:job_id>', methods=['GET'])
def get_new(job_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(job_id)
    return jsonify(
        {
            'news':
                [news.to_dict(only=('id',
                                    'team_leader',
                                    'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))]
        }
                   )


@blueprint.route('/api/jobs/post', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    news = Jobs(
        id=request.json['id'],
        leader_id=request.json['leader_id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})


@blueprint.route('/api/jobs/delete/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(jobs_id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/db.db")
    app.register_blueprint(blueprint)
    app.run()
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()