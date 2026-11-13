class Quiz:
    """퀴즈 한 문제를 표현한다."""

    def __init__(self, question, choices, answer):
        # Quiz(...)로 객체를 만들 때 자동으로 실행된다. self는 만들어지는 객체 자신이다.
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 문제, 선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        # enumerate(..., start=1): 선택지를 꺼내면서 1부터 번호를 붙인다.
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
