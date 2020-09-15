# Denton, Jay B.L.
# jbd9386
# 2019-05-02

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import math

#----------------------------------------------------------------------
from ModelData           import ModelData
from constructTransform  import constructTransform

#----------------------------------------------------------------------
class cl_widgets :
  def __init__( self, ob_root_window, ob_world = [] ) :
    self.ob_root_window = ob_root_window
    self.ob_world = ob_world

    self.m_ModelData = None

    self.m_clip = tk.BooleanVar()
    self.m_clip.set( False )

    self.m_Perspective = tk.BooleanVar()
    self.m_Perspective.set( False )

    self.m_Euler = tk.BooleanVar()
    self.m_Euler.set(False)

    self.m_distance = float('inf')

    self.m_phi = 0.0
    self.m_theta = 0.0
    self.m_psi = 0.0

    self.m_Resolution = 4

    self.menu = cl_menu( self )

    self.toolbar = cl_toolbar( self )

    self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
    self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.statusBar_frame.set( 'This is the status bar' )

    self.ob_canvas_frame = cl_canvas_frame( self )
    self.ob_world.add_canvas( self.ob_canvas_frame.canvas )

#----------------------------------------------------------------------
class cl_canvas_frame :
  def __init__( self, master ) :
    self.master = master
    self.canvas = tk.Canvas(
      master.ob_root_window, width=1, height=1, bg='violet' )

    self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
    self.canvas.bind( '<Configure>',       self.canvas_resized_callback )
    self.canvas.bind( '<Key>',             self.key_callback )

    self.canvas.bind( '<ButtonPress-1>',   lambda e : self.btn_callback( 'LMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-1>', lambda e : self.btn_callback( 'LMB', 'release', e ) )
    self.canvas.bind( '<B1-Motion>',       lambda e : self.btn_callback( 'LMB', 'motion', e ) )
    self.canvas.bind( '<ButtonPress-2>',   lambda e : self.btn_callback( 'MMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-2>', lambda e : self.btn_callback( 'MMB', 'release', e ) )
    self.canvas.bind( '<B2-Motion>',       lambda e : self.btn_callback( 'MMB', 'motion', e ) )
    self.canvas.bind( '<ButtonPress-3>',   lambda e : self.btn_callback( 'RMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-3>', lambda e : self.btn_callback( 'RMB', 'release', e ) )
    self.canvas.bind( '<B3-Motion>',       lambda e : self.btn_callback( 'RMB', 'motion', e ) )

    self.canvas.bind( '<Up>',              lambda e : self.arrow_callback( 'Up', False, e ) )
    self.canvas.bind( '<Down>',            lambda e : self.arrow_callback( 'Down', False, e ) )
    self.canvas.bind( '<Right>',           lambda e : self.arrow_callback( 'Right', False, e ) )
    self.canvas.bind( '<Left>',            lambda e : self.arrow_callback( 'Left', False, e ) )
    self.canvas.bind( '<Shift-Up>',        lambda e : self.arrow_callback( 'Up', True, e ) )
    self.canvas.bind( '<Shift-Down>',      lambda e : self.arrow_callback( 'Down', True, e ) )
    self.canvas.bind( '<Shift-Right>',     lambda e : self.arrow_callback( 'Right', True, e ) )
    self.canvas.bind( '<Shift-Left>',      lambda e : self.arrow_callback( 'Left', True, e ) )

  def arrow_callback( self, arrow, shift, event ) :
    shiftValue = 'Shift-' if shift else ''
    self.master.statusBar_frame.set( f'{shiftValue}{arrow} arrow pressed.' )

  def btn_callback( self, btn, action, event ) :
    if action == 'press' :
      self.master.statusBar_frame.set( f'{btn} pressed. ({event.x}, {event.y})' )
      self.x = event.x
      self.y = event.y
      self.canvas.focus_set()

    elif action == 'release' :
      self.master.statusBar_frame.set( f'{btn} released. ({event.x}, {event.y})' )
      self.x = None
      self.y = None

    elif action == 'motion' :
      self.master.statusBar_frame.set( f'{btn} dragged. ({event.x}, {event.y})' )
      self.x = event.x
      self.y = event.y

    else :
      self.master.statusBar_frame.set( f'Unknown {btn} action {action}.' )

  def key_callback( self, event ) :
    msg = f'{event.char!r} ({ord( event.char )})' \
      if len( event.char ) > 0 else '<non-printing char>'

    self.master.statusBar_frame.set(
      f'{msg} pressed at ({event.x},{event.y})' )

  def canvas_resized_callback( self, event ) :
    self.canvas.config( width = event.width-4, height = event.height-4 )

    self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.master.statusBar_frame.set(
      f'Canvas width, height ({self.canvas.cget( "width" )}, ' +
      f'{self.canvas.cget( "height" )})' )

    self.canvas.pack()

#----------------------------------------------------------------------
class cl_statusBar_frame( tk.Frame ) :
  def __init__( self, master ) :
    tk.Frame.__init__( self, master )
    self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
    self.label.pack( fill = tk.X )

  def set( self, formatStr, *args ) :
    self.label.config( text = 'jbd9386: ' + ( formatStr % args ) )
    self.label.update_idletasks()

  def clear( self ) :
    self.label.config( text='' )
    self.label.update_idletasks()

#----------------------------------------------------------------------
class cl_menu :
  def __init__( self, master ) :
    self.master = master
    self.menu = tk.Menu( master.ob_root_window )
    master.ob_root_window.config( menu = self.menu )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'File', menu = dummy )
    dummy.add_command( label = 'New', command = lambda : self.menu_callback( 'file>new' ) )
    dummy.add_command( label = 'Open...', command = lambda : self.menu_callback( 'file>open' ) )
    dummy.add_separator()
    dummy.add_command( label = 'Exit', command = lambda : self.menu_callback( 'file>exit' ) )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Settings', menu = dummy )
    #dummy.add_command( label = 'Item1', command = lambda : self.menu_callback( 'settings>item1' ) )
    #dummy.add_command( label = 'Item2', command = lambda : self.menu_callback( 'settings>item2' ) )
    dummy.add_checkbutton( label = 'Clip', variable = self.master.m_clip )
    dummy.add_checkbutton( label = 'Euler', variable=self.master.m_Euler )
    dummy.add_checkbutton( label = 'Perspective', variable=self.master.m_Perspective )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Help', menu = dummy )
    dummy.add_command( label = 'About...', command = lambda : self.menu_callback( 'help>about' ) )

  def menu_callback( self, which = None ) :
    item = 'menu' if which is None else which
    self.master.statusBar_frame.set( f'{item!r} callback' )

#----------------------------------------------------------------------
class cl_toolbar :
  def __init__( self, master ) :
    self.master = master
    self.toolbar = tk.Frame( master.ob_root_window )

    dummy = tk.Button(self.toolbar, text='Resolution', width=10, command=self.resolution_callback)
    dummy.pack(side=tk.LEFT, padx=2, pady=2)

    dummy = tk.Button(self.toolbar, text='Distance', width=10, command=self.distance_callback)
    dummy.pack(side=tk.LEFT, padx=2, pady=2)

    dummy = tk.Button(self.toolbar, text='φ', width=2, command=lambda: self.angle_callback(angle='phi'))
    dummy.pack(side=tk.LEFT, padx=2, pady=2)

    dummy = tk.Button(self.toolbar, text='θ', width=2, command=lambda: self.angle_callback(angle='theta'))
    dummy.pack(side=tk.LEFT, padx=2, pady=2)

    dummy = tk.Button(self.toolbar, text='ψ', width=2, command=lambda: self.angle_callback(angle='psi'))
    dummy.pack(side=tk.LEFT, padx=2, pady=2)

    dummy = tk.Button( self.toolbar, text = 'Reset', width = 10, command = self.reset_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Load', width = 10, command = self.load_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Draw', width = 10, command = self.draw_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    self.toolbar.pack( side = tk.TOP, fill = tk.X )

  def reset_callback( self ) :
    self.master.ob_world.reset()
    self.master.statusBar_frame.set( 'Reset callback' )

  def load_callback( self ) :
    fName = tk.filedialog.askopenfilename( filetypes = [ ( "allfiles", "*" ) ] )
    if ( len( fName ) == 0 ) :
        self.master.statusBar_frame.set( "%s", "[Load was cancelled]" )

    else :
      self.master.m_ModelData = ModelData( fName )

      print( f'---Load {fName!r}' )
      print(  'Window line   :', self.master.m_ModelData.getWindow() )
      print(  'Viewport line :', self.master.m_ModelData.getViewport() )
      print(  'Bounding box  :', self.master.m_ModelData.getBoundingBox() )

      self.master.statusBar_frame.set( 'Load callback' )

  def draw_callback( self ) :
    if self.master.m_ModelData is None :
      self.master.statusBar_frame.set( 'No model loaded.' )
      return

    # Reset the window before draw, so each of time only one picture is drawn
    #self.master.ob_world.reset()

    width  = int( self.master.ob_canvas_frame.canvas.cget( "width" ) )
    height = int( self.master.ob_canvas_frame.canvas.cget( "height" ) )

    w = self.master.m_ModelData.getWindow()
    v = self.master.m_ModelData.getViewport()
    d = self.master.m_distance

    ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )

    self.master.m_ModelData.specifyTransform( ax, ay, sx, sy, d )

    fPhi = self.master.m_phi * math.pi / 180
    fTheta = self.master.m_theta * math.pi / 180
    fPsi = self.master.m_psi * math.pi / 180

    self.master.m_ModelData.specifyEuler(fPhi, fTheta, fPsi)

    clip_state = self.master.m_clip.get()
    pers_state = self.master.m_Perspective.get()
    euler_state = self.master.m_Euler.get()

    resolution = self.master.m_Resolution

    vxMin = v[0] * width
    vxMax = v[2] * width
    vyMin = v[1] * height
    vyMax = v[3] * height
    self.master.ob_canvas_frame.canvas.create_line(
      vxMin, vyMin, vxMin, vyMax, vxMax, vyMax, vxMax, vyMin, vxMin, vyMin)

    print(  '---Draw' )
    print( f'Canvas size    : ({width}, {height})' )
    print( f'Transform      : ax={ax:.2f}, ay={ay:.2f}, sx={sx:.2f}, sy={sy:.2f}' )
    print( f'Clip State     : {clip_state}')
    print( f'Perspective    : {pers_state}')
    print( f'Euler          : {euler_state}')
    print( f'Distance       : {self.master.m_distance}')
    print( f'Angle(radians) : φ={fPhi:.2f}, θ={fTheta:.2f}, ψ={fPsi:.2f}')
    print( f'Resolution     : {resolution}')
    print( f'Portal         : Xmin-max:({vxMin:.2f}, {vxMax:.2f}), Ymin-max({vyMin:.2f}, {vyMax:.2f})')

    self.master.ob_world.create_graphic_objects( self.master.ob_canvas_frame.canvas, self.master.m_ModelData,
                                                 clip_state, pers_state, euler_state, resolution)

    self.master.statusBar_frame.set( f'resolution={resolution}, distance={d:.2f}, φ={self.master.m_phi:.2f}°,'
                          f' θ={self.master.m_theta:.2f}°, ψ={self.master.m_psi:.2f}°' )

  def distance_callback(self):
    theOldValue = self.master.m_distance
    someMinVal = 1.0
    f = simpledialog.askfloat("Distance", "Enter value(≥1.0):",
                              initialvalue=theOldValue, minvalue=someMinVal)
    if f is None:
      self.master.statusBar_frame.set('User cancelled the Distance operation.')
      return

    self.master.m_distance = f
    self.master.statusBar_frame.set(f'Distance set to {f:.2f}')

  def angle_callback(self, angle):
    theOldPhiValue = self.master.m_phi
    theOldThetaValue = self.master.m_theta
    theOldPsiValue = self.master.m_psi

    if angle is 'phi':
      fPhi = simpledialog.askfloat("Angle Phi", "Enter value in degree:",
                                initialvalue=theOldPhiValue)
      if fPhi is None:
        self.master.statusBar_frame.set(f'User cancelled the Angle\'{angle}\' operation.')
        return
      self.master.m_phi = fPhi
      self.master.statusBar_frame.set(f'Angle{angle!r} sets to {fPhi}°')
    elif angle is 'theta':
      fTheta = simpledialog.askfloat("Angle Theta", "Enter value in degree:",
                                initialvalue=theOldThetaValue)
      if fTheta is None:
        self.master.statusBar_frame.set(f'User cancelled the Angle\'{angle}\' operation.')
        return
      self.master.m_theta = fTheta
      self.master.statusBar_frame.set(f'Angle{angle!r} sets to {fTheta}°')
    elif angle is 'psi':
      fPsi = simpledialog.askfloat("Angle Psi", "Enter value in degree:",
                                initialvalue=theOldPsiValue)
      if fPsi is None:
        self.master.statusBar_frame.set(f'User cancelled the Angle\'{angle}\' operation.')
        return
      self.master.m_psi = fPsi
      self.master.statusBar_frame.set(f'Angle{angle!r} sets to {fPsi}°')

  def resolution_callback( self ):
    theOldValue = self.master.m_Resolution
    someMinVal = 4
    i = simpledialog.askinteger("Resolution", "Enter integer:",
                              initialvalue=theOldValue, minvalue=someMinVal)
    if i is None:
      self.master.statusBar_frame.set('User cancelled the Distance operation.')
      return

    self.master.m_Resolution = i
    self.master.statusBar_frame.set(f'Resolution set to {i}')


#----------------------------------------------------------------------
