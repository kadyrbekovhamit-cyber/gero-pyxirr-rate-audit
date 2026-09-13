import pyxirr as px

print('PyXIRR', px.__version__)
print('Unconverged vector rate:', px.rate([360], -1000, 200000, guess=0.5))
print('Scalar, same start:', px.rate(360, -1000, 200000, guess=0.5))
print('Ordinary starting guess:', px.rate(360, -1000, 200000))
# The failed solve must return [None], not approximately [0.135844].

print('Zero guess, scalar:', px.rate(1, -1100, 1000, guess=0))
print('Zero guess, vector:', px.rate([1], -1100, 1000, guess=0))
# Both have the unique exact solution 0.1: 1000*(1+r) - 1100 = 0.

print('Zero-rate root, scalar:', px.rate(12, -100, 1200, guess=0))
print('Zero-rate root, vector:', px.rate([12], -100, 1200, guess=0))
# Both have the unique exact solution 0.0.
