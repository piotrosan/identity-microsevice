import logging

from collections import namedtuple
from urllib.parse import urlencode, urlunparse, unquote

from inrastructure.database.sql.models import User
from inrastructure.security.jwt.token import TokenFactory

logger = logging.getLogger("root")

# get from https://stackoverflow.com/questions/15799696/how-to-build-urls-in-python-with-the-standard-library

Components = namedtuple(
    typename='Components',
    field_names=['scheme', 'netloc', 'url', 'params', 'query', 'fragment']
)

def generate_url(query_parameters: dict, host: str, secure: bool, path: str):
    url = urlunparse(
        Components(
            scheme="https" if secure else "http",
            netloc=host,
            url=path,
            params="",
            query=unquote(urlencode(query_parameters)),
            fragment=''
        )
    )

    return str(url)


def generate_activation_link(
        user: User,
        host: str,
        secure: bool
) -> str:
    refresh_token = TokenFactory.create_refresh_token({
        "user_data": {
            "user_identifier": user.hash_identifier
        }
    })
    query_params = {
        'token': refresh_token.refresh_token,
        'email': user.email
    }
    return generate_url(query_params, host, secure, '/activate')


def generate_reset_password_link(
        user: User,
        host: str,
        secure: bool
):
    refresh_token = TokenFactory.create_refresh_token({
        "user_data": {
            "user_identifier": user.hash_identifier
        }
    })
    query_params = {
        'token': refresh_token.refresh_token,
    }
    return generate_url(query_params, host, secure, '/reset')


# def get_params_from_url(url: str, elements: List[str]) -> List[str]:
#     """
#
#     @param url:
#     @param elements: ['scheme', 'netloc', 'hostname', 'port', 'query', 'params']
#     @return: In the same order []
#     """
#     o = urlparse(url)
#     return [getattr(o, element) for element in elements]

