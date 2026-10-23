# Docker: localhost의 데이터베이스에 연결할 수 없을 때

> Velog 원문: https://velog.io/@hyeonminee/Docker-localhost%EC%9D%98-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%97%90-%EC%97%B0%EA%B2%B0%ED%95%A0-%EC%88%98-%EC%97%86%EC%9D%84-%EB%95%8C

- 작성일: Fri, 23 Oct 2026 00:06:04 GMT

---

<p><strong>상황</strong>
Docker Compose로 API와 PostgreSQL을 실행했다. DB 컨테이너는 정상이지만 API가 계속 재시작된다.</p>
<pre><code>$ docker compose ps

NAME       SERVICE   STATUS
shop-api   api       Restarting
shop-db    db        Up</code></pre><p>API 로그:</p>
<pre><code>connection to server at &quot;localhost&quot;, port 5432 failed:
Connection refused</code></pre><p>Compose 설정 일부:</p>
<pre><code>services:
  api:
    environment:
      DB_HOST: localhost
      DB_PORT: 5432
    depends_on:
      - db

  db:
    image: postgres:16</code></pre><p><strong>문제</strong></p>
<ol>
<li>DB 컨테이너가 실행 중인데 localhost:5432 연결이 실패하는 이유는 무엇일까?</li>
<li>무엇을 수정하고 어떤 순서로 검증해야 할까? depends_on이 있으면 DB가 연결 가능한 상태까지 보장될까?</li>
</ol>
<p><strong>풀이</strong>
<strong>1. 컨테이너 안의 localhost는 API 컨테이너 자신을 가리킨다.</strong>
API와 DB는 서로 다른 컨테이너다. API 컨테이너의 localhost:5432에는 PostgreSQL이 없으므로 연결이 거부된다.
같은 Compose 네트워크에서는 서비스 이름을 호스트 이름처럼 사용할 수 있다. 따라서 다음과 같이 수정한다.</p>
<pre><code>environment:
  DB_HOST: db
  DB_PORT: 5432</code></pre><p>여기서 <code>db</code>는 Compose에 정의된 DB의 서비스 이름이다.</p>
<p><strong>2. 설정과 로그를 확인한 뒤 API 컨테이너를 재생성한다.</strong></p>
<pre><code>docker compose ps
docker compose logs api --tail=30
docker compose logs db --tail=30
docker compose config</code></pre><ul>
<li><code>ps</code>: 컨테이너 상태 확인</li>
<li><code>logs</code>: 최근 오류 확인</li>
<li><code>config</code>: 환경변수 치환까지 반영된 최종 Compose 설정 확인</li>
</ul>
<p>DB 자체의 준비 상태도 확인한다.</p>
<pre><code>docker compose exec db pg_isready</code></pre><p>설정을 수정한 다음 API를 다시 생성한다.</p>
<pre><code>docker compose up -d --force-recreate api
docker compose ps
docker compose logs api --tail=30</code></pre><p>마지막으로 API의 실제 응답까지 확인한다.</p>
<pre><code>curl --max-time 5 http://localhost:8080/health</code></pre><p><code>depends_on</code>은 기본적으로 컨테이너 시작 순서를 관리할 뿐, DB가 요청을 받을 준비가 끝났는지까지 보장하지 않는다. 시작 직후에도 연결 오류가 난다면 DB healthcheck와 API의 연결 재시도 설정을 함께 검토한다.</p>
<p><strong>핵심 개념</strong></p>
<ul>
<li><strong>컨테이너의 localhost</strong>: 현재 컨테이너 자신</li>
<li><strong>Compose 서비스 이름</strong>: 같은 Compose 네트워크에서 사용할 수 있는 내부 호스트 이름</li>
<li><strong>Connection refused</strong>: 대상 주소에는 도달했지만 해당 포트에서 서비스가 연결을 받지 않는 상태</li>
<li><strong>Healthcheck</strong>: 컨테이너 내부 서비스가 실제로 준비됐는지 검사하는 설정</li>
<li><strong>Restarting</strong>: 프로세스 종료와 재시작 정책 때문에 컨테이너가 반복 실행되는 상태</li>
</ul>
<p><strong>실무에서 중요한 이유</strong>
컨테이너마다 독립된 네트워크 공간이 있으므로, VM에서 실행하던 설정을 그대로 옮겨 <code>localhost</code>를 사용하면 의존 서비스 연결이 실패할 수 있다. 또한 실행 순서와 서비스 준비 상태를 구분해야 간헐적인 시작 실패를 예방할 수 있다.</p>
<p><strong>실행 전 점검</strong>: 현재 작업 디렉터리와 Compose 프로젝트가 운영 대상인지 확인한다. <code>docker compose config</code> 출력에는 치환된 비밀번호가 나타날 수 있으므로 공유에 주의한다. <code>docker compose down -v</code>는 DB 볼륨까지 삭제할 수 있으므로 이 문제 해결에는 사용하지 않는다.</p>
