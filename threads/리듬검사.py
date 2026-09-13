# -*- coding: utf-8 -*-
"""스레드 초안 검사. 기준값 출처: corpus/2026-09-11_본문수집.md(실제 본문 92문장) + 8부작 원안(849자).

   중요: 문장 길이는 '합격 기준'이 아니라 참고값이다.
   길이를 맞추려고 문장을 자르면 의미 없는 토막이 되고 정보 밀도가 떨어진다.
   반드시 통과해야 하는 건 글자수 / 어휘 온도 / C-11 / 종결 반복 넷이다."""
import re, sys, statistics, os

타격 = ['눈탱이','목줄','인질','갈취','뜯기','뜯길','튀','유령','참사','쇠사슬','깡통','까발','팩폭','속지','속아',
        '사망','쓰레기','하수구','통행세','독식','주범','날리','잔돈','대놓고','통째로','번지르르','백지','갇힌',
        '때려박','수두룩','멍때리','태우','깔려','바닥','어이없','소름','아찔','경악','최악','붓고','갈아치','버리고','못 버티','0곳','0점']
C11 = re.compile(r'[가-힣]{1,5}(?:고|며|지만|면서|아서|어서|는데|니까),')

def 문장들(t):
    return [s.strip() for s in re.split(r'(?<=[.?!])\s+|\n', t) if 1 < len(s.strip()) < 200]

def 검사(경로):
    t = open(경로, encoding='utf-8').read()
    S = 문장들(t); L = [len(s) for s in S]
    타 = sum(t.count(w) for w in 타격); 밀도 = 1000 * 타 / len(t)
    인용 = t.count('"') + t.count("'") + t.count('“') + t.count('"')
    ends = [s[-3:] for s in S]; run = worst = 1
    for i in range(1, len(ends)):
        run = run + 1 if ends[i] == ends[i-1] else 1
        worst = max(worst, run)

    print(f"\n{os.path.basename(경로)} — {len(t)}자 / {len(S)}문장")
    print("  [합격 기준]")
    print(f"   {'통과' if len(t)<=500 else '초과'}  글자수         {len(t):>5}자   (상한 500)")
    print(f"   {'통과' if 밀도>=10 else '미달'}  어휘 온도      {밀도:>5.1f}/1000자  (원안 38.9 · 10 미만이면 밋밋)")
    print(f"   {'통과' if not C11.findall(t) else '미달'}  C-11 쉼표     {len(C11.findall(t)):>5}건   (AI 최강 신호 · 0이어야 함)")
    print(f"   {'통과' if worst<4 else '미달'}  같은 종결 연속  {worst:>5}회   (4 이상이면 손볼 것)")
    print("  [참고값 — 맞추려고 문장 자르지 말 것]")
    print(f"        평균 {statistics.mean(L):>4.0f}자 · 중앙값 {statistics.median(L):>3.0f}자   (실제 본문 22 / 20)")
    print(f"        짧은문장 {100*len([x for x in L if x<=12])/len(L):>3.0f}%  대사 {인용}개   (실제 본문 25% / 34개)")

if __name__ == '__main__':
    for p in sys.argv[1:]:
        검사(p)
