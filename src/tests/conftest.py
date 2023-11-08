from html.parser import HTMLParser
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from api.main import api


class EmailHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html = {}

    def handle_starttag(self, tag, attrs):
        self.html.update({"start_tag": tag})

    def handle_endtag(self, tag):
        self.html.update({"end_tag": tag})

    def handle_data(self, data):
        self.html.update({"data": data})


@pytest.fixture(scope="module")
def email_html_parser() -> EmailHTMLParser:
    return EmailHTMLParser()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(api) as c:
        yield c
