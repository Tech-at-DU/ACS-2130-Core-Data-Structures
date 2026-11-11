#!python
"""Flask shell for the mini thread tool.

Routes, forms, and the page shell are wired. The doll walks live in
comments.py, and the recursive page markup lives in the templates.
"""

import os

from flask import Flask, abort, redirect, render_template, request, url_for

import comments

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_PATH = os.path.join(BASE_DIR, "sample_thread.json")

# Top-level dolls already on the shelf. Empty until load_thread is hooked up.
THREAD = []


@app.get("/")
def view_thread():
    # TODO: load the sample thread into Comment dolls with comments.load_thread(SAMPLE_PATH) and render thread.html with that list as thread
    raise NotImplementedError(
        "TODO: load the sample thread into Comment dolls with "
        "comments.load_thread(SAMPLE_PATH) and render thread.html with "
        "that list as thread"
    )
    return render_template("thread.html", thread=THREAD, error=None)


@app.post("/comments")
def post_comment():
    author = request.form.get("author", "").strip()
    text = request.form.get("text", "").strip()
    if not author or not text:
        abort(400)
    # TODO: call comments.add_top_level(THREAD, author, text) so the new comment sits on the shelf as its own outermost doll, then delete this raise so the redirect runs
    raise NotImplementedError(
        "TODO: call comments.add_top_level(THREAD, author, text) so the "
        "new comment sits on the shelf as its own outermost doll, then "
        "delete this raise so the redirect runs"
    )
    return redirect(url_for("view_thread"))


@app.post("/replies")
def post_reply():
    parent_id = request.form.get("parent_id", "").strip()
    author = request.form.get("author", "").strip()
    text = request.form.get("text", "").strip()
    if not parent_id or not author or not text:
        abort(400)
    # TODO: call comments.add_reply(THREAD, parent_id, author, text) so this reply is nested inside the parent doll, then delete this raise so the redirect runs
    raise NotImplementedError(
        "TODO: call comments.add_reply(THREAD, parent_id, author, text) "
        "so this reply is nested inside the parent doll, then delete this "
        "raise so the redirect runs"
    )
    return redirect(url_for("view_thread"))


@app.errorhandler(NotImplementedError)
def show_todo(exc):
    return render_template("thread.html", thread=[], error=str(exc)), 501


@app.errorhandler(400)
def show_bad_form(_exc):
    return render_template(
        "thread.html",
        thread=[],
        error="Author and text are required. A reply also needs the parent comment id.",
    ), 400


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
