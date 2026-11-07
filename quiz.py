class Quiz:
    """퀴즈 한 문제를 표현한다."""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 문제, 선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, selected):
        """입력한 번호가 정답이면 True를 돌려준다."""
        return selected == self.answer

    def to_dict(self):
        """JSON으로 저장할 수 있도록 딕셔너리로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리를 검사해 Quiz 객체로 만든다. 형식이 틀리면 ValueError를 낸다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 형식이 올바르지 않습니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        if not cls.is_filled_text(question):
            raise ValueError("문제가 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if not all(cls.is_filled_text(choice) for choice in choices):
            raise ValueError("빈 선택지가 있습니다.")
        # bool은 int의 한 종류라서 True가 1로 통과하지 않도록 type으로 비교한다.
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 중 하나여야 합니다.")

        return cls(question, choices, answer)

    @staticmethod
    def is_filled_text(value):
        """공백이 아닌 내용이 있는 문자열이면 True를 돌려준다."""
        return isinstance(value, str) and bool(value.strip())
