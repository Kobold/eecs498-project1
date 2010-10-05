from javax.swing import JFrame
from processing.core import PApplet

def in_box(x, y, (x_box, y_box, width, height)):
    return (x_box < x < x_box + width) and (y_box < y < y_box + height)

def insert(tree, x_new, y_new):
    if len(tree) == 1:
        x, y, width, height = tree[0]
        mid_x = x + width / 2.0
        mid_y = y + height / 2.0
        return [tree[0],
                [(x,     y,     width / 2.0, height / 2.0)],
                [(x,     mid_y, width / 2.0, height / 2.0)],
                [(mid_x, mid_y, width / 2.0, height / 2.0)],
                [(mid_x, y,     width / 2.0, height / 2.0)]]
    else:
        main_box, tl, tr, bl, br = tree
        
        if in_box(x_new, y_new, tl[0]):
            return [main_box, insert(tl, x_new, y_new), tr, bl, br]
        elif in_box(x_new, y_new, tr[0]):
            return [main_box, tl, insert(tr, x_new, y_new), bl, br]
        elif in_box(x_new, y_new, bl[0]):
            return [main_box, tl, tr, insert(bl, x_new, y_new), br]
        elif in_box(x_new, y_new, br[0]):
            return [main_box, tl, tr, bl, insert(br, x_new, y_new)]
        else:
            assert False

def drawT(tree):
    if len(tree) == 1:
        x, y, width, height = tree[0]
        
        p.fill(average(IMAGE, tree[0]))
        p.rect(x, y, width, height)
    else:
        _, tl, tr, bl, br = tree
        drawT(tl)
        drawT(tr)
        drawT(bl)
        drawT(br)

def averageColors(xs):
    r, g, b = 0, 0, 0
    count = 0
    
    for pixel in xs:
        r += p.red(pixel)
        g += p.green(pixel)
        b += p.blue(pixel)
        count += 1
    
    return p.color(r / count, g / count, b / count)
    

def average(image, area):
    box_x, box_y, width, height = area
    colors = (image.pixels[y * image.width + x] for y in xrange(box_y, box_y + height)
                                                for x in xrange(box_x, box_x + width))
    return averageColors(colors)


TREE = [(0, 0, 500, 500)]

class HelloProcessing(PApplet):

    def setup(self):
        global IMAGE, p
        p = self
        p.size(500, 500)
        p.frameRate(3)
        
        IMAGE = p.loadImage('michigan.jpg')
        IMAGE.loadPixels()
    
    def draw(self):
        global TREE
        p.noStroke()
        drawT(TREE)
        TREE = insert(TREE, p.random(500), p.random(500))


if __name__ == '__main__':
    frame = JFrame(title="Processing",
                   resizable=0,
                   defaultCloseOperation=JFrame.EXIT_ON_CLOSE)
    panel = HelloProcessing()
    frame.add(panel)
    panel.init()
    while panel.defaultSize and not panel.finished:
        pass
    frame.pack()
    frame.visible = 1
