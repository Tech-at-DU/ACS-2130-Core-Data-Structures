# Mini thread

GOAL: Ship a small thread tool where each reply sits inside its parent the
way a smaller doll sits inside a larger one.

The page lets someone post a top-level comment or reply to any comment.
Replies nest. A comment with no replies is the solid doll: you stop opening.

The picture of that motion is in the lesson,
[Nesting dolls](../../Lessons/nesting_dolls_threads.md).

Next up: install, run the page, and see the copied loops drop the innermost
reply.

## Run

1. From this folder, create a virtualenv and install:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

1. Start the page:

    ```bash
    python app.py
    ```

1. Open `http://127.0.0.1:5000`. The banner is the next function to write.
   The forms are already wired.

1. See the old renderer drop the innermost replies:

    ```bash
    python messy_indent.py
    ```

    The line about the previous build never appears. That reply is nested
    further than the copied loops reach.

Next up: write the dolls in `comments.py`, one function at a time.

## What is already here

- `app.py` reads the forms and knows the routes. It loads the sample once,
  on the first request, and every route reuses that same thread. Restarting
  the server resets it to the sample. A reply to a parent id that is not in
  the thread comes back as a 404 page.
- `templates/base.html` is the page shell.
- `templates/thread.html` and `templates/_comment.html` have the blocks you
  fill in. The recursive markup is yours.
- `sample_thread.json` is a synthetic thread. The names are made up.
  The file is the whole data source.
- `comments_test.py` checks the functions in `comments.py`.
- `app_test.py` checks the page with Flask's test client: drawing the
  thread, posting, the redirect, escaping, new ids, an empty thread, and a
  missing parent.

## What you write

Every place to start is marked `TODO`.

1. `comments.py`: the `Comment` doll, then `load_thread`, `render_lines`,
   `add_top_level`, `find_by_id`, `add_reply`, and the walks that bring
   results back out.
2. `app.py`: the two post routes that call `add_top_level` and
   `add_reply`.
3. `templates/_comment.html`: render one comment, then call the same macro
   on each reply. A comment with no replies stops.
4. `templates/thread.html`: call that macro for each top-level comment.

Next up: Exercise 1 in the lesson, then come back and run the tests.

## Exercises

The lesson is the full ticket. The short list:

1. Store a doll that can hold smaller dolls.
1. Open `sample_thread.json` until every comment is a `Comment`. `""` for
   replies means a solid doll.
1. Replace `messy_indent.py` with one recursive `render_lines`.
1. Draw the thread in the template by calling the macro on each reply.
1. Nest a new reply inside the parent id. `c3` is a parent you can use.
1. Bring authors, keyword mentions, a flat list, a thread with deleted
   comments removed, and the longest chain down to a solid doll back out.

**With a partner.** After `load_thread` works, trade files for ten minutes.
Point at their solid-doll stop and at the line that opens the next doll.

**Solo.** Write down the line number of your own solid-doll stop and of the
line that opens the next doll. Then check one nested doll in a Python shell
from this folder:

```python
import comments
thread = comments.load_thread("sample_thread.json")
print(thread[0].replies[0].author)
```

You should see `cobalt_kite`.

## Tests

Both test files fail on purpose until you write the `TODO`s. That is the
starter working as intended, not a broken setup.

```bash
python -m pytest
```

- On a fresh starter, `app_test.py` has one passing test (an empty thread
  still draws the forms). Everything else fails at the first `TODO` it
  reaches.
- Session checkpoint: `python -m pytest app_test.py` passes once the page
  draws the sample and a reply to `c3` nests under it.
- Full project: `python -m pytest` passes with both files green.

Next up: `python -m pytest` and read the first failure.

## Ship

- `python app.py` serves the page.
- A new top-level comment shows up.
- A reply to `c3` shows inside that comment, indented under it.
- `python -m pytest` exits 0. That runs `comments_test.py` and
  `app_test.py`.
- The page uses your template, and `messy_indent.py` is retired from the page.
- The branch is pushed.

Turn-in date: TBD.

> PROTIP: Write the solid-doll case before the recursive call. If you cannot
> say when you stop opening, leave the call unshipped.

Next up: read Watch the dolls in the lesson, then start Exercise 1.

> BE AWARE: In the sample, a solid doll has `"replies": ""`. A doll with
> something inside has a listing. A deleted comment can still hold replies.
