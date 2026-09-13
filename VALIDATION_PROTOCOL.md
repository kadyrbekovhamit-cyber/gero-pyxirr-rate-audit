# PyXIRR RATE validation protocol

Fixed on 13 September 2026 after exploratory probing, before testing the candidate Rust correction.

## Source and scope

PyPI release 0.10.8 and upstream main commit 5f31a85684051fb6badb542afba0ac1af5a68f9c. Source snapshots are isolated from existing research checkouts. All calculations and builds use one worker. No customer records are used.

Exclude the previously reported NL day counts, first annuity-due principal payment, Fineract calculations, FinancePy principal scaling and mortgage small-rate defects. XIRR cash-flow scaling has existing issues #62 and #75 and is not a new finding here.

## Contracts

1. A vectorized RATE result that has not met its iteration tolerance must be reported as failure, regardless of the sign of the last Newton step.
2. A finite zero starting guess is in the documented rate domain. Where the equation and derivative have finite limits at zero and the root is unique, array wrapping must not turn a successful ordinary calculation into failure solely through division by zero.
3. For conventional loans, compare rates with a separate Decimal bisection of discounted payments, using recurrence rather than the implementation's future-value Newton equation.
4. Verify ordinary controls, positive and negative expected rates, beginning/end payments, scaling, lists, NumPy arrays and broadcasting.

## Candidate scope

Use an absolute, finite final step when rejecting unconverged vector elements; evaluate the analytic zero-rate limit in the vector derivative. The first correction reports nonconvergence; it does not claim to solve those difficult starts. This is not a redesign or comprehensive validation of the scalar or vector root solvers, near-zero cancellation, extreme magnitudes or multiple roots.

## Gates

- Run the public Python API against the unmodified released wheel, a freshly built upstream wheel and a freshly built candidate wheel.
- Verify the released and native baseline have the same results in this validation set.
- Add native Rust regressions and run the existing complete Rust test suite on the candidate.
- Restore each defective source fragment separately and require its focused regression to fail.
- Retain versions, source and binary hashes, raw results, duplicate search queries, and a minimal reproducer.
- Do not describe broad solver convergence issues in XIRR as novel or claim production losses.

## Recorded amendment after the first control run

The fixed released-wheel grid had 117/120 ordinary controls passing. The retained exception (three shapes of the same input) is a two-period annuity due: principal 1000, payment -497.48743718592965, default guess 0.1. Its unique rate is -0.01, but the vector solver returns approximately 4.96e-15. Original results and the failed gate are retained as `results/release-initial.json` and `logs/reproduce-release-initial.log`.

This exposed cancellation during a near-zero intermediate iterate, beyond division at an exactly zero guess. Before building/testing the candidate, extend the zero-limit correction to a fourth-order annuity-factor series when `abs(r) * max(abs(n), 1) <= 1e-4`, with its corresponding derivative. Retain every original control and require all 255 observations to pass on the candidate. The baseline expected count is now explicitly 117/120 ordinary controls, not 120/120. Add a native regression for this newly observed path and include it in the mutation control.
