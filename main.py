import sys

from quiz_game import QuizGame


def main():
    # Windows 기본 인코딩(cp949)은 이모지를 출력하지 못해서 UTF-8로 바꾼다.
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    game = QuizGame()
    game.run()


# 이 파일을 직접 실행할 때만 게임을 시작한다.
if __name__ == "__main__":
    main()
