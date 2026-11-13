# quiz.py: 퀴즈 "한 문제"를 표현하는 Quiz 클래스.
# 문제, 선택지, 정답은 항상 함께 다니는 데이터라 하나의 클래스로 묶었다.
# 클래스 = 설계도, Quiz(...)로 만든 각각의 퀴즈 = 객체(인스턴스)


class Quiz:
    """퀴즈 한 문제를 표현한다."""

    def __init__(self, question, choices, answer):
        # __init__은 Quiz(...)로 객체를 만들 때 자동으로 실행되는 초기화 메서드다.
        # self는 "지금 만들어지는 그 객체 자신"이다.
        # self.이름 = 값 으로 저장한 것이 속성(attribute)이고, 객체마다 따로 저장된다.
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 문제, 선택지를 출력한다."""
        # 문제 번호는 출제 순서에 따라 바뀌므로 속성으로 저장하지 않고 매개변수로 받는다.
        print(f"[문제 {number}]")
        print(self.question)
        print()  # 빈 줄
        # enumerate(..., start=1): 선택지를 하나씩 꺼내면서 1부터 번호를 함께 준다.
        # 예) (1, "동해"), (2, "홍해"), ...
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, selected):
        """입력한 번호가 정답이면 True를 돌려준다."""
        # == 비교 결과는 True 또는 False(bool)이므로 그대로 반환한다.
        # selected는 QuizGame.read_number()에서 이미 1~4로 검증된 값만 들어온다.
        return selected == self.answer

    def to_dict(self):
        """JSON으로 저장할 수 있도록 딕셔너리로 바꾼다."""
        # json 모듈은 dict, list, str, int, None 같은 기본 타입만 저장할 수 있다.
        # Quiz 객체는 직접 만든 타입이라 그대로 저장할 수 없어서 dict로 바꿔 준다.
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리를 검사해 Quiz 객체로 만든다. 형식이 틀리면 ValueError를 낸다."""
        # @classmethod: 객체가 아직 없을 때 호출하는 메서드다. self 대신 클래스 자체(cls)를 받는다.
        # 사용 예) Quiz.from_dict({"question": ..., "choices": [...], "answer": 2})

        # 파일에서 읽은 값이 딕셔너리가 아니면 퀴즈로 만들 수 없다.
        if not isinstance(data, dict):
            raise ValueError("퀴즈 형식이 올바르지 않습니다.")

        # data["키"]는 키가 없으면 KeyError가 나지만, data.get("키")는 None을 돌려준다.
        # None이면 아래 검사에서 걸러지므로 오류 종류를 ValueError 하나로 통일할 수 있다.
        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        # raise: 문제가 있으면 일부러 오류를 발생시켜, 호출한 쪽(QuizGame.load)이 처리하게 한다.
        if not cls.is_filled_text(question):
            raise ValueError("문제가 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        # all(...): 안의 값이 전부 True일 때만 True. 선택지 4개가 모두 내용이 있는지 확인한다.
        if not all(cls.is_filled_text(choice) for choice in choices):
            raise ValueError("빈 선택지가 있습니다.")
        # bool은 int의 한 종류라서 True가 1로 통과하지 않도록 type으로 비교한다.
        # (isinstance(True, int)는 True가 나오기 때문에 isinstance로는 막을 수 없다.)
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 중 하나여야 합니다.")

        # 모든 검사를 통과하면 Quiz 객체를 만들어 돌려준다. cls(...)는 Quiz(...)와 같다.
        return cls(question, choices, answer)

    @staticmethod
    def is_filled_text(value):
        """공백이 아닌 내용이 있는 문자열이면 True를 돌려준다."""
        # @staticmethod: self도 cls도 쓰지 않는 도우미 함수를 클래스 안에 둘 때 쓴다.
        # value.strip()은 앞뒤 공백을 지운 문자열이고, 빈 문자열("")은 bool로 바꾸면 False다.
        return isinstance(value, str) and bool(value.strip())
