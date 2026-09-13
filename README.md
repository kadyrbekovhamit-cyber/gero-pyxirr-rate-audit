# PyXIRR RATE can return an unfinished calculation as a result

Independent GERO research by Xamit Kadirbekov, 13 September 2026. Synthetic inputs only; AI-assisted analysis and preparation.

[Technical report](REPORT.md) · [Evidence archive](gero-pyxirr-rate-evidence-2026-09-13.zip) · [Candidate patch](candidate.patch)

GERO page: prepared; awaiting restoration of Vercel access. The complete evidence and video are available in this repository.

GERO page: prepared; awaiting restoration of Vercel access. The complete evidence and video are available in this repository.

## What is demonstrated

With an explicit starting guess of **50% per period**, `pyxirr.rate([360], -1000, 200000, guess=0.5)` returns **13.5844% per period** in PyXIRR 0.10.8. Direct discounting gives **0.3655928% per period** for the same 200,000 principal and 360 end-of-period payments of 1,000. The vector solver has not converged; a signed final-step check lets the unfinished value through. The candidate returns `None` in this case — it does not find the valid root from that starting guess.

A second defect produces scalar/vector disagreements at a zero starting guess and cancellation near zero. A matched annuity-factor/derivative series fixes the tested cases.

## Evidence

- PyPI 0.10.8 and a fresh compiled baseline at `5f31a85684051fb6badb542afba0ac1af5a68f9c` reproduce the same outputs.
- Candidate: **242/242 Rust tests**, **255/255 main API observations** and **154/154 boundary checks** pass. These are checks, not separate bugs.
- Restoring each original defect fails its respective native regressions.
- Bounded duplicate screening found no direct match; priority is not guaranteed.
- No production use, customer losses or frequency of exposure were measured. No upstream acceptance is claimed.

## Reproduce

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install pyxirr==0.10.8
.venv/bin/python minimal_repro.py
```

The ZIP includes complete baseline/candidate source snapshots, build logs, numerical results, the patch and macOS arm64 wheels. Other platforms require building from source. See [REPORT.md](REPORT.md) for exact commands, constraints and the retained build warning.

Archive SHA-256: `c633cb43a3f77ff94972ad9b994830e5961a2253dfadfb5578476e87c4dfd38b`. The original evidence ZIP is unchanged; its prepublication statements describe the preparation stage.

## Video

[English video](pyxirr-rate-vector-convergence.mp4) · [Captions](pyxirr-rate-vector-convergence.en.vtt) · [Video source package](pyxirr-rate-video-source.zip). Original GERO graphics; preset synthetic Microsoft Andrew voice via edge-tts; no voice cloning, third-party footage or music.

## Provenance and rights

PyXIRR source retains its upstream Unlicense and attribution in both source snapshots. Original report and graphics: Xamit Kadirbekov / GERO. No affiliation with PyXIRR or its maintainers is implied.
