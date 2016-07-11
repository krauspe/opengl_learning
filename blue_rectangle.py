from OpenGL.GL import *
from OpenGL.GLUT import *



# Creating the OpenGL Window
#
# So the first thing we want to do is create our window. We will need a window variable that holds our window id,
# a width and a height variable, and a few GLUT function calls.
# If you never heard about GLUT, it's just a little library that wraps all kinds of complicated OpenGL
# things into little functions (like creating a window or drawing text).
#
# So, let's initialize OpenGL and make a window:

# The most interesting thing about the initialization code is the glutDisplayFunc(draw) call. It tells OpenGL that
# it should call our draw function over and over again. If we want to draw something, we would do so in our draw function then.
# Now you might noticed something similar in there: glutIdleFunc(draw). This basically tells OpenGL to draw our things all the time,
# and not just every time the user interacts with the window. If in doubt, always use glutDisplayFunc and glutIdleFunc.
#
# Note: the draw function will be called about 60 times per second completely automatically. The concept is called callback.
#
# Let's talk about our draw() function for a second. A standard OpenGL draw function always follows a fixed sequence:
#
#     Clear Screen, Load Identity
#     Draw whatever should be drawn
#     Swap the Buffers
#
# This is the most important thing to know about OpenGL: the draw function always starts with a black screen (after calling
# glClear to clear the screen and glLoadIdentity to reset the position) and then draws our players, monsters and landscapes.
#  In the end it calls glutSwapBuffers to make double buffering possible (we don't worry about what that is),
# and then it starts all over again with glClear (and so on).
#
# So, if we want to have a monster that runs from the left to the right of our screen, we would do this:
#
#     glClear and glLoadIdentity
#     draw the monster at position (0 , ...)
#     glSwapBuffers
#     ...
#     glClear and glLoadIdentity
#     draw the monster at position (1 , ...)
#     glSwapBuffers
#     ...
#     glClear and glLoadIdentity
#     draw the monster at position (2 , ...)
#     glSwapBuffers
#     ...
#
# (and so on until it's at position (500 , ...) because our screen has a width of 500 pixels)
#
# Okay let's be honest, we only want to draw a little rectangle today, no complex monster that changes its position.
# But the monster example is great to understand how OpenGL works.

window = 0  # glut window number
width, height = 500, 400  # window size


def draw():  # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    # ToDo draw rectangle
    glutSwapBuffers()  # important for double buffering


# initialization

glutInit()  # initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)  # set window size
glutInitWindowPosition(0, 0)  # set window position
window = glutCreateWindow("noobtuts.com")  # create window with title
glutDisplayFunc(draw)  # set draw function callback
glutIdleFunc(draw)  # draw all the time
glutMainLoop()  # start everything

# Creating the Draw-Rectangle function
#
# Alright, we want to draw a rectangle. But where?
#
# Let's take a look at the following picture to understand OpenGL's window coordinate system:

# This means that the bottom left part of our window is (0, 0), the bottom right part is (500, 0)
# because our window has the width of 500 pixels. The top left part would be (0, 400) because our
# window has the height of 400 pixels, and the top right part would be (500, 400).
#
# Note: those are (x, y) coordinates. For example: (2, 5) means x=2 and y=5.
#
# In order to draw a rectangle in OpenGL, we will do the following:
#
#     Tell OpenGL that we want to draw a rectangle
#     Draw the bottom left point
#     Draw the bottom right point
#     Draw the top right point
#     Draw the top left point
#     Tell OpenGL that we are done drawing the rectangle
#
# Again it's always the same concept in OpenGL: we tell it to start something, then we do whatever
# we want to do and then we tell it to stop it again. This is how everything in OpenGL works!
#
# So, let's create a function that draws our rectangle:

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x + width, y)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x, y + height)                          # top left point
    glEnd()

    # done drawing a rectangle

# Drawing the Rectangle
#
# Alright, we are just a few steps away from seeing our rectangle on the screen. We have OpenGL set up,
# we have our draw_rect function set up and we know how OpenGL works. Let's go back into our draw()
# function where it currently still says "ToDo draw rectangle":

def draw():  # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    # ToDo draw rectangle
    glutSwapBuffers()  # important for double buffering

# We want to use our draw_rect function in there, but wait. The screen is currently black and if
    # we would draw a rectangle, it would be black too. Hence we wouldn't see anything.
#
# In order to draw our rectangle in something different than black, we will use the glColor3f function.
# The function takes three parameters, which are the red, green and blue parts of the color.
# The parameters have to be between 0 and 1. Which means that (0, 0, 0) would be black and
# something like (0.5, 0, 0) would be a dark red.
#
# Let's use a blue color:

def draw():  # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    glColor3f(0.0, 0.0, 1.0)  # set color to blue
    glutSwapBuffers()  # important for double buffering

# Now it's finally time to use our draw_rect function. Its parameters are the rectangle's position and the size.
# Let's position it somewhere at the bottom left at (10, 10) with a width of 200 pixels and a height of 100 pixels:

# So, why is that?
#
# OpenGL is a incredibly powerful graphics library which allows us to draw things in 3D and in 2D.
# But wait, we forgot to tell OpenGL that we want to draw our rectangle in 2D!
#
# Here is our function that tells OpenGL to draw things in 2D:

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# Please don't try to bend your mind around that code, as you won't understand it without a lot of OpenGL knowledge. It looks so complicated because we don't actually tell OpenGL to draw things in 2D. What we really do is set up our screen and our perspective in order to look like it was 2D. Hence the complicated looking code.
#
# Just keep in mind to call that function before you want to draw things in 2D.
#
# Anyway, let's modify our draw function to do the following:
# 1. Clear and Load Identity
# 2. Set mode to 2D
# 3. Draw our rectangle
# 4. Swap Buffers
#
# Here is our new draw function:

def draw():  # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the screen
    glLoadIdentity()  # reset position
    refresh2d(width, height)  # set mode to 2d
    glColor3f(0.0, 0.0, 1.0)  # set color to blue
    draw_rect(10, 10, 200, 100)  # rect at (10, 10) with width 200, height 100
    glutSwapBuffers()  # important for double buffering

# Summary
#
# That's how to work with OpenGL in Python. From that point all other OpenGL techniques are straight
# forward. For example, if we would want to use a spaceship texture for our rectangle, we would do
# it the same way we set the color, just with the OpenGL set texture function.
#
# A small advice on your journey through OpenGL: a lot of the OpenGL tutorials out there are overly
#  complicated. OpenGL is actually a really nice and simple library to work with.