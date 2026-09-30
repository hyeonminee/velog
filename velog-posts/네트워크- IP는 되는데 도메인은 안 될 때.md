# 네트워크: IP는 되는데 도메인은 안 될 때

> Velog 원문: https://velog.io/@hyeonminee/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-IP%EB%8A%94-%EB%90%98%EB%8A%94%EB%8D%B0-%EB%8F%84%EB%A9%94%EC%9D%B8%EC%9D%80-%EC%95%88-%EB%90%A0-%EB%95%8C

- 작성일: Wed, 30 Sep 2026 02:39:55 GMT

---

<p><strong>상황</strong>
Ubuntu 서버에서 <code>ping 8.8.8.8</code>은 성공하지만, <code>curl https://example.com</code>은 <code>Could not resolve host</code> 오류로 실패했다.</p>
<p><strong>문제</strong></p>
<ol>
<li>가장 먼저 의심할 기능은 무엇일까?</li>
<li>아래 명령 중 도메인 이름이 IP 주소로 변환되는지 확인하는 데 가장 적합한 것은?
 A. <code>ip route</code>
 B. <code>getent hosts example.com</code>
 C. <code>ss -tuln</code></li>
</ol>
<p><strong>정답과 풀이</strong></p>
<ol>
<li>DNS 이름 해석을 먼저 의심한다. IP 주소로는 통신되지만 도메인 이름을 IP 주소로 바꾸는 단계에서 오류가 났기 때문이다. 다만 <code>ping</code> 성공만으로 HTTPS 연결까지 정상이라고 단정할 수는 없다.</li>
<li>B. <code>gentent hosts example.com</code> 주소가 출력되는지 확인한다. 출력되지 않으면 <code>resolvectl status</code>로 서버가 사용하는 DNS 설정을 살펴볼 수 있다.</li>
</ol>
<p><strong>핵심 개념</strong>
DNS는 <code>example.com</code> 같은 이름을 접속에 필요한 IP 주소로 찾는 기능이다. <code>ip route</code>는 패킷이 나갈 경로를, <code>ss -tuln</code>은 현재 열려 있는 소켓을 확인할 때 쓴다.</p>
<p><strong>실무에서 중요한 이유</strong>
서비스 접속 실패를 모두 방화벽 문제로 보면 원인을 찾는 데 시간이 걸린다. <strong>IP 통신 -&gt; 이름 해석 -&gt; 해당 서비스 연결</strong> 순서로 확인하면 장애 범위를 빠르게 좁힐 수 있다. DNS 설정을 바꾸기 전에는 현재 설정과 영향을 받는 서비스를 먼저 확인한다. </p>
