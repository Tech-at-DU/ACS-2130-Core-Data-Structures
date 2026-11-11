#!python
"""Comment dolls for the mini thread tool.

Each comment can hold replies. A reply is a smaller doll inside its parent.
A comment with no replies is a solid doll.
"""


class Comment:
    """One comment doll. Replies are smaller dolls nested inside."""

    def __init__(self, comment_id, author, text, replies=None, deleted=False):
        """Store this doll's id, author, text, deleted flag, and child replies.

        replies is a list of Comment dolls. None means nothing is inside yet.
        """
        # TODO: store comment_id, author, text, deleted, and replies (use an empty list when replies is None) so this doll can hold smaller dolls inside
        raise NotImplementedError(
            "TODO: store comment_id, author, text, deleted, and replies "
            "(use an empty list when replies is None) so this doll can hold "
            "smaller dolls inside"
        )


def load_thread(path):
    """Open sample_thread.json and return a list of top-level Comment dolls.

    The file is a Reddit-shaped listing. Each child has id, author, body,
    deleted, and replies. body is the comment text. A replies value of ""
    is a solid doll. A replies listing means smaller dolls are inside.
    """
    # TODO: read the JSON at path and recursively build Comment dolls, stopping when replies is "" (the solid doll) and opening each nested listing the same way
    raise NotImplementedError(
        "TODO: read the JSON at path and recursively build Comment dolls, "
        "stopping when replies is \"\" (the solid doll) and opening each "
        "nested listing the same way"
    )


def render_lines(thread):
    """Return lines of 'author: text', indented further for each nested reply.

    Each reply is indented two spaces further than its parent. The lines for
    the replies come back from the recursive call and sit under this comment.
    A comment with no replies returns its own line only.
    """
    # TODO: replace the copied loops in messy_indent.py with one recursive walk that prints this doll, then indents whatever the call on its replies returns
    raise NotImplementedError(
        "TODO: replace the copied loops in messy_indent.py with one "
        "recursive walk that prints this doll, then indents whatever the "
        "call on its replies returns"
    )


def add_top_level(thread, author, text):
    """Put a new outermost doll on the shelf and return it.

    thread is the list of top-level comments. The new comment has no replies.
    Give it a comment_id that is not already in the thread.
    """
    # TODO: append a new Comment with no replies onto thread and return it (a new outermost doll, not one nested inside another)
    raise NotImplementedError(
        "TODO: append a new Comment with no replies onto thread and return "
        "it (a new outermost doll, not one nested inside another)"
    )


def find_by_id(thread, comment_id):
    """Return the Comment with this id, opening replies until you find it.

    Return None when the id is not in the thread.
    """
    # TODO: open each doll until comment_id matches, then return that doll; a doll with no replies that does not match is the solid stop, and a miss returns None
    raise NotImplementedError(
        "TODO: open each doll until comment_id matches, then return that "
        "doll; a doll with no replies that does not match is the solid stop, "
        "and a miss returns None"
    )


def add_reply(thread, parent_id, author, text):
    """Nest a new reply inside the comment with parent_id and return it.

    Open dolls until that parent is found, then put the new reply in its
    replies. Raise LookupError when the parent id is missing.
    """
    # TODO: implement recursive add_reply that opens dolls until it finds the parent comment id, then nests the new reply inside
    raise NotImplementedError(
        "TODO: implement recursive add_reply that opens dolls until it "
        "finds the parent comment id, then nests the new reply inside"
    )


def find_by_author(thread, author):
    """Return every Comment by this author.

    Open a doll, keep it when the author matches, then do the same for the
    dolls inside. The list comes back as the dolls close.
    """
    # TODO: walk every doll and bring back the ones whose author matches, attaching inner results after the recursive call returns
    raise NotImplementedError(
        "TODO: walk every doll and bring back the ones whose author matches, "
        "attaching inner results after the recursive call returns"
    )


def find_mentioning(thread, keyword):
    """Return every Comment whose text mentions keyword.

    Match without caring about letter case. Bring matches back as each
    call returns, parent before the dolls that were inside it.
    """
    # TODO: open each doll, keep it when keyword appears in its text, and extend that list with whatever the call on its replies returns
    raise NotImplementedError(
        "TODO: open each doll, keep it when keyword appears in its text, "
        "and extend that list with whatever the call on its replies returns"
    )


def flatten(thread):
    """Return every Comment in one list, parent before the dolls inside it."""
    # TODO: open each doll, then append what the recursive call returns for its replies so the nested dolls come back out into one list
    raise NotImplementedError(
        "TODO: open each doll, then append what the recursive call returns "
        "for its replies so the nested dolls come back out into one list"
    )


def collapse_deleted(thread):
    """Return a new thread with deleted comments removed.

    A deleted doll does not appear. The dolls that were inside it move up
    under the parent that remains. Build that list from what the recursive
    call returns.
    """
    # TODO: open each doll's replies first, drop the doll when it is deleted, and keep the inner dolls that came back in its place
    raise NotImplementedError(
        "TODO: open each doll's replies first, drop the doll when it is "
        "deleted, and keep the inner dolls that came back in its place"
    )


def deepest_chain(thread):
    """Return the comments from an outermost doll down to an innermost one.

    Follow replies until a solid doll. When two replies both still have a
    doll inside, keep the first reply you meet. The list starts at the outer
    comment and ends on the solid doll.
    """
    # TODO: open replies until a solid doll and return the chain of comments you opened, keeping the first reply that still has a doll inside when you have a choice
    raise NotImplementedError(
        "TODO: open replies until a solid doll and return the chain of "
        "comments you opened, keeping the first reply that still has a doll "
        "inside when you have a choice"
    )
