def P(pid: int, title: str, body: str, hint: str, solution: str) -> dict:
    return {
        "id": pid,
        "title": title,
        "body": body.strip(),
        "hint": hint.strip(),
        "solution": solution.strip(),
    }

PROBLEMS = [
    {
        "id": 1,
        "title": "단 한 번의 암호화(최단거리 + 1회 할인)",
        "body": """
## 문제
가중치가 있는 **방향 그래프**에서 1→N 최단거리를 구하라.
단, 경로 상의 간선 **하나**를 선택해 가중치를 **⌊w/2⌋** 로 바꾸는 “암호화”를 **최대 1번(0/1회)** 사용할 수 있다.

## 입력
- `N M`
- M줄: `u v w`

## 출력
- 최단 거리

## 제한(예시)
- N≤200,000, M≤300,000, w≤1e9

## 예시
입력
4 5
1 2 10
2 4 10
1 3 100
3 4 1
2 3 1
출력
15

""".strip(),
        "hint": """
- 다익스트라를 (정점, 암호화 사용 여부 0/1) 2상태로 확장.
- dist[v][0], dist[v][1]만 관리하면 됨.
""".strip(),
        "solution": """
### 해설(개요)
상태를 (v, used)로 두고 다익스트라.

간선 (u→v, w)에서:
- used=0: (v,0)에 w / (v,1)에 ⌊w/2⌋ relax
- used=1: (v,1)에 w relax

정답은 min(dist[N][0], dist[N][1]).
""".strip(),
    },
    {
        "id": 2,
        "title": "연결성 로그(동적 그래프 연결성)",
        "body": """
## 문제
정점 1..N 무방향 그래프가 비어있는 상태로 시작한다. Q개의 연산:
- `+ u v` : 간선 추가 (중복 추가 없음)
- `- u v` : 간선 삭제 (항상 존재하는 간선만 삭제)
- `? u v` : 현재 u, v가 같은 연결요소면 YES, 아니면 NO

## 입력
- `N Q`
- Q줄: `op u v`

## 출력
- `?`마다 YES/NO

## 제한(예시)
- N,Q ≤ 200,000
""".strip(),
        "hint": """
- 오프라인으로 풀기: “간선 활성 시간 구간”을 만들고
  시간 세그트리에 구간별로 간선을 넣는다.
- DFS하며 DSU rollback으로 처리.
""".strip(),
        "solution": """
### 해설(개요)
1) 각 간선의 활성 구간 [add_time, del_time)을 계산.
2) 시간 세그트리(1..Q) 노드에 그 구간을 커버하는 간선을 저장.
3) 세그트리 DFS:
   - 노드 진입 시 저장된 간선들을 DSU union
   - 리프에서 ?면 find로 답
   - 복귀 시 union들을 rollback(스택으로 parent/size 변경 기록)

전체는 대략 O(Q log Q).
""".strip(),
    },
    {
        "id": 3,
        "title": "제곱 DP 최적화(Convex Hull Trick / Li Chao)",
        "body": """
## 문제
수열 a1..aN, 누적합 P[i]=a1+...+ai (P[0]=0).
dp[0]=0, 그리고
dp[i] = min_{0≤j<i} ( dp[j] + (P[i]-P[j])^2 + C )
dp[N]을 구하라.

## 입력
- `N C`
- `a1 ... aN`

## 출력
- dp[N]

## 제한(예시)
- N≤200,000, ai≤1e6, C≤1e12
""".strip(),
        "hint": """
- (P[i]-P[j])^2를 전개해서 “직선 최소값 쿼리”로 바꾸기.
- x=P[i], 직선은 j에서 만들어짐 → Li Chao Tree가 무난.
""".strip(),
        "solution": """
### 해설(개요)
전개:
dp[j] + (P[i]-P[j])^2 + C
= (dp[j]+P[j]^2) + (-2P[j]) * P[i] + (P[i]^2 + C)

x=P[i]에 대해 직선 y = m x + b 최소값을 쿼리:
- m = -2P[j]
- b = dp[j] + P[j]^2

i를 1..N 순회하며:
1) x=P[i]로 최소 y 쿼리
2) dp[i] = y + P[i]^2 + C
3) (m,b) 삽입
""".strip(),
    },
    {
        "id": 4,
        "title": "역전된 행군(구간 뒤집기 + 구간합)",
        "body": """
## 문제
길이 N 배열 A가 있다. Q개의 연산을 처리하라.
- `R l r` : 구간 [l,r]를 reverse
- `S l r` : 구간 [l,r]의 합 출력

## 입력
- N Q
- A1 ... AN
- Q줄: 연산

## 출력
- S 연산마다 합 출력

## 제한(예시)
- N,Q ≤ 200,000
- |Ai| ≤ 1e9
""".strip(),
        "hint": """
- Implicit Treap / Splay / Rope 같은 “시퀀스 자료구조” 정석.
- lazy reverse 토글 + 구간합(sum) 유지.
""".strip(),
        "solution": """
### 해설(개요)
Implicit Treap 노드에 size, sum, rev(lazy) 저장.
split/merge로 [l,r]를 분리 → rev 토글 → 다시 merge.
S는 분리된 가운데 트리 sum을 출력.
""".strip(),
    },
    {
        "id": 5,
        "title": "바람 격자(0-1 BFS)",
        "body": """
## 문제
H×W 격자에서 (1,1)→(H,W)로 이동한다. 상하좌우 이동 비용은 기본 1이다.
일부 칸은 바람 칸이며, 그 칸에서 지정 방향으로 한 칸 이동은 비용 0이다.
최소 비용을 구하라.

## 입력
- H W
- 격자 정보(벽/빈칸/바람방향 등은 너희 포맷으로 정해도 됨)

## 출력
- 최소 비용

## 제한(예시)
- H,W ≤ 2000
""".strip(),
        "hint": """
- 간선 비용이 0 또는 1 → deque 쓰는 0-1 BFS가 정석.
""".strip(),
        "solution": """
### 해설(개요)
dist 배열을 INF로 초기화.
deque에서 pop:
- 비용 0 이동이면 pushleft
- 비용 1 이동이면 pushright
0-1 BFS로 최단거리 계산.
""".strip(),
    },
    {
        "id": 6,
        "title": "트리 경로 최댓값(업데이트 포함, HLD)",
        "body": """
## 문제
N개 정점 트리, 각 정점 값 val[i].
Q개의 연산:
- `U i x` : val[i]=x
- `Q u v` : u-v 경로 위 정점 값의 최댓값 출력

## 입력
- N Q
- val1..valN
- N-1줄 간선
- Q줄 연산

## 출력
- Q 연산마다 답

## 제한(예시)
- N,Q ≤ 200,000
""".strip(),
        "hint": """
- HLD로 경로를 O(log^2 N)개의 연속 구간으로 쪼갬.
- 베이스 배열 위 세그트리(max).
""".strip(),
        "solution": """
### 해설(개요)
HLD로 pos/head 부여 후 세그트리 구축.
경로 질의는 head가 다를 동안 깊은 쪽 head 구간을 처리하며 끌어올림.
업데이트는 pos[i] 점 업데이트.
""".strip(),
    },
    {
        "id": 7,
        "title": "구간 k번째 수(퍼시스턴트 세그트리)",
        "body": """
## 문제
수열 A(길이 N). 질의 `l r k`:
A[l..r]에서 k번째로 작은 수(1-indexed)를 출력하라.

## 입력
- N Q
- A1..AN
- Q줄: l r k

## 출력
- 질의마다 답

## 제한(예시)
- N,Q ≤ 200,000
- |Ai| ≤ 1e9
""".strip(),
        "hint": """
- 값 좌표압축 + prefix 버전 퍼시스턴트 세그트리.
- root[r] - root[l-1]의 “개수 차이”를 따라 k번째를 내려감.
""".strip(),
        "solution": """
### 해설(개요)
root[i] = root[i-1]에서 A[i] rank 위치 +1 업데이트한 버전.
질의 시 두 루트의 왼쪽 카운트 차이를 보며 좌/우로 내려가 k번째를 찾음.
시간: 빌드 O(N log M), 질의 O(log M).
""".strip(),
    },
    {
        "id": 8,
        "title": "암호문 복원(사전 단어 최소 비용, Aho–Corasick)",
        "body": """
## 문제
문자열 S를 사전 단어들을 이어 붙여 정확히 만들고 싶다.
각 단어 w에는 비용 c(w)가 있다. 최소 비용을 구하라. 불가능하면 -1.

## 입력
- S
- D
- D줄: word cost

## 출력
- 최소 비용 또는 -1

## 제한(예시)
- |S| ≤ 200,000
- 사전 단어 총 길이 합 ≤ 400,000
""".strip(),
        "hint": """
- Aho–Corasick + DP.
- dp[i]=S[:i] 최소 비용. i에서 끝나는 매칭 단어 길이 L로 갱신.
""".strip(),
        "solution": """
### 해설(개요)
AC 자동자 구축 후 S를 한 번 스캔.
i에서 끝나는 모든 단어(길이 L, 비용 c)에 대해:
dp[i]=min(dp[i], dp[i-L]+c).
매칭 열거가 많으면 output-link로 필요한 것만 순회.
""".strip(),
    },
    {
        "id": 9,
        "title": "슬라이딩 윈도우 중앙값(삭제 포함 2-힙)",
        "body": """
## 문제
길이 N 배열과 윈도우 크기 K가 주어진다.
각 i=1..N-K+1에 대해 A[i..i+K-1]의 중앙값(짝수면 아래쪽 중앙값)을 출력하라.

## 입력
- N K
- A1..AN

## 출력
- N-K+1개의 중앙값

## 제한(예시)
- N ≤ 200,000
""".strip(),
        "hint": """
- max-heap(왼쪽) + min-heap(오른쪽) 2개 유지.
- 윈도우에서 빠지는 값은 “지연 삭제”(hash map 카운트)로 처리.
""".strip(),
        "solution": """
### 해설(개요)
왼쪽 힙 크기가 (K+1)//2가 되도록 유지하면 top이 중앙값.
삽입/삭제 시 힙 균형 조정 + lazy deletion으로 top 정리.
전체 O(N log N).
""".strip(),
    },
    {
        "id": 10,
        "title": "서브트리 최빈색(DSU on Tree)",
        "body": """
## 문제
트리의 각 정점에는 색 color[i]가 있다.
각 정점 v에 대해 “v의 서브트리에서 가장 많이 등장하는 색의 등장 횟수”를 구하라.
(최빈색이 여러 개면 횟수만 출력)

## 입력
- N
- color1..colorN
- N-1줄 간선

## 출력
- v=1..N에 대해 답

## 제한(예시)
- N ≤ 200,000
""".strip(),
        "hint": """
- DSU on Tree(=small-to-large, sack)로 서브트리 빈도 누적.
- heavy child는 유지하고, light는 합치고 버리는 방식.
""".strip(),
        "solution": """
### 해설(개요)
dfs로 subtree size/ heavy child 계산.
solve(v, keep):
- light child 먼저 keep=0으로 처리(기여 제거)
- heavy child keep=1로 처리(빈도 유지)
- light들의 빈도를 heavy에 합침
- 현재 v 색도 반영, 현재 서브트리 최댓값 기록
keep=0이면 서브트리 빈도 제거.
""".strip(),
    },
    {
        "id": 11,
        "title": "Range Chmin + Range Sum(세그트리 비츠)",
        "body": """
## 문제
길이 N 배열 A에 대해 Q 연산:
- `C l r x` : A[l..r] = min(A[l..r], x)
- `S l r` : sum(A[l..r]) 출력

## 제한(예시)
- N,Q ≤ 200,000
- Ai,x ≤ 1e9
""".strip(),
        "hint": """
- Segment Tree Beats: 노드에 max, second_max, count_max, sum 유지.
- x < max일 때만 내려가거나(필요하면 push) 노드 레벨에서 처리.
""".strip(),
        "solution": """
### 해설(개요)
노드가 가진 최대값 maxV와 두 번째 최대값 smaxV를 사용.
chmin x에서:
- x >= maxV면 변화 없음
- smaxV < x < maxV면 maxV인 원소들만 x로 낮춰 sum 갱신(노드에서 처리)
- x <= smaxV면 자식으로 push하며 재귀
S는 sum을 이용.
""".strip(),
    },
    {
        "id": 12,
        "title": "최소 비용 최대 유량(MCMF)",
        "body": """
## 문제
용량과 비용이 있는 방향 그래프에서 s→t로 가능한 한 많이 보내되,
(또는 요구 유량 F를 만족시키되) 총 비용을 최소화하라.
포맷은 너희가 정해서 넣으면 됨.

## 제한(예시)
- 정점 ≤ 500, 간선 ≤ 5000
""".strip(),
        "hint": """
- Successive Shortest Path + potentials(잠재치)로 다익스트라 반복.
""".strip(),
        "solution": """
### 해설(개요)
잔여 그래프에서 (비용) 최단경로를 반복적으로 찾아 augment.
잠재치(potential)로 reduced cost를 비음수로 만들어 매번 다익스트라 사용.
유량이 더 이상 못 가거나 목표 유량 채우면 종료.
""".strip(),
    },
    {
        "id": 13,
        "title": "일반 CRT(서로소 아님)",
        "body": """
## 문제
K개의 합동식이 주어진다:
x ≡ a_i (mod m_i)
m_i들은 서로소일 필요가 없다. 해가 존재하면 x의 최소 비음수 해를 출력하고,
없으면 -1을 출력하라.

## 제한(예시)
- K ≤ 200,000
- m_i ≤ 1e12
""".strip(),
        "hint": """
- 두 합동식을 병합하는 함수(extended gcd)로 fold.
- (a2-a1) % gcd(m1,m2) == 0 조건 체크.
""".strip(),
        "solution": """
### 해설(개요)
(x≡r1 mod m1), (x≡r2 mod m2) 병합:
g=gcd(m1,m2).
(r2-r1)%g!=0이면 불가능.
가능하면 확장 유클리드로 해를 구해 r를 lcm(m1,m2)로 갱신.
이를 K번 누적 병합.
""".strip(),
    },
    {
        "id": 14,
        "title": "브리지와 2-간선연결요소(Bridge / 2ECC)",
        "body": """
## 문제
무방향 그래프에서 모든 브리지(다리)를 찾고,
브리지를 제거했을 때의 2-간선연결요소(2-edge-connected components)를 구하라.
각 정점이 속한 컴포넌트 번호를 출력하라.

## 제한(예시)
- N ≤ 200,000
- M ≤ 300,000
""".strip(),
        "hint": """
- DFS 타임스탬프 tin/low로 브리지 판정.
- 브리지를 제외하고 다시 DFS/DSU로 컴포넌트 번호 부여.
""".strip(),
        "solution": """
### 해설(개요)
DFS로 tin[u], low[u] 계산.
트리 간선 u-v에서 low[v] > tin[u]이면 (u,v)는 브리지.
브리지 목록을 표시한 뒤, 브리지가 아닌 간선만 따라가며 컴포넌트 라벨링.
""".strip(),
    },
    {
        "id": 15,
        "title": "구간 서로 다른 값 개수(Mo's Algorithm)",
        "body": """
## 문제
수열 A(길이 N)와 Q개의 질의 (l,r)가 주어진다.
각 질의마다 A[l..r]에 등장하는 서로 다른 값의 개수를 출력하라.

## 제한(예시)
- N,Q ≤ 200,000
""".strip(),
        "hint": """
- 오프라인 정렬(Mo): 블록 크기 ≈ sqrt(N).
- 현재 구간의 빈도 배열과 distinct 카운트 유지.
""".strip(),
        "solution": """
### 해설(개요)
질의를 (l 블록, r) 기준으로 정렬.
포인터 curL/curR을 이동하며 add/remove를 O(1)로 갱신.
전체 O((N+Q)*sqrt(N)) 정도.
""".strip(),
    },
    {
        "id": 16,
        "title": "오일러 투어 + Fenwick(서브트리 합 업데이트)",
        "body": """
## 문제
트리에서 연산 Q개:
- `U v x` : 정점 v 값에 x를 더함 (add)
- `S v` : v의 서브트리 값의 합 출력

## 제한(예시)
- N,Q ≤ 200,000
""".strip(),
        "hint": """
- Euler tour로 서브트리를 연속 구간 [tin, tout]으로 만든다.
- Fenwick(BIT)로 점 업데이트 + 구간합.
""".strip(),
        "solution": """
### 해설(개요)
DFS로 tin[v], tout[v] 부여(서브트리 연속성).
U v x → BIT.add(tin[v], x)
S v → BIT.sum(tout[v]) - BIT.sum(tin[v]-1)
""".strip(),
    },
    {
        "id": 17,
        "title": "DAG 최장경로 개수(위상정렬 + DP)",
        "body": """
## 문제
방향 그래프는 DAG이다. 1에서 N까지 가는 경로 중
“최장 경로 길이”와 “그 최장 경로 개수(mod M)”를 구하라.
(경로 길이는 간선 수)

## 제한(예시)
- N ≤ 200,000, M ≤ 300,000
""".strip(),
        "hint": """
- 위상정렬 후 dpLen[v]=최장 길이, dpCnt[v]=그 개수.
- relax 시 길이가 같으면 개수 더함.
""".strip(),
        "solution": """
### 해설(개요)
위상정렬 순서로 v를 처리.
간선 v→to:
cand = dpLen[v] + 1
- cand > dpLen[to]: dpLen[to]=cand, dpCnt[to]=dpCnt[v]
- cand == dpLen[to]: dpCnt[to]+=dpCnt[v] (mod)
초기 dpLen[1]=0, dpCnt[1]=1.
""".strip(),
    },
    {
        "id": 18,
        "title": "서로 다른 부분문자열 개수(Suffix Array/LCP)",
        "body": """
## 문제
문자열 S가 주어진다. 서로 다른 부분문자열의 개수를 구하라.

## 제한(예시)
- |S| ≤ 200,000
""".strip(),
        "hint": """
- suffix array 정렬 후 인접 접미사 LCP를 이용.
- 전체 부분문자열 수 = n(n+1)/2
- 중복 제거량 = sum(LCP)
""".strip(),
        "solution": """
### 해설(개요)
접미사들을 정렬한 SA와 인접 LCP 배열을 구한다.
서로 다른 부분문자열 개수 = n(n+1)/2 - Σ LCP[i].
(각 접미사가 새로 기여하는 길이 = (n-SA[i]) - LCP[i])
""".strip(),
    },
    {
        "id": 19,
        "title": "전역 카운트다운(행렬 거듭제곱)",
        "body": """
## 문제
상태가 0..S-1로 총 S개. 전이 행렬 A(S×S)와 길이 L이 주어진다.
초기 벡터 init에서 시작해 길이 L 이후의 상태 분포를 계산하고,
최종 벡터의 합(또는 특정 상태 값)을 mod로 출력하라.
(출력 정의는 너희 포맷으로 정해도 됨)

## 제한(예시)
- S ≤ 200
- L ≤ 1e18
""".strip(),
        "hint": """
- 분할정복으로 행렬 빠른 거듭제곱.
- A^L을 구해 init과 곱한다.
""".strip(),
        "solution": """
### 해설(개요)
A^L을 이진 거듭제곱으로 O(S^3 log L)에 계산.
init(1×S) * A^L (또는 A^L * init)을 곱해 결과를 얻고 mod 적용.
S가 크면 파이썬 최적화/희소성 활용 고려.
""".strip(),
    },
]
