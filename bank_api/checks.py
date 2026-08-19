from http import HTTPStatus
from requests import Response


class HttpCheck:

    # 200
    @staticmethod
    def assert_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    # 201
    @staticmethod
    def assert_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    # 400
    @staticmethod
    def assert_bad_request():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    # 404
    @staticmethod
    def assert_not_found():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text
        return confirm
