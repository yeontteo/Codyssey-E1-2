import sys

from quiz_game import QuizGame


def main():
    # Windows의 기본 인코딩(cp949)은 이모지를 출력하지 못하므로 UTF-8로 맞춘다.
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
