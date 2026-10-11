# 클라우드 보안: (트렌드) IAM, DPU, Zero Trust

> Velog 원문: https://velog.io/@hyeonminee/%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C-%EB%B3%B4%EC%95%88-%ED%8A%B8%EB%A0%8C%EB%93%9C-IAM-DPU-Zero-Trust

- 작성일: Sun, 11 Oct 2026 03:19:12 GMT

---

<blockquote>
<p>클라우드 보안은 외부 공격을 차단하는 것뿐 아니라 접근 권한 관리, 위협 탐지, 데이터 보호, 사고 대응까지 포함한다.</p>
</blockquote>
<h3 id="1-aws-클라우드-보안--티빙-사례">1. AWS 클라우드 보안 — 티빙 사례</h3>
<h4 id="핵심-용어">핵심 용어</h4>
<table>
<thead>
<tr>
<th>용어</th>
<th>개념</th>
</tr>
</thead>
<tbody><tr>
<td>IAM</td>
<td>사용자 및 서비스의 AWS 리소스 접근 권한 관리</td>
</tr>
<tr>
<td>Security Group</td>
<td>인스턴스 등 리소스의 네트워크 트래픽 통제</td>
</tr>
<tr>
<td>CloudTrail</td>
<td>AWS 계정 내 API 활동 등의 기록 및 감사</td>
</tr>
<tr>
<td>GuardDuty</td>
<td>AWS 환경의 의심스러운 활동 및 위협 탐지</td>
</tr>
<tr>
<td>Least Privilege</td>
<td>업무 수행에 필요한 최소한의 권한만 부여하는 원칙</td>
</tr>
<tr>
<td>Defense in Depth</td>
<td>여러 보안 계층을 결합해 위험을 줄이는 다계층 방어</td>
</tr>
</tbody></table>
<h4 id="사례-및-기술-설명">사례 및 기술 설명</h4>
<p>2026년 10월 2일, 티빙은 개인정보 유출 사고 이후 AWS의 Security Improvement Program(SIP)을 활용해 클라우드 보안 체계를 진단하고 개선한다고 발표했다.</p>
<p>주요 점검 영역은 <strong>계정·권한 관리, 위협 탐지, 인프라 보호, 데이터 보호, 사고 대응</strong>이다.</p>
<p>클라우드 보안은 다음 요소를 함께 고려해야 한다.</p>
<pre><code class="language-text">IAM / 최소 권한
    ↓
Network Access Control
    ↓
Logging &amp; Threat Detection
    ↓
Incident Response</code></pre>
<p>이는 보안 기능의 실제 실행 순서가 아니라, 함께 구축해야 하는 주요 통제 영역을 나타낸다.</p>
<h4 id="배운-점과-내-생각">배운 점과 내 생각</h4>
<p>기존에는 클라우드 보안을 생각하면 Security Group이나 방화벽 같은 네트워크 접근통제를 먼저 떠올렸다.</p>
<p>하지만 이번 사례를 통해 <strong>네트워크 접근을 차단하는 것뿐 아니라 누가 어떤 리소스에 접근할 수 있는지 관리하고, 비정상적인 활동을 탐지하는 체계까지 필요하다</strong>는 점을 알게 되었다.</p>
<p>특히 AWS의 IAM, CloudTrail, GuardDuty가 각각 어떤 역할을 하며 사고 대응 과정에서 어떻게 연결되는지 학습할 필요가 있다고 느꼈다.</p>
<p><strong>참고:</strong> <a href="https://www.yna.co.kr/amp/view/AKR20261002113200017">연합뉴스 - 티빙, AWS와 보안체계 고도화</a></p>
<hr />
<h3 id="2-ai-인프라-보안--nvidia-dpu-사례">2. AI 인프라 보안 — NVIDIA DPU 사례</h3>
<h4 id="핵심-용어-1">핵심 용어</h4>
<table>
<thead>
<tr>
<th>용어</th>
<th>개념</th>
</tr>
</thead>
<tbody><tr>
<td>CPU</td>
<td>운영체제와 애플리케이션 실행 등 범용 연산 담당</td>
</tr>
<tr>
<td>GPU</td>
<td>AI 학습·추론 등에 필요한 대규모 병렬 연산 담당</td>
</tr>
<tr>
<td>DPU</td>
<td>네트워크·보안·인프라 데이터 처리 등을 가속하는 프로세서</td>
</tr>
<tr>
<td>Isolation</td>
<td>실행 환경이나 워크로드를 분리해 영향 범위를 제한</td>
</tr>
<tr>
<td>Control Plane</td>
<td>네트워크 장비의 경로·정책 등을 결정하는 제어 영역</td>
</tr>
<tr>
<td>Data Plane</td>
<td>결정된 정책에 따라 실제 패킷을 처리·전달하는 영역</td>
</tr>
</tbody></table>
<h4 id="사례-및-기술-설명-1">사례 및 기술 설명</h4>
<p>NVIDIA는 2026년 9월 28일 AI 에이전트 보안을 위한 <strong>Open Agent Safety Platform</strong>을 발표했다.</p>
<p>이 플랫폼에는 BlueField DPU를 이용해 AI 에이전트의 행동을 독립적으로 감시·통제하는 NVIDIA Sentry 구조가 포함된다.</p>
<pre><code class="language-text">AI Agent
    ↓
CPU / GPU (실행)
    |
    └── DPU (독립적인 보안 감시·통제)</code></pre>
