"""
`quadrature_tables` are organized as follows::

    quadrature_tables = {
        '<geometry1>' : {
            order1 : QuadraturePoints(args1),
            order2 : QuadraturePoints(args2),
            ...
        },
        '<geometry2>' : {
            order1 : QuadraturePoints(args1),
            order2 : QuadraturePoints(args2),
            ...
        },
        ...
    }

**Note** The order for quadratures on tensor product domains (`'2_4'`,
`'3_8'` geometries) in case of composite Gauss quadratures (products of
1D quadratures) holds for each component separately, so the actual
polynomial order may be much higher (up to `order * dimension`).

Naming conventions in problem description files::

    `<family>_<order>_<dimension>`

Integral 'family' is just an arbitrary name given by user.

Quadrature coordinates and weights copied from The Finite Element Method
Displayed by Gouri Dhatt and Gilbert Touzat, Wiley-Interscience Production,
1984.

The line integral (geometry '1_2') coordinates and weights are taken from
Abramowitz, M. and Stegun, I.A., Handbook of Mathematical Functions, Dover
Publications, New York, 1972.

Examples
--------
* gauss_o2_d2 # second order, 2D
* gauss_o1_d3 # first order, 3D
* my_int_o1_d3 # same as above
"""
import numpy as nm

from sfepy.base.base import Struct

class QuadraturePoints(Struct):
    """
    Representation of a set of quadrature points.

    Parameters
    ----------
    data : array_like
        The array of shape `(n_point, dim + 1)` of quadrature point
        coordinates (first `dim` columns) and weights (the last column). 
    coors : array_like, optional
        Optionally, instead of using `data`, the coordinates and weights can
        be provided separately - `data` are then ignored.
    weights : array_like, optional
        Optionally, instead of using `data`, the coordinates and weights can
        be provided separately - `data` are then ignored.
    bounds : (float, float), optional
        The coordinates and weights should correspond to a reference
        element in `[0, 1]` x `dim`. Provide the correct bounds if this is
        not the case.
    tp_fix : float, optional
        The value that is used to multiply the tensor product element
        volume (= 1.0) to get the correct volume.
    symmetric : bool
        If True, the integral is 1D and the given coordinates and weights are
        symmetric w.r.t. the centre of bounds; only the non-negative
        coordinates are given.
    """

    def __init__(self, data, coors=None, weights=None, bounds=None, tp_fix=1.0,
                 symmetric=False):
        if coors is None:
            data = nm.array(data, dtype=nm.float64, ndmin=2)
            self.coors = data[:,:-1].copy()
            self.weights = data[:,-1].copy()

        elif weights is not None:
            self.coors = nm.array(coors, dtype=nm.float64, ndmin=2)
            self.weights = nm.array(weights, dtype=nm.float64)

        else:
            raise ValueError('both "coors" and "weights" have to be provided!')

        self.n_point, self.dim = self.coors.shape

        self.bounds = (0, 1)
        bbox = nm.array([self.bounds] * self.dim, dtype=nm.float64)
        self.volume = nm.prod(bbox.sum(axis=1)) * tp_fix

        if symmetric:
            isym = 0 if data[0, 0] == 0 else None

        if bounds is not None:
            # Transform from given bounds to self.bounds.
            bbox = nm.array([bounds] * self.dim, dtype=nm.float64)
            volume = nm.prod(nm.diff(bbox, axis=1)) * tp_fix

            a, b = bounds
            c, d = self.bounds

            c1 = (d - c) / (b - a)
            c2 = ((b * c) - (a * d)) / (b - a)

            self.coors = c1 * self.coors + c2
            self.weights *= self.volume / volume

        if symmetric:
            if self.coors.shape[1] != 1:
                raise ValueError()
            origin = 0.5 * (self.bounds[0] + self.bounds[1])

            self.coors = nm.r_[2 * origin - self.coors[:isym:-1], self.coors]
            self.weights = nm.r_[self.weights[:isym:-1], self.weights]

