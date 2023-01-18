import os
import app
import unittest
import tempfile


class SiteTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('Zahar', 'z-1996')
        assert 'You were logged in'.encode() in rv.data
        rv = self.logout()
        assert 'You were logged out'.encode() in rv.data
        rv = self.login('Kolya', 'z-1996')
        assert 'Invalid username'.encode() in rv.data
        rv = self.login('Zahar', '122')
        assert 'Invalid password'.encode() in rv.data

    # def test_empty_db(self):
    # проходит тест только когда база данных реально пустая
    #     rv = self.app.get('/posts')
    #     assert 'Еще нет заметок на сайте, будьте первым!!!'.encode() in rv.data
    #
    # def test_messages(self):
    # тест проходит, но тестовое сообщение не удаляется из базы данных и видно на сайте
    #     rv = self.app.post('/create_article', data=dict(
    #         title='<Hello>',
    #         text='<strong>HTML</strong> allowed here'
    #     ), follow_redirects=True)
    #     assert 'Еще нет заметок на сайте, будьте первым!!!'.encode() not in rv.data
    #     assert '&lt;Hello&gt;'.encode() in rv.data


if __name__ == '__main__':
    unittest.main()

