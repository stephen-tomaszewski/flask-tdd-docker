import json

from project.api.models import User


"""
# normal run
$ docker-compose exec users python -m pytest "project/tests"

# disable warnings
$ docker-compose exec users python -m pytest "project/tests" -p no:warnings

# run only the last failed tests
$ docker-compose exec users python -m pytest "project/tests" --lf

# run only the tests with names that match the string expression
$ docker-compose exec users python -m pytest "project/tests" -k "config and not test_development_config"

# stop the test session after the first failure
$ docker-compose exec users python -m pytest "project/tests" -x

# enter PDB after first failure then end the test session
$ docker-compose exec users python -m pytest "project/tests" -x --pdb

# stop the test run after two failures
$ docker-compose exec users python -m pytest "project/tests" --maxfail=2

# show local variables in tracebacks
$ docker-compose exec users python -m pytest "project/tests" -l

# list the 2 slowest tests
$ docker-compose exec users python -m pytest "project/tests" --durations=2
"""


def test_add_user(test_app, test_database):
    # has access to test_client since conftest initializes first
    client = test_app.test_client()
    # try to connect to /users and post the data
    resp = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "michael@testdriven.io was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", data=json.dumps({}), content_type="application/json",)
    # will get validate error since mission required fields
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    """Test if the api handles duplicate users."""
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database, add_user):

    # using declarative base model from SQLAlchemy to make connection
    user = add_user(username="jeffrey", email="jeffrey@testdriven.io")

    # https://flask.palletsprojects.com/en/1.1.x/api/#test-client
    # test_client is wrapper around werkzeug.test.Client()
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")  # using user atr in request string
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "jeffrey" in data["username"]
    assert "jeffrey@testdriven.io" in data["email"]


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("michael", "michael@mherman.org")
    add_user("fletcher", "fletcher@notreal.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@mherman.org" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]
