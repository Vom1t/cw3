from flask import Flask, Blueprint, render_template, current_app, abort, request

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO

from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

# Создаем блупринт
bp_posts = Blueprint('bp_posts', __name__, template_folder='templates')

# Создаем объекты доступа к данным
post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)


@bp_posts.route('/')
def page_posts_index():
    """
    Страничка все постов
    """
    all_posts = post_dao.get_all()
    return render_template('posts_index.html', posts=all_posts)


@bp_posts.route('/posts/<int:pk>/')
def page_posts_single(pk: int):
    """
    Страничка одного поста
    """
    post = post_dao.get_by_pk(pk)
    comments: list[Comment] = comments_dao.get_comments_by_post_pk(pk)
    if post is None:
        abort(404)

    return render_template('posts_single.html', post=post, comments=comments, comments_len=len(comments))


@bp_posts.route('/users/<user_name>')
def page_posts_by_users(user_name: str):
    """
    Возвращает посты пользователя
    """
    posts: list[Post] = post_dao.get_by_poster(user_name)

    if not posts:
        abort(404, "Такого пользователя нет")

    return render_template('posts_user-feed.html', posts=posts, user_name=user_name)


@bp_posts.route('/search/')
def page_posts_search():
    """
    Возвращает результаты поиска
    """
    query: str = request.args.get('s', )
    if query == "":
        posts: list = []
    else:
        posts: list[Post] = post_dao.search_in_content(query)

    return render_template('posts_search.html', posts=posts, query=query, posts_len=len(posts))


