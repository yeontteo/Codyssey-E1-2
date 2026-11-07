# E1-2 나만의 퀴즈 게임

코디세이(Codyssey) 입학연수 미션 E1-2 제출 저장소입니다. 미션 원문은 [docs/mission.md](docs/mission.md)에 있습니다.

## 1. 프로젝트 개요

터미널에서 동작하는 넌센스 퀴즈 게임입니다. Python 클래스로 코드를 역할별로 나누고, 퀴즈와 최고 점수를 `state.json`에 저장해 프로그램을 다시 실행해도 유지되도록 합니다.

## 2. 수행 체크리스트

- [x] Git 저장소 설정 (`.gitignore`, `README.md`, 첫 커밋과 푸시)
- [x] 메뉴와 공통 입력 처리
- [x] Quiz 클래스
- [ ] 기본 퀴즈 데이터 5개 이상
- [ ] 퀴즈 풀기 (브랜치 생성과 병합)
- [ ] `state.json` 저장/불러오기
- [ ] 퀴즈 추가
- [ ] 퀴즈 목록
- [ ] 점수 확인
- [ ] QuizGame 구조 정리
- [ ] README 작성
- [ ] clone/pull 실습
- [ ] 최종 검증과 스크린샷

## 3. 수행 기록

### 3.1 Git 저장소 설정

GitHub 저장소에 `Initial commit`이 이미 있어서, 로컬에서 `git init`으로 저장소를 만들고 원격을 연결한 뒤 `git pull`로 받았습니다. 전체 출력은 [docs/logs/01-git-setup.log](docs/logs/01-git-setup.log)에 있습니다.

`state.json`은 실행할 때 내용이 바뀌는 데이터이고, 없으면 기본 퀴즈로 시작하도록 만들 예정이라 `.gitignore`로 제외했습니다.

### 3.2 메뉴와 공통 입력 처리

`main.py`는 프로그램을 시작만 하고, 메뉴와 입력 처리는 `quiz_game.py`의 `QuizGame` 클래스가 맡습니다. 숫자 입력은 `read_number()` 하나로 처리해서 이후 정답 입력에서도 같은 검증을 사용합니다. 아직 만들지 않은 기능은 준비 중 안내를 출력합니다. 전체 출력은 [docs/logs/02-menu.log](docs/logs/02-menu.log)에 있습니다.

| 입력 또는 상황 | 결과 |
| --- | --- |
| `abc` | 안내 후 재입력 |
| `9`, `0` | 안내 후 재입력 |
| 빈 입력 | 안내 후 재입력 |
| ` 1 ` (앞뒤 공백) | 공백 제거 후 1번 메뉴 실행 |
| `5` | 종료 안내 후 종료 코드 0 |
| 입력 스트림 종료 (`python main.py < /dev/null`) | 안내 후 종료 코드 0 |

Windows의 기본 인코딩(cp949)에서는 출력이 파이프로 연결될 때 이모지를 출력하다가 `UnicodeEncodeError`가 발생해서, `main.py` 시작부에서 입출력 인코딩을 UTF-8로 맞췄습니다.

### 3.3 Quiz 클래스

`quiz.py`의 `Quiz` 클래스는 문제 하나를 표현합니다. 속성은 문제(`question`), 선택지 4개(`choices`), 정답 번호 1~4(`answer`)이고, `display()`가 문제를 출력하고 `is_correct()`가 정답을 확인합니다. 전체 출력은 [docs/logs/03-quiz-class.log](docs/logs/03-quiz-class.log)에 있습니다.
