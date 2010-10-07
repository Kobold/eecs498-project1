from javax.swing import JFrame
from processing.core import PApplet
import csv
import random

READER = None
COUNTY_TO_COORDINATES = None

def in_box(x, y, (x_box, y_box, width, height)):
    return (x_box < x < x_box + width) and (y_box < y < y_box + height)

def insert(tree, x_new, y_new):
    if len(tree) == 1:
        x, y, width, height = tree[0]
        
        if width < 2:
            return (tree, tree)
        
        mid_x = x + width / 2.0
        mid_y = y + height / 2.0
        subtree = [tree[0],
                   [(x,     y,     width / 2.0, height / 2.0)],
                   [(x,     mid_y, width / 2.0, height / 2.0)],
                   [(mid_x, mid_y, width / 2.0, height / 2.0)],
                   [(mid_x, y,     width / 2.0, height / 2.0)]]
        return (subtree, subtree)
    else:
        main_box, tl, tr, bl, br = tree
        
        if in_box(x_new, y_new, tl[0]):
            tl_new, updated = insert(tl, x_new, y_new)
            return ([main_box, tl_new, tr, bl, br], updated)
        elif in_box(x_new, y_new, tr[0]):
            tr_new, updated = insert(tr, x_new, y_new)
            return ([main_box, tl, tr_new, bl, br], updated)
        elif in_box(x_new, y_new, bl[0]):
            bl_new, updated = insert(bl, x_new, y_new)
            return ([main_box, tl, tr, bl_new, br], updated)
        elif in_box(x_new, y_new, br[0]):
            br_new, updated = insert(br, x_new, y_new)
            return ([main_box, tl, tr, bl, br_new], updated)
        else:
            from pprint import pprint
            print 'tree', x_new, y_new
            pprint(tree)
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


def county_to_coordinates(county):
    global COUNTY_TO_COORDINATES
    
    if county not in COUNTY_TO_COORDINATES:
        print 'unknown county:', county
        raise Exception('not in coord')
    
    r_lat = random.normalvariate(0, 0.0114597)
    r_lng = random.normalvariate(0, 0.4245944)
    
    lat, lng = COUNTY_TO_COORDINATES[county]
    x = -82.89855072463796 * lng - 6736.318260869589 + r_lng
    y = 117.03511053316019 * lat - 5031.944083224978 + r_lat
    
    if x < 0 or x > p.width or y < 0 or y > p.height:
        print 'outside boundaries'
        raise Exception('outside')
    
    print (x, y)
    
    x_constrain = p.constrain(x, 1, p.width - 1)
    y_constrain = p.constrain(y, 1, p.height - 1)
    return (x_constrain, y_constrain)
    
def load_coordinates():
    reader = csv.reader(file('counties.csv'))
    d = {}
    for county, lat, lon in reader:
        d[county] = (float(lat), float(lon))
    return d


TREE = [(0, 0, 500, 500)]

class HelloProcessing(PApplet):

    def setup(self):
        global IMAGE, READER, COUNTY_TO_COORDINATES, p
        p = self
        p.size(500, 500)
        p.frameRate(10)
        
        COUNTY_TO_COORDINATES = load_coordinates()
        
        IMAGE = p.loadImage('michigan.jpg')
        IMAGE.loadPixels()
        
        READER = csv.reader(file('crashes.csv'))
    
    def draw(self):
        global TREE, READER
        date, county = READER.next()
        
        try:
            x, y = county_to_coordinates(county)
        except Exception:
            return
        TREE, updated = insert(TREE, x, y)
        
        p.noStroke()
        p.rectMode(p.CORNER)
        drawT(updated)
        
        p.stroke(0)
        p.fill(255)
        p.rectMode(p.CORNERS)
        p.rect(0, p.height, 150, p.height - 20)
        
        p.fill(0)
        p.text(date, 5, p.height - 5)


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
