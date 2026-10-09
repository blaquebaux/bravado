#!/usr/bin/python3
# =============================================================================
# bravado_1.py — the hall-of-fame audit: was the legend edge, convexity-luck, or ruin?
#
# The celebrated unorthodox bets are told as genius. Ex-ante they were asymmetric GAMBLES, and the
# fat-tail scorecard sorts them by the sign of their tail:
#   • positive-convexity / tail-seeking (Taleb, the Big Short, Paulson-Abacus, Soros/GBP) — paid HUGE
#     once, bleeds otherwise, un-timeable; "right" but not repeatable.
#   • negative-skew / ruin (MF Global, LTCM, the Volmageddon short-vol blowups) — steady pennies, one
#     catastrophic loss; the shape the scorecard flags BEFORE the blowup.
# Most legends predate Alpaca's 2016+ window and used bespoke instruments, so Part A is a documented-
# record TAXONOMY (facts, not a backtest). Part B then proves the two shapes EMPIRICALLY on the one era
# fully in-sample — 2018 "Volmageddon", 2020, 2022 — via instruments that still trade.
# =============================================================================
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from _bravado_common import panel, rets

def shape(r, months):
    r = np.asarray(r, float); c = np.cumprod(1+r); dd = (c/np.maximum.accumulate(c)-1).min()
    sd = r.std(); sh = r.mean()/sd*math.sqrt(252) if sd>0 else float("nan"); z=(r-r.mean())/sd
    cagr = c[-1]**(252/len(r))-1
    mo = {}
    for m,x in zip(months,r): mo[m]=mo.get(m,1.0)*(1+x)
    return dict(sh=sh, cagr=cagr, dd=float(dd), skew=float(np.mean(z**3)), kurt=float(np.mean(z**4))-3,
                wday=float(r.min()), wmo=min(v-1 for v in mo.values()))

# Part A — the documented record (the historical facts, not a backtest)
LEGENDS = [
    # name, year, shape, outcome, repeatable?, in 2016+ window?
    ("Soros — breaking the GBP",   1992, "convex / contrarian",    "+$1B in days",          "no — one policy peg", "no"),
    ("LTCM — levered convergence", 1998, "NEGATIVE-SKEW / ruin",       "~4y of ~40%/yr, then −100%", "no — the ruin realized", "no"),
    ("Paulson / Burry — Big Short",2007, "convex / contrarian",        "+$15B / +489%",         "no — Paulson gave it back later", "no"),
    ("Goldman/Paulson — Abacus",   2007, "convex / one-sided",         "the short side paid once","no — a single structured bet", "no"),
    ("MF Global — Euro repo-to-mat",2011,"NEGATIVE-SKEW / ruin",       "steady carry, then bankruptcy","no — leverage on a 'sure thing'","no"),
    ("XIV / SVXY — Volmageddon",   2018, "NEGATIVE-SKEW / ruin",       "brilliant Sharpe, then −90% in a day","no — the shape self-destructs","YES"),
    ("Universa / Taleb — tail",    2020, "convex / tail-seeking",      "+4000% in the crash month","as insurance, not as alpha","partial (long-vol)"),
]

def main():
    print("="*98); print("BRAVADO — the hall-of-fame audit: edge, convexity-luck, or ruin?"); print("="*98)

    print("\n  PART A — the documented record (facts, not a backtest)")
    print(f"    {'legend':30}{'yr':>5}  {'bet-shape':24}{'repeatable?':34}{'in-window'}")
    for n,y,s,o,rep,win in LEGENDS:
        print(f"    {n:30}{y:>5}  {s:24}{rep:34}{win}")
    print("    → two families: convex winners PAID ONCE and can't be timed; steady-Sharpe winners were")
    print("      negative-skew RUIN. 'Genius' ex-post = asymmetric gamble ex-ante.")

    # Part B — the shapes, empirically, on what trades in 2016+
    specs = {"SVXY":"short-vol (the Volmageddon RUIN shape)", "VIXM":"long-vol (the Taleb CONVEXITY shape)",
             "UPRO":"3x SPY (leverage amplifies the tail)", "SPY":"baseline"}
    P, dates = panel(list(specs)); R = {s: rets(P[s]) for s in P}
    L = min(len(R[s]) for s in R); months=[d[:7] for d in dates[1:]][-L:]
    print(f"\n  PART B — the two shapes, EMPIRICAL (Alpaca {dates[-L]}..{dates[-1]}, {L/252:.1f}y)")
    print(f"    {'proxy':6}{'Sharpe':>8}{'CAGR':>9}{'maxDD':>8}{'skew':>7}{'exKurt':>8}{'worstDay':>10}{'worstMo':>9}")
    for s in specs:
        if s not in R: continue
        m = shape(R[s][-L:], months)
        print(f"    {s:6}{m['sh']:>+8.2f}{m['cagr']*100:>+8.1f}%{m['dd']*100:>+7.0f}%{m['skew']:>+7.2f}{m['kurt']:>+8.1f}{m['wday']*100:>+9.1f}%{m['wmo']*100:>+8.1f}%")
    print("    "+specs["SVXY"]+" vs "+specs["VIXM"])

    # Part C — the Volmageddon close-up: the only legend fully in-sample ---------------------
    if "SVXY" in R:
        svxy = R["SVXY"]; d = dates[1:]
        pre = np.array([svxy[i] for i in range(len(d)) if d[i] < "2018-02-05"])
        preSh = pre.mean()/pre.std()*math.sqrt(252) if len(pre)>30 and pre.std()>0 else float("nan")
        worst_i = int(np.argmin(svxy));
        print("\n  PART C — VOLMAGEDDON close-up (SVXY, the one legend fully in Alpaca's window)")
        print(f"      pre-blowup Sharpe (2016 → 2018-02-04): {preSh:+.2f}   ← looked like genius")
        print(f"      worst single day: {svxy[worst_i]*100:+.1f}% on {d[worst_i]}   ← the ruin, in one session")
        print(f"      a +{preSh:.0f}-Sharpe track record erased in a day is the scorecard's whole point:")
        print(f"      negative skew + fat kurtosis flag the steamroller BEFORE it arrives.")

    print("\n  READ: bravado is a diagnostic, not a sleeve. The legends are SURVIVORSHIP — convex bets that")
    print("  paid once (un-timeable), or negative-skew carry that blew up (flagged ex-ante by skew/kurtosis).")
    print("  This is the empirical motivation for the `brink` ruin-gate: a great Sharpe can hide a path to zero.")

if __name__ == "__main__":
    main()
