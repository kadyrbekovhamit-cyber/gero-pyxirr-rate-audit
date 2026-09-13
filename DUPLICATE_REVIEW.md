# Duplicate screening

Checked 13 September 2026 using GitHub REST search, official issue/PR bodies and their comments. Raw responses and query timestamps are retained locally in `duplicate-screen/`.

| Repository query | Results |
|---|---:|
| `repo:Anexen/pyxirr rate` | 16 |
| `repo:Anexen/pyxirr convergence` | 1 |
| `repo:Anexen/pyxirr vector` | 4 |
| `repo:Anexen/pyxirr "guess"` | 8 |
| `repo:Anexen/pyxirr "zero"` | 14 |
| `repo:Anexen/pyxirr "negative"` | 9 |

Reviewed issues/PRs 17, 18, 21, 24, 25, 31, 36, 45, 54, 56, 57, 60, 62, 65, 68, 72, 75 and 77, including comments.

- [#17](https://github.com/Anexen/pyxirr/issues/17), [#18](https://github.com/Anexen/pyxirr/pull/18): original RATE implementation requests and implementation; no report of the two findings.
- [#21](https://github.com/Anexen/pyxirr/issues/21), [#36](https://github.com/Anexen/pyxirr/pull/36): adding array support and vectorized functions; no signed convergence-mask or zero-guess report found.
- [#24](https://github.com/Anexen/pyxirr/issues/24), [#25](https://github.com/Anexen/pyxirr/issues/25), [#45](https://github.com/Anexen/pyxirr/issues/45): IRR algorithms, multiple roots, speed and convergence configuration. The findings here concern the separate periodic RATE vector solver.
- [#31](https://github.com/Anexen/pyxirr/issues/31), [#54](https://github.com/Anexen/pyxirr/issues/54), [#56](https://github.com/Anexen/pyxirr/issues/56), [#57](https://github.com/Anexen/pyxirr/issues/57), [#60](https://github.com/Anexen/pyxirr/issues/60), [#65](https://github.com/Anexen/pyxirr/issues/65), [#68](https://github.com/Anexen/pyxirr/issues/68), [#72](https://github.com/Anexen/pyxirr/issues/72): IRR/XIRR disagreements, multiple roots, initial guesses or dated-flow convergence. These must not be presented as new general discoveries about XIRR.
- [#62](https://github.com/Anexen/pyxirr/issues/62), [#75](https://github.com/Anexen/pyxirr/issues/75): known cash-flow magnitude/normalization defects. Explicitly excluded from novelty claims.
- [#77](https://github.com/Anexen/pyxirr/pull/77): our prior PPMT annuity-due correction; different method and source branches.
- Prior local NL day-count, actuarial, loan-schedule, Fineract and FinancePy reports were screened and excluded before narrowing this investigation.

Conclusion: no direct duplicate of the signed final-step test in `rate_vec`, or of its zero-rate derivative singularity, was found in this bounded search. This is not a guarantee of priority or absence of reports elsewhere. No new issue, PR, social reply or site publication was sent during this search task.
