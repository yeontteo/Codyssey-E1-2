import json
from pathlib import Path

from quiz import Quiz

# 실행 위치와 관계없이 프로젝트 루트(이 파일이 있는 폴더)의 state.json을 쓴다.
STATE_FILE = Path(__file__).parent / "state.json"
LINE = "=" * 40
THIN_LINE = "-" * 40


def create_default_quizzes():
    """기본 넌센스 퀴즈 5개를 Quiz 객체로 만들어 돌려준다."""
    return [
        Quiz("세상에서 가장 뜨거운 바다는?", ["동해", "홍해", "열바다", "태평양"], 3),
        Quiz("세상에서 가장 빠른 닭은?", ["후다닥", "치킨", "장닭", "토종닭"], 1),
        Quiz("왕이 넘어지면?", ["왕따", "킹콩", "꽈당", "퀸콩"], 2),
        Quiz("딸기가 직장을 잃으면?", ["딸기잼", "딸기우유", "산딸기", "딸기시럽"], 4),
        Quiz("사람의 몸무게가 가장 많이 나갈 때는?", ["명절 때", "철들 때", "회식 때", "야식 먹을 때"], 2),
    ]


class QuizGame:
    """메뉴, 게임 진행, 저장과 불러오기를 관리한다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()  # Quiz 객체 목록
        self.best_score = None  # 최고 점수. 아직 풀지 않았으면 None (0점과 구분)

    # ---------- 실행 흐름 ----------

    def run(self):
        """메뉴를 반복하고, 어떻게 끝나든 저장한 뒤 종료한다."""
        try:
            print(LINE)
            print("🤪 넌센스 퀴즈 게임 🤪".center(36))
            self.load()
            while True:
                self.show_menu()
                choice = self.input_number("선택: ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                else:
                    print("👋 프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C(KeyboardInterrupt)나 입력 종료(EOFError)가 나도 오류 없이 끝낸다.
            print("\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")
        self.save()

    def show_menu(self):
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    # ---------- 입력 ----------

    def input_number(self, prompt, low, high):
        """low~high 사이의 정수를 입력받을 때까지 다시 묻는다."""
        while True:
            text = input(prompt).strip()  # 앞뒤 공백 제거
            if text == "":
                print(f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue
            try:
                number = int(text)  # "abc"처럼 숫자가 아니면 ValueError
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue
            if low <= number <= high:
                return number
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")

    def input_text(self, prompt):
        """빈 값이 아닌 글자를 입력받을 때까지 다시 묻는다."""
        while True:
            text = input(prompt).strip()
            if text != "":
                return text
            print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")

    # ---------- 메뉴 기능 ----------

    def play(self):
        """퀴즈를 차례로 출제하고 점수를 계산한다."""
        if len(self.quizzes) == 0:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(THIN_LINE)
            quiz.display(number)
            selected = self.input_number("정답 입력: ", 1, 4)
            if quiz.is_correct(selected):
                print("✅ 정답입니다!\n")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = round(correct / total * 100)  # 100점 만점으로 환산
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        # 처음 풀었거나 기존 최고 점수보다 높으면 갱신하고 바로 저장한다.
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
            self.save()
        print(LINE)

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 추가하고 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.input_text("문제를 입력하세요: ")
        choices = []
        for number in range(1, 5):
            choices.append(self.input_text(f"선택지 {number}: "))
        answer = self.input_number("정답 번호 (1-4): ", 1, 4)

        # 입력이 모두 끝난 뒤에 추가하므로, 도중에 Ctrl+C를 눌러도 반쯤 입력된 퀴즈는 남지 않는다.
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 문제를 번호와 함께 보여 준다. 정답은 보여 주지 않는다."""
        if len(self.quizzes) == 0:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    def show_score(self):
        """최고 점수를 보여 준다."""
        if self.best_score is None:
            print("📭 아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"🏆 최고 점수: {self.best_score}점")

    # ---------- 파일 저장/불러오기 ----------

    def load(self):
        """state.json을 불러온다. 없거나 손상되었으면 기본 퀴즈를 그대로 쓴다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)  # JSON 문법이 틀리면 ValueError

            quizzes = []
            for item in data["quizzes"]:  # 키가 없으면 KeyError
                quiz = Quiz(item["question"], item["choices"], item["answer"])
                # type(...) is not int: True도 1과 같다고 판단되므로 bool을 따로 막는다.
                if len(quiz.choices) != 4 or type(quiz.answer) is not int or quiz.answer not in (1, 2, 3, 4):
                    raise ValueError("퀴즈 형식이 올바르지 않습니다.")
                quizzes.append(quiz)

            best_score = data["best_score"]
            if best_score is not None and type(best_score) is not int:
                raise ValueError("점수 형식이 올바르지 않습니다.")

            # 검사를 모두 통과했을 때만 게임에 반영한다.
            self.quizzes = quizzes
            self.best_score = best_score
            best = "기록 없음" if best_score is None else f"{best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best})")
        except FileNotFoundError:
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
        except (ValueError, KeyError, TypeError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈로 복구합니다.")
        except OSError as error:
            print(f"⚠️ 저장 파일을 읽지 못해 기본 퀴즈로 시작합니다. ({error})")

    def save(self):
        """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                # ensure_ascii=False: 한글을 글자 그대로 저장, indent=4: 보기 좋게 들여쓰기
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다. ({error})")
