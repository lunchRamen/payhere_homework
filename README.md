# 페이히어 과제 프로젝트입니다.

- 개발환경과 배포환경을 분리하였습니다.
    - 개발환경의 경우 Django와 sqlite3로 간편한 확인 및 테스트를 진행하도록 하였습니다
        - 개발환경에서 서버를 실행하고 싶은 경우, python backend/manage.py runserver를 실행합니다
        - 개발환경에서 테스트를 진행하고 싶은 경우,
    - 배포환경의 경우 Django와 Mysql:5.7로 docker-compose 형태로 서버를 구축하였습니다.
        - 배포환경에서 서버를 실행하고 싶은 경우, docker-compose up --build를 실행합니다.
        - 배포환경에서 테스트를 진행하고 싶은 경우,



- User와 AccountBook으로 유저와 가계부 스키마를 구성하였습니다.
    - User
        - email
        - password
        - created_at
        - updated_at
    - AccountBook
        - money
        - memo
        - created_at
        - updated_at
    - User와 AccountBook은 1:N 관계를 가지고 있습니다.


- 개발 API
    - users/signup (POST) -> 회원가입
    - users/login (GET) -> 로그인
    - users/logout (GET) -> 로그아웃

    - users/accountbook (GET) -> user가 만든 가계부 리스트 반환.
    - users/accountbook (POST) -> user의 가계부 생성
    - users/accountbook/{accountbook_id} (GET) -> user의 accountbook_id 가계부 조회
    - users/accountbook/{accountbook_id} (PATCH) -> user의 accountbook_id 가계부 수정
    - users/accountbook/{accountbook_id} (DELETE) -> user의 accountbook_id 가계부 삭제
    - ?? -> users의 account_id 가계부 복제
    - users/accountbook/{accountbook_id}/url (GET) -> user의 account_id 가계부를 볼수 있는 url링크 조회. (url링크는 특정시간 후 만료.)

- 테스트 API
    - 회원가입 성공/실패
    - 로그인 성공/실패
    - 로그아웃 성공

    - 가계부 생성 성공/실패
    - 가계부 리스트 조회
    - 특정 가계부 조회 성공/실패
    - 특정 가계부 수정 성공/실패
    - 특정 가계부 삭제 성공/실패
    - 특정 가계부 복제
    - 특정 가계부 url 생성 성공/실패
