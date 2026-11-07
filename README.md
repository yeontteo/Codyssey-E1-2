# E1-2 나만의 퀴즈 게임

코디세이(Codyssey) 입학연수 미션 E1-2 제출 저장소입니다. 미션 원문은 [docs/mission.md](docs/mission.md)에 있습니다.

## 1. 프로젝트 개요

터미널에서 동작하는 넌센스 퀴즈 게임입니다. 메뉴에서 번호를 골라 퀴즈를 풀고, 새 퀴즈를 추가하고, 목록과 최고 점수를 확인할 수 있습니다.

Python 클래스로 코드를 역할별로 나누고, 퀴즈와 최고 점수를 `state.json`에 저장해 프로그램을 다시 실행해도 유지되도록 했습니다. 변경 이력은 기능 단위 커밋과 브랜치 병합으로 Git에 기록했습니다.

## 2. 퀴즈 주제와 선정 이유

주제는 **넌센스 퀴즈**입니다.

전공 지식을 주제로 하면 비전공자 동료들이 재미없어 하고 풀기도 어려울 것 같았습니다. 그래서 배경지식 없이 누구나 가볍게 풀 수 있는 주제를 골랐습니다.

## 3. 실행 방법

Python 3.10 이상이 필요하고, 외부 라이브러리는 사용하지 않습니다. Python 3.14.2에서 동작을 확인했습니다.

```bash
git clone https://github.com/yeontteo/Codyssey-E1-2.git
cd Codyssey-E1-2
python main.py
```

`state.json`을 지우면 기본 퀴즈와 기록 없음 상태로 다시 시작합니다.

## 4. 기능 목록

| 메뉴 | 기능 | 내용 |
| --- | --- | --- |
| 1 | 퀴즈 풀기 | 등록된 퀴즈를 차례로 출제하고 정답 여부와 결과 점수를 보여 줍니다 |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력받아 바로 저장합니다 |
| 3 | 퀴즈 목록 | 등록된 문제를 번호와 함께 보여 줍니다 |
| 4 | 점수 확인 | 최고 점수와 그때의 정답 수를 보여 줍니다 |
| 5 | 종료 | 데이터를 저장하고 종료합니다 |

공통 처리는 다음과 같습니다.

- 숫자 입력은 앞뒤 공백을 제거하고, 빈 입력, 문자, 범위 밖 숫자는 안내 후 다시 입력받습니다.
- Ctrl+C나 입력 스트림 종료가 발생하면 안내 후 저장하고 종료합니다.
- 데이터 파일이 없으면 기본 퀴즈로 시작하고, 손상되었으면 안내 후 기본 퀴즈로 복구합니다.

## 5. 파일 구조

```text
.
├── main.py             # 프로그램 시작
├── quiz.py             # Quiz 클래스: 문제 하나의 데이터와 동작
├── quiz_game.py        # QuizGame 클래스: 메뉴, 입력, 게임 진행, 점수
├── quiz_storage.py     # QuizStorage 클래스: state.json 읽기와 쓰기
├── default_quizzes.py  # 기본 넌센스 퀴즈 5개
├── state.json          # 실행 시 생성되는 데이터 파일 (Git 제외)
├── .gitignore
├── README.md
└── docs/
    ├── mission.md      # 미션 원문
    └── logs/           # 단계별 실행 결과 로그
```

## 6. 데이터 파일 설명

| 항목 | 내용 |
| --- | --- |
| 경로 | 프로젝트 루트의 `state.json` (실행 위치와 관계없이 같은 파일 사용) |
| 역할 | 퀴즈 목록과 최고 점수를 저장해 재실행해도 유지 |
| 인코딩 | UTF-8 |
| 저장 시점 | 퀴즈 추가 직후, 최고 점수 갱신 직후, 프로그램 종료 시 |
| Git 관리 | 실행할 때 내용이 바뀌는 데이터이므로 `.gitignore`로 제외 |

```json
{
    "quizzes": [
        {
            "question": "왕이 넘어지면?",
            "choices": ["왕따", "킹콩", "꽈당", "퀸콩"],
            "answer": 2
        }
    ],
    "best_score": 100,
    "best_correct": 5,
    "best_total": 5
}
```

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int 또는 null | 최고 점수 (0~100), 아직 풀지 않았으면 `null` |
| `best_correct` | int 또는 null | 최고 점수를 낸 게임의 정답 수 |
| `best_total` | int 또는 null | 최고 점수를 낸 게임의 문제 수 |

## 7. 수행 체크리스트

