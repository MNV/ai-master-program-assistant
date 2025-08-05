from typing import List
from .course import Course


def recommend_electives(
        courses: List[Course],
        background: dict,
        top_n: int = 3
) -> List[Course]:
    """
    Простейшая логика рекомендаций элективов:
    - Вычисляет средний уровень пользователя по бэкграунду.
    - Фильтрует только элективные курсы.
    - Возвращает первые top_n курсов.

    background: {"math": int, "prog": int, "ml": int}
    """
    # средний уровень знаний
    avg_lvl = sum(background.values()) // len(background)

    # оставляем только элективы
    electives = [c for c in courses if c.type.lower() == "электив"]

    # TODO: позже можно ранжировать по сложности
    return electives[:top_n]
