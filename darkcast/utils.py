import os, inspect, operator, collections, math

###############################################################################
# Create the data paths to search.
paths = []
if os.getenv("DARKCAST_DATA_PATH"):
    paths += [os.path.abspath(os.path.expandvars(path)) for path in 
              reversed(os.getenv("DARKCAST_DATA_PATH").split(":"))]
paths.append(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
paths.append(paths[-1] + "/limits")

###############################################################################
def find(name):
    """
    Find a file, either absolute or along the following paths in the
    order given:
    (0) The absolute path, if the absolute path is given.
    (1) The current directory within the Python interpreter.
    (2) The paths defined by the environment variable 'DARKCAST_DATA_PATH'.
    (3) The Darkcast package path.
    Returns the absolute path if it exists, otherwise 'None' is
    returned.

    name: name of the absolute or relative file to find.
    """
    name = os.path.expandvars(name)
    if os.path.isabs(name) and os.path.isfile(name):
        return name
    if os.path.isfile(os.path.join(os.getcwd(), name)):
        return os.path.join(os.getcwd(), name)
    for path in paths:
        if os.path.isfile(os.path.join(path, name)):
            return os.path.join(path, name)
    return None

###############################################################################
def trace(*ts):
    """
    Return the sum of products for a set of lists, e.g. the trace
    when the lists provided are the diagonals of matrices.

    ts: lists to multiply and sum.
    """
    return sum(reduce(operator.mul, t) for t in zip(*ts))

###############################################################################
class SolveError(Exception):
    """
    Simple exception for the 'solve' method.
    """
    pass

###############################################################################
def solve(f, x0 = None, x1 = None, x = 1, tol = 1e-2, itrs = 100):
    """
    Solve a zero for a function, 'f(x)', using Ridders' method and
    with the assumption that x >= 0. If no bracketing interval for the
    zero is provided, then the method tries to determine an initial
    bracket. If a lower bracket value is provided, then an attempt is
    made to determine the upper value, and vice versa. Alternatively,
    a starting value for the bracket finding can be provided.

    f:    function to solve, must take a single float argument, e.g. 'f(x)'.
    x0:   optional lower bracket value.
    x1:   optional upper bracket value.
    x:    optional starting value for bracket finding.
    tol:  relative tolerance required on x.
    itrs: maximum number of iterations 
    """
    # Guess the initial bracket.
    sx, g0, g1 = 2.0, x0 == None, x1 == None
    if g0 and not g1: x0 = x1/sx
    elif g1 and not g0: x1 = x0*sx
    else: x0, x1 = x*0.8, x*1.2
    f0, f1 = f(x0), f(x1)

    # Expand the bracket if needed.
    if g0 and not g1:
        for itr in range(0, int(itrs)):
            if f0*f1 < 0: break
            x0 = x0/sx
            f0 = f(x0)
    elif g1 and not g0:
        for itr in range(0, int(itrs)):
            if f0*f1 < 0: break
            x1 = x1*sx
            f1 = f(x1)
    else:
        xmin, xmax, fmin, fmax = x0, x1, f0, f1
        if fmin < fmax: xmin, xmax, fmin, fmax = xmax, xmin, fmax, fmin
        for itr in xrange(0, int(itrs)):
            if fmin*fmax < 0: break
            x0, x1 = x0/sx, x1*sx
            f0, f1 = f(x0), f(x1)
            if f0 < fmin: xmin, fmin = x0, f0
            if f1 < fmin: xmin, fmin = x1, f1
            if f0 > fmax: xmax, fmax = x0, f0
            if f1 > fmax: xmax, fmax = x1, f1
        x0, x1, f0, f1 = xmin, xmax, fmin, fmax
        if x0 > x1: x0, x1, f0, f1 = x1, x0, f1, f0
    if not f0*f1 < 0: raise SolveError(
        "Could not find bracketing interval.")

    # Apply Ridders' method.
    for itr in xrange(0, int(itrs)):
        xm = (x0 + x1)/2.0
        fm = f(xm)
        xn = xm + (xm - x0)*(-1.0 if f0 < 0 else 1.0)*fm/math.sqrt(
            fm**2 - f0*f1)
        fn = f(xn)
        if fn == 0.0 or abs(x1 - x0)/xn < tol: return xn
        elif fn*fm < 0: x0, x1, f0, f1 = xn, xm, fn, fm
        elif fn*f0 < 0: x1, f1 = xn, fn
        else: x0, f0 = xn, fn
    raise SolveError("Could not find a solution.")

###############################################################################
class DatasetError(Exception):
    """
    Simple exception for the 'Dataset' class.
    """
    pass

###############################################################################
class Dataset:
    """
    Represents an n-dimensional dataset where the nth dimension is
    provided as a function of the preceding n - 1 dimensions with the
    '()' operator. Within the dataset range linear interpolation is
    used, while outside the dataset range the nearest edge point is
    used. The dataset is assumed to be a regular grid but is not
    required to have constant spacing.
    
    axes: defining axes for the dataset.
    vals: dataset values.
    dim:  dimension of the dataset.
    len:  number of stored dataset values.
    """
    ###########################################################################
    def __init__(self, name = None, vals = None):
        """
        Initiate the dataset from a whitespace separated text file
        with the format 'x_0 x_1 ... x_n' for each line. The dataset
        is assumed to be a regular grid; any missing points are
        initialized as 0.

        name: name of the text file to read the dataset from.
        vals: optional list of values, rather than a file.
        """
        import os.path, copy
        self.vals, self.axes, self.len, self.dim = [], [], 0, 0

        # Read from a file.
        if name != None:
            try: data, vals = file(find(name)), []
            except: raise DatasetError(
                "Could not find the dataset '%s'." % name)
            for idx, line in enumerate(data):
                line = line.split("#")[0].split()
                if len(line) == 0: continue
                if self.dim == 0:
                    self.axes = [set() for i in xrange(len(line) - 1)]
                    self.dim  = len(self.axes)
                if len(line) != self.dim + 1: raise DatasetError(
                    "Line %i has size %i, %i required." 
                    % (idx + 1,len(line), self.dim + 1))
                try:
                    for axis, val in zip(self.axes, line): axis.add(float(val))
                    vals.append([float(val) for val in line])
                except: raise DatasetError(
                    "Failed to read line %i." % (idx + 1))
            data.close()
        
        # Read from a list of values.
        elif vals:
            for idx, line in enumerate(vals):
                if self.dim == 0:
                    self.axes = [set() for i in xrange(len(line) - 1)]
                    self.dim  = len(self.axes)
                try:
                    for axis, val in zip(self.axes, line): axis.add(float(val))
                except: raise DatasetError(
                    "Failed to read line %i." % (idx + 1))
        else: return

        # Sort the axes and allocate the values.
        for idx, axis in enumerate(self.axes):
            self.axes[idx] = sorted(list(axis))
        self.__init(vals)

    ###########################################################################
    def __init(self, vals = None):
        """
        Initialize the dimension, length, and stored values of the
        dataset.
        
        vals: values to assign, each of the form [x_0, x_1, ..., x_n].
        """
        self.dim = len(self.axes)
        self.len = reduce(operator.mul, [len(a) for a in self.axes], 1)
        if vals != None:
            self.vals = [0]*self.len
            for i, val in enumerate(vals):
                self[self.__fkey(val)] = val[-1]

    ###########################################################################
    def __call__(self, xs, method = 1):
        """
        Return the interpolated/extrapolated dataset x_n value, given
        the point x_0, ..., x_n-1.

        xs:     point to interpolate, must be of length n-1.
        method: interpolation method.
        """
        if not hasattr(xs, "__iter__"): xs = (xs,)
        if self.dim != len(xs): raise DatasetError(
            "Incorrect dimension %i, %i required." % (len(xs), self.dim))

        # Nearest neighbor.
        if method == 0: return self[self.__fkey(xs)]
        
        # Polynomial interpolation.
        vals, bxs, ks = [], [], self.__skey(xs, True)
        for k in xrange(2**self.dim):
            bks = []
            for d in xrange(self.dim): bks.append(k % 2); k = (k - bks[-1])/2
            sks = [ks[bk][d] for d, bk in enumerate(bks)]
            vals.append(self[self.__s2f(sks)])
            bxs.append(self.__s2x(sks))
        for d, x in enumerate(xs):
            step = 2**(d + 1)
            for k in xrange(0, len(vals), step):
                
                # Currently just linear interpolation.
                x0, x1 = bxs[k][d], bxs[k + step/2][d]
                val0, val1 = vals[k], vals[k + step/2]
                if x0 == x1: continue
                vals[k] = (x1 - x)/(x1 - x0)*val0 + (x - x0)/(x1 - x0)*val1
        return vals[0]

    ###########################################################################
    def __skey(self, xs, bk = False):
        """
        Find the structured key of the nearest neighbor for a given
        point x_0, x_1, ..., x_n-1. Key finding is performed per axis
        with a modified regula falsi method: if regula falsi fails to
        find a new bracket, bisection is used to find a new bracket.

        xs: point to determine the key of the nearest neighbor.
        bk: if true, return the bracketing structured keys of the point.
        """
        dbg = xs[0] == 1.14
        k0s, k1s = [], []
        for x, axis in zip(xs, self.axes):
            k, k0, k1 = 0, 0, len(axis) - 1
            if x <= axis[k0]:   k1 = k0
            elif x >= axis[k1]: k0 = k1
            else:
                while k1 - k0 > 1:
                    k = k0+int(round((x-axis[k0])*(k1-k0)/(axis[k1]-axis[k0])))
                    if x == axis[k]: k0, k1 = k, k; break
                    if k == k0 or k == k1: k = k0 + (k1 - k0)/2
                    if x > axis[k]: k0 = k
                    else: k1 = k
            k0s.append(k0)
            k1s.append(k1)
        if bk: return (k0s, k1s)
        else: return [k1 if abs(axis[k1] - x) < abs(axis[k0] - x) else k0
                      for axis, k0, k1 in zip(self.axes, k0s, k1s)]

    ###########################################################################
    def __fkey(self, xs, bk = False):
        """
        Find the flat key of the nearest neighbor for a given point
        x_0, x_1, ..., x_n-1. See the method 'skey' for details.

        xs: point to determine the key of the nearest neighbor.
        bk: if true, return the bracketing flat keys of the point.
        """
        if bk: 
            k0s, k1s = self.__skey(xs)
            return self.__s2f(k0s), self.__s2f(k1s)
        else: return self.__s2f(self.__skey(xs))

    ###########################################################################
    def __s2f(self, skey):
        """
        Transform a structured key to a flat key.
        
        skey: structured key to transform.
        """
        f, c = 0, 1
        for s, axis in zip(skey, self.axes): f += c*s; c *= len(axis)
        return f

    ###########################################################################
    def __f2s(self, fkey):
        """
        Transform a flat key to a structured key.

        fkey: flat key to transform.
        """
        s, c = [], fkey
        for axis in self.axes: s.append(c % len(axis)); c = (c-s[-1])/len(axis)
        return s

    ###########################################################################
    def __s2x(self, skey):
        """
        Transform a structure key to coordinates, e.g. x_0, x_1, ...,
        x_n-1.

        skey: structured key to transform.
        """
        return [self.axes[i][j] for i, j in enumerate(skey)]

    ###########################################################################
    def __f2x(self, fkey):
        """
        Transform a flat key to coordinates, e.g. x_0, x_1, ...,
        x_n-1.

        fkey: flat key to transform.
        """
        return self.__s2x(self.__f2s(fkey))

    ###########################################################################
    def __opr(self, o, a, b):
        """
        Internal method used to apply an operator of the form 
        'c = a o b'.

        o: operator which can be called as o(a, b).
        a: left-hand value of the operator.
        b: right-hand value of the operator.
        """
        import copy
        c = dataset()

        # Both objects are of type 'Dataset'.
        if type(a) == type(self) and type(b) == type(self):
            if a.dim != b.dim: raise DatasetError(
                "Incompatible dimensions %i and %i."  % (a.dim, b.dim))
            asub, bsub = True, True
            for aaxis, baxis in zip(a.axes, b.axes):
                c.axes.append(sorted(list(set(aaxis) | set(baxis))))
                asub &= len(baxis) == len(c.axes[-1])
                bsub &= len(aaxis) == len(c.axes[-1])
            c.__init([])
            if asub and bsub:
                for fkey in xrange(len(c)):
                    c[fkey] = o(a[fkey], b[fkey])
            elif asub:
                for fkey in xrange(len(c)): 
                    c[fkey] = o(a(c.__f2x(fkey)), b[fkey])
            elif bsub:
                for fkey in xrange(len(c)): 
                    c[fkey] = o(a[fkey], b(c.__f2x(fkey)))
            else:
                for fkey in xrange(len(c)):
                    xs = c.__f2x(fkey); c[fkey] = o(a(xs), b(xs))

        # One object is of type 'Dataset'.
        elif type(a) == type(self):
            c = copy.deepcopy(a)
            for fkey, val in enumerate(c.vals): c[fkey] = o(val, b)
        elif type(b) == type(self):
            c = copy.deepcopy(b)
            for fkey, val in enumerate(c.vals): c[fkey] = o(val, a)
        return c

    ###########################################################################
    def __setitem__(self, fkey, val): self.vals[fkey] = val
    def __getitem__(self, fkey): return self.vals[fkey]
    def __len__ (self): return self.len
    def __add__ (self, b): return self.__opr(operator.add, self, b)
    def __sub__ (self, b): return self.__opr(operator.sub, self, b)
    def __mul__ (self, b): return self.__opr(operator.mul, self, b)
    def __div__ (self, b): return self.__opr(operator.div, self, b)
    def __mod__ (self, b): return self.__opr(operator.mod, self, b)
    def __pow__ (self, b): return self.__opr(operator.pow, self, b)
    def __radd__(self, b): return self.__opr(operator.add, self, b)
    def __rsub__(self, b): return self.__opr(operator.sub, self, b)
    def __rmul__(self, b): return self.__opr(operator.mul, self, b)
    def __rdiv__(self, b): return self.__opr(operator.div, self, b)
    def __rmod__(self, b): return self.__opr(operator.mod, self, b)
    def __rpow__(self, b): return self.__opr(operator.pow, self, b)

###############################################################################
class DatasetsError(Exception):
    """
    Simple exception for the 'Datasets' class.
    """
    pass

###############################################################################
class Datasets(collections.OrderedDict):
    """
    Loads multiple 2-dimensional 'Dataset's from a single file, all as
    a function of the first column. The first row is read as labels
    for the columns. The 'Dataset' object acts as an ordered
    dictionary for the individual datasets.
    """
    ###########################################################################
    def __init__(self, name):
        """
        Load the datasets for a given file.

        name: name of the text file to read the datasets from.
        """
        super(Datasets, self).__init__()
        try: data = file(find(name))
        except: raise DatasetsError(
            "Could not find the dataset '%s'." % name)

        # Read from a file.
        keys = data.readline().replace("#", "").split()[1:]
        dats = [[] for key in keys]
        for idx, line in enumerate(data):
            line = line.split("#")[0].split()
            if len(line) == 0: continue
            if len(line) != len(keys) + 1: raise DatasetsError(
                "Line %i has size %i, %i required." 
                % (idx + 1, len(line), len(keys)))
            try:
                var = float(line[0])
                for dat, val in zip(dats, line[1:]):
                    dat.append([var, float(val)])
            except: raise DatasetsError(
                "Failed to read line %i." % (idx + 1))
        data.close()

        # Create the datasets.
        for key, vals in zip(keys, dats): self[key] = Dataset(vals = vals)
