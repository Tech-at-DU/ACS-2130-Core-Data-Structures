# Nesting Dolls

GOAL: Ship a mini thread tool where each reply sits inside its parent the
way a smaller doll sits inside a larger one, and every walk down the thread
comes back out with a result.

Next up: watch the dolls open and close.

## Watch the dolls

![The outer doll splits open, the middle doll splits open, a small solid doll remains, then they close from the inside out.](./assets/nesting-dolls.svg)

Opening a doll is a recursive call. You look inside.

The small solid doll is the base case. Nothing is inside, so you stop.

Closing the dolls is unwinding. What you found comes back out with you.

If the picture stays still, read it left to right in time: one closed doll,
then the outer shell apart, then the middle shell apart around a gold doll,
then the shells coming back together from the inside out.

Next up: the same open-and-close motion in a function someone copied by hand.

## The same motion in code

All right. A teammate printed a thread by pasting the same loop once per
nesting:

```python
for comment in thread:
    print(comment)
    for reply in comment.replies:
        print(reply)
        for nested in reply.replies:
            print(nested)
```

That is three dolls, and then it stops. Anything nested further never shows
up. Real quick, run the copy that is already in the starter:

```bash
python messy_indent.py
```

The reply about the previous build is in `sample_thread.json` and missing
from that printout.

The refactor is one function. It handles the doll it was handed, then calls
itself on the dolls inside. The solid doll is the call with nothing to open.
The lines come back as the calls return. You delete the copied loops.

Next up: four questions, then the thread you are shipping.

## Teacher talk

> ASK AUDIENCE: You pull a doll apart and another doll is sitting inside.
> What do you do next?

<details>
<summary>Answer</summary>

The same move, on the smaller doll. Open it. That repeated move is the
recursive call.

</details>

> ASK AUDIENCE: You open a doll and it is solid. Nothing is inside. What do
> you do?

<details>
<summary>Answer</summary>

Stop opening. That solid doll is the base case. Close it and hand it back
to the doll you came from.

</details>

> ASK AUDIENCE: Someone hits reply on a comment buried inside other
> comments. What does `add_reply` do before the new comment exists?

<details>
<summary>Answer</summary>

Open each doll until the parent id matches, then nest the new reply in that
doll. The new reply is solid until someone answers it.

</details>

> ASK AUDIENCE: The copied loops drop the innermost reply. What is the
> refactor?

<details>
<summary>Answer</summary>

One function. It renders the comment it was handed, then calls itself on
that comment's replies. The solid doll is the call that has no replies to
open. The results come back as the dolls close.

</details>

Next up: the ticket.

## The ticket

Build the thread tool in
[Code/nesting-dolls-threads](../Code/nesting-dolls-threads/).

People post a top-level comment, or they reply to any comment. You keep the
thread in memory, draw it in the browser, and walk it. The sample file is
the whole data source. The names in it are made up.

Mapping, same as the picture:

- Each reply is a smaller doll inside its parent.
- Posting a reply opens dolls until you find the parent, then nests a new
  doll inside.
- Rendering and the later walks open dolls until a comment with no replies,
  then close back up with a result.

`comments.py`, the route bodies in `app.py`, and the two templates are
marked `TODO`. The page shell and the forms are already wired.

Next up: Exercise 1.

## Exercise 1: Make a doll that can hold dolls

A comment needs an id, an author, text, a deleted flag, and a list of
replies. Replies are smaller dolls. No list yet means nothing is inside.

Fill in `Comment.__init__` in `comments.py`.

Next up: open the sample file and build those dolls for real.

## Exercise 2: Open the sample until every doll is real

`load_thread` reads `sample_thread.json`.

The file is shaped like a thread listing. Each child has an id, an author,
a body, a deleted flag, and replies. `body` is the text you store.

`"replies": ""` is a solid doll. Build the comment and stop.

A replies listing means smaller dolls are inside. Open each one the same
way.

**With a partner.** Ten minutes. Trade `load_thread`. Point at their solid
stop, then at the line that opens the next doll. They do the same on yours.

Next up: retire the copied loops.

## Exercise 3: Retire the copied loops

`render_lines` returns lines of `author: text`. Indent each reply two
spaces further than its parent.

The lines for the replies come back from the recursive call and sit under
this comment. A solid doll returns its own line only.

`messy_indent.py` stays in the folder as the version you are replacing. The
page uses `render_lines`, not the copied loops.

> PROTIP: Write the solid-doll case before the recursive call. If you cannot
> say when you stop opening, leave the call unshipped.

Next up: draw that same walk in the browser.

## Exercise 4: Draw the thread in the page

The template does the same open-and-close motion as `render_lines`.

In `templates/_comment.html`, render this comment's author and text. When
the comment is deleted, show the author and the word removed. Then call
`render_comment` on each reply. A comment with no replies is the solid
doll: render it and stop.

