#!python
"""Browser-side checks for the thread page, run with Flask's test client.

These fail until the session checkpoint works: Comment, load_thread, the
two templates, find_by_id, add_top_level, add_reply, and the post routes.
"""

import unittest

import app as thread_app


def all_comments(thread):
    """Every comment in the thread. A plain helper so these tests do not depend on flatten."""
    found = []
    for comment in thread:
        found.append(comment)
        found.extend(all_comments(comment.replies))
    return found


class ThreadPageTests(unittest.TestCase):
    def setUp(self):
        # Same as restarting the server: the next request loads the sample once.
        thread_app.THREAD = None
        thread_app.app.config["TESTING"] = True
        self.client = thread_app.app.test_client()

    def page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        return response.get_data(as_text=True)

    def test_page_draws_every_comment_parent_before_replies(self):
        html = self.page()
        texts = [
            "Friday deploy failed",
            "The migration step hung.",
            "I left a rollback note on the ticket.",
            "serving the previous build",
            "Status page matches the rollback.",
        ]
        positions = [html.find(text) for text in texts]
        self.assertNotIn(-1, positions, "a sample comment is missing from the page")
        self.assertEqual(positions, sorted(positions))

    def test_page_loads_the_sample_once_and_reuses_it(self):
        self.page()
        first = thread_app.THREAD
        self.page()
        self.assertIs(thread_app.THREAD, first)

    def test_new_top_level_comment_survives_the_redirect(self):
        response = self.client.post(
            "/comments", data={"author": "harbor_note", "text": "Checklist updated."}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("Checklist updated.", self.page())

    def test_reply_to_c3_survives_the_redirect_and_nests_under_it(self):
        response = self.client.post(
            "/replies",
            data={"parent_id": "c3", "author": "maple_orbit", "text": "Noted on the ticket."},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("Noted on the ticket.", self.page())
        parent = [c for c in all_comments(thread_app.THREAD) if c.comment_id == "c3"][0]
        self.assertEqual(parent.replies[-1].text, "Noted on the ticket.")

    def test_posted_author_and_text_are_escaped(self):
        self.client.post(
            "/comments",
            data={"author": "<b>bold</b>", "text": "<script>alert(1)</script>"},
        )
        html = self.page()
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<b>bold</b>", html)

    def test_new_comments_get_ids_no_other_comment_has(self):
        self.client.post("/comments", data={"author": "a", "text": "First new."})
        self.client.post("/comments", data={"author": "b", "text": "Second new."})
        self.client.post("/replies", data={"parent_id": "c3", "author": "c", "text": "Third new."})
        ids = [c.comment_id for c in all_comments(thread_app.THREAD)]
        self.assertEqual(len(ids), 11)
        self.assertEqual(len(ids), len(set(ids)))

    def test_empty_thread_still_draws_the_page(self):
        thread_app.THREAD = []
        html = self.page()
        self.assertIn('action="/comments"', html)
        self.assertIn('action="/replies"', html)

    def test_reply_to_a_missing_parent_is_404_and_changes_nothing(self):
        self.page()
        before = len(all_comments(thread_app.THREAD))
        response = self.client.post(
            "/replies", data={"parent_id": "missing", "author": "a", "text": "Lost reply."}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(all_comments(thread_app.THREAD)), before)
        self.assertNotIn("Lost reply.", self.page())


if __name__ == "__main__":
    unittest.main()
