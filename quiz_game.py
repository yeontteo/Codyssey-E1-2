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
            print("🚧 퀴즈 풀기는 준비 중입니다.")
        elif choice == 2:
            print("🚧 퀴즈 추가는 준비 중입니다.")
        elif choice == 3:
            print("🚧 퀴즈 목록은 준비 중입니다.")
        elif choice == 4:
            print("🚧 점수 확인은 준비 중입니다.")
