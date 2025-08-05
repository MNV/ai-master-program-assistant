import re
from typing import List, Dict, Optional
from pdfminer.high_level import extract_text


def parse_study_plan(pdf_path: str) -> List[Dict[str, str]]:
    """
    Извлекает список курсов из учебного плана:
      - Ищет разделы по заголовкам:
        * "Обязательные дисциплины. X семестр" → обязательные
        * "Пул выборных дисциплин. X семестр" → элективы
        * скрытые заголовки формата "<Название курса>. X семестр"
      - Игнорирует мусорные строки:
        * состоящие только из цифр, запятых или пробелов
        * одиночные символы
        * без кириллических букв или длиной <3
      - Возвращает список словарей с полями:
        semester: int, name: str, type: "обязательный"|"электив"
    """
    # Извлечение текста
    text = extract_text(pdf_path)
    # Разбиение на непустые строки
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    courses: List[Dict[str, str]] = []
    section: Optional[str] = None  # 'mandatory' или 'elective'
    semester: Optional[int] = None

    # Префиксы, которые пропускаем
    skip_prefixes = (
        "Учебный план", "ОП ", "Наименование", "Блок ",
        "Индивидуальная профессиональная подготовка",
    )

    for line in lines:
        # Пропускаем заголовки и нумерацию
        if any(line.startswith(pref) for pref in skip_prefixes):
            continue
        # Пропускаем строки из одних цифр/запятых/пробелов
        if re.fullmatch(r"[\d,\s]+", line):
            continue
        # Пропускаем одиночные символы
        if len(line) == 1:
            continue
        # Явный заголовок обязательных дисциплин
        m_mand = re.match(r"Обязательные дисциплины\.\s*(\d+)\s*семестр", line)
        if m_mand:
            semester = int(m_mand.group(1))
            section = "mandatory"
            continue
        # Явный заголовок пула элективов
        m_elect = re.match(r"Пул выборных дисциплин\.\s*(\d+)\s*семестр", line)
        if m_elect:
            semester = int(m_elect.group(1))
            section = "elective"
            continue
        # Скрытый заголовок: "Курс. X семестр"
        m_hdr = re.match(r"^(.+?)\.\s*(\d+)\s*семестр$", line)
        if m_hdr and (section is None or not line.startswith(("Обязательные", "Пул"))):
            name = m_hdr.group(1).strip()
            semester = int(m_hdr.group(2))
            section = "mandatory"
            courses.append({
                "semester": semester,
                "name": name,
                "type": "обязательный",
            })
            continue
        # Строка курса внутри выбранного раздела
        if section and semester is not None:
            # Фильтруем мусорные строки: должны содержать минимум одну кириллическую букву
            if not re.search(r"[А-Яа-яЁё]", line):
                continue
            # Отбрасываем короткие строки (<3 символов)
            if len(line) < 3:
                continue
            courses.append({
                "semester": semester,
                "name": line,
                "type": "обязательный" if section == "mandatory" else "электив",
            })
    return courses
