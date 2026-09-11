# -*- coding: utf-8 -*-
"""스레드 초안을 실제 수집 본문의 리듬 수치와 대조한다.
   사용법: python3 threads/리듬검사.py 초안.txt
   기준값 출처: threads/corpus/2026-09-11_본문수집.md (실제 스레드 본문 92문장)"""
import re, sys, statistics, os

기준 = {'평균': 22, '중앙값': 20, '짧은문장비율': 25, '인용부호': 34}
C11 = re.compile(r'[가-힣]{1,5}(?:고|며|지만|면서|아서|어서|는데|니까),')

def 문장들(t):
    return [s.strip() for s in re.split(r'(?<=[.?!])\s+|\n', t) if 1 < len(s.strip()) < 200]

def 검사(경로):
    t = open(경로, encoding='utf-8').read()
    S = 문장들(t); L = [len(s) for s in S]
    짧 = 100 * len([x for x in L if x <= 12]) / len(L)
    평균, 중앙 = statistics.mean(L), statistics.median(L)
    인용 = t.count('"') + t.count("'") + t.count('“') + t.count('"')
    ends = [s[-3:] for s in S]
    run = worst = 1
    for i in range(1, len(ends)):
        run = run + 1 if ends[i] == ends[i-1] else 1
        worst = max(worst, run)

    def 줄(라벨, 값, 목표, 단위='', 비교='근접'):
        if 비교 == '근접':
            ok = abs(값 - 목표) <= 목표 * 0.25
        else:
            ok = 값 >= 목표
        print(f"  {'통과' if ok else '미달'}  {라벨:12} {값:>5.0f}{단위}   (실제 본문 {목표}{단위})")
        return ok

    print(f"\n{os.path.basename(경로)} — {len(t)}자 / {len(S)}문장")
    print(f"  {'통과' if len(t)<=500 else '초과'}  {'글자수':12} {len(t):>5}자   (상한 500자)")
    줄('평균 문장', 평균, 기준['평균'], '자')
    줄('중앙값', 중앙, 기준['중앙값'], '자')
    줄('짧은문장(12자↓)', 짧, 기준['짧은문장비율'], '%', '이상')
    print(f"  {'통과' if t.count('근데')>=1 else '미달'}  {'전환어 근데':12} {t.count('근데'):>5}회   (실제 본문 11회/2125자)")
    print(f"  {'통과' if 인용>=2 else '미달'}  {'대사 인용부호':12} {인용:>5}개   (실제 본문 34개 — 사람이 말을 한다)")
    print(f"  {'통과' if worst<4 else '미달'}  {'같은 종결 연속':12} {worst:>5}회   (4회 이상이면 손볼 것)")
    print(f"  {'통과' if not C11.findall(t) else '미달'}  {'C-11 쉼표':12} {len(C11.findall(t)):>5}건   (연결어미 뒤 쉼표 = AI 최강 신호)")

if __name__ == '__main__':
    for p in sys.argv[1:]:
        검사(p)
