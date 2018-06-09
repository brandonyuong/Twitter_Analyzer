from database import CursorFromConnectionFromPool
import oauth2
from twitter_utils import consumer
import json


class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name  # 'self.email' is the object, 'email' is the parameter
        self.id = id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def __repr__(self):  # prints the object
        return "<User {}>".format(self.screen_name)


    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO userstwitter (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
                           (self.screen_name, self.oauth_token, self.oauth_token_secret))


    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM userstwitter WHERE screen_name=%s', (screen_name,))  # Cursor stores data
            """ (email,) is a tuple. Needs a ',' 
            because (email) is an arbitrary syntax that could mean (5 + 5) +2 for e.g."""
            user_data = cursor.fetchone()  # fetchone is first row
            if user_data:  # Compares and returns True or False. If 'user_data' exists, then this returns True
                return cls(screen_name=user_data[1], oauth_token=user_data[2],
                       oauth_token_secret=user_data[3], id=user_data[0])
            #else:
            #    return None
            # This section is logically sound, but 'return None' is already the default output, so it is redundant
            # 'return None' is also equivalent to False in a Boolean comparison

    def twitter_request(self, uri, verb='GET'):
        # Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # Make Twitter API calls!
        response, content = authorized_client.request(uri, verb)
        if response.status != 200:
            print("Error occurred when searching!")

        return json.loads(content.decode('utf-8'))
        # loads is load string

