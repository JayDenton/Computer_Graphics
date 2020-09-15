# Denton, Jay B.L.
# jbd9386
# 2019-05-02

#---------#---------#---------#---------#---------#--------#
import sys
import math

#----------------------------------------------------------------------
class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.m_Patch    = []

    self.m_minX     = float( '+inf' )
    self.m_maxX     = float( '-inf' )
    self.m_minY     = float( '+inf' )
    self.m_maxY     = float( '-inf' )
    self.m_minZ     = float( '+inf' )
    self.m_maxZ     = float( '-inf' )

    self.m_sx       = 1.0
    self.m_ax       = 0.0
    self.m_sy       = 1.0
    self.m_ay       = 0.0

    self.m_d = None

    self.m_r00 = 0.0
    self.m_r01 = 0.0
    self.m_r02 = 0.0
    self.m_r10 = 0.0
    self.m_r11 = 0.0
    self.m_r12 = 0.0
    self.m_r20 = 0.0
    self.m_r21 = 0.0
    self.m_r22 = 0.0

    self.m_ex = 0.0
    self.m_ey = 0.0
    self.m_ez = 0.0


    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    with open( inputFile, 'r' ) as fp :
      lines = fp.read().replace('\r', '' ).split( '\n' )

    for ( index, line ) in enumerate( lines, start = 1 ) :
      line = line.strip()
      if ( line == '' or line[ 0 ] == '#' ) :
        continue

      if ( line[ 0 ] == 'v' ) :
        try :
          ( _, x, y, z ) = line.split()
          x = float( x )
          y = float( y )
          z = float( z )

          self.m_minX = min( self.m_minX, x )
          self.m_maxX = max( self.m_maxX, x )
          self.m_minY = min( self.m_minY, y )
          self.m_maxY = max( self.m_maxY, y )
          self.m_minZ = min( self.m_minZ, z )
          self.m_maxZ = max( self.m_maxZ, z )

          self.m_Vertices.append( ( x, y, z ) )

        except :
          print( 'Line %d is a malformed vertex spec.' % index )

      elif ( line[ 0 ] == 'f' ) :
        try :
          ( _, v1, v2, v3 ) = line.split()
          v1 = int( v1 )-1
          v2 = int( v2 )-1
          v3 = int( v3 )-1
          self.m_Faces.append( ( v1, v2, v3 ) )

        except :
          print( 'Line %d is a malformed face spec.' % index )

      elif ( line[ 0 ] == 'w' ) :
        if ( not self.m_Window == [] ) :
          print( 'Line %d is a duplicate window spec.' % index )

        try :
          ( _, xmin, ymin, xmax, ymax ) = line.split()
          xmin = float( xmin )
          ymin = float( ymin )
          xmax = float( xmax )
          ymax = float( ymax )
          self.m_Window = ( xmin, ymin, xmax, ymax )

        except :
          print( 'Line %d is a malformed window spec.' % index )

      elif ( line[ 0 ] == 's' ) :
        if ( not self.m_Viewport == [] ) :
          print( 'Line %d is a duplicate viewport spec.' % index )

        try :
          ( _, xmin, ymin, xmax, ymax ) = line.split()
          xmin = float( xmin )
          ymin = float( ymin )
          xmax = float( xmax )
          ymax = float( ymax )
          self.m_Viewport = ( xmin, ymin, xmax, ymax )

        except :
          print( 'Line %d is a malformed viewport spec.' % index )

      elif (line[0] == 'p'):
        try:
          v16 = []
          pline = line.split()
          pline.pop(0) # Skip first element
          for v in pline:
            v = int(v) - 1
            v16.append(v)
          if len(v16) is not 16: # Check for exactly 16 elements
            raise
          else:
            self.m_Patch.append(tuple(v16))

        except:
          print('Line %d is a malformed patch spec.' % index)

      else :
          print( 'Line %d \'%s\' is unrecognized.' % ( index, line ) )

  def getBoundingBox( self ) :
    return (
      self.m_minX, self.m_maxX,
      self.m_minY, self.m_maxY,
      self.m_minZ, self.m_maxZ )

  def specifyEuler(self, phi, theta, psi):
    cosPhi,   sinPhi    = math.cos( phi ),  math.sin( phi )
    cosTheta, sinTheta  = math.cos( theta ),math.sin( theta )
    cosPsi,   sinPsi    = math.cos( psi ),  math.sin( psi )

    cPhiXcPsi = cosPhi*cosPsi
    cPhiXsPsi = cosPhi*sinPsi
    sPhiXcPsi = sinPhi*cosPsi
    sPhiXsPsi = sinPhi*sinPsi

    self.m_r00 = cosPsi*cosTheta
    self.m_r01 = -cosTheta*sinPsi
    self.m_r02 = sinTheta

    self.m_r10 = cPhiXsPsi + sPhiXcPsi*sinTheta
    self.m_r11 = cPhiXcPsi - sPhiXsPsi*sinTheta
    self.m_r12 = -cosTheta*sinPhi

    self.m_r20 = -cPhiXcPsi*sinTheta + sPhiXsPsi
    self.m_r21 = cPhiXsPsi*sinTheta + sPhiXcPsi
    self.m_r22 = cosPhi*cosTheta

    tx, ty, tz = self.getCenter()

    self.m_ex = -self.m_r00*tx - self.m_r01*ty - self.m_r02*tz + tx
    self.m_ey = -self.m_r10*tx - self.m_r11*ty - self.m_r12*tz + ty
    self.m_ez = -self.m_r20*tx - self.m_r21*ty - self.m_r22*tz + tz

  def specifyTransform( self, ax, ay, sx, sy, d) :
    self.m_ax = ax
    self.m_sx = sx
    self.m_ay = ay
    self.m_sy = sy
    self.m_d = d

  def getTransformedVertex( self, vNum, doPerspective, doEuler ) :
    x, y, z = self.m_Vertices[vNum]
    divisor = 1.0

    if doEuler:
      tx, ty, tz = x, y, z
      x = self.m_r00 * tx + self.m_r01 * ty + self.m_r02 * tz + self.m_ex
      y = self.m_r10 * tx + self.m_r11 * ty + self.m_r12 * tz + self.m_ey
      z = self.m_r20 * tx + self.m_r21 * ty + self.m_r22 * tz + self.m_ez

    if doPerspective and self.m_d is not None:
      if z < self.m_d:
        divisor = 1 - z/self.m_d
      else:
        # point is at or behind view spot so
        # we force it to map the origin
        divisor = float( 'inf' )

    x = x / divisor
    y = y / divisor

    return (self.m_sx*x + self.m_ax, self.m_sy*y + self.m_ay, 0.0)

  def getCenter( self ) :
    return (
      ( self.m_minX + self.m_maxX ) / 2.0,
      ( self.m_minY + self.m_maxY ) / 2.0,
      ( self.m_minZ + self.m_maxZ ) / 2.0 )

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window
  def getPatch( self )    : return self.m_Patch

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load.
  fName = sys.argv[1]

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( f'{fName}: {len( model.getVertices() )} vert%s, {len( model.getFaces() )} face%s' % (
    'ex' if len( model.getVertices() ) == 1 else 'ices',
    '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( f'     {v}' )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( f'     {f}' )

  print( f'Window line    : {model.getWindow()}' )
  print( f'Viewport line  : {model.getViewport()}' )

  print( f'Center         : {model.getCenter()}' )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
