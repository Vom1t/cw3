import logging

from flask import Blueprint, jsonify, abort

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO

from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

# Создаем блупринт
bp_api = Blueprint('bp_api', __name__)

# Создаем объекты доступа к данным
post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)

api_logger = logging.getLogger('api_logger')



@bp_api.route('/posts/')
def api_posts_all():
    """
    Эндпоинты для все постов
    """
    all_posts = post_dao.get_all()

    api_logger.debug('Запрошены все посты')

    return jsonify([post.as_dict() for post in all_posts]), 200


@bp_api.route('/posts/<int:pk>/')
def api_posts_single(pk: int):
    """
    Эндпоинт для одного поста
    """
    post = post_dao.get_by_pk(pk)
    if post is None:
        api_logger.debug(f'Обращение к несуществующему посту {pk}')
        abort(404)
    api_logger.debug(f'Запрошен пост {pk}')

    return jsonify(post.as_dict()), 200


@bp_api.errorhandler(404)
def api_error_404(error):
    api_logger.debug(f'Ошибка {error}')
    return jsonify({'error': str(error)}), 404


@bp_api.route('/')
def api_posts_hello():
    return f'Это апи. Доступные эндпоинты /api/posts и /api/posts/<pk>. Смотри документацию у меня на гитхабе!)'