- [x] Git 저장소 설정 (`.gitignore`, `README.md`, 첫 커밋과 푸시)
- [x] 메뉴와 공통 입력 처리
- [x] Quiz 클래스
- [x] 기본 퀴즈 데이터 5개 이상
- [x] 퀴즈 풀기 (브랜치 생성과 병합)
- [x] `state.json` 저장/불러오기
- [x] 퀴즈 추가
- [x] 퀴즈 목록
- [x] 점수 확인
- [x] QuizGame 구조 정리
- [x] README 작성
- [ ] clone/pull 실습
- [ ] 최종 검증과 스크린샷

## 8. 수행 기록

### 8.1 Git 저장소 설정

GitHub 저장소에 `Initial commit`이 이미 있어서, 로컬에서 `git init`으로 저장소를 만들고 원격을 연결한 뒤 `git pull`로 받았습니다. 전체 출력은 [docs/logs/01-git-setup.log](docs/logs/01-git-setup.log)에 있습니다.

`state.json`은 실행할 때 내용이 바뀌는 데이터이고, 없으면 기본 퀴즈로 시작하도록 만들 예정이라 `.gitignore`로 제외했습니다.

### 8.2 메뉴와 공통 입력 처리

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

### 8.3 Quiz 클래스

`quiz.py`의 `Quiz` 클래스는 문제 하나를 표현합니다. 속성은 문제(`question`), 선택지 4개(`choices`), 정답 번호 1~4(`answer`)이고, `display()`가 문제를 출력하고 `is_correct()`가 정답을 확인합니다. 전체 출력은 [docs/logs/03-quiz-class.log](docs/logs/03-quiz-class.log)에 있습니다.

### 8.4 기본 퀴즈 데이터

`default_quizzes.py`의 `create_default_quizzes()`가 넌센스 퀴즈 5개를 `Quiz` 객체로 만들어 돌려주고, `QuizGame`이 시작할 때 이 목록을 불러옵니다. 호출할 때마다 새 목록을 만들기 때문에, 게임 중 퀴즈 목록이 바뀌어도 기본 데이터는 영향을 받지 않습니다. 전체 출력은 [docs/logs/04-default-quizzes.log](docs/logs/04-default-quizzes.log)에 있습니다.

### 8.5 퀴즈 풀기

`feature/play-quiz` 브랜치에서 작업하고 `main`에 병합했습니다. `play()`가 퀴즈를 차례로 출제하고, 정답 입력은 메뉴와 같은 `read_number()`로 1~4 범위를 검증합니다. 점수는 `정답 수 / 전체 문제 수 * 100`을 반올림해 100점 만점으로 계산합니다. 전체 출력은 [docs/logs/05-play.log](docs/logs/05-play.log)에 있습니다.

| 입력 또는 상황 | 결과 |
| --- | --- |
| 전부 정답 | 100점 |
| 일부 오답 | 오답마다 정답 번호 안내, 맞힌 비율로 점수 계산 |
| 전부 오답 | 0점 |
| 정답에 `0`, `abc`, 빈 입력 | 안내 후 같은 문제 재입력 |
| 풀이 중 입력 스트림 종료 | 안내 후 종료 코드 0 |
| 퀴즈 목록이 비어 있음 | 퀴즈 없음 안내 후 메뉴로 복귀 |

### 8.6 state.json 저장/불러오기

프로그램을 시작할 때 `load()`로 불러오고, 종료할 때 `save()`로 저장합니다. Ctrl+C나 입력 스트림 종료로 끝나도 저장합니다. `Quiz` 객체는 JSON으로 바로 저장할 수 없어서 `to_dict()`로 딕셔너리로 바꾸고, 불러올 때는 `from_dict()`가 형식을 검사한 뒤 객체로 되돌립니다. 전체 출력은 [docs/logs/06-state-json.log](docs/logs/06-state-json.log)에 있습니다.

저장할 때는 임시 파일에 다 쓴 뒤 `state.json`과 교체합니다. 쓰는 도중 문제가 생겨도 기존 파일은 그대로 남습니다.

| 상황 | 결과 |
| --- | --- |
| 파일 없음 | 기본 퀴즈로 시작, 종료할 때 파일 생성 |
| 정상 파일 | 퀴즈와 최고 점수 복원, 한글 그대로 저장 |
| 깨진 JSON, 빈 파일, 잘못된 인코딩 | 안내 후 기본 퀴즈로 복구 |
| 구조 오류 (필수 키 없음, 선택지 3개, 정답 7, 정답 `true`, 점수가 문자열) | 안내 후 기본 퀴즈로 복구 |
| `"quizzes": []` | 정상으로 처리, 풀기에서 퀴즈 없음 안내 |
| 읽기/쓰기 오류 | 안내 후 계속 실행, 종료 코드 0 |
| 다른 폴더에서 실행 | 프로젝트 루트의 `state.json` 사용 |

### 8.7 퀴즈 추가

