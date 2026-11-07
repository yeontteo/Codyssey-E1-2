import json
from pathlib import Path

from default_quizzes import create_default_quizzes
from quiz import Quiz

# 실행 위치와 관계없이 프로젝트 루트의 state.json을 사용한다.
STATE_PATH = Path(__file__).parent / "state.json"


class QuizGame:
    """메뉴와 게임 진행, 데이터 저장을 관리한다."""

    LINE = "=" * 40
    MENU_ITEMS = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")
    EXIT_NUMBER = len(MENU_ITEMS)

    def __init__(self, state_path=STATE_PATH):
        self.state_path = Path(state_path)
        self.reset_state()

    def reset_state(self):
        """기본 퀴즈와 기록 없음 상태로 되돌린다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None    # 최고 점수 (아직 풀지 않았으면 None)
        self.best_correct = None  # 최고 점수를 낸 게임의 정답 수
        self.best_total = None    # 최고 점수를 낸 게임의 문제 수

    def run(self):
        """프로그램을 실행하고, 입력이 중단되어도 저장 후 안전하게 끝낸다."""
        try:
            self.show_title()
            self.load()
            self.menu_loop()
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")
        self.save()

    def menu_loop(self):
        """종료를 선택할 때까지 메뉴를 반복한다."""
        while True:
            self.show_menu()
            choice = self.read_number("선택: ", 1, self.EXIT_NUMBER)
            if choice == self.EXIT_NUMBER:
                print("👋 프로그램을 종료합니다.")
                break
            self.handle_choice(choice)

    def show_title(self):
        print(self.LINE)
        print("🤪 넌센스 퀴즈 게임 🤪".center(36))

    def show_menu(self):
        print(self.LINE)
        for number, item in enumerate(self.MENU_ITEMS, start=1):
            print(f"{number}. {item}")
        print(self.LINE)

    def read_number(self, prompt, low, high):
        """low 이상 high 이하의 정수를 입력받을 때까지 반복한다."""
        guide = f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요."
        while True:
            text = input(prompt).strip()
            if not text:
                print(f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue
            try:
                number = int(text)
            except ValueError:
                print(guide)
                continue
            if low <= number <= high:
                return number
            print(guide)

    def read_text(self, prompt):
        """비어 있지 않은 문자열을 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")

    def handle_choice(self, choice):
        """선택한 번호에 맞는 기능을 실행한다."""
        if choice == 1:
            self.play()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.list_quizzes()
        elif choice == 4:
            self.show_score()

    def play(self):
        """모든 퀴즈를 차례로 출제하고 결과를 보여 준다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(number)
            selected = self.read_number("정답 입력: ", 1, 4)
            if quiz.is_correct(selected):
                print("✅ 정답입니다!\n")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")
        self.show_result(correct, total)

    def show_result(self, correct, total):
        """점수를 계산해 출력하고, 최고 점수를 넘으면 갱신해 저장한다."""
        score = round(correct / total * 100)
        print(self.LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.update_best_score(score, correct, total):
            print("🎉 새로운 최고 점수입니다!")
            self.save()
        print(self.LINE)

    def update_best_score(self, score, correct, total):
        """최고 점수보다 높으면 기록을 바꾸고 True를 돌려준다."""
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        return True

    def show_score(self):
        """최고 점수를 출력한다."""
        if self.best_score is None:
            print("📭 아직 퀴즈를 푼 기록이 없습니다.")
        elif self.best_correct is None or self.best_total is None:
            print(f"🏆 최고 점수: {self.best_score}점")
        else:
            print(f"🏆 최고 점수: {self.best_score}점 "
                  f"({self.best_total}문제 중 {self.best_correct}문제 정답)")

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.read_text("문제를 입력하세요: ")
        choices = [self.read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = self.read_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        if self.save():
            print("\n✅ 퀴즈가 추가되었습니다!")
        else:
            print("\n⚠️ 퀴즈는 추가했지만 파일에 저장하지 못해 종료하면 사라질 수 있습니다.")

    def list_quizzes(self):
        """등록된 퀴즈의 문제를 번호와 함께 출력한다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def load(self):
        """state.json을 불러온다. 실패하면 기본 데이터로 시작한다."""
        try:
            with open(self.state_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.apply_state(data)
        except FileNotFoundError:
            self.reset_state()
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
        except ValueError:
            # 깨진 JSON, 잘못된 인코딩, 형식 오류는 모두 ValueError 계열이다.
            self.reset_state()
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈로 복구합니다.")
        except OSError as error:
            self.reset_state()
            print(f"⚠️ 저장 파일을 읽지 못해 기본 퀴즈로 시작합니다. ({error})")
        else:
            best = "기록 없음" if self.best_score is None else f"{self.best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best})")

    def apply_state(self, data):
        """불러온 데이터를 검사한 뒤 게임 상태에 반영한다."""
        if not isinstance(data, dict) or "quizzes" not in data or "best_score" not in data:
            raise ValueError("필수 항목이 없습니다.")
        if not isinstance(data["quizzes"], list):
            raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        best_score = self.check_record(data["best_score"], 100)
        best_correct = self.check_record(data.get("best_correct"), None)
        best_total = self.check_record(data.get("best_total"), None)

        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total

    def check_record(self, value, high):
        """기록 값이 None이거나 0 이상의 정수인지 확인한다."""
        if value is None:
            return None
        if type(value) is not int or value < 0 or (high is not None and value > high):
            raise ValueError("기록 값이 올바르지 않습니다.")
        return value

    def save(self):
        """게임 상태를 state.json에 저장하고 성공 여부를 돌려준다."""
        state = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        # 임시 파일에 다 쓴 뒤 교체해서, 저장 중 문제가 생겨도 기존 파일을 지킨다.
        temp_path = self.state_path.with_name(self.state_path.name + ".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(state, file, ensure_ascii=False, indent=4)
            temp_path.replace(self.state_path)
        except OSError as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다. ({error})")
            return False
        return True