In `templates/thread.html`, call `render_comment` for each top-level
comment.

Jinja escapes `{{ comment.text }}`. Use that for author and text.

**With a partner.** One of you reads the macro aloud. The other points at
the solid stop and at the call that opens replies. Swap.

> BE AWARE: A deleted comment can still hold replies. Those replies are
> real dolls. Your macro still opens them.

Next up: nest a new reply inside the doll it answers.

## Exercise 5: Put a new reply inside the right doll

`find_by_id` opens each doll until the id matches. A solid doll that does
not match is the stop. A miss returns `None`.

`add_reply` uses that walk, then appends a new solid doll to the parent's
replies. A missing parent raises `LookupError`.

`add_top_level` puts a new doll on the shelf, not inside another doll.
Give every new doll an id that is not already in the thread.

In `app.py`, the view route loads the sample into dolls and renders
`thread.html`. The post routes call `add_top_level` and `add_reply`, then
let the redirect run. `c3` is a parent id already in the sample.

**With a partner.** One of you names a parent id. The other says which
dolls `find_by_id` opens to reach it, outermost first.

Next up: bring results back out as the dolls close.

## Exercise 6: Bring matching authors back out

`find_by_author` opens a doll, keeps it when the author matches, then does
the same for the dolls inside. Attach what the inner call returns after it
comes back. Parent before the dolls that were inside it.

Next up: the same walk, matching text instead of author.

## Exercise 7: Bring keyword mentions back out

`find_mentioning` keeps a doll when the keyword appears in its text. Letter
case does not matter. The list comes back as each call returns.

Next up: one list, still in the order you opened them.

## Exercise 8: Lay every doll in one row

`flatten` returns every comment. Open a doll, then append what the call on
its replies returns. The nested dolls come back out into one list.

Next up: a deleted doll drops out, and the dolls inside it stay.

## Exercise 9: Close out deleted dolls

`collapse_deleted` returns a new thread.

Open the replies first. When the doll is deleted, it does not appear, and
the dolls that came back from inside it take its place. When it is not
deleted, it stays, holding those inner dolls.

> BE AWARE: The deleted comment in the sample still has a reply inside it.
> That reply remains, under the parent that remains.

**Peer review.** Swap with someone else. Check only this: a solid doll
stops, a deleted doll's reply still appears under the parent that remains,
and the template calls itself on replies.

Next up: the chain of dolls from the outside down to a solid center.

## Exercise 10: Follow the chain to the innermost doll

`deepest_chain` returns the comments from an outermost doll down to a solid
one.

Follow replies until a doll has nothing inside. When two replies both still
have a doll inside, keep the first reply you meet. The list starts at the
outer comment and ends on the solid doll.

Next up: the ship bar.

## Ship

Done means all of this is true:

- From `Code/nesting-dolls-threads`, `python app.py` serves the page.
- Posting a top-level comment shows that comment.
- Replying to `c3` shows the reply inside that comment, indented under it.
- `python -m pytest comments_test.py` exits 0.
- The page uses your recursive template. `messy_indent.py` is not on the
  page.
- The branch is pushed.

Turn-in date: TBD.

Next up: the links below, if you want a second source on macros or on the
dolls themselves.

## Additional Resources

1. [Flask quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
1. [Jinja macros](https://jinja.palletsprojects.com/en/stable/templates/#macros)
1. [Matryoshka doll](https://en.wikipedia.org/wiki/Matryoshka_doll)
1. [Starter folder](../Code/nesting-dolls-threads/)

<details>
<summary>For curriculum authors</summary>

## For curriculum authors

The schedule row in the course README is unchanged on purpose.

The animation file is `Lessons/assets/nesting-dolls.svg`. It loops: outer
shell opens, middle shell opens, gold doll is the stop, middle closes, outer
closes. If a browser will not animate an SVG used as an image, the still
description under the picture is the fallback.

There is no solution in this file. `comments.py` and the templates raise or
show a placeholder until the TODOs are replaced.

### In Class

1. Play the animation once with the room. Ask the first two teacher-talk
   questions while it is on screen.
1. Run `messy_indent.py` so the room sees the innermost reply missing.
1. Build path: `Comment`, `load_thread`, `render_lines`, the template macro,
   then `add_reply` under `c3`.
1. The walks that bring results back (`find_by_author` through
   `deepest_chain`) are the same open-and-close motion. Leave them for
   after a reply renders.
1. Pair trace after `load_thread`. Peer review before ship: solid stop,
   deleted reply still present, template calls itself.

Common misses: treating `"replies": ""` as a listing, scanning only the
top-level dolls in `find_by_id`, leaving the route `raise` in place, and
dropping the reply that was inside a deleted comment.

MVP for the session: the page draws the sample with nesting, and a reply
to `c3` shows inside that comment.

Next up: demo a reply nested under `c3` before the room leaves.

</details>
