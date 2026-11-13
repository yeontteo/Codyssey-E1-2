# quiz_game.py: 게임 전체를 관리하는 QuizGame 클래스.
# 맡는 일: 메뉴 표시, 입력 검증, 퀴즈 풀기/추가/목록/점수, 저장/불러오기 흐름.
# 파일을 실제로 읽고 쓰는 일은 QuizStorage에 맡긴다.

from default_quizzes import create_default_quizzes  # 기본 퀴즈 5개를 만드는 함수
from quiz import Quiz                               # 퀴즈 한 문제 클래스
from quiz_storage import STATE_PATH, QuizStorage    # state.json 경로와 파일 입출력 클래스


class QuizGame:
    """메뉴와 게임 진행을 관리한다. 파일 처리는 QuizStorage에 맡긴다."""

    # ── 클래스 속성 ──────────────────────────────────────────────
    # 모든 QuizGame 객체가 함께 쓰는 고정값이다. self.LINE처럼 꺼내 쓴다.
    # 여러 곳에서 쓰는 값을 한 곳에 모아 두면, 바꿀 때 여기만 고치면 된다.
    LINE = "=" * 40       # 문자열 * 숫자 = 그 문자열을 숫자만큼 반복 ("====...")
    THIN_LINE = "-" * 40
    NO_QUIZ_MESSAGE = "📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요."
    # 튜플(tuple): 리스트와 비슷하지만 바꿀 수 없다. 메뉴 항목은 바뀌지 않으므로 튜플로 둔다.
    MENU_ITEMS = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")
    # 종료 번호 = 메뉴 개수(5). 메뉴가 늘어나도 종료 번호가 자동으로 맞춰진다.
    EXIT_NUMBER = len(MENU_ITEMS)

    # ── 초기화 ──────────────────────────────────────────────────
    def __init__(self, state_path=STATE_PATH):
        # QuizGame()으로 객체를 만들 때 자동 실행된다.
        # 객체가 다른 객체(QuizStorage)를 속성으로 가지고 일을 맡기는 구조다. (구성, composition)
        self.storage = QuizStorage(state_path)
        self.reset_state()  # 퀴즈 목록과 점수 기록을 처음 상태로 만든다.

    def reset_state(self):
        """기본 퀴즈와 기록 없음 상태로 되돌린다."""
        # 처음 만들 때, 그리고 파일이 없거나 손상됐을 때 모두 이 메서드로 초기화한다.
        self.quizzes = create_default_quizzes()  # Quiz 객체가 담긴 list
        # 0이 아니라 None을 쓰는 이유: 0점은 "풀었는데 0점"이고 None은 "아직 안 풀었음"이다.
        self.best_score = None    # 최고 점수 (아직 풀지 않았으면 None)
        self.best_correct = None  # 최고 점수를 낸 게임의 정답 수
        self.best_total = None    # 최고 점수를 낸 게임의 문제 수

    # ── 실행 흐름 ────────────────────────────────────────────────
    def run(self):
        """프로그램을 실행하고, 입력이 중단되어도 저장 후 안전하게 끝낸다."""
        # 가장 바깥에서 try로 감싸서, 프로그램 어디에서 Ctrl+C가 눌려도 여기서 한 번에 처리한다.
        try:
            self.show_title()  # 제목 출력
            self.load()        # state.json 불러오기
            self.menu_loop()   # 종료를 고를 때까지 메뉴 반복
        # KeyboardInterrupt: Ctrl+C를 누르면 발생
        # EOFError: 입력 스트림이 끝났을 때 발생 (예: python main.py < /dev/null, Ctrl+Z)
        # 두 오류를 튜플로 묶어 한 번에 잡는다. 잡지 않으면 빨간 Traceback을 내며 비정상 종료된다.
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")
        # try/except 뒤에 있으므로 정상 종료든 Ctrl+C든 항상 실행된다. 종료 직전에 저장한다.
        self.save()

    def menu_loop(self):
        """종료를 선택할 때까지 메뉴를 반복한다."""
        # 언제 끝날지 미리 알 수 없으므로 for가 아니라 while True(무한 반복)를 쓰고,
        # 종료를 고르면 break로 빠져나간다.
        while True:
            self.show_menu()
            # 1~5 사이의 올바른 숫자를 받을 때까지 read_number가 알아서 다시 묻는다.
            choice = self.read_number("선택: ", 1, self.EXIT_NUMBER)
            if choice == self.EXIT_NUMBER:
                print("👋 프로그램을 종료합니다.")
                break  # while 반복을 끝낸다. → run()으로 돌아가 save()가 실행된다.
            self.handle_choice(choice)

    # ── 화면 출력 ────────────────────────────────────────────────
    def show_title(self):
        print(self.LINE)
        # .center(36): 문자열을 폭 36칸의 가운데에 오도록 양쪽에 공백을 채운다.
        print("🤪 넌센스 퀴즈 게임 🤪".center(36))

    def show_menu(self):
        print(self.LINE)
        # enumerate(..., start=1): (1, "퀴즈 풀기"), (2, "퀴즈 추가"), ... 처럼 번호와 함께 꺼낸다.
        for number, item in enumerate(self.MENU_ITEMS, start=1):
            print(f"{number}. {item}")  # f-string: {} 안의 변수 값을 문자열에 넣는다.
        print(self.LINE)

    # ── 입력 처리 ────────────────────────────────────────────────
    def read_number(self, prompt, low, high):
        """low 이상 high 이하의 정수를 입력받을 때까지 반복한다."""
        # 메뉴(1~5), 정답(1~4), 정답 번호 등록(1~4)에서 모두 이 메서드 하나를 쓴다.
        # 범위를 매개변수(low, high)로 받기 때문에 재사용할 수 있다.
        guide = f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요."
        while True:
            # input()은 항상 문자열(str)을 돌려준다. .strip()으로 앞뒤 공백을 지운다. (" 1 " → "1")
            text = input(prompt).strip()

            # 1) 빈 입력: 빈 문자열("")은 조건문에서 False로 취급된다.
            if not text:
                print(f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue  # 아래 코드를 건너뛰고 while의 처음으로 돌아가 다시 입력받는다.

            # 2) 숫자 변환: "abc"를 int()로 바꾸면 ValueError가 난다. try/except로 잡는다.
            try:
                number = int(text)  # str → int 변환
            except ValueError:
                print(guide)
                continue

            # 3) 범위 검사: 파이썬은 low <= number <= high처럼 비교를 이어 쓸 수 있다.
            if low <= number <= high:
                return number  # 올바른 값이면 돌려주고 메서드(반복)를 끝낸다.
            print(guide)  # 범위 밖(예: 0, 9)이면 안내 후 while 처음으로 돌아간다.

    def read_text(self, prompt):
        """비어 있지 않은 문자열을 입력받을 때까지 반복한다."""
        # 퀴즈 추가에서 문제와 선택지를 받을 때 쓴다. 공백만 입력해도 strip() 후 빈 값이 되어 걸러진다.
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")

    def handle_choice(self, choice):
        """선택한 번호에 맞는 기능을 실행한다."""
        # if/elif: 위에서부터 차례로 검사해 처음으로 맞는 하나만 실행한다.
        # 종료(5)는 menu_loop에서 먼저 처리하므로 여기서는 1~4만 다룬다.
        if choice == 1:
            self.play()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.list_quizzes()
        elif choice == 4:
            self.show_score()

    # ── 1. 퀴즈 풀기 ─────────────────────────────────────────────
    def play(self):
        """모든 퀴즈를 차례로 출제하고 결과를 보여 준다."""
        # 빈 리스트([])는 False로 취급된다. 퀴즈가 없으면 안내하고 바로 끝낸다.
        # (먼저 빠져나가 두면 아래 코드는 퀴즈가 있다는 전제로 쓸 수 있다.)
        if not self.quizzes:
            print(self.NO_QUIZ_MESSAGE)
            return

        total = len(self.quizzes)  # 전체 문제 수
        correct = 0                # 맞힌 개수 (0에서 시작해 맞힐 때마다 1씩 증가)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")  # \n은 줄바꿈
        # 문제 수가 정해져 있으므로 while이 아니라 for로 처음부터 끝까지 돈다.
        for number, quiz in enumerate(self.quizzes, start=1):
            print(self.THIN_LINE)
            quiz.display(number)                            # 출력은 Quiz 객체가 담당
            selected = self.read_number("정답 입력: ", 1, 4)  # 1~4 검증된 숫자를 받는다
            if quiz.is_correct(selected):                   # 정답 판정도 Quiz 객체가 담당
                print("✅ 정답입니다!\n")
                correct += 1  # correct = correct + 1 과 같다
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")
        self.show_result(correct, total)

    def show_result(self, correct, total):
        """점수를 계산해 출력하고, 최고 점수를 넘으면 갱신해 저장한다."""
        # 100점 만점으로 환산한다. 퀴즈를 추가하면 문제 수가 달라지므로 정답 수보다 비율이 공정하다.
        # round(): 반올림해서 정수로 만든다. (예: 2/3*100 = 66.66... → 67)
        # total은 play()에서 0이 아님을 확인했으므로 0으로 나누는 오류가 나지 않는다.
        score = round(correct / total * 100)
        print(self.LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        # update_best_score가 True를 돌려줄 때(새 기록일 때)만 축하 메시지를 내고 바로 저장한다.
        if self.update_best_score(score, correct, total):
            print("🎉 새로운 최고 점수입니다!")
            self.save()
        print(self.LINE)

    def update_best_score(self, score, correct, total):
        """최고 점수보다 높으면 기록을 바꾸고 True를 돌려준다."""
        # 기록이 있고(None이 아니고), 이번 점수가 기존 기록 이하면 갱신하지 않는다.
        # 같은 점수도 갱신하지 않는다. (<= 이므로)
        if self.best_score is not None and score <= self.best_score:
            return False
        # 첫 게임(best_score가 None)이거나 더 높은 점수면 기록을 바꾼다.
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        return True

    # ── 4. 점수 확인 ─────────────────────────────────────────────
    def show_score(self):
        """최고 점수를 출력한다."""
        if self.best_score is None:
            # 아직 한 번도 풀지 않은 경우
            print("📭 아직 퀴즈를 푼 기록이 없습니다.")
        elif self.best_correct is None or self.best_total is None:
            # 미션 예시처럼 best_score만 저장된 파일을 불러온 경우
            print(f"🏆 최고 점수: {self.best_score}점")
        else:
            # 괄호 안에서는 문자열을 여러 줄로 나눠 써도 하나로 이어진다.
            print(f"🏆 최고 점수: {self.best_score}점 "
                  f"({self.best_total}문제 중 {self.best_correct}문제 정답)")

    # ── 2. 퀴즈 추가 ─────────────────────────────────────────────
    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.read_text("문제를 입력하세요: ")
        # 리스트 컴프리헨션: [식 for 변수 in 범위]
        # range(1, 5)는 1, 2, 3, 4. 선택지 1~4를 차례로 입력받아 리스트 하나로 만든다.
        # 아래 4줄과 같은 뜻이다:
        #   choices = []
        #   for number in range(1, 5):
        #       choices.append(self.read_text(f"선택지 {number}: "))
        choices = [self.read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = self.read_number("정답 번호 (1-4): ", 1, 4)

        # 입력이 모두 끝난 뒤에 append한다. 도중에 Ctrl+C가 나면 여기까지 오지 않으므로
        # 반쯤 입력된 퀴즈가 목록에 들어가지 않는다.
        self.quizzes.append(Quiz(question, choices, answer))
        # 종료 때까지 기다리지 않고 바로 저장한다. save()는 성공하면 True, 실패하면 False.
        if self.save():
            print("\n✅ 퀴즈가 추가되었습니다!")
        else:
            print("\n⚠️ 퀴즈는 추가했지만 파일에 저장하지 못해 종료하면 사라질 수 있습니다.")

    # ── 3. 퀴즈 목록 ─────────────────────────────────────────────
    def list_quizzes(self):
        """등록된 퀴즈의 문제를 번호와 함께 출력한다."""
        if not self.quizzes:
            print(self.NO_QUIZ_MESSAGE)
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(self.THIN_LINE)
        # 풀기 전에 답이 보이면 안 되므로 문제만 출력한다.
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(self.THIN_LINE)

    # ── 파일 불러오기 ────────────────────────────────────────────
    def load(self):
        """state.json을 불러온다. 실패하면 기본 데이터로 시작한다."""
        # try 안에서 오류가 나면, 오류 종류에 맞는 except 하나로 이동한다.
        # 위에서부터 차례로 검사하므로 구체적인 오류(FileNotFoundError)를 먼저 쓴다.
        # (FileNotFoundError도 OSError의 한 종류라서 순서가 바뀌면 OSError에 먼저 잡힌다.)
        try:
            # storage.read()가 파일을 dict로 읽고, apply_state()가 검사 후 게임에 반영한다.
            self.apply_state(self.storage.read())
        except FileNotFoundError:
            # 파일이 없음 = 첫 실행
            self.reset_state()
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
        except ValueError:
            # 깨진 JSON, 잘못된 인코딩, 형식 오류는 모두 ValueError 계열이다.
            self.reset_state()
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈로 복구합니다.")
        except OSError as error:
            # 권한 문제 등 그 밖의 읽기 오류. as error로 오류 내용을 받아 함께 보여 준다.
            self.reset_state()
            print(f"⚠️ 저장 파일을 읽지 못해 기본 퀴즈로 시작합니다. ({error})")
        else:
            # else: try 안에서 오류가 하나도 나지 않았을 때만 실행된다.
            # 조건부 표현식: A if 조건 else B → 조건이 참이면 A, 거짓이면 B
            best = "기록 없음" if self.best_score is None else f"{self.best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best})")

    def apply_state(self, data):
        """불러온 데이터를 검사한 뒤 게임 상태에 반영한다."""
        # 최상위가 dict인지, 필수 키("quizzes", "best_score")가 있는지 확인한다.
        # "키" in 딕셔너리 → 그 키가 있으면 True
        if not isinstance(data, dict) or "quizzes" not in data or "best_score" not in data:
            raise ValueError("필수 항목이 없습니다.")
        if not isinstance(data["quizzes"], list):
            raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

        # 먼저 지역 변수에 담아 전부 검사한다. 하나라도 틀리면 ValueError가 나서 load()로 넘어간다.
        # 퀴즈 dict 하나하나를 Quiz.from_dict로 검사하며 Quiz 객체 리스트로 바꾼다.
        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        best_score = self.check_record(data["best_score"], 100)  # 0~100 또는 None
        # .get()은 키가 없으면 None을 돌려준다. 미션 예시처럼 best_score만 있는 파일도 읽을 수 있다.
        best_correct = self.check_record(data.get("best_correct"), None)
        best_total = self.check_record(data.get("best_total"), None)

        # 검사를 모두 통과한 뒤에 한꺼번에 반영한다.
        # 중간에 오류가 나도 게임 상태가 반쯤만 바뀐 채로 남지 않는다.
        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total

    @staticmethod
    def check_record(value, high):
        """기록 값이 None이거나 0 이상의 정수인지 확인한다."""
        # self를 쓰지 않는 검사 함수라 정적 메서드로 두었다. high가 None이면 상한을 검사하지 않는다.
        if value is None:
            return None
        # type(value) is not int: True/False(bool)나 "80"(str)처럼 정수가 아닌 값을 막는다.
        if type(value) is not int or value < 0 or (high is not None and value > high):
            raise ValueError("기록 값이 올바르지 않습니다.")
        return value

    # ── 파일 저장 ────────────────────────────────────────────────
    def save(self):
        """게임 상태를 state.json에 저장하고 성공 여부를 돌려준다."""
        # JSON으로 저장할 수 있게 기본 타입(dict, list, int, None)으로만 구성한다.
        # Quiz 객체는 to_dict()로 dict로 바꾼다.
        # 파이썬 None은 JSON에서 null로 저장된다.
        state = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            self.storage.write(state)
        except OSError as error:
            # 쓰기 실패(권한 없음 등)해도 프로그램을 멈추지 않고 안내만 한다.
            print(f"⚠️ 데이터를 저장하지 못했습니다. ({error})")
            return False
        return True
