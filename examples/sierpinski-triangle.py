"""
PyMuPDF demonstration program drawing Sierpinski's Triangle.

This is a mathematical fractal created by taking a start triangle
(equal-sided in this example) and recursively "cutting out" the middle
triangle with points as the middle points of the starting triangle's
sides.

@author: Jorj X. McKie
@copyright: (c) 2020, Jorj X. McKie
@license: GNU GPL 3.0+, GNU AGPL 3.0
"""
import math
import os
import time

import fitz

outfile = __file__.replace(".py", ".pdf")

w = 150  # PDF page width, also determines triangle size.
h = 0.5 * math.sqrt(3) * w  # this makes it equal-sided
doc = fitz.open()  # empty new PDF
page = doc.newPage(-1, width=w, height=h)  # make a new page
color1 = (0, 0, 1)  # start triangle is filled with this (blue)
fill = fitz.utils.getColor("papayawhip")  # cut out triangle fill color
shape = page.newShape()  # make a new Shape object


def triangle(shape, a, b, c, fill, triangle_count):
    """Cut out the center triangle and recurse to the three
    remaining triangles.

    Args:
        shape: Shape object to use
        a: bottom-left point
        b: bottom-right point
        c: top point
        fill: fill the cut-out triangle with this color
    """
    # check resolution limit (avoid taking square root for this)
    if abs(b.x - a.x) + abs(b.y - a.y) < 1.0:  # resolution limit reached
        return triangle_count

    ab = a + (b - a) * 0.5  # calculate ...
    ac = a + (c - a) * 0.5  # the middle points ...
    bc = b + (c - b) * 0.5  # of all sides
    shape.drawPolyline((ab, ac, bc))  # draw the cut-out triangle
    shape.finish(fill=fill, closePath=True)  # colorize it

    triangle_count += 1  # just created one new triangle
    # call myself again
    triangle_count = triangle(shape, a, ab, ac, fill, triangle_count)
    triangle_count = triangle(shape, ab, b, bc, fill, triangle_count)
    triangle_count = triangle(shape, ac, bc, c, fill, triangle_count)
    return triangle_count


# calculate points of start triangle
# note: this need not be an equal-sided triangle - will equally work for
# any three points not on on the same line.
a = page.rect.bl + (5, -5)  # go away 5 pixels from corner
b = page.rect.br + (-5, -5)  # go away 5 pixels from corner
x = (b.x - a.x) * 0.5  # middle point of line
y = a.y - x * math.sqrt(3)
c = fitz.Point(x, y)  # top corner of drawn triangle

shape.drawPolyline((a, b, c))  # draw start triangle on it
shape.finish(fill=color1, closePath=True)  # colorize it

t0 = time.perf_counter()
triangle_count = 0
triangle_count = triangle(shape, a, b, c, fill, triangle_count)  # draw the fractal
t1 = time.perf_counter()

compute_time = round(t1 - t0, 3)
shape.commit()  # write the shape to the page

meta = {
    "title": "Sierpinski Triangle with %i sub-triangles, %g seconds"
    % (triangle_count, compute_time),
    "author": "Jorj X. McKie",
    "subject": "Demonstration of PyMuPDF's features",
    "keywords": "PDF, fractal, Sierpinski, triangle",
    "creator": os.path.basename(__file__),
    "producer": "PyMuPDF v%s" % fitz.VersionBind,
    "creationDate": fitz.getPDFnow(),
    "modDate": fitz.getPDFnow(),
}
doc.setMetadata(meta)
doc.save(outfile, deflate=True)
print(
    "Computation time %g seconds, triangle side %g pixels, %i sub-triangles."
    % (compute_time, abs(b - a), triangle_count)
)
