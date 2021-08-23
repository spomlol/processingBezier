# Start settings
points = 2
pointsToDraw=100
lines=False
width,height=800,800

# Key controls
## UP/DOWN: more or less control points
## LEFT/RIGHT: change lines vs dots view
def keyPressed():
    global points
    global vs
    global lines
    if keyCode == UP:
        points += 1
        vs = [particle(width / (points - 1) * i, 0) for i in range(points)]
    if keyCode == DOWN:
        points = max(2, points - 1)
        vs = [particle(width / (points - 1) * i, 0) for i in range(points)]
        
    if keyCode == RIGHT or keyCode==LEFT:
        lines=not lines

# Lerp function for 2 vectors
def lerpVector(vecA, vecB, i):
    x = lerp(vecA.x, vecB.x, i)
    y = lerp(vecA.y, vecB.y, i)
    return(PVector(x, y))

# Recursive lerp function for multiple control points (2 or more)
def anylerp(vs, f):
    #If we have more than 1 vector: calculate lerp between the vectors
    if len(vs) > 1:
        #Check if its a particle (starting point) because we need to take the pos vector from this
        if vs[0].__class__.__name__ == "particle":
            #Calculate the lerp between all following vector
            ## Example: 4 vectors: v1,v2,v3,v4
            ##          will calculate a new list of vectors: [va=lerp(v1,v2),vb=lerp(v2,v3),vc=lerp(v3,v4)]
            ##          Next passage: [vx=lerp(va,vb),vy=lerp(vb,vc)]
            ##          Next passage: [lerp(vx,vy)]
            ##          Since length now ==1: return this.
            newvs = [lerpVector(vs[x].pos, vs[x + 1].pos, f) for x in range(len(vs) - 1)]
        #If not a particle but just a vector: we are inside our recursive function
        else:
            newvs = [lerpVector(vs[x], vs[x + 1], f)
                     for x in range(len(vs) - 1)]
        #Calculate new lerp for the new vectors  
        return anylerp(newvs, f)
    #If 1 vector: we got our result!
    else:
        return vs[0]

# Simple particle class
class particle():
    def __init__(self, x, y):
        self.pos = PVector(x, y)
        self.vel = PVector(0, random(-3, 3))

    def update(self):
        p = self.pos
        v = self.vel
        if (0 > p.x + v.x) or (p.x + v.x > width):
            self.vel.x *= -1
        if (0 > p.y + v.y) or (p.y + v.y > height):
            self.vel.y *= -1
        self.pos.add(self.vel)

# Create new list of particles on startup
vs = [particle(width / (points - 1) * i, 0) for i in range(points)]

def setup():
    size(width, height)
    strokeWeight(5)
    noFill()

def draw():
    background(0)
    #Set stroke for lerped points/line
    stroke(255, 0, 0)
    
    if lines:
        beginShape()
    #lerp interpolation size
    for i in range(100):
        f = float(i) / pointsToDraw
        v = anylerp(vs, f)
        if lines:
            vertex(v.x,v.y)
        else:
            point(v.x, v.y)
    if lines:
        endShape()
        
    #Set stroke for control points
    stroke(0, 0, 255)
    for v in vs:
        point(v.pos.x, v.pos.y)
        #Update positions
        v.update()
