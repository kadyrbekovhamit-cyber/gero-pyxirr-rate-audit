"""Native public-API checks around the new near-zero series boundary."""
import json
from decimal import Decimal
from pathlib import Path

import pyxirr as px

from reproduce import payment_for, present_value

rows = []
for n in [1, 2, 12, 120, 360, 1200]:
    threshold = 1e-4 / n
    for due in [False, True]:
        if n == 1 and due:
            continue
        for target in [-1.001*threshold, -.999*threshold, -1e-8,
                       0., 1e-8, .999*threshold, 1.001*threshold]:
            pmt = payment_for(n, target, 1000., due)
            for guess in [0., target*.9]:
                observed = px.rate([n], pmt, 1000., pmt_at_beginning=due, guess=guess)[0]
                residual = None if observed is None else float(present_value(observed, n, pmt, due) - Decimal(1000))
                passed = (observed is not None and abs(observed-target) < 1e-7
                          and abs(residual) < 1e-5)
                rows.append(dict(nper=n, due=due, target=target, guess=guess,
                                 pmt=pmt, observed=observed, pv_residual=residual, passed=passed))
out = dict(total=len(rows), passed=sum(x['passed'] for x in rows), cases=rows)
Path('results/series-boundary.json').write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
print(out['passed'], '/', out['total'])
assert all(x['passed'] for x in rows), [x for x in rows if not x['passed']][:5]
