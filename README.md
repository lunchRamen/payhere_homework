# 페이히어 과제 프로젝트입니다.

- 개발환경과 배포환경을 분리하였습니다.
    - 개발환경과 배포환경 모두 Django와 Mysql:5.7로 구현 및 테스트를 진행하도록 하였습니다
        - 개발환경에서 서버를 실행하고 싶은 경우
            - backend/mysql_settings.py파일을 만들고, 개인 mysql 서버 설정을 설정합니다.
            - python backend/manage.py makemigrations, python backend/manage.py migrate를 진행합니다.
            - python backend/manage.py runserver로 서버를 실행합니다.
        - 개발환경에서 테스트를 진행하고 싶은 경우,

        - 배포환경에서 서버를 실행하고 싶은 경우, docker-compose up --build를 실행합니다.
        - 배포환경에서 테스트를 진행하고 싶은 경우,


- 일정한 코드 컨벤션을 유지하기 위해, flake8과 isort를 이용해 PEP8기반의 코드 컨벤션을 유지하였습니다.



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
    - default url : api/

    - users/signup (POST) -> 회원가입 [o]
    - users/login (GET) -> 로그인 [o]
    - users/logout (GET) -> 로그아웃 [o]

    - users/accountbook (GET) -> user가 만든 가계부 리스트 반환. [o]
    - users/accountbook (POST) -> user의 가계부 생성 [o]
    - users/accountbook/{accountbook_id} (GET) -> user의 accountbook_id 가계부 조회
    - users/accountbook/{accountbook_id} (PATCH) -> user의 accountbook_id 가계부 수정
    - users/accountbook/{accountbook_id} (DELETE) -> user의 accountbook_id 가계부 삭제
    - ?? -> users의 account_id 가계부 복제
    - users/accountbook/{accountbook_id}/url (GET) -> user의 account_id 가계부를 볼수 있는 url링크 조회. (url링크는 특정시간 후 만료.)

- 테스트 API
    - 회원가입 성공/실패 [o]
        - 이메일 형식 성공/실패 [o]
        - 패스워드 형식 성공/실패 [o]
    - 로그인 성공/실패 [o]
    - 로그아웃 성공 [o]
    - access_token 시간 이후, 인증상태가 아닌것에 대한 테스트.

    - 가계부 생성 성공/실패 [o]
    - 가계부 리스트 조회 [o]
    - 특정 가계부 조회 성공/실패
    - 특정 가계부 수정 성공/실패
    - 특정 가계부 삭제 성공/실패
    - 특정 가계부 복제
    - 특정 가계부 url 생성 성공/실패
