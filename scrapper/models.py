from mongoengine import FloatField, Document, StringField


class Submission(Document):
    id = StringField(primary_key=True, max_length=10, required=True)
    subreddit = StringField(max_length=200, required=True)
    title = StringField(max_length=300, required=True)
    timestamp = FloatField(required=True)

    meta = {
        'indexes': [
            {'fields': ['$title'],
             'default_language': 'english'}
        ]
    }


class Comment(Document):
    id = StringField(primary_key=True,  max_length=10, required=True)
    subreddit = StringField(max_length=200, required=True)
    content = StringField(max_length=1000, required=True)
    timestamp = FloatField(required=True)

    meta = {
        'indexes': [
            {'fields': ['$content'],
             'default_language': 'english'}
        ]
    }