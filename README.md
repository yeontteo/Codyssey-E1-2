# E1-2 나만의 퀴즈 게임

코디세이(Codyssey) 입학연수 미션 E1-2 제출 저장소입니다. 미션 원문은 [docs/mission.md](docs/mission.md)에 있습니다.

## 1. 프로젝트 개요

터미널에서 동작하는 넌센스 퀴즈 게임입니다. Python 클래스로 코드를 역할별로 나누고, 퀴즈와 최고 점수를 `state.json`에 저장해 프로그램을 다시 실행해도 유지되도록 합니다.

## 2. 수행 체크리스트

- [x] Git 저장소 설정 (`.gitignore`, `README.md`, 첫 커밋과 푸시)
- [ ] 메뉴와 공통 입력 처리
- [ ] Quiz 클래스
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
