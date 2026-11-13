# main.py: 프로그램의 시작점(진입점)이다.
# 실행 방법: 터미널에서 `python main.py`
# 이 파일은 게임 객체를 만들고 실행만 한다. 실제 기능은 quiz_game.py의 QuizGame이 맡는다.

import sys  # 표준 입출력(sys.stdin, sys.stdout)을 다루기 위한 표준 라이브러리

# quiz_game.py 파일에서 QuizGame 클래스를 가져온다.
from quiz_game import QuizGame


def main():
    """프로그램 전체를 시작하는 함수."""
    # Windows의 기본 인코딩은 cp949라서 이모지(🎯 등)를 출력하면
    # UnicodeEncodeError로 프로그램이 죽을 수 있다. 입출력 인코딩을 UTF-8로 바꿔 막는다.
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    game = QuizGame()  # QuizGame 클래스로 게임 객체(인스턴스)를 만든다. 이때 __init__이 실행된다.
    game.run()         # 게임을 시작한다. 메뉴 반복, 저장까지 run() 안에서 처리한다.


# 이 파일을 직접 실행했을 때만 main()을 호출한다.
# 다른 파일이 `import main`으로 가져갈 때는 게임이 저절로 시작되지 않는다.
if __name__ == "__main__":
    main()
