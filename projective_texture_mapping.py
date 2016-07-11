# This script will create a Texture containing a Ring image, then it will project this on some green cubes
# ("project" as in "overhead projector", not as in "flat projection"). This is usually called "projective Texturing".
# The secret in this is the GLSL Function texture2DProj, which does nothing more than to divide by the (usually useless)
# last Texture coordinate. Be careful however, as, since if you specify a vec4, the homogenous fourth coordinate, which
# is constant, will be used. Then you'd get a Projection without perspective.
#
# Try using "GL_REPEAT" for the projected texture's wrapping, it looks fun.
#
# The Distance measurement between projector and projection actually is a little clumsy, i bet there's a better way, ' \

# Pygame/PyopenGL example by Bastiaan Zapf, May 2009
#
# Projective Textures
#
# Employed techniques:
#
# - Vertex and Fragment shaders
# - Display Lists
# - Texturing

from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import *  # trigonometry
import numpy

import pygame  # just to get a display

import Image
import sys
import time

# get an OpenGL surface

pygame.init()
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)


def jpg_file_write(name, number, data):
    im = Image.frombuffer("RGBA", (800, 600), data, "raw", "RGBA", 0, 0)


fnumber = "%05d" % number
im.save(name + fnumber + ".jpg")


# Create and Compile a shader
# but fail with a meaningful message if something goes wrong

def createAndCompileShader(type, source):
    shader = glCreateShader(type)


glShaderSource(shader, source)
glCompileShader(shader)

# get "compile status" - glCompileShader will not fail with
# an exception in case of syntax errors

result = glGetShaderiv(shader, GL_COMPILE_STATUS)

if (result != 1):  # shader didn't compile
    raise Exception("Couldn't compile shader\nShader compilation Log:\n" + glGetShaderInfoLog(shader))
return shader

vertex_shader = createAndCompileShader(GL_VERTEX_SHADER, """

   varying vec3 normal, lightDir;

   void main()
   {
   normal = gl_NormalMatrix * gl_Normal;
   vec4 posEye = gl_ModelViewMatrix * gl_Vertex;

   // Put World coordinates of Vertex, multiplied by TextureMatrix[0]
   // into TexCoord[0]

   gl_TexCoord[0] = gl_TextureMatrix[0]*gl_ModelViewMatrix*gl_Vertex;

   // LightSource[0] position is assumed to be the projector position

   lightDir = vec3(gl_LightSource[0].position.xyz - posEye.xyz);
   gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
   }
   """);

fragment_shader = createAndCompileShader(GL_FRAGMENT_SHADER, """
                                                                                               uniform sampler2D projMap;
                                                                                               varying vec3 normal, lightDir;

                                                                                               void main (void)
                                                                                               {
                                                                                               vec4 final_color = vec4(0.0,0.5,0,0.3);
                                                                                               vec3 N = normalize(normal);
                                                                                               vec3 L = normalize(lightDir);

                                                                                               float lambert = dot(N,L);

                                                                                               if( gl_TexCoord[0].z>0.0 // in front of projector?
                                                                                               &&
                                                                                               lambert>0 ) // facing projector?
                                                                                               {

                                                                                               // project texture - see notes for pitfall

                                                                                               vec4 ProjMapColor = texture2DProj(projMap, gl_TexCoord[0].xyz);
                                                                                               final_color += ProjMapColor*lambert*pow(length(L),-2.0);
                                                                                               }

                                                                                               gl_FragColor = final_color;
                                                                                               }
                                                                                               """);

# build shader program

program = glCreateProgram()
glAttachShader(program, vertex_shader)
glAttachShader(program, fragment_shader)
glLinkProgram(program)

# try to activate/enable shader program
# handle errors wisely

try:
    glUseProgram(program)
except OpenGL.error.GLError:
    print glGetProgramInfoLog(program)
raise

done = False

t = 0

# load a cube into a display list

glNewList(1, GL_COMPILE)

glBegin(GL_QUADS)

glColor3f(1, 1, 1)

glNormal3f(0, 0, -1)
glVertex3f(-1, -1, -1)
glVertex3f(1, -1, -1)
glVertex3f(1, 1, -1)
glVertex3f(-1, 1, -1)

