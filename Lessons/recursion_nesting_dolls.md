# Recursion Nesting Dolls

GOAL: Use one nesting-doll picture to ship a recursive walk: open a smaller
copy of the same task, stop at the solid doll, and bring a result back out
when the dolls close.

Next up: the shape of today, then the picture.

## Today

About two hours. The talk is the dolls. The build is the thread tool.

1. Watch the animation.
1. Teacher talk, about 35 minutes, with the picture still up.
1. A short break.
1. Trace a partner's walk, then build the thread.
1. Peer review, then ship.

Next up: play the animation.

## Watch the dolls

Opening a doll is a recursive call. You do the same job on what is inside.

![The outer doll splits open, the middle doll splits open, a small solid doll remains, then they close from the inside out.](./assets/nesting-dolls.svg)

The file is [assets/nesting-dolls.svg](./assets/nesting-dolls.svg). It loops.

The small gold doll is the base case. It is solid. You stop opening.

Closing the dolls is the call stack unwinding. Each doll closes and hands
what it found back to the doll it came from.

If the picture stays still, use the frames below. Same three moves.

```text
1. Nested
                 ( RED )

2. Open the outer doll. A call.
        ( RED )            ( RED )
                 ( BLUE )

3. Open the middle doll. Same move, smaller doll.
        ( RED )            ( RED )
            ( BLUE )   ( BLUE )
                 ( GOLD )  <- solid, stop

4. Close the middle doll. A return.
        ( RED )            ( RED )
            ( BLUE, holding what was inside )

5. Close the outer doll. The result is back.
                 ( RED, holding what came back )
```

Next up: the talk. Keep the animation in view.

## Teacher talk

All right. About 35 minutes. One picture, then the same picture in code.

A recursive function does one slice of the work and hands the rest to a
smaller copy of itself. It's kind of like opening a doll and finding a
smaller doll that needs the same gesture.

Next up: the open.

### Open means the same move on a smaller doll

You do not open every doll with a different gesture. You pull this one
apart. If another doll is inside, you pull that one apart the same way.

Real quick, a shipment of nested boxes works the same way. The label you
want might be on this box, or inside a box inside it. One function. The
next call gets the inner box.

```python
def find_in_boxes(box, label):
    """Return the box with this label, opening inner boxes along the way."""
    if box["label"] == label:
        return box
    for inner in box["inside"]:
        found = find_in_boxes(inner, label)
        if found is not None:
            return found
    return None
```

`box["inside"]` is the smaller doll. An empty `inside` list means this box
has nothing nested in it.

> ASK AUDIENCE: You pull a doll apart and another doll is sitting inside.
> What do you do next?

<details>
<summary>Answer</summary>

The same move, on the smaller doll. Open it. That call is the recursive
call.

</details>

Next up: when you are allowed to stop.

### The solid doll is the stop

The gold doll does not open. That is the base case. Write that case before
you write the call. If you cannot say when the opening stops, the call
never comes back.

A folder with no folders inside it is the same stop. An org chart stops
when you reach the person who can approve, or when there is no manager
left to ask.

> ASK AUDIENCE: You open a doll and it is solid wood. What do you do?

<details>
<summary>Answer</summary>

Stop opening. Close it. Hand it back to the doll you came from. That
solid doll is the base case.

</details>

Next up: what "hand it back" looks like in code.

### Closing is the result coming back

Unwinding is the walk back out. The inner call returns. The outer call
attaches that result to its own work and returns too.

It's kind of like unpacking a crate, finding the part, and closing each
crate on the way out with the part in your hand. The call stack is the
line of open crates. The return closes one crate.

> PROTIP: Do the recursive call, then use what it returns. The useful
> work of unwinding happens after the call comes back.

The part comes out with the innermost box.

> ASK AUDIENCE: Three boxes are open, one inside the next, and the part
> is in the innermost box. What closes first?

<details>
<summary>Answer</summary>

The innermost box. Then the middle one. Then the outer one. Returns
happen in that order: the solid doll closes before the doll that held it.

</details>

Next up: why this is the same move as a refactor.

### One function replaces the copied steps

A messy version of "list this folder" pastes the same loop once per level
of nesting. It works until someone adds another folder inside, and then
that level is invisible.

```python
def list_names_messy(folder):
    names = [folder["name"]]
    for inner in folder["inside"]:
        names.append(inner["name"])
        for deeper in inner["inside"]:
            names.append(deeper["name"])
    return names
```

The refactor is the doll move. Handle this folder. Call the same function
on each folder inside. A folder with nothing inside returns its own name
and stops.

```python
def list_names(folder):
    """This folder's name, then whatever each inner folder returns."""
    names = [folder["name"]]
    for inner in folder["inside"]:
        names.extend(list_names(inner))
    return names
```

The second version is the same shape at every size. That is the
refactoring parallel. Medium folders and tiny folders share that one
function.

> BE AWARE: Copying the loop "one more time" feels faster than the
> refactor, and it drops whatever is nested further than the copies.
> The single function still sees that inner folder.

Ship the single function.

> ASK AUDIENCE: A teammate pasted the folder loop a third time so a new
> nesting would show up. What do you ship instead?

