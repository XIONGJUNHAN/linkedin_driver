class Contact:

    def _stream(self):
        'Provides item retrieval by id.'
        raise NotImplemented

    def _filter(self):
        'Provides filtering and searching on contacts.'
        raise NotImplemented

    def send_message(self):
        'Sends message to contact via LinkedIn.'


class Post:

    def _stream(self):
        'Provides item retrieval by id.'
        raise NotImplemented

    def _filter(self):
        'Provides filtering and searching on contacts.'
        raise NotImplemented

    def send_like(self):
        'Likes the post.'

    def add_comment(self):
        'Creates comment to post.'


class Comment:

    def _stream(self):
        'Provides item retrieval by id.'
        raise NotImplemented

    def _filter(self):
        'Provides filtering and searching on contacts.'
        raise NotImplemented

    def delete(self):
        'Deletes a comment.'

    def send_like(self):
        'Likes the comment.'


