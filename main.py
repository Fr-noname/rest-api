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
            'jobs':
                [item.to_dict(only=('id',
                                    'team_leader',
                                    'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
                 for item in news]
        }
                   )


@blueprint.route('/api/job/<int:job_id>', methods=['GET'])
def get_new(job_id):
    print(type(job_id))
    if type(job_id) != int:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).all()
    flag = []
    for r in news:
        flag.append(r.id)
    if job_id not in flag:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    news = db_sess.query(Jobs).get(job_id)
    return jsonify(
        {
            'jobs':
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
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})


@blueprint.route('/api/jobs/del/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    if not jobs_id:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(jobs_id)
    if not news:
        return make_response(jsonify({'error': 'Bad request'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/red', methods=['POST'])
def redact_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    if not request.json['id']:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(request.json['id'])
    if not news:
        return make_response(jsonify({'error': 'Bad request'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    db_sess = db_session.create_session()
    news = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})


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
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()