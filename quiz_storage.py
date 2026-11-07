import json
from pathlib import Path

# 실행 위치와 관계없이 프로젝트 루트의 state.json을 사용한다.
STATE_PATH = Path(__file__).parent / "state.json"


class QuizStorage:
    """게임 데이터를 JSON 파일로 읽고 쓴다."""

    def __init__(self, path=STATE_PATH):
        self.path = Path(path)

    def read(self):
        """파일을 읽어 파이썬 데이터로 돌려준다. 오류는 호출한 쪽에서 처리한다."""
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def write(self, state):
        """임시 파일에 다 쓴 뒤 교체해서, 저장 중 문제가 생겨도 기존 파일을 지킨다."""
        temp_path = self.path.with_name(self.path.name + ".tmp")
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=4)
        temp_path.replace(self.path)
