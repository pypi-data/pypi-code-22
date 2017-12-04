import numpy as np

from collections import deque

from . import arc
from . import entities

from ..nsphere import fit_nsphere
from ..util import unitize, diagonal_dot
from ..constants import log
from ..constants import tol_path as tol


def fit_circle_check(points, scale, prior=None, final=False, verbose=False):
    '''
    Fit a circle, and reject the fit if:
    * the radius is larger than tol.radius_min*scale or tol.radius_max*scale
    * any segment spans more than tol.seg_angle
    * any segment is longer than tol.seg_frac*scale
    * the fit deviates by more than tol.radius_frac*radius
    * the segments on the ends deviate from tangent by more than tol.tangent

    Parameters
    ---------
    points:  (n, d) set of points which represent a path
    prior:   (center, radius) tuple for best guess, or None if unknown
    scale:   float, what is the overall scale of the set of points
    verbose: boolean, if True output log.debug messages for the reasons
             for fit rejection. Potentially generates hundreds of thousands of
             messages so only suggested in manual debugging.

    Returns
    ---------
    if fit is acceptable:
        (center, radius) tuple
    else:
        None
    '''
    # an arc needs at least three points
    if len(points) < 3:
        return None

    # do a least squares fit on the points
    C, R, r_deviation = fit_nsphere(points, prior=prior)

    # check to make sure radius is between min and max allowed
    if not tol.radius_min < (R / scale) < tol.radius_max:
        if verbose:
            log.debug('circle fit error: R %f', R / scale)
        return None

    # check point radius error
    r_error = r_deviation / R
    if r_error > tol.radius_frac:
        if verbose:
            log.debug('circle fit error: fit %s', str(r_error))
        return None

    vectors = np.diff(points, axis=0)
    segment = np.linalg.norm(vectors, axis=1)

    # approximate angle in radians, segments are linear length
    # not arc length but this is close and avoids a cosine
    angle = segment / R

    if (angle > tol.seg_angle).any():
        if verbose:
            log.debug('circle fit error: angle %s', str(angle))
        return None

    if final and (angle > tol.seg_angle_min).sum() < 3:
        log.debug('final: angle %s', str(angle))
        return None

    # check segment length as a fraction of drawing scale
    scaled = segment / scale

    if (scaled > tol.seg_frac).any():
        if verbose:
            log.debug('circle fit error: segment %s', str(scaled))
        return None

    # check to make sure the line segments on the ends are actually
    # tangent with the candidate circle fit
    mid_pt = points[[0, -2]] + (vectors[[0, -1]] * .5)
    radial = unitize(mid_pt - C)
    ends = unitize(vectors[[0, -1]])
    tangent = np.abs(np.arccos(diagonal_dot(radial, ends)))
    tangent = np.abs(tangent - np.pi / 2).max()
    if tangent > tol.tangent:
        if verbose:
            log.debug('circle fit error: tangent %f',
                      np.degrees(tangent))
        return None

    return (C, R)


def is_circle(points, scale, verbose=False):
    '''
    Given a set of points, quickly determine if they represent
    a circle or not.
    '''

    # make sure input is a numpy array
    points = np.asanyarray(points)
    scale = float(scale)

    # can only be a circle if the first and last point are the
    # same (AKA is a closed path)
    if np.linalg.norm(points[0] - points[-1]) > tol.merge:
        return None

    box = points.ptp(axis=0)
    # the bounding box size of the points
    # check aspect ratio as an early exit if the path is not a circle
    aspect = np.divide(*box)
    if np.abs(aspect - 1.0) > tol.aspect_frac:
        return None

    # fit a circle with tolerance checks
    CR = fit_circle_check(points, scale=scale)
    if CR is None:
        return None

    # return the circle as three control points
    control = arc.angles_to_threepoint([0, np.pi * .5], *CR)
    return control


