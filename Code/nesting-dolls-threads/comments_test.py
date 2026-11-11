#!python

import os
import unittest

from comments import (
    Comment,
    add_reply,
    add_top_level,
    collapse_deleted,
    deepest_chain,
    find_by_author,
    find_by_id,
    find_mentioning,
    flatten,
    load_thread,
    render_lines,
)

SAMPLE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sample_thread.json"
)


class CommentDollTests(unittest.TestCase):
    def setUp(self):
        self.thread = load_thread(SAMPLE)

    def test_load_opens_nested_replies(self):
        self.assertEqual([comment.comment_id for comment in self.thread], ["c1"])
        innermost = find_by_id(self.thread, "c4")
        self.assertEqual(innermost.author, "pixel_finch")
        self.assertIn("previous build", innermost.text)
        self.assertEqual(innermost.replies, [])

    def test_deleted_flag_on_a_doll_that_still_holds_a_reply(self):
        deleted = find_by_id(self.thread, "c5")
        self.assertTrue(deleted.deleted)
        self.assertEqual(deleted.author, "juniper_lane")
        self.assertEqual(deleted.replies[0].comment_id, "c6")

    def test_find_by_id_missing(self):
        self.assertIsNone(find_by_id(self.thread, "missing"))

    def test_add_top_level_puts_a_new_outer_doll_on_the_shelf(self):
        created = add_top_level(self.thread, "harbor_note", "Shipping the notes.")
        self.assertIs(self.thread[-1], created)
        self.assertEqual(created.author, "harbor_note")
        self.assertEqual(created.text, "Shipping the notes.")
        self.assertEqual(created.replies, [])
        self.assertFalse(created.deleted)

    def test_add_reply_nests_inside_the_parent(self):
        created = add_reply(self.thread, "c3", "maple_orbit", "Noted on the ticket.")
        parent = find_by_id(self.thread, "c3")
        self.assertIs(parent.replies[-1], created)
        self.assertEqual(created.text, "Noted on the ticket.")

    def test_add_reply_missing_parent(self):
        with self.assertRaises(LookupError):
            add_reply(self.thread, "missing", "pixel_finch", "Hello.")

    def test_render_lines_indents_the_innermost_reply(self):
        lines = render_lines(self.thread)
        self.assertTrue(lines[0].startswith("pixel_finch: Friday deploy failed"))
        inner = [line for line in lines if "previous build" in line]
        self.assertEqual(inner, ["      pixel_finch: Rollback finished. The site is serving the previous build."])

    def test_find_by_author_brings_matches_back_in_open_order(self):
        found = find_by_author(self.thread, "pixel_finch")
        self.assertEqual([comment.comment_id for comment in found], ["c1", "c4"])

    def test_find_mentioning_rollback_ignores_letter_case(self):
        found = find_mentioning(self.thread, "rollback")
        self.assertEqual(
            [comment.comment_id for comment in found], ["c3", "c4", "c8"]
        )

    def test_flatten_puts_parent_before_the_dolls_inside(self):
        self.assertEqual(
            [comment.comment_id for comment in flatten(self.thread)],
            ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"],
        )

    def test_collapse_deleted_lifts_the_doll_that_was_inside(self):
        collapsed = collapse_deleted(self.thread)
        self.assertIsNone(find_by_id(collapsed, "c5"))
        parent = find_by_id(collapsed, "c2")
        self.assertEqual(
            [comment.comment_id for comment in parent.replies], ["c3", "c6"]
        )

    def test_deepest_chain_keeps_the_first_chain_on_a_tie(self):
        # c1 > c2 > c3 > c4 and c1 > c2 > c5 > c6 are the same length.
        chain = deepest_chain(self.thread)
        self.assertEqual(
            [comment.comment_id for comment in chain], ["c1", "c2", "c3", "c4"]
        )


class DeepestChainTests(unittest.TestCase):
    """Small hand-built threads where the deeper branch comes later."""

    def test_deepest_chain_keeps_the_longer_branch_even_when_it_comes_later(self):
        short = Comment("b1", "pixel_finch", "Short branch.", replies=[
            Comment("b2", "cobalt_kite", "Stops here."),
        ])
        longer = Comment("b3", "maple_orbit", "Longer branch.", replies=[
            Comment("b4", "quiet_harbor", "One more doll.", replies=[
                Comment("b5", "juniper_lane", "Solid."),
            ]),
        ])
        thread = [Comment("b0", "pixel_finch", "Root.", replies=[short, longer])]
        chain = deepest_chain(thread)
        self.assertEqual(
            [comment.comment_id for comment in chain], ["b0", "b3", "b4", "b5"]
        )

    def test_deepest_chain_checks_every_top_level_comment(self):
        thread = [
            Comment("t1", "pixel_finch", "Solid on the shelf."),
            Comment("t2", "cobalt_kite", "Has a reply.", replies=[
                Comment("t3", "maple_orbit", "Solid."),
            ]),
        ]
        chain = deepest_chain(thread)
        self.assertEqual([comment.comment_id for comment in chain], ["t2", "t3"])

    def test_deepest_chain_of_an_empty_thread_is_empty(self):
        self.assertEqual(deepest_chain([]), [])


if __name__ == "__main__":
    unittest.main()
