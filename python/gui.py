maxf = open("maxs.json", "r")
minf = open("mins.json", "r")
canf = open("candle.json", "r")

import json

maxC = json.loads(maxf.readline())
minC = json.loads(minf.readline())
cand = json.loads(canf.readline())

tMax = 0
tMin = 999999

#print(maxC)

for x in maxC:
  if float(maxC[x]) > tMax:
    tMax = float(maxC[x])

for x in minC:
  if float(minC[x]) < tMin:
    tMin = float(minC[x])

yOffset = 10
y = int((tMax-tMin)/yOffset) + 50
x = len(cand)
windowSize = str(x)+"x"+str(y)

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

    scrollBar = Scrollbar(self, orient='horizontal')
    scrollBar.pack(side=BOTTOM, fill=X)
    
    canvas = Canvas(self)

    for i in range(len(cand)):

      color = green if float(cand[str(i)]['cPrice']) - float(cand[str(i)]['oPrice']) > 0 else red

      #(x1, y1, x2, y2)
      canvas.create_rectangle(i*2, (float(cand[str(i)]['oPrice'])-tMin)/yOffset, (i*2)+2, (float(cand[str(i)]['cPrice'])-tMin)/yOffset,
        outline=color, fill=color)

    canvas.pack(side=TOP, fill=BOTH)
    scrollBar.config(command=canvas.xview)


def main():
  root = Tk()
  ex = Example()
  root.geometry(windowSize)
  root.mainloop()


if __name__ == '__main__':
    main()
