# quiz_storage.py: state.json 파일을 읽고 쓰는 일만 맡는 QuizStorage 클래스.
# 게임(QuizGame)은 "무엇을 저장할지"만 정하고, "어떻게 파일에 쓸지"는 이 클래스가 맡는다.
# 저장 방식이 바뀌어도 이 파일만 고치면 된다.

import json               # 파이썬 데이터(dict, list 등) <-> JSON 문자열 변환
from pathlib import Path  # 파일 경로를 운영체제와 관계없이 다루는 표준 라이브러리

# __file__은 지금 이 파일(quiz_storage.py)의 경로다. .parent는 그 파일이 있는 폴더(프로젝트 루트).
# 그래서 어느 폴더에서 `python main.py`를 실행해도 항상 프로젝트 루트의 state.json을 쓴다.
# 그냥 "state.json"이라고 쓰면 "터미널의 현재 위치" 기준이 되어 실행 위치마다 파일이 달라진다.
STATE_PATH = Path(__file__).parent / "state.json"


class QuizStorage:
    """게임 데이터를 JSON 파일로 읽고 쓴다."""

    def __init__(self, path=STATE_PATH):
        # path를 넘기지 않으면 기본값 STATE_PATH를 쓴다. (테스트할 때 다른 경로를 넣을 수 있다.)
        self.path = Path(path)

    def read(self):
        """파일을 읽어 파이썬 데이터로 돌려준다. 오류는 호출한 쪽에서 처리한다."""
        # with open(...) as file: 블록이 끝나면 오류가 나더라도 파일을 자동으로 닫는다.
        # "r" = 읽기 모드. encoding="utf-8"을 꼭 지정한다. (Windows 기본값 cp949로 읽으면 한글이 깨진다.)
        # json.load(file): 파일의 JSON 문자열을 파이썬 dict/list로 바꾼다.
        # 여기서 생길 수 있는 오류:
        #   FileNotFoundError: 파일이 없음 (첫 실행)
        #   json.JSONDecodeError: JSON 문법이 깨짐 (ValueError의 한 종류)
        #   UnicodeDecodeError: UTF-8이 아닌 파일 (역시 ValueError의 한 종류)
        # 이 오류들은 여기서 잡지 않고 QuizGame.load()로 넘긴다. 어떻게 안내할지는 게임이 정한다.
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def write(self, state):
        """임시 파일에 다 쓴 뒤 교체해서, 저장 중 문제가 생겨도 기존 파일을 지킨다."""
        # state.json에 바로 쓰면, 쓰는 도중 오류가 났을 때 파일이 반쯤 쓰인 채로 망가진다.
        # 그래서 state.json.tmp에 먼저 끝까지 쓰고, 성공하면 그때 state.json과 바꿔치기한다.
        temp_path = self.path.with_name(self.path.name + ".tmp")
        # "w" = 쓰기 모드(파일이 있으면 내용을 지우고 새로 쓴다).
        with open(temp_path, "w", encoding="utf-8") as file:
            # json.dump(데이터, 파일): 파이썬 데이터를 JSON 문자열로 바꿔 파일에 쓴다.
            # ensure_ascii=False: 한글을 "\ud55c" 같은 유니코드 코드가 아니라 글자 그대로 저장한다.
            # indent=4: 사람이 읽기 좋게 4칸 들여쓰기로 저장한다.
            json.dump(state, file, ensure_ascii=False, indent=4)
        # 임시 파일을 진짜 파일 이름으로 바꾼다. 기존 state.json은 이 순간 한 번에 교체된다.
        # 실패하면 OSError가 나고, QuizGame.save()가 잡아서 안내한다.
        temp_path.replace(self.path)