<details>
<summary>Answer</summary>

Delete the copied loops. One function handles the folder it was handed,
then calls itself on `folder["inside"]`. The empty `inside` list is the
solid doll.

</details>

Next up: three other tickets with that same shape.

### The same shape on other tickets

You will see this any time a thing holds a smaller copy of itself.

An approval walks up an org chart. The person who can approve is the
solid doll. The name comes back down through the managers you opened.

```python
def approver(person):
    """Walk up until someone can approve, then bring that name back."""
    if person["can_approve"]:
        return person["name"]
    manager = person["manager"]
    if manager is None:
        return None
    return approver(manager)
```

A settings screen with a menu inside a menu is the same walk. Draw this
item, then draw each child item with the same function. A leaf item has
no children. You draw it and stop.

A comment thread is the same shape again. A reply is a smaller doll
inside its parent. A comment with no replies is solid.

Next up: trace one of these with a partner before you build the thread.

## With a partner

Ten minutes. Three people if you have a trio. Two is enough.

1. Pick `find_in_boxes` or `approver`.
1. One person opens the dolls. Say each call out loud, and name the
   smaller input you pass.
1. The partner tracks the stack. Write the calls that are still open.
   When a call returns, cross it off.
1. Swap. The partner explains your base case in one sentence: the solid
   doll, and what comes back.

> BE AWARE: If your partner's trace never crosses a call off, the base
> case is missing. Stop and name the solid doll before you add another
> call.

Next up: a break, then the thread ticket.

## Break

Ten minutes. Leave the animation up.

Next up: build the thread tool.

## The ticket

Ship the mini thread in
[Code/nesting-dolls-threads](../Code/nesting-dolls-threads/).

The build steps are the exercises in
[Nesting dolls](./nesting_dolls_threads.md). Each reply is a smaller doll
inside its parent. Posting a reply opens dolls until that parent, then
nests a new one. Drawing the thread and the later walks open until a
comment with no replies, then close back up with a result.

The page shell, the forms, and the sample thread are already there.
`comments.py`, the route bodies in `app.py`, and the recursive template
are marked `TODO`. The sample names are made up. The file is the whole
data source.

`messy_indent.py` is the copied-loop version. Run it once. The innermost
reply never appears. Your `render_lines` retires that file from the page.

Next up: a peer review before you call it shipped.

## Peer review

Swap branches with someone who did not trace with you.

Check only these:

1. A comment with no replies stops.
1. A result from inside is attached after the recursive call returns.
1. The template calls itself on replies.
1. A deleted comment's reply is still there, under the parent that
   remains.

Say the base case out loud on their code. They say yours.

Next up: the ship bar.

## Ship

Done means all of this is true:

- From `Code/nesting-dolls-threads`, `python app.py` serves the page.
- A new top-level comment shows up.
- A reply to `c3` shows inside that comment, indented under it.
- `python -m pytest comments_test.py` exits 0.
- The page uses the recursive template.
- The branch is pushed.

Turn-in date: TBD.

Next up: a few links if you want the same idea from another source.

## Additional Resources

1. [Nesting dolls animation](./assets/nesting-dolls.svg)
1. [Thread project](./nesting_dolls_threads.md)
1. [Starter folder](../Code/nesting-dolls-threads/)
1. [Flask quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
1. [Matryoshka doll](https://en.wikipedia.org/wiki/Matryoshka_doll)

<details>
<summary>For curriculum authors</summary>

## For curriculum authors

The course README schedule is unchanged on purpose.

This page is the session plan. The build ticket and the exercise list
live in `Lessons/nesting_dolls_threads.md`. The code shell is
`Code/nesting-dolls-threads/`. Do not paste a solution for `comments.py`
into either page.

The animation is `Lessons/assets/nesting-dolls.svg`. The ASCII frames in
Watch the dolls are the fallback when a browser will not animate an SVG.

`find_in_boxes`, `list_names`, and `approver` are talk samples. They are
not the thread starter. If the room starts porting them line for line
into `comments.py`, point them back at the TODOs and the sample JSON
shape (`"replies": ""` is the solid doll).

### In Class

1. 10 min. Play the animation with the room. Read frames 1 to 3 out loud
   if it will not move. Ask the first audience question while it is open.
1. 35 min. Teacher talk in this order: open, solid stop, close and
   return, the folder refactor, then approver and menus as extra
   tickets. Ask the four questions where they sit in the talk. Stay on
   the boxes and the folder. Leave the thread code for the build.
1. 10 min. Break. Leave the animation up.
1. 15 min. Pair trace on `find_in_boxes` or `approver`. Visit pairs.
   Listen for a base case and for calls getting crossed off.
1. 40 min. Starter. Milestone for the room: the page draws the sample
   with nesting, and a reply to `c3` sits inside that comment. The later
   walks in the project file are the same open-and-close motion.
1. 10 min. Peer review, then the ship bar.

Common misses: no base case, so the trace never returns. Copying one more
loop into `messy_indent.py` instead of replacing it. Scanning only the
top-level comments in `find_by_id`. Dropping the reply that was inside a
deleted comment.

Next up: demo a reply nested under `c3` before people leave.

</details>