def merge_colinear(points, scale=None):
    '''
    Given a set of points representing a path in space,
    merge points which are colinear.

    Parameters
    ----------
    points: (n, d) set of points (where d is dimension)
    scale:  float, scale of drawing

    Returns
    ----------
    merged: (j, d) set of points with colinear and duplicate
             points merged, where (j < n)
    '''
    points = np.array(points)
    if scale is None:
        scale = np.ptp(points, axis=0).max()

    # the vector from one point to the next
    direction = points[1:] - points[:-1]
    # the length of the direction vector
    direction_norm = np.linalg.norm(direction, axis=1)
    # make sure points don't have zero length
    direction_ok = direction_norm > tol.merge

    # remove duplicate points
    points = np.vstack((points[0], points[1:][direction_ok]))
    direction = direction[direction_ok]
    direction_norm = direction_norm[direction_ok]

    # create a vector between every other point, then turn it perpendicular
    # if we have points A B C D
    # and direction vectors A-B, B-C, etc
    # these will be perpendicular to the vectors A-C, B-D, etc
    perpendicular = (points[2:] - points[:-2]).T[::-1].T
    perpendicular /= np.linalg.norm(perpendicular, axis=1).reshape((-1, 1))

    # find the projection of each direction vector
    # onto the perpendicular vector
    projection = np.abs(diagonal_dot(perpendicular, direction[:-1]))

    projection_ratio = np.max((projection / direction_norm[1:],
                               projection / direction_norm[:-1]), axis=0)

    mask = np.ones(len(points), dtype=np.bool)
    # since we took diff, we need to offset by one
    mask[1:-1][projection_ratio < 1e-4 * scale] = False

    merged = points[mask]
    return merged


def resample_spline(points, smooth=.001, count=None, degree=3):
    '''
    Resample a path in space, smoothing along a b-spline.
    
    Parameters
    -----------
    points: (n, dimension) float, points in space
    smooth: float, smoothing amount
    count:  number of samples in output
    degree: int, degree of spline polynomial

    Returns
    ---------
    resampled: (count, dimension) float, points in space
    '''
    from scipy.interpolate import splprep, splev
    if count is None:
        count = len(points)
    points = np.asanyarray(points)
    closed = np.linalg.norm(points[0] - points[-1]) < tol.merge

    tpl = splprep(points.T, s=smooth, k=degree)[0]
    i = np.linspace(0.0, 1.0, count)
    resampled = np.column_stack(splev(i, tpl))

    if closed:
        shared = resampled[[0, -1]].mean(axis=0)
        resampled[0] = shared
        resampled[-1] = shared

    return resampled


def points_to_spline_entity(points, smooth=.0005, count=None):
    '''
    Create a spline entity from a curve in space

    Parameters
    -----------
    points: (n, dimension) float, points in space
    smooth: float, smoothing amount
    count:  int, number of samples in result

    Returns
    ---------
    entity: entities.BSpline object with points indexed at zero
    control: (m, dimension) float, new vertices for entity
    '''
    
    from scipy.interpolate import splprep
    if count is None:
        count = len(points)
    points = np.asanyarray(points)
    closed = np.linalg.norm(points[0] - points[-1]) < tol.merge

    knots, control, degree = splprep(points.T, s=smooth)[0]
    control = np.transpose(control)
    index = np.arange(len(control))

    if closed:
        control[0] = control[[0, -1]].mean(axis=0)
        control = control[:-1]
        index[-1] = index[0]

    entity = entities.BSpline(points=index,
                              knots=knots,
                              closed=closed)

    return entity, control


def three_point(indices):
    '''
    Given a long list of ordered indices,
    return the first, middle and last.

    Parameters
    -----------
    indices: (n,) array

    Returns
    ----------
    three: (3,) array
    '''
    three = [indices[0],
             indices[int(len(indices) / 2)],
             indices[-1]]
    return np.array(three)


def simplify_basic(drawing):
    '''
    Merge colinear segments and fit circles.

    Parameters
    -----------
    drawing: Path2D object

    Returns
    -----------
    simplified: Path2D with circles.
    '''

    if any([i.__class__.__name__ != 'Line' for i in drawing.entities]):
        log.debug('Path contains non- linear entities, skipping')
        return

    vertices_new = deque()
    entities_new = deque()

    for polygon in drawing.polygons_closed:
        # clean up things like self intersections
        buffered = polygon.buffer(0.0)
        # get the exterior as an (n,2) array
        points = merge_colinear(np.array(buffered.exterior.coords),
                                scale=drawing.scale)
        # check to see if the closed entity represents a circle
        circle = is_circle(points, 
                           scale=drawing.scale)

        
        if circle is not None:
            entities_new.append(
                entities.Arc(points=np.arange(3) +
                             len(vertices_new),
                             closed=True))
            vertices_new.extend(circle)
        else:
            line = np.arange(len(points)) + len(vertices_new)
            entities_new.append(entities.Line(points=line))
            vertices_new.extend(points)

    simplified = type(drawing)(entities=entities_new,
                               vertices=vertices_new)

    return simplified

