"""Run with the released wheel, or either isolated source-built wheel.

All amounts are synthetic. Decimal discounts payments directly; it does not
copy the implementation's Newton step or future-value residual.
"""
import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
from decimal import Decimal, localcontext
from pathlib import Path

import numpy as np
import pyxirr as px


def present_value(rate, n, payment, due=False):
    with localcontext() as ctx:
        ctx.prec = 70
        r = rate if isinstance(rate, Decimal) else Decimal.from_float(float(rate))
        p = Decimal.from_float(float(payment))
        v = 1 / (1 + r)
        discount = Decimal(1) if due else v
        total = Decimal(0)
        for _ in range(n):
            total -= p * discount
            discount *= v
        return +total


def bisect_rate(n, payment, principal, due=False):
    with localcontext() as ctx:
        ctx.prec = 70
        lo, hi = Decimal('-0.5'), Decimal('0.5')
        pv = Decimal.from_float(float(principal))
        assert present_value(lo, n, payment, due) > pv
        assert present_value(hi, n, payment, due) < pv
        for _ in range(180):
            mid = (lo + hi) / 2
            if present_value(mid, n, payment, due) > pv:
                lo = mid
            else:
                hi = mid
        result = (lo + hi) / 2
        assert abs(present_value(result, n, payment, due) - pv) / pv < Decimal('1e-45')
        return str(result)


def payment_for(n, rate, principal, due):
    with localcontext() as ctx:
        ctx.prec = 70
        factor = present_value(Decimal(str(rate)), n, -1., due)
        return float(-Decimal(str(principal)) / factor)


def call_vector(n, payment, principal, due, guess, shape):
    periods = {'list': [n], 'ndarray': np.array([n]),
               'matrix': np.array([[n], [n]])}[shape]
    result = px.rate(periods, payment, principal,
                     pmt_at_beginning=due, guess=guess)
    values = np.asarray(result, dtype=float).ravel().tolist()
    assert all((math.isnan(x) and math.isnan(values[0])) or x == values[0]
               for x in values)
    return None if not math.isfinite(values[0]) else values[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--expect', choices=['affected', 'corrected'], required=True)
    args = ap.parse_args()
    cases = []
    for n, guess in [(240, 1.), (360, .5), (480, .3), (600, .2), (1200, .1)]:
        oracle = bisect_rate(n, -1000., 200000.)
        for shape in ['list', 'ndarray', 'matrix']:
            observed = call_vector(n, -1000., 200000., False, guess, shape)
            residual = None if observed is None else str(
                present_value(observed, n, -1000.) - Decimal(200000))
            cases.append(dict(family='unconverged', nper=n, pmt=-1000., pv=200000.,
                              due=False, guess=guess, shape=shape, observed=observed,
                              oracle=oracle, pv_residual=residual,
                              contract_pass=observed is None))

    for n in [1, 2, 12]:
        for due in [False, True]:
            if n == 1 and due:
                continue  # A single time-zero payment does not identify a rate.
            for rate in [-.01, 0., .01, .1]:
                for principal in [1000., 1e6]:
                    payment = payment_for(n, rate, principal, due)
                    oracle = bisect_rate(n, payment, principal, due)
                    for family, guess in [('zero_guess', 0.), ('ordinary', .1)]:
                        for shape in ['list', 'ndarray', 'matrix']:
                            observed = call_vector(n, payment, principal, due, guess, shape)
                            passed = observed is not None and abs(observed - float(oracle)) < 2e-7
                            cases.append(dict(family=family, nper=n, pmt=payment,
                                              pv=principal, due=due, guess=guess, shape=shape,
                                              observed=observed, oracle=oracle,
                                              contract_pass=passed))
    counts = {family: dict(total=sum(c['family'] == family for c in cases),
                          passed=sum(c['family'] == family and c['contract_pass'] for c in cases))
              for family in ['unconverged', 'zero_guess', 'ordinary']}
    native = Path(px._pyxirr.__file__)
    data = dict(metadata=dict(python=platform.python_version(), platform=platform.platform(),
                              pyxirr=px.__version__, numpy=np.__version__,
                              binary_sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
                              binary_path=str(native)), counts=counts, cases=cases)
    args.output.parent.mkdir(exist_ok=True, parents=True)
    args.output.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')
    print(json.dumps(counts, indent=2))
    if args.expect == 'affected':
        assert counts['unconverged']['passed'] == 0
        assert counts['zero_guess']['passed'] == 0
        # The initial fixed control grid exposed one additional failing input
        # in three shapes. Retain it; do not remove it to make controls pass.
        assert counts['ordinary']['passed'] == 117
    else:
        assert all(c['contract_pass'] for c in cases), [c for c in cases if not c['contract_pass']][:3]
    print('Expected-state verification PASSED')


if __name__ == '__main__':
    main()
