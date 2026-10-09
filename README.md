# bravado

**The hall-of-fame audit — was the legend edge, convexity-luck, or ruin?**

The celebrated unorthodox bets — Soros breaking the pound, LTCM, the Big Short, Abacus, MF Global, the
Volmageddon short-vol blowups, Taleb's tail fund — are told as genius. Ex-ante they were asymmetric
*gambles*, and the family's fat-tail scorecard sorts them by the sign of their tail. This is the
graveyard turned on the legends: a diagnostic, not a tradable sleeve.

## Verdict

**DIAGNOSTIC — the legends are survivorship, and the two shapes are provable on real data.** Convex
winners (Big Short, Soros, Taleb) paid *once*, bleed otherwise, and can't be timed. Steady-Sharpe
winners (LTCM, MF Global, short-vol) were negative-skew *ruin* — a brilliant track record with a hidden
path to zero, flagged ex-ante by skew and kurtosis. "Genius" ex-post is an asymmetric gamble ex-ante.

## Part A — the record (facts, not a backtest)

| legend | yr | bet-shape | repeatable? |
|---|---|---|---|
| Soros — breaking the GBP | 1992 | convex / contrarian | no — one policy peg |
| LTCM — levered convergence | 1998 | **negative-skew / ruin** | no — the ruin realized (−100%) |
| Paulson / Burry — Big Short | 2007 | convex / contrarian | no — Paulson gave it back later |
| Goldman/Paulson — Abacus | 2007 | convex / one-sided | no — a single structured bet |
| MF Global — Euro repo-to-maturity | 2011 | **negative-skew / ruin** | no — leverage on a "sure thing" |
| XIV / SVXY — Volmageddon | 2018 | **negative-skew / ruin** | no — the shape self-destructs |
| Universa / Taleb — tail | 2020 | convex / tail-seeking | as insurance, not as alpha |

Two families: convex winners **paid once**; steady-Sharpe winners **blew up**.

## Part B — the two shapes, empirical (Alpaca 2016–2026, what still trades)

| proxy | Sharpe | CAGR | maxDD | skew | exKurt | worst day | worst mo |
|---|---|---|---|---|---|---|---|
| **SVXY** — short-vol (the *ruin* shape) | +0.41 | +2.0% | **−95%** | **−7.88** | **+175** | **−83%** | −90% |
| **VIXM** — long-vol (the *convexity* shape) | −0.23 | **−12.0%** | −79% | **+1.75** | +17 | −15% | −18% |
| UPRO — 3× SPY (leverage amplifies the tail) | +0.75 | +29.1% | −77% | −0.40 | +12 | −30% | −48% |
| SPY — baseline | +0.88 | +15.0% | −34% | −0.35 | +13 | −11% | −13% |

The two legend-shapes are night and day: short-vol carries pennies at a **−7.88 skew / +175 kurtosis**
until a −83% day; long-vol **bleeds −12%/yr** but with **positive skew (+1.75)** — it pays precisely
when everything else breaks. One is a steamroller; the other is insurance.

## Part C — Volmageddon close-up (the one legend fully in-window)

`SVXY` (short-vol) was the in-sample legend:

- **Pre-blowup Sharpe (2016 → 2018-02-04): +1.55** — it looked like genius.
- **Worst single day: −83% on 2018-02-06** — the ruin, in one session.

A +1.55-Sharpe track record erased in a day is the scorecard's entire purpose: the negative skew and
the fat kurtosis were visible *before* the blowup. The number that impresses is the number that kills.

## Why this is a diagnostic, and `bravado_2`

Most legends predate Alpaca's 2016+ window and used bespoke instruments (CDS on subprime, OTC FX,
levered repo), so their actual P&L can't be reconstructed here — Part A is the documented record. What
Part B *can* do, and does, is prove the two shapes on the instruments that survive. The honest product
of this study is a **gate, not a trade**: `brink` (the batch-3 ruin-probability / time-to-blowup
detector) is motivated directly by Part C — a great Sharpe can hide a path to zero. **`bravado_2`** =
reconstruct the 2008 levered-beta/credit ruin shape on Massive's 2003+ history, and wire `brink` to
flag it ex-ante.

## Reproduce

```bash
export ALPACA_KEY_ID=... ALPACA_SECRET_KEY=...
python3 research/bravado_1.py
```

*(SVXY changed from −1× to −0.5× after Feb 2018; the −83% day and pre-blowup record are the −1× era.)*

---

*Blaque Baux — a Carter Warrens research initiative. Research only; not investment advice. The legends
are survivorship; the scorecard is how you avoid being the next cautionary tale.*
