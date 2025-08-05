from dataclasses import dataclass


@dataclass
class Course:
    """
    Represents a single course in the study plan.
    """
    semester: int  # Семестр курса
    name: str  # Название курса
    credits: int  # Число кредитов
    type: str  # Тип: "обязательный" или "электив"