`add_quiz()`가 문제, 선택지 4개, 정답 번호를 입력받아 목록에 추가하고 바로 `state.json`에 저장합니다. 문자열은 `read_text()`로 빈 입력을 걸러 내고, 정답 번호는 `read_number()`를 재사용합니다. 전체 출력은 [docs/logs/07-add-quiz.log](docs/logs/07-add-quiz.log)에 있습니다.

| 입력 또는 상황 | 결과 |
| --- | --- |
| 정상 입력 | 추가 후 저장, 재실행해도 유지되고 풀기에 출제됨 |
| 문제나 선택지에 빈 입력, 공백만 입력 | 안내 후 같은 항목 재입력 |
| 정답 번호에 `0`, `abc`, 빈 입력, `5` | 안내 후 재입력 |
| 입력 도중 입력 스트림 종료 | 미완성 퀴즈는 추가하지 않고 안전하게 종료 |
| 저장 실패 | 안내 후 계속 실행 |

### 8.8 퀴즈 목록

`list_quizzes()`가 등록된 퀴즈의 문제를 번호와 함께 출력합니다. 풀기 전에 답이 보이지 않도록 정답은 출력하지 않고, 목록이 비어 있으면 안내 후 메뉴로 돌아갑니다. 전체 출력은 [docs/logs/08-list-quiz.log](docs/logs/08-list-quiz.log)에 있습니다.

### 8.9 점수 확인

게임이 끝나면 `update_best_score()`가 최고 점수와 비교하고, 더 높을 때만 기록을 바꿔 바로 저장합니다. 메뉴 4번의 `show_score()`로 확인합니다. 아직 풀지 않은 상태는 `null`로 저장해서 0점 기록과 구분합니다. 전체 출력은 [docs/logs/09-score.log](docs/logs/09-score.log)에 있습니다.

| 상황 | 결과 |
| --- | --- |
| 풀기 전 점수 확인 | 기록 없음 안내 |
| 첫 게임 | 점수와 상관없이 최고 점수로 기록 (0점 포함) |
| 최고 점수보다 낮거나 같음 | 갱신하지 않음 |
| 최고 점수보다 높음 | 갱신 후 저장 |
| 재실행 | 최고 점수 유지 |

### 8.10 QuizGame 구조 정리

`QuizGame`이 맡던 JSON 파일 읽기와 쓰기를 `quiz_storage.py`의 `QuizStorage` 클래스로 분리했습니다. `QuizGame`의 `load()`와 `save()`는 그대로 두고, 게임 상태를 검사하고 안내 문구를 출력하는 일만 맡습니다. 반복되던 구분선과 안내 문구는 클래스 속성으로 모았습니다.

| 클래스 | 파일 | 역할 |
| --- | --- | --- |
| `Quiz` | `quiz.py` | 문제 하나의 데이터, 출력, 정답 확인, 딕셔너리 변환 |
| `QuizGame` | `quiz_game.py` | 메뉴, 입력 검증, 게임 진행, 점수 관리 |
| `QuizStorage` | `quiz_storage.py` | `state.json` 읽기와 쓰기 |

리팩터링 전후로 같은 입력을 넣어 전체 출력을 비교했고 완전히 일치했습니다. 결과는 [docs/logs/10-refactor.log](docs/logs/10-refactor.log)에 있습니다.

### 8.11 clone/pull 실습

저장소를 별도 폴더에 `git clone`으로 복제해 이 문단을 추가하고, 기존 작업 폴더에서 `git pull`로 받았습니다.

## 9. 트러블슈팅

### 트러블슈팅 1: 출력을 파이프로 연결하면 이모지에서 프로그램이 종료됨

- **문제**: 메뉴에 이모지를 쓰기 전에 `python -c "print('🎯 메뉴')" | cat`으로 시험하니 `UnicodeEncodeError`가 발생했습니다.
- **원인 가설**: 출력이 터미널이 아니라 파이프로 연결되면 Python이 Windows 기본 인코딩을 쓰는데, 이 인코딩이 이모지를 지원하지 않을 수 있습니다.
- **확인**: 같은 조건에서 `locale.getencoding()`과 `sys.stdout.encoding`이 모두 `cp949`로 나왔습니다.
- **해결**: `main.py` 시작부에서 `sys.stdout.reconfigure(encoding="utf-8")`을 호출하니 정상 출력되었습니다. 파일을 열 때도 같은 이유로 항상 `encoding="utf-8"`을 지정했습니다.

```console
$ python -c "print('🎯 메뉴')" | cat
UnicodeEncodeError: 'cp949' codec can't encode character '🎯' in position 0: illegal multibyte sequence

$ python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); print('🎯 메뉴')" | cat
🎯 메뉴
```
