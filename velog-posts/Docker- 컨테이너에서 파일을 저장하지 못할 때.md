# Docker: 컨테이너에서 파일을 저장하지 못할 때

> Velog 원문: https://velog.io/@hyeonminee/Docker-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%97%90%EC%84%9C-%ED%8C%8C%EC%9D%BC%EC%9D%84-%EC%A0%80%EC%9E%A5%ED%95%98%EC%A7%80-%EB%AA%BB%ED%95%A0-%EB%95%8C

- 작성일: Wed, 14 Oct 2026 00:21:52 GMT

---

<p><strong>상황</strong></p>
<p>Spring Boot 컨테이너는 실행 중이지만 사용자가 파일을 업로드하면 <code>500</code> 오류가 발생한다.</p>
<pre><code class="language-text">$ docker logs web --tail 20

java.nio.file.FileSystemException:
 /app/uploads/report.pdf: Read-only file system</code></pre>
<p>컨테이너의 마운트 설정은 다음과 같다.</p>
<pre><code class="language-text">$ docker inspect web

Source:      /srv/web/uploads
Destination: /app/uploads
RW:          false</code></pre>
<p>Docker Compose에는 다음 설정이 있다.</p>
<pre><code class="language-yaml">volumes:
  - /srv/web/uploads:/app/uploads:ro</code></pre>
<p><strong>문제</strong></p>
<ol>
<li>컨테이너가 실행 중인데도 업로드 파일을 저장하지 못하는 원인은 무엇일까?</li>
<li>어떤 내용을 확인한 뒤 설정을 어떻게 수정해야 할까?</li>
</ol>
<hr />
<h3 id="풀이">풀이</h3>
<p>볼륨 끝의 <code>:ro</code>는 컨테이너에서 해당 경로를 <strong>읽기 전용(read-only)</strong> 으로 사용한다는 뜻이다. <code>docker inspect</code>의 <code>RW: false</code>도 쓰기가 허용되지 않았음을 보여준다.</p>
<p>표기 형식은 다음과 같다.</p>
<pre><code class="language-text">호스트 경로 : 컨테이너 경로 : 접근 모드</code></pre>
<p>먼저 애플리케이션이 실제로 <code>/app/uploads</code>에 파일을 써야 하는지 확인한다. 쓰기가 필요한 경로가 맞다면 <code>:ro</code>를 제거하거나 <code>rw</code>로 변경한다.</p>
<pre><code class="language-yaml">volumes:
  - /srv/web/uploads:/app/uploads:rw</code></pre>
<p>변경된 설정을 확인한 후 컨테이너를 재생성한다.</p>
<pre><code class="language-bash">docker compose config
docker compose up -d</code></pre>
<p><code>docker compose config</code>는 여러 Compose 설정을 합친 최종 구성을 보여준다. <code>up -d</code>는 변경된 설정으로 컨테이너를 재생성할 수 있다.</p>
<p>재생성 후에는 다음 순서로 확인한다.</p>
<pre><code class="language-bash">docker inspect web
docker exec web test -w /app/uploads &amp;&amp; echo &quot;쓰기 가능&quot;
docker logs web --tail 20</code></pre>
<p><code>test -w</code>는 실제 파일을 만들지 않고 현재 실행 사용자가 경로에 쓸 수 있는지 검사한다.</p>
<h3 id="핵심-개념">핵심 개념</h3>
<ul>
<li>바인드 마운트는 호스트 디렉터리를 컨테이너 내부 경로에 연결한다.</li>
<li><code>ro</code>는 읽기 전용, <code>rw</code>는 읽기·쓰기 허용을 뜻한다.</li>
<li>컨테이너가 <code>Up</code> 상태여도 특정 기능에 필요한 파일 접근은 실패할 수 있다.</li>
<li><code>rw</code>로 바꾼 뒤에도 실패한다면 호스트 디렉터리의 소유자와 권한을 추가로 확인해야 한다.</li>
</ul>
<h3 id="실무에서-중요한-이유">실무에서 중요한 이유</h3>
<p>설정 파일이나 인증서처럼 변경되면 안 되는 데이터는 <code>ro</code>로 마운트하는 것이 안전하다. 반대로 업로드·로그·데이터 저장 경로에는 필요한 범위에서 쓰기 권한이 있어야 한다. 모든 경로를 무조건 <code>rw</code>로 열면 컨테이너 침해 시 호스트 파일까지 변조될 위험이 커진다.</p>
<p>컨테이너를 재생성하기 전에는 볼륨의 실제 호스트 경로, 데이터 백업 여부, 실행 중인 요청을 확인한다. 특히 <code>docker compose down -v</code>는 볼륨 데이터를 삭제할 수 있으므로 데이터 보존 여부를 확인하지 않고 실행하면 안 된다.</p>