_QP = QuadraturePoints
quadrature_tables = {
    '1_2' : {

        1 : _QP([[0.000000000000000e+00, 2.0]],
                bounds=(-1.0, 1.0), symmetric=True),

        3 : _QP([[0.577350269189626e+00, 1.0]],
                bounds=(-1.0, 1.0), symmetric=True),

        5 : _QP([[0.000000000000000e+00, 0.888888888888889e+00],
                 [0.774596669241483e+00, 0.555555555555556e+00]],
                bounds=(-1.0, 1.0), symmetric=True),

        7 : _QP([[0.339981043584856e+00, 0.652145154862546e+00],
                 [0.861136311594053e+00, 0.347854845137454e+00]],
                bounds=(-1.0, 1.0), symmetric=True),

        9 : _QP([[0.000000000000000e+00, 0.568888888888889e+00],
                 [0.538469310105683e+00, 0.478628670499366e+00],
                 [0.906179845938664e+00, 0.236926885056189e+00]],
                bounds=(-1.0, 1.0), symmetric=True),

        11 : _QP([[0.238619186083197e+00, 0.467913934572691e+00],
                  [0.661209386466265e+00, 0.360761573048139e+00],
                  [0.932469514203152e+00, 0.171324492379170e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        13 : _QP([[0.000000000000000e+00, 0.417959183673469e+00],
                  [0.405845151377397e+00, 0.381830050505119e+00],
                  [0.741531185599394e+00, 0.279705391489277e+00],
                  [0.949107912342759e+00, 0.129484966168870e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        15 : _QP([[0.183434642495650e+00, 0.362683783378362e+00],
                  [0.525532409916329e+00, 0.313706645877887e+00],
                  [0.796666477413627e+00, 0.222381034453374e+00],
                  [0.960289856497536e+00, 0.101228536290376e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        17 : _QP([[0.000000000000000e+00, 0.330239355001260e+00],
                  [0.324253423403809e+00, 0.312347077040003e+00],
                  [0.613371432700590e+00, 0.260610696402935e+00],
                  [0.836031107326636e+00, 0.180648160694857e+00],
                  [0.968160239507626e+00, 0.081274388361574e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        19 : _QP([[0.148874338981631e+00, 0.295524224714753e+00],
                  [0.433395394129247e+00, 0.269266719309996e+00],
                  [0.679409568299024e+00, 0.219086362515982e+00],
                  [0.865063366688985e+00, 0.149451349150581e+00],
                  [0.973906528517172e+00, 0.066671344308688e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        23 : _QP([[0.125233408511469e+00, 0.249147045813403e+00],
                  [0.367831498998180e+00, 0.233492536538355e+00],
                  [0.587317954286617e+00, 0.203167426723066e+00],
                  [0.769902674194305e+00, 0.160078328543346e+00],
                  [0.904117256370475e+00, 0.106939325995318e+00],
                  [0.981560634246719e+00, 0.047175336386512e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        31 : _QP([[0.095012509837637440185e+00, 0.189450610455068496285e+00],
                  [0.281603550779258913230e+00, 0.182603415044923588867e+00],
                  [0.458016777657227386342e+00, 0.169156519395002538189e+00],
                  [0.617876244402643748447e+00, 0.149595988816576732081e+00],
                  [0.755404408355003033895e+00, 0.124628971255533872052e+00],
                  [0.865631202387831743880e+00, 0.095158511682492784810e+00],
                  [0.944575023073232576078e+00, 0.062253523938647892863e+00],
                  [0.989400934991649932596e+00, 0.027152459411754094852e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        39 : _QP([[0.076526521133497333755e+00, 0.152753387130725850698e+00],
                  [0.227785851141645078080e+00, 0.149172986472603746788e+00],
                  [0.373706088715419560673e+00, 0.142096109318382051329e+00],
                  [0.510867001950827098004e+00, 0.131688638449176626898e+00],
                  [0.636053680726515025453e+00, 0.118194531961518417312e+00],
                  [0.746331906460150792614e+00, 0.101930119817240435037e+00],
                  [0.839116971822218823395e+00, 0.083276741576704748725e+00],
                  [0.912234428251325905868e+00, 0.062672048334109063570e+00],
                  [0.963971927277913791268e+00, 0.040601429800386941331e+00],
                  [0.993128599185094924786e+00, 0.017614007139152118312e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),

        47 : _QP([[0.064056892862605626085e+00, 0.127938195346752156974e+00],
                  [0.191118867473616309159e+00, 0.125837456346828296121e+00],
                  [0.315042679696163374387e+00, 0.121670472927803391204e+00],
                  [0.433793507626045138487e+00, 0.115505668053725601353e+00],
                  [0.545421471388839535658e+00, 0.107444270115965634783e+00],
                  [0.648093651936975569252e+00, 0.097618652104113888270e+00],
                  [0.740124191578554364244e+00, 0.086190161531953275917e+00],
                  [0.820001985973902921954e+00, 0.073346481411080305734e+00],
                  [0.886415527004401034213e+00, 0.059298584915436780746e+00],
                  [0.938274552002732758524e+00, 0.044277438817419806169e+00],
                  [0.974728555971309498198e+00, 0.028531388628933663181e+00],
                  [0.995187219997021360180e+00, 0.012341229799987199547e+00]],
                 bounds=(-1.0, 1.0), symmetric=True),
    },

    '2_3' : {

        1 : _QP([[ 1.0/3.0, 1.0/3.0, 0.5]], tp_fix=0.5),

        2 : _QP([[ 1.0/6.0, 1.0/6.0, 1.0/6.0],
                 [ 2.0/3.0, 1.0/6.0, 1.0/6.0],
                 [ 1.0/6.0, 2.0/3.0, 1.0/6.0]], tp_fix=0.5),

        3 : _QP([[ 1.0/3.0, 1.0/3.0,-27.0/96.0],
                 [ 1.0/5.0, 1.0/5.0, 25.0/96.0],
                 [ 3.0/5.0, 1.0/5.0, 25.0/96.0],
                 [ 1.0/5.0, 3.0/5.0, 25.0/96.0]], tp_fix=0.5),

    },

    '2_4' : {

        2 : _QP([[ nm.sqrt(2.0/3.0), 0.0         , 4.0/3.0],
                 [-1/nm.sqrt(6)    , 1/nm.sqrt(2), 4.0/3.0],
                 [-1/nm.sqrt(6)    ,-1/nm.sqrt(2), 4.0/3.0]], bounds=(-1.0, 1.0)),

        3 : _QP([[-1/nm.sqrt(3),-1/nm.sqrt(3), 1.0],
                 [ 1/nm.sqrt(3),-1/nm.sqrt(3), 1.0],
                 [ 1/nm.sqrt(3), 1/nm.sqrt(3), 1.0],
                 [-1/nm.sqrt(3), 1/nm.sqrt(3), 1.0]], bounds=(-1.0, 1.0)),

        5 : _QP([[ nm.sqrt(7.0/15.0), 0.0              , 0.816326530612245],
                 [-nm.sqrt(7.0/15.0), 0.0              , 0.816326530612245],
                 [ 0.0              , nm.sqrt(7.0/15.0), 0.816326530612245],
                 [ 0.0              ,-nm.sqrt(7.0/15.0), 0.816326530612245],
                 [ 0.881917103688197, 0.881917103688197, 0.183673469387755],
                 [ 0.881917103688197,-0.881917103688197, 0.183673469387755],
                 [-0.881917103688197, 0.881917103688197, 0.183673469387755],
                 [-0.881917103688197,-0.881917103688197, 0.183673469387755]], bounds=(-1.0, 1.0)),

    },

    '3_4' : {
        1 : _QP([[ 1.0/4.0, 1.0/4.0, 1.0/4.0, 1.0/6.0]], tp_fix=1.0/6.0),

        2 : _QP([[ (5-nm.sqrt(5))/20  , (5-nm.sqrt(5))/20  , (5-nm.sqrt(5))/20  , 1.0/24.0],
                 [ (5-nm.sqrt(5))/20  , (5-nm.sqrt(5))/20  , (5+3*nm.sqrt(5))/20, 1.0/24.0],
                 [ (5-nm.sqrt(5))/20  , (5+3*nm.sqrt(5))/20, (5-nm.sqrt(5))/20  , 1.0/24.0],
                 [ (5+3*nm.sqrt(5))/20, (5-nm.sqrt(5))/20  , (5-nm.sqrt(5))/20  , 1.0/24.0]], tp_fix=1.0/6.0),

        3 : _QP([[ 1.0/4.0, 1.0/4.0, 1.0/4.0,-2.0/15.0],
                 [ 1.0/6.0, 1.0/6.0, 1.0/6.0, 3.0/40.0],
                 [ 1.0/6.0, 1.0/6.0, 1.0/2.0, 3.0/40.0],
                 [ 1.0/6.0, 1.0/2.0, 1.0/6.0, 3.0/40.0],
                 [ 1.0/2.0, 1.0/6.0, 1.0/6.0, 3.0/40.0]], tp_fix=1.0/6.0),

        4 : _QP([[-0.5000000000000000, -0.5000000000000000, -0.5000000000000000, -0.1052444444444440],
                 [-0.8571428571428570, -0.8571428571428570, -0.8571428571428570,  0.0609777777777780],
                 [-0.8571428571428570, -0.8571428571428570,  0.5714285714285710,  0.0609777777777780],
                 [-0.8571428571428570,  0.5714285714285710, -0.8571428571428570,  0.0609777777777780],
                 [ 0.5714285714285710, -0.8571428571428570, -0.8571428571428570,  0.0609777777777780],
                 [-0.2011928476664020, -0.2011928476664020, -0.7988071523335980,  0.1991111111111110],
                 [-0.2011928476664020, -0.7988071523335980, -0.2011928476664020,  0.1991111111111110],
                 [-0.7988071523335980, -0.2011928476664020, -0.2011928476664020,  0.1991111111111110],
                 [-0.2011928476664020, -0.7988071523335980, -0.7988071523335980,  0.1991111111111110],
                 [-0.7988071523335980, -0.2011928476664020, -0.7988071523335980,  0.1991111111111110],
                 [-0.7988071523335980, -0.7988071523335980, -0.2011928476664020,  0.1991111111111110]],
                bounds=(-1.0, 1.0), tp_fix=1.0/6.0),

        6 : _QP([[-0.5707942574816960, -0.5707942574816960, -0.5707942574816960, 0.0532303336775570],
                 [-0.2876172275549120, -0.5707942574816960, -0.5707942574816960, 0.0532303336775570],
                 [-0.5707942574816960, -0.2876172275549120, -0.5707942574816960, 0.0532303336775570],
                 [-0.5707942574816960, -0.5707942574816960, -0.2876172275549120, 0.0532303336775570],
                 [-0.9186520829307770, -0.9186520829307770, -0.9186520829307770, 0.0134362814070940],
                 [0.7559562487923320, -0.9186520829307770, -0.9186520829307770, 0.0134362814070940],
                 [-0.9186520829307770, 0.7559562487923320, -0.9186520829307770, 0.0134362814070940],
                 [-0.9186520829307770, -0.9186520829307770, 0.7559562487923320, 0.0134362814070940],
                 [-0.3553242197154490, -0.3553242197154490, -0.3553242197154490, 0.0738095753915400],
                 [-0.9340273408536530, -0.3553242197154490, -0.3553242197154490, 0.0738095753915400],
                 [-0.3553242197154490, -0.9340273408536530, -0.3553242197154490, 0.0738095753915400],
                 [-0.3553242197154490, -0.3553242197154490, -0.9340273408536530, 0.0738095753915400],
                 [-0.8726779962499650, -0.8726779962499650, -0.4606553370833680, 0.0642857142857140],
                 [-0.8726779962499650, -0.4606553370833680, -0.8726779962499650, 0.0642857142857140],
                 [-0.8726779962499650, -0.8726779962499650, 0.2060113295832980, 0.0642857142857140],
                 [-0.8726779962499650, 0.2060113295832980, -0.8726779962499650, 0.0642857142857140],
                 [-0.8726779962499650, -0.4606553370833680, 0.2060113295832980, 0.0642857142857140],
                 [-0.8726779962499650, 0.2060113295832980, -0.4606553370833680, 0.0642857142857140],
                 [-0.4606553370833680, -0.8726779962499650, -0.8726779962499650, 0.0642857142857140],
                 [-0.4606553370833680, -0.8726779962499650, 0.2060113295832980, 0.0642857142857140],
                 [-0.4606553370833680, 0.2060113295832980, -0.8726779962499650, 0.0642857142857140],
                 [0.2060113295832980, -0.8726779962499650, -0.4606553370833680, 0.0642857142857140],
                 [0.2060113295832980, -0.8726779962499650, -0.8726779962499650, 0.0642857142857140],
                 [0.2060113295832980, -0.4606553370833680, -0.8726779962499650, 0.0642857142857140]],
                bounds=(-1.0, 1.0), tp_fix=1.0/6.0),

    },

    '3_8' : {

        2 : _QP([[ 0.0             , nm.sqrt(2.0/3.0),-1/nm.sqrt(3), 2.0],
                 [ 0.0             ,-nm.sqrt(2.0/3.0),-1/nm.sqrt(3), 2.0],
                 [ nm.sqrt(2.0/3.0), 0.0             , 1/nm.sqrt(3), 2.0],
                 [-nm.sqrt(2.0/3.0), 0.0             , 1/nm.sqrt(3), 2.0]], bounds=(-1.0, 1.0)),

        3 : _QP([[-1.0, 0.0, 0.0, 4.0/3.0],
                 [ 1.0, 0.0, 0.0, 4.0/3.0],
                 [ 0.0,-1.0, 0.0, 4.0/3.0],
                 [ 0.0, 1.0, 0.0, 4.0/3.0],
                 [ 0.0, 0.0,-1.0, 4.0/3.0],
                 [ 0.0, 0.0, 1.0, 4.0/3.0]], bounds=(-1.0, 1.0)),

        5 : _QP([[-nm.sqrt(19.0/30.0), 0.0               , 0.0               , 320.0/361.0],
                 [ nm.sqrt(19.0/30.0), 0.0               , 0.0               , 320.0/361.0],
                 [ 0.0               ,-nm.sqrt(19.0/30.0), 0.0               , 320.0/361.0],
                 [ 0.0               , nm.sqrt(19.0/30.0), 0.0               , 320.0/361.0],
                 [ 0.0               , 0.0               ,-nm.sqrt(19.0/30.0), 320.0/361.0],
                 [ 0.0               , 0.0               , nm.sqrt(19.0/30.0), 320.0/361.0],
                 [ nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0), 121.0/361.0],
                 [ nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0), 121.0/361.0],
                 [ nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0), 121.0/361.0],
                 [ nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0), 121.0/361.0],
                 [-nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0), 121.0/361.0],
                 [-nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0), 121.0/361.0],
                 [-nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0), nm.sqrt(19.0/33.0), 121.0/361.0],
                 [-nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0),-nm.sqrt(19.0/33.0), 121.0/361.0]], bounds=(-1.0, 1.0)),

    },
}
del _QP
