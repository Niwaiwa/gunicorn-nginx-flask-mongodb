import pytest
import json
from tests.test_app import client


def register(client, email, password, password2):
    return client.post('/register', json={'email': email, 'password': password, 'password2': password})

def login(client, email, password):
    return client.post('/login', json={'email': email, 'password': password})

def logout(client, authorization):
    return client.post('/logout', headers={'Authorization': authorization})

def delete_user(client, authorization):
    return client.delete('/user', headers={'Authorization': authorization})


class TestAuth:

    def test_home(self, client):
        """test home"""
        rv = client.get('/')
        assert b'Server running' in rv.data

    def test_jwt(self, client):
        """test jwt authentication"""
        rv = client.get('/logout', data=dict())
        res_data = json.loads(rv.data)
        assert 401 == rv.status_code
        assert 7 == res_data.get('header').get('code')

    def test_register_logout(self, client):
        """test register logout"""
        email = "test@gmail.com"
        password = "123456"

        rv = register(client, email, password, password)
        res_data = json.loads(rv.data)
        assert 201 == rv.status_code
        assert 0 == res_data.get('header').get('code')
        assert email == res_data.get('body').get('email')
        assert "" != rv.headers.get('Authorization', "")
        assert None != rv.headers.get('Authorization', None)

        authorization = rv.headers.get('Authorization')
        rv = logout(client, authorization)
        assert 204 == rv.status_code

    def test_login_delete(self, client):
        """test register logout"""
        email = "test@gmail.com"
        password = "123456"

        rv = login(client, email, password)
        res_data = json.loads(rv.data)
        assert 200 == rv.status_code
        assert 0 == res_data.get('header').get('code')
        assert email == res_data.get('body').get('email')
        assert "" != rv.headers.get('Authorization', "")
        assert None != rv.headers.get('Authorization', None)

        authorization = rv.headers.get('Authorization')
        rv = delete_user(client, authorization)
        assert 204 == rv.status_code
