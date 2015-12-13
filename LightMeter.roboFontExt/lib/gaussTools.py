import  math
from fontTools.misc.transform import Transform

"""



"""
    
def getCircle(x0, y0, radius):
    """
    http://en.wikipedia.org/wiki/Midpoint_circle_algorithm

    public static void DrawCircle(int x0, int y0, int radius)
    {
      int x = radius, y = 0;
      int radiusError = 1-x;
     
      while(x >= y)
      {
        DrawPixel(x + x0, y + y0);
        DrawPixel(y + x0, x + y0);
        DrawPixel(-x + x0, y + y0);
        DrawPixel(-y + x0, x + y0);
        DrawPixel(-x + x0, -y + y0);
        DrawPixel(-y + x0, -x + y0);
        DrawPixel(x + x0, -y + y0);
        DrawPixel(y + x0, -x + y0);
        y++;
        if (radiusError<0)
        {
          radiusError += 2 * y + 1;
        }
        else
        {
          x--;
          radiusError += 2 * (y - x + 1);
        }
      }
    }
    # Get a bitmapped circle as runlengths.
    >>> getCircle(0,0,5)
    {0: [-5, 5], 1: [-5, 5], 2: [-5, 5], 3: [-4, 4], 4: [-3, 3], 5: [-2, 2], -2: [-5, 5], -5: [-2, 2], -4: [-3, 3], -3: [-4, 4], -1: [-5, 5]}

    """
    points = {}
    x = radius
    y = 0
    radiusError = 1-x
    while x >= y:
        points[y + y0] = [-x + x0, x + x0]
        points[x + y0] = [-y + x0, y + x0]
        points[-y + y0] = [-x + x0, x + x0]
        points[-x + y0] = [-y + x0, y + x0]
        y += 1
        if (radiusError<0):
            radiusError += 2 * y + 1
        else:
            x -= 1
            radiusError += 2 * (y - x + 1)
    return points

def xyGaussian(x, y, a, bx, by, sigmax, sigmay):
    """ 
        # Two dimensional gaussian function.
        # from https://en.wikipedia.org/wiki/Gaussian_function
        >>> xyGaussian(0, 0, 1, 0, 0, 10, 10)
        1.0
        >>> xyGaussian(0, 0, 1, 1000, 0, 10, 10)
        0.0
    """
    return a * math.exp(-((x-bx)**2/(2*sigmax**2)+(y-by)**2/(2*sigmay**2)))

def gaussian(x, amplitude, mu, sigma):
    """ 
        #
        # from https://en.wikipedia.org/wiki/Gaussian_function
        >>> gaussian(0, 1, 0, 10)
        1.0
        >>> gaussian(0, 1, 1000, 10)
        0.0

    """
    val = amplitude * math.exp(-(x - mu)**2 / sigma**2)
    return val

def getArea(radius):
    """
        >>> getArea(2)
        [(0, 1), (0, -2), (-2, 1), (0, 0), (-2, 0), (-1, -2), (-1, -1), (-1, 2), (-1, 1), (0, 2), (-2, -1), (0, -1), (1, 0), (1, -1), (1, 1), (-1, 0)]
    
    """
    grid = set()
    lines = getCircle(0, 0, radius)
    for y, (xMin, xMax) in lines.items():
        for x in range(xMin, xMax):
            grid.add((x,y))
    return list(grid)

def getKernel(radius, amplitude=1, depth=50, angle=0):
    """
    >>> a = getKernel(5)
    >>> a[(0,0)]
    0.03662899097662087
    >>> a[(2,0)]
    0.02371649522786113
    """
    t = Transform()
    t = t.rotate(angle)
    lines = getCircle(0, 0, radius)
    sigma = (radius+1) / math.sqrt(2*math.log(depth))
    grid = {}
    total = 0
    for y, (xMin, xMax) in lines.items():
        for x in range(xMin, xMax+1, 1):
            g = xyGaussian(x,y, amplitude, 0, 0, sigma, sigma)
            grid[(x,y)]=grid.get((x,y), 0)+g
            total += g
    # scale the amplitude based on the total
    grid = {k: float(v)/total for k, v in grid.items()}
    # rotate the grid
    grid = grid
    new = {}
    for k, v in grid.items():
        k_ = t.transformPoint(k)
        new[k_] = v
    grid = new
    return grid
                
if __name__ == "__main__":
    import doctest
    from pprint import pprint
    doctest.testmod()
    pprint(getKernel(7, 50))