glNormal3f(0, 0, 1)
glVertex3f(-1, -1, 1)
glVertex3f(1, -1, 1)
glVertex3f(1, 1, 1)
glVertex3f(-1, 1, 1)

glNormal3f(0, -1, 0)
glVertex3f(-1, -1, -1)
glVertex3f(1, -1, -1)
glVertex3f(1, -1, 1)
glVertex3f(-1, -1, 1)

glNormal3f(0, 1, 0)
glVertex3f(-1, 1, -1)
glVertex3f(1, 1, -1)
glVertex3f(1, 1, 1)
glVertex3f(-1, 1, 1)

glNormal3f(-1, 0, 0)
glVertex3f(-1, -1, -1)
glVertex3f(-1, 1, -1)
glVertex3f(-1, 1, 1)
glVertex3f(-1, -1, 1)

glNormal3f(1, 0, 0)
glVertex3f(1, -1, -1)
glVertex3f(1, 1, -1)
glVertex3f(1, 1, 1)
glVertex3f(1, -1, 1)

glEnd()
glEndList()

texture = glGenTextures(1)

glActiveTexture(GL_TEXTURE0);  # use first texturing unit
glBindTexture(GL_TEXTURE_2D, texture);

glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);

glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                GL_CLAMP);  # try GL_REPEAT for fun
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                GL_CLAMP);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)

texdata = numpy.zeros((256, 256, 4))

# a ring-shaped projection texture

for i in range(0, 256):
    x = (i - 128.1) / 128.0
for j in range(0, 256):
    y = (j - 128.1) / 128.0
if ((x * x + y * y > 0.9) | (x * x + y * y < 0.3)):
    texdata[i][j][0] = 0
texdata[i][j][1] = 0
texdata[i][j][2] = 0
texdata[i][j][3] = 0
else:
texdata[i][j][0] = 1
texdata[i][j][1] = 1
texdata[i][j][2] = 1
texdata[i][j][3] = 1

glTexImage2Df(GL_TEXTURE_2D, 0, GL_RGBA, 0, GL_RGBA,
              texdata)

loc = glGetUniformLocation(program, "projMap");
glUniform1i(loc, 0)  # use first texturing unit in shader

glEnable(GL_DEPTH_TEST)

while not done:

t = t + 1

# Projector position and angle - this is rather rough so far

ppos = [sin(t / 260.0) * 4, cos(t / 240.0) * 4, 0]
palpha = t
pbeta = t / 3.0

# the texture matrix stores the intended projection
# however, signs seem to be reversed. This somehow makes sense, as
# we're transforming the texture coordinates

glMatrixMode(GL_TEXTURE);
glLoadIdentity()

glRotate(-palpha, 0, 1, 0);
glRotate(-pbeta, 0, 0, 1);
glTranslate(-ppos[0], -ppos[1], -ppos[2])

# set light source position

glLightfv(GL_LIGHT0, GL_POSITION, [ppos[0], ppos[1], ppos[2]]);

# Set view

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(90, 1, 0.01, 1000)
gluLookAt(sin(t / 200.0) * 8, sin(t / 500.0) * 3 + 8, cos(t / 200.0) * 8, 0, 0, 0, 0, 1, 0)

glClearColor(0.0, 0.0, 0.0, 1.0)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

glMatrixMode(GL_MODELVIEW)

# draw a triangle to visualize the projector
# i don't have a clue how to relate the angles correctly here

glLoadIdentity()

glTranslate(ppos[0], ppos[1], ppos[2])

glBegin(GL_TRIANGLES)

glVertex3f(1, 0, 0)
glVertex3f(0, 1, 0)
glVertex3f(0, 0, 1)

glEnd()

# fallback

glColor3f(1, 1, 1)

glLoadIdentity()

# render a range of cubes

for i in range(-1, 2):
    for j in range(-1, 2):
        for k in range(-1, 2):
        glPushMatrix()
glTranslate(i * 5, j * 5, k * 5)
glScale(1, 1, 1)
glCallList(1)
glPopMatrix()

time.sleep(0.01);

pygame.display.flip()
'but this one works so far.