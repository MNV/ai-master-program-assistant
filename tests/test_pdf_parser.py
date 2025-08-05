import re
import pytest
from parsers.pdf_parser import parse_study_plan

# Патчим extract_text
@pytest.fixture(autouse=True)
def patch_extract(monkeypatch):
    def fake_extract_text(path):
        return (
            "Обязательные дисциплины. 1 семестр\n"
            "Математический анализ\n"
            "Линейная алгебра\n"
            "Пул выборных дисциплин. 2 семестр\n"
            "Эмпатичная коммуникация / Empathetic communication\n"
        )
    monkeypatch.setattr('parsers.pdf_parser.extract_text', fake_extract_text)


def test_parse_study_plan_mandatory_and_elective():
    courses = parse_study_plan('dummy.pdf')
    # Обязательный
    assert any(
        c['name'] == 'Математический анализ' and c['semester'] == 1 and c['type'] == 'обязательный'
        for c in courses
    )
    # Электив
    assert any(
        'Эмпатичная коммуникация' in c['name'] and c['semester'] == 2 and c['type'] == 'электив'
        for c in courses
    )
