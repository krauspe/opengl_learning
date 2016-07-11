# Screenshots from OpenGL
# The shortest way I found to bring OpenGL screenshots to the hard drive is using the
# function "frombuffer" from the "imaging Library" "Image", which understands the same
# format that OpenGL outputs.
#
# Documentation for Image
# Documentation for glReadPixels

... to be filled

screenshot = glReadPixels( 0,0, 800, 600, GL_RGBA, GL_UNSIGNED_BYTE)
im = Image.frombuffer("RGBA", (800,600), screenshot, "raw", "RGBA", 0, 0)
im.save("test.jpg")