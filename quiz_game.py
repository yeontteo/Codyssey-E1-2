from default_quizzes import create_default_quizzes


class QuizGame:
    """메뉴와 게임 진행을 관리한다."""

    LINE = "=" * 40
    MENU_ITEMS = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")
    EXIT_NUMBER = len(MENU_ITEMS)

    def __init__(self):
        self.quizzes = create_default_quizzes()

    def run(self):
        """프로그램을 실행하고, 입력이 중단되어도 안전하게 끝낸다."""
        try:
            self.show_title()
            self.menu_loop()
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")

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

    def handle_choice(self, choice):
        """선택한 번호에 맞는 기능을 실행한다."""
        if choice == 1:
            self.play()
        elif choice == 2:
            print("🚧 퀴즈 추가는 준비 중입니다.")
        elif choice == 3:
            print("🚧 퀴즈 목록은 준비 중입니다.")
        elif choice == 4:
            print("🚧 점수 확인은 준비 중입니다.")

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
        """맞힌 개수를 100점 만점 점수로 바꿔 출력한다."""
        score = round(correct / total * 100)
        print(self.LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
