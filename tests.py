import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        # party details
        result = self.client.get("/")
        self.assertIn("Please RSVP", result.data)
        self.assertNotIn("123 Magic Unicorn Way", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertNotIn("Please RSVP", result.data)
        self.assertIn("123 Magic Unicorn Way", result.data)



class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        result = self.client.get("/games")
        self.assertIn("Apples", result.data)

        #FIXME: test that the games page displays the game from example_data()
    def test_games_not_logged_in(self):
        
        # if user not RSVP'ed, they should be redirected to "/" route

        # If there is a contradicting event to what is in the setup, include in
        # function. Ex. default for setup here is logged in, and we're testing
        # for functionality when logged out.
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = False

        # when desired result is a redirect, ensure that the 
        # "follow_redirects" clause is true
        result = self.client.get("/games", follow_redirects=True)
        self.assertNotIn("Apples", result.data)
        self.assertIn("I'm having an after-party!", result.data)


if __name__ == "__main__":
    unittest.main()
