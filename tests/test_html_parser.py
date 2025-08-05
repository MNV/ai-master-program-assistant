import pytest
from parsers.html_parser import get_program_info

class DummyResp:
    text = (
        '<html><head><title>Test</title></head>'
        '<body><h1>AI Program</h1>'
        '<div class="program-description">Описание программы</div>'
        'Менеджер программы<div>Ivan Ivanov</div>'
        '</body></html>'
    )
    def raise_for_status(self):
        pass

@pytest.fixture(autouse=True)
def patch_requests(monkeypatch):
    import requests
    monkeypatch.setattr(requests, 'get', lambda url: DummyResp())


def test_get_program_info_fields():
    info = get_program_info('dummy_url')
    assert info['title'] == 'AI Program'
    assert 'Описание программы' in info['description']
    assert info['manager'] == 'Ivan Ivanov'
