# Denton, Jay B.L.
# jbd9386
# 2019-05-02

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
from CohenSutherland import clipLine
from resolveBezierPatch import resolveBezierPatch


class cl_world :
  def __init__( self, objects = [], canvases = []) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas, modelData, doClip, doPerspective,
                              doEuler, resolution) :
    width = int(canvas.cget("width"))
    height = int(canvas.cget("height"))
    v = modelData.getViewport()
    vxMin = v[0] * width
    vxMax = v[2] * width
    vyMin = v[1] * height
    vyMax = v[3] * height
    portal = (vxMin, vyMin, vxMax, vyMax)

    for v1Num, v2Num, v3Num in modelData.getFaces() :
      v1 = modelData.getTransformedVertex( v1Num, doPerspective, doEuler )
      v2 = modelData.getTransformedVertex( v2Num, doPerspective, doEuler )
      v3 = modelData.getTransformedVertex( v3Num, doPerspective, doEuler )

      self.drawTriangle(canvas, v1, v2, v3, portal, doClip)

    for pline in modelData.getPatch():
      controlPts = []
      for v16 in pline:
        v = modelData.getTransformedVertex( v16, doPerspective, doEuler )
        controlPts.append(v)
      pointList = resolveBezierPatch(resolution, controlPts)

      for row in range(resolution - 1):
        rowStart = row * resolution

        for col in range(resolution - 1):
          here = rowStart + col
          there = here + resolution

          triangleA = (pointList[here], pointList[there], pointList[there + 1])
          triangleB = (pointList[there + 1], pointList[here + 1], pointList[here])

          self.drawTriangle(canvas, triangleA[0], triangleA[1], triangleA[2], portal, doClip)
          self.drawTriangle(canvas, triangleB[0], triangleB[1], triangleB[2], portal, doClip)

  def drawTriangle(self, canvas, v1, v2, v3, portal, doClip):
    if doClip:
      for (vax, vay, _), (vbx, vby, _) in [(v1, v2), (v2, v3), (v3, v1)]:
        doDraw, vax, vay, vbx, vby = clipLine(vax, vay, vbx, vby, portal)
        if doDraw:
          canvas.create_line(vax, vay, vbx, vby)

    else:
      canvas.create_line(*v1[:-1], *v2[:-1], *v3[:-1], *v1[:-1])

  def redisplay( self, canvas, event ) :
    pass

#----------------------------------------------------------------------