<p>핵심은 <strong>서비스 실행 환경과 보안 감시 환경을 분리</strong>해, 실행 환경 자체가 침해되더라도 별도의 통제 수단을 확보하려는 것이다.</p>
<h4 id="배운-점과-내-생각-1">배운 점과 내 생각</h4>
<p>기존에는 DPU를 네트워크 처리 성능을 높이기 위한 하드웨어 정도로 이해했지만, 보안 기능을 분리하고 독립적으로 수행하는 데도 활용할 수 있다는 점이 흥미로웠다.</p>
<p>Control Plane과 Data Plane을 분리하는 네트워크 아키텍처와 목적이 완전히 같지는 않지만, <strong>기능을 분리하여 통제 가능성과 안정성을 높인다는 점</strong>에서 연결해 이해할 수 있었다.</p>
<p>AI 인프라가 확대되면 GPU뿐 아니라 네트워크·보안 인프라의 중요성도 함께 높아질 것으로 생각한다.</p>
<p><strong>참고:</strong> <a href="https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Launches-Open-Agent-Safety-Platform-to-Secure-Agents-From-Testing-to-Deployment/">NVIDIA - Open Agent Safety Platform</a></p>
<hr />
<h3 id="3-경계-기반-보안에서-zero-trust--sse로">3. 경계 기반 보안에서 Zero Trust / SSE로</h3>
<h4 id="핵심-용어-2">핵심 용어</h4>
<table>
<thead>
<tr>
<th>용어</th>
<th>개념</th>
</tr>
</thead>
<tbody><tr>
<td>Perimeter Security</td>
<td>내부·외부 네트워크의 경계를 중심으로 보호하는 보안 방식</td>
</tr>
<tr>
<td>Zero Trust</td>
<td>네트워크 위치만으로 신뢰하지 않고 접근 요청을 검증하는 보안 원칙</td>
</tr>
<tr>
<td>SSE</td>
<td>사용자와 인터넷·클라우드 애플리케이션 간 접근을 보호하는 클라우드 보안 서비스 집합</td>
</tr>
<tr>
<td>ZTNA</td>
<td>인증·인가된 사용자에게 필요한 애플리케이션 접근만 제공</td>
</tr>
<tr>
<td>Microsegmentation</td>
<td>워크로드 등을 세분화해 불필요한 내부 통신을 제한</td>
</tr>
</tbody></table>
<h4 id="기술-설명">기술 설명</h4>
<p>전통적인 경계 기반 보안은 사내 네트워크와 외부 네트워크를 구분하고, 방화벽 등을 통해 외부 접근을 통제하는 방식이다.</p>
<p>하지만 클라우드·SaaS·원격근무 환경이 확대되면서 리소스가 여러 위치에 분산되고, 내부 네트워크에 있다는 사실만으로 안전하다고 판단하기 어려워졌다.</p>
<p>이에 따라 <strong>사용자의 신원, 기기 상태, 접근 대상, 권한을 기반으로 접근을 통제하는 Zero Trust</strong>가 중요해지고 있다.</p>
<pre><code class="language-text">[경계 기반 보안]
Internet → Firewall → Internal Network

[Zero Trust]
User / Device
    ↓
Identity &amp; Policy Verification
    ↓
Authorized Application
    ↓
Continuous Monitoring</code></pre>
<p>Zero Trust는 보안 원칙이며, SSE는 이를 구현하는 데 활용할 수 있는 클라우드 보안 서비스 집합이다.</p>
<h4 id="배운-점과-내-생각-2">배운 점과 내 생각</h4>
<p>기존 네트워크 보안에서는 IP 주소, 포트, 방화벽 정책을 중심으로 접근통제를 공부했다.</p>
<p>Zero Trust는 이러한 기술을 대체하는 것이 아니라 <strong>사용자의 신원과 리소스별 권한, 지속적인 검증까지 접근통제의 범위를 확장한다는 점</strong>에서 차이가 있다.</p>
<p>앞으로 클라우드 보안을 학습할 때 네트워크 구성뿐 아니라 IAM, 인증·인가, 워크로드 단위 접근통제를 함께 이해해야겠다고 생각했다.</p>
<p><strong>참고:</strong> <a href="https://www.nist.gov/publications/zero-trust-architecture">NIST - Zero Trust Architecture</a></p>
<hr />
<h3 id="4-종합-정리">4. 종합 정리</h3>
<p>이번 사례들의 공통점은 <strong>클라우드 보안이 단순한 네트워크 경계 보호에서 신원·리소스·워크로드 중심의 다계층 보안으로 확장되고 있다는 것</strong>이다.</p>
<ul>
<li><strong>티빙:</strong> IAM, 위협 탐지, 사고 대응을 결합한 클라우드 보안 체계</li>
<li><strong>NVIDIA:</strong> 실행 환경과 독립적인 보안 감시·통제 구조</li>
<li><strong>Zero Trust:</strong> 내부 네트워크 여부가 아닌 신원과 정책에 기반한 접근통제</li>
</ul>
<p>네트워크, AWS, Kubernetes를 개별 기술로 학습하는 것에서 더 나아가 실제 서비스 아키텍처에서 <strong>어디서 접근을 통제하고, 장애와 위협을 어떻게 탐지하며, 사고 발생 시 어떻게 대응할 것인지</strong> 연결해서 이해하는 것이 중요하다고 느꼈다.</p>
