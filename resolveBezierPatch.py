# Denton, Jay B.L.
# jbd9386
# 2019-05-02

#----------------------------------------------------------------------
# This code takes the desired resolution and a list of the transformed
# control points for a Bézier patch and returns a list of the generated
# points for the surface.
import numpy

#----------------------------------------------------------------------
def resolveBezierPatch(resolution, controlPts):
  pointList = []

  for u in numpy.linspace(0.0, 1.0, resolution):
    for v in numpy.linspace(0.0, 1.0, resolution):
      point = (0.0, 0.0, 0.0)
      for i in range(4):
        for j in range(4):
          c = computeCValue(u, v, i, j)
          point = (point[0] + c * controlPts[i*4+j][0],
                   point[1] + c * controlPts[i*4+j][1],
                   0.0) # Since already projected on a 2D, so Z-axes=0.0

      pointList.append(point)

  return pointList

def computeCValue(u, v, i, j):
  return binomialCoef(3,i)*u**i*(1-u)**(3-i)*binomialCoef(3,j)*v**j*(1-v)**(3-j)

# Returns value of Binomial Coefficient C(n, k)
def binomialCoef(n, k):
  C = [[0 for x in range(k + 1)] for x in range(n + 1)]

  # Calculate value of Binomial Coefficient in bottom up manner
  for i in range(n + 1):
    for j in range(min(i, k) + 1):
      # Base Cases
      if j == 0 or j == i:
        C[i][j] = 1

      # Calculate value using previosly stored values
      else:
        C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

  return C[n][k]