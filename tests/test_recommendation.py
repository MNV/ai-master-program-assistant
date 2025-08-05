from models.recommendation import recommend_electives
from models.course import Course


def test_recommend_electives_basic():
    courses = [
        Course(1, 'A', 4, 'обязательный'),
        Course(2, 'B', 3, 'электив'),
        Course(2, 'C', 3, 'электив'),
        Course(3, 'D', 3, 'электив'),
    ]
    bg = {'math': 5, 'prog': 4, 'ml': 3}
    recs = recommend_electives(courses, bg, top_n=2)
    assert len(recs) == 2
    assert all(r.type == 'электив' for r in recs)
