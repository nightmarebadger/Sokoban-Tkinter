from tkinter import *

"""
    O ... igralec
    # ... zid
    * ... blokec (ki se ga lahko premika)
    X ... tocka za zmago
    A ... igralec na tocki za zmago
    R ... blokec na tocki za zmago
    
"""


def makeLevel(string):
    p = []
    with open(string, 'r') as f:
        for line in f:
            line = line.strip()
            foo = []
            for i in line:
               foo.append(i)
            p.append(foo)
    return p

def findPlayer():
    for i in range(w):
        for j in range(h):
            if(p[j][i] == 'O'):
                return(i,j)

def kvadrat(x, y, barva):
    canvas.create_rectangle(x, y, x+wid, y+hei, fill=barva)

def krog(x, y, barva):
    canvas.create_oval(x, y, x+wid, y+hei, fill=barva)

def draw():
    canvas.delete("all")
    for i in range(wid, width, wid):
        canvas.create_line(i, 0, i, height)

    for i in range(hei, height, hei):
        canvas.create_line(0, i, width, i)

    for i in range(w):
        for j in range(h):
            if(p[j][i] == '#'):
                kvadrat(i*wid, j*hei, "#252525")
            if(p[j][i] == 'O'):
                krog(i*wid, j*hei, "red")
            if(p[j][i] == '*'):
                kvadrat(i*wid, j*hei, "blue")
            if(p[j][i] == 'X'):
                kvadrat(i*wid, j*hei, "yellow")
            if(p[j][i] == 'A'):
                kvadrat(i*wid, j*hei, "yellow")
                krog(i*wid, j*hei, "red")
            if(p[j][i] == 'R'):
                kvadrat(i*wid, j*hei, "pink")
            
            
def kill(event):
    root.destroy()

def odmik(x, y):
    #global ply_y, ply_x
    if(p[y][x] == 'O'):
        p[y][x] = ' '
    if(p[y][x] == 'A'):
        p[y][x] = 'X'

def premik_na(x, y):
    if(p[y][x] == 'X'):
        p[y][x] = 'A'
    if(p[y][x] == ' '):
        p[y][x] = 'O'

def odmik_stvar(x, y):
    if(p[y][x] == '*'):
        p[y][x] = ' '
    if(p[y][x] == 'R'):
        p[y][x] = 'X'
        
def premik_stvar_na(x, y):
    if(p[y][x] == ' '):
        p[y][x] = '*'
    if(p[y][x] == 'X'):
        p[y][x] = 'R'


def premikanje(x, y):
#    print("Hej")
    global ply_y, ply_x
    if(p[ply_y + y][ply_x + x] in dovoljeni):
        odmik(ply_x, ply_y)
        ply_y += y
        ply_x += x
        premik_na(ply_x, ply_y)

    elif(p[ply_y + y][ply_x + x] in premikajoci):
        if(p[ply_y + 2*y][ply_x + 2*x] in dovoljeni):
            odmik_stvar(ply_x + x, ply_y + y)
            premik_stvar_na(ply_x + 2*x, ply_y + 2*y)
            odmik(ply_x, ply_y)
            ply_y += y
            ply_x += x
            premik_na(ply_x, ply_y)
            

def jeZmaga():
    for i in p:
        for j in i:
            if(j == 'X'):
                return False
            elif(j == 'A'):
                return False
    return True

def movement(n):
    global ply_x, ply_y

    if(n == 'Up'):
        premikanje(0, -1)

    elif(n == 'Down'):
        premikanje(0, 1)

    elif(n == 'Left'):
        premikanje(-1, 0)

    elif(n == 'Right'):
        premikanje(1, 0)

    draw()
    if(jeZmaga()):
        print("Bravo, zmagu si!")
        root.destroy()
    
    

def restart():
    global p
    global ply_x, ply_y
    p = makeLevel(level)
    ply_x, ply_y = findPlayer()
    draw()
    
    


def keyHandler(event):
    foo = event.keysym
    movement(foo)
    if(event.char == 'r'):
        restart()

level = "level/lvl1.lvl"
p = makeLevel(level)

w = len(p[0])
h = len(p)

dovoljeni = [' ', 'X']
premikajoci = ['*', 'R']

width = 800
height = 600

wid = width // w
hei = height // h

width = wid * w
height = hei * h

ply_x, ply_y = findPlayer()





root = Tk()

canvas = Canvas(root, width=width, height=height)
canvas.pack()
draw()


root.bind_all("<Escape>", kill)
root.bind_all("<Key>", keyHandler)

root.mainloop()