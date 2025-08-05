import requests
from bs4 import BeautifulSoup
from typing import Dict


def get_program_info(program_url: str) -> Dict[str, str]:
    """
    1. Получает HTML страницы программы методом requests.get  [oai_citation:9‡TutorialsPoint](https://www.tutorialspoint.com/downloading-files-from-web-using-python?utm_source=chatgpt.com).
    2. Парсит его через BeautifulSoup ('html.parser') и извлекает:
       - title из первого <h1>
       - description из div с классом 'program-description'
       - manager: текст в блоке после заголовка "Менеджер программы"  [oai_citation:10‡Crummy](https://www.crummy.com/software/BeautifulSoup/bs4/doc/?utm_source=chatgpt.com) [oai_citation:11‡GeeksforGeeks](https://www.geeksforgeeks.org/python/beautifulsoup-search-by-text-inside-a-tag/?utm_source=chatgpt.com)
    """
    resp = requests.get(program_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    desc_elem = soup.find("div", class_="program-description")
    description = desc_elem.get_text(strip=True) if desc_elem else ""

    manager = ""
    mgr_label = soup.find(text="Менеджер программы")
    if mgr_label:
        next_div = mgr_label.find_next("div")
        manager = next_div.get_text(strip=True) if next_div else ""

    return {
        "title": title,
        "description": description,
        "manager": manager
    }
