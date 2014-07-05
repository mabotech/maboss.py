
import math

import logging

log= logging.getLogger('root')

class Color:

    def hsvToRGB(self, h, s, v):
        """Convert HSV color space to RGB color space

        @param h: Hue
        @param s: Saturation
        @param v: Value
        return (r, g, b)
        """
        #import math
        hi = math.floor(h / 60.0) % 6
        f =  (h / 60.0) - math.floor(h / 60.0)
        p = v * (1.0 - s)
        q = v * (1.0 - (f*s))
        t = v * (1.0 - ((1.0 - f) * s))
        return {
            0: (v, t, p),
            1: (q, v, p),
            2: (p, v, t),
            3: (p, q, v),
            4: (t, p, v),
            5: (v, p, q),
        }[hi]

    def rgbToHSV(self, r, g, b):
        """Convert RGB color space to HSV color space

        @param r: Red
        @param g: Green
        @param b: Blue
        return (h, s, v)
        """
        maxc = max(r, g, b)
        minc = min(r, g, b)
        colorMap = {
            id(r): 'r',
            id(g): 'g',
            id(b): 'b'
        }
        if colorMap[id(maxc)] == colorMap[id(minc)]:
            h = 0
        elif colorMap[id(maxc)] == 'r':
            h = 60.0 * ((g - b) / (maxc - minc)) % 360.0
        elif colorMap[id(maxc)] == 'g':
            h = 60.0 * ((b - r) / (maxc - minc)) + 120.0
        elif colorMap[id(maxc)] == 'b':
            h = 60.0 * ((r - g) / (maxc - minc)) + 240.0
        v = maxc
        if maxc == 0.0:
            s = 0.0
        else:
            s = 1.0 - (minc / maxc)
        return (h, s, v)

    def cr(self, i):

        return "%02X"%(i * 255)

    def getc(self, x):

        # pass with short time, less than 40 seconds
        if x >= 0 and x < 40:
            r = 240 -2.5*x
        # pass in 40 to 80 seconds
        elif x>=40 and x < 80:
            r = 160 -x
        # pass in 80 to 160 seconds
        elif x>=80 and x < 160:
            r = 100-x/4
        # passed by more than 160 seconds
        elif x >= 160:
            r = 60 * 160/x
        else:
            r = 0
            log.debug(x)
            #raise Exception('error:%s'%(x))

        return int(r)


    def getColor(self, i):
        """
        0 <= i < **
        0:Blue
        standard cycletime(81) : Green
        """
        t = self.getc(i)
        cl = "".join(map(self.cr, self.hsvToRGB(t,1,1)))
        return cl


def main():

    out = open('color.html','w')
    out.write( "<table><tr>")

    color = Color()

    for i in range(3,43):
        #v = color.getc(i)
        #cl = "".join(map(color.cr, color.hsvToRGB(v,1,1)))
        v = i *i/2 - 3
        """
        if i > 26:
            v = i*i-226
        else:
            v = i * 10
        """
        cl = color.getColor(v)
        s = '''<td bgcolor = "#%s">%ss</td>''' %(cl, v)
        out.write(s)
    out.write( "</tr></table>")
    out.close()

if __name__ == '__main__':
    main()
