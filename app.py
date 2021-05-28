"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "santanarush"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


#### Part 2 Further Study with Homepage

@app.route('/')
def homepage():
    """the homepage to a page that shows the 5 most recent posts."""

    recent_posts = Post.query.order_by(Post.id.desc()).limit(5)

    return render_template('home.html', recent_posts=recent_posts)

@app.errorhandler(404)
def not_found(e):
    """Custom 404 page"""

    return render_template("404.html"), 404


#### Part 1 setting up Users and profile abilities

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)


@app.route('/users/new', methods=["GET"])
def create_user():
    """Show a form to create a new user"""
    
    return render_template('new.html')


@app.route('/users/new', methods=["POST"])
def new_user():
    """Handle form submission for creating a new user"""
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"] or None

    new_user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)

    return render_template('show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

#### Part 2 Starts Here - posting abilities

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    return render_template('new-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_create(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added!")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Show a post. Show buttons to edit and delete the post."""

    post = Post.query.get_or_404(post_id)

    return render_template('show-post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_update(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post ' {post.title}' edited!")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' is gone forever!!")

    return redirect(f"/users/{post.user_id}")

#### Part 3 Starts here - tagging abilities

@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page."""

    tags = Tag.query.order_by(Tag.name).all()

    return render_template('list-tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('show-tag.html', tag=tag)


@app.route('/tags/new', methods=["GET"])
def create_tag(tag_id):
    """Shows a form to add a new tag."""

    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('new-tag.html')


@app.route('/tags/new', methods=["POST"])
def new_tag(tag_id):
    """Process add form, adds tag, and redirect to tag list."""

    tag = Tag.query.get_or_404(tag_id)
    name = request.form["name"]

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def tag_edit(tag_id):
    """Show edit form for a tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit-tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_tag_update(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited!")

    return redirect(f"/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tag_destroy(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' is gone forever!!")

    return redirect(f"/tags")