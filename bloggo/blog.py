from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy.orm import joinedload

from . import db
from werkzeug.exceptions import abort
from bloggo.auth import login_required
from bloggo.models import Post, User, Comment

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Post.query.options(joinedload('user')).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, user_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = Post.query.filter_by(id=id).first()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.user_id != g.user.id:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:post_id>/<int:id>/delete_comment', methods=['GET'])
@login_required
def delete_comment(post_id, id):
    deleted_comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(deleted_comment)
    db.session.commit()
    return redirect(url_for('blog.view', id=post_id))


@bp.route('/<int:id>/view', methods=['GET'])
def view(id):
    post = Post.query.filter_by(id=id).first_or_404()

    return render_template('blog/view.html', post=post)


@bp.route('/<int:id>/comment', methods=['POST'])
@login_required
def comment(id):
    body = request.form['body']
    error = None

    if not body:
        error = 'Empty comment.'

    if error is not None:
        flash(error)
    else:
        new_comment = Comment(body=body, post_id=id, user_id=g.user.id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('blog.view', id=id))
