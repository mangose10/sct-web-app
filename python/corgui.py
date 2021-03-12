import json

trans = ""

with open("trans.json", "r") as infile:
  trans += infile.read()

trano = json.loads(trans)

tMax = 0
tMin = 999999
pMax = 0
pMin = 999999

#print(maxC)

for x in range(trano['numTransactions']):
  if float(trano[str(x)]['change']['slope']) > tMax:
    tMax = float(trano[str(x)]['change']['slope'])
  if float(trano[str(x)]['change']['slope']) < tMin:
    tMin = float(trano[str(x)]['change']['slope'])

for x in range(trano['numTransactions']):
  if float(trano[str(x)]['change']['percent']) > pMax:
    pMax = float(trano[str(x)]['change']['percent'])
  if float(trano[str(x)]['change']['percent']) < pMin:
    pMin = float(trano[str(x)]['change']['percent'])

yOffset = .00001
xOffset = .0001
ymax = int((tMax-tMin)/yOffset) + 50
xmax = int((pMax-pMin)/xOffset) + 50
windowSize = str(ymax)+"x"+str(xmax)

def xConvert(x):
  x = 25+((x)/xOffset)-pMin
  return x

def yConvert(y):
  y = 25+((y)/yOffset)-tMin
  return y

from tkinter import Tk, Canvas, Frame, BOTH, TOP, BOTTOM, Scrollbar, X

class Example(Frame):

  def __init__(self):
    super().__init__()

    self.initUI()

  def initUI(self):
    self.master.title("Test")
    self.pack(fill=BOTH, expand=1)

    red="#ff6347"
    green="#00cc00"
    off = 2
    sell="break"

    canvas = Canvas(self)

    for i in range(trano['numTransactions']):
      if trano[str(i)]['change']['sellType'] == sell:
        x = xConvert(trano[str(i)]['change']['percent'])
        y = yConvert(trano[str(i)]['change']['slope'])
        color = green if trano[str(i)]['change']['percent'] > 0 else red
        canvas.create_oval(y-off,xmax-(x-off),y+off,xmax-(x+off), fill=color)

    canvas.pack(fill=BOTH, expand=1)


def main():
  root = Tk()
  ex = Example()
  root.geometry(windowSize)
  root.mainloop()


if __name__ == '__main__':
    main()
