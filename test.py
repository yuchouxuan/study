

import numpy as np
from mayavi import mlab
x,y,z = np.mgrid[-5:5:24j,-5:5:24j,-5:5:24j]
u,v,w = x,x*y,z-1
mlab.figure(size=(500,540))
SimpleHandle = mlab.quiver3d(x,y,z,u,v,w)
mlab.show()