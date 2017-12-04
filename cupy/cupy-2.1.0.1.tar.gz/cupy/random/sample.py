import six

import cupy
from cupy import core
from cupy.creation import basic
from cupy.random import distributions
from cupy.random import generator


def rand(*size, **kwarg):
    """Returns an array of uniform random values over the interval ``[0, 1)``.

    Each element of the array is uniformly distributed on the half-open
    interval ``[0, 1)``. All elements are identically and independently
    distributed (i.i.d.).

    Args:
        size (tuple of ints): The shape of the array.
        dtype: Data type specifier. Only :class:`numpy.float32` and
            :class:`numpy.float64` types are allowed. The default is
            :class:`numpy.float64`.

    Returns:
        cupy.ndarray: A random array.

    .. seealso:: :func:`numpy.random.rand`

    """
    dtype = kwarg.pop('dtype', float)
    if kwarg:
        raise TypeError('rand() got unexpected keyword arguments %s'
                        % ', '.join(kwarg.keys()))
    return random_sample(size=size, dtype=dtype)


def randn(*size, **kwarg):
    """Returns an array of standard normal random values.

    Each element of the array is normally distributed with zero mean and unit
    variance. All elements are identically and independently distributed
    (i.i.d.).

    Args:
        size (tuple of ints): The shape of the array.
        dtype: Data type specifier. Only :class:`numpy.float32` and
            :class:`numpy.float64` types are allowed.
            The default is :class:`numpy.float64`.

    Returns:
        cupy.ndarray: An array of standard normal random values.

    .. seealso:: :func:`numpy.random.randn`

    """
    dtype = kwarg.pop('dtype', float)
    if kwarg:
        raise TypeError('randn() got unexpected keyword arguments %s'
                        % ', '.join(kwarg.keys()))
    return distributions.normal(size=size, dtype=dtype)


def randint(low, high=None, size=None, dtype='l'):
    """Returns a scalar or an array of integer values over ``[low, high)``.

    Each element of returned values are independently sampled from
    uniform distribution over left-close and right-open interval
    ``[low, high)``.

    Args:
        low (int): If ``high`` is not ``None``,
            it is the lower bound of the interval.
            Otherwise, it is the **upper** bound of the interval
            and lower bound of the interval is set to ``0``.
        high (int): Upper bound of the interval.
        size (None or int or tuple of ints): The shape of returned value.
        dtype: Data type specifier.

    Returns:
        int or cupy.ndarray of ints: If size is ``None``,
        it is single integer sampled.
        If size is integer, it is the 1D-array of length ``size`` element.
        Otherwise, it is the array whose shape specified by ``size``.
    """
    if high is None:
        lo = 0
        hi = low
    else:
        lo = low
        hi = high

    if lo >= hi:
        raise ValueError('low >= high')
    if lo < cupy.iinfo(dtype).min:
        raise ValueError(
            'low is out of bounds for {}'.format(cupy.dtype(dtype).name))
    if hi > cupy.iinfo(dtype).max + 1:
        raise ValueError(
            'high is out of bounds for {}'.format(cupy.dtype(dtype).name))

    diff = hi - lo - 1
    if diff > cupy.iinfo(cupy.int32).max - cupy.iinfo(cupy.int32).min + 1:
        raise NotImplementedError(
            'Sampling from a range whose extent is larger than int32 range is '
            'currently not supported')
    rs = generator.get_random_state()
    x = rs.interval(diff, size).astype(dtype, copy=False)
    cupy.add(x, lo, out=x)
    return x


def random_integers(low, high=None, size=None):
    """Return a scalar or an array of integer values over ``[low, high]``

    Each element of returned values are independently sampled from
    uniform distribution over closed interval ``[low, high]``.

    Args:
        low (int): If ``high`` is not ``None``,
            it is the lower bound of the interval.
            Otherwise, it is the **upper** bound of the interval
            and the lower bound is set to ``1``.
        high (int): Upper bound of the interval.
        size (None or int or tuple of ints): The shape of returned value.

    Returns:
        int or cupy.ndarray of ints: If size is ``None``,
        it is single integer sampled.
        If size is integer, it is the 1D-array of length ``size`` element.
        Otherwise, it is the array whose shape specified by ``size``.
    """
    if high is None:
        high = low
        low = 1
    return randint(low, high + 1, size)


def random_sample(size=None, dtype=float):
    """Returns an array of random values over the interval ``[0, 1)``.

    This is a variant of :func:`cupy.random.rand`.

    Args:
        size (int or tuple of ints): The shape of the array.
        dtype: Data type specifier. Only :class:`numpy.float32` and
            :class:`numpy.float64` types are allowed.

    Returns:
        cupy.ndarray: An array of uniformly distributed random values.

    .. seealso:: :func:`numpy.random.random_sample`

    """
    rs = generator.get_random_state()
    return rs.random_sample(size=size, dtype=dtype)


def choice(a, size=None, replace=True, p=None):
    """Returns an array of random values from a given 1-D array.

    Each element of the returned array is independently sampled
    from ``a`` according to ``p`` or uniformly.

    .. note::

       Currently ``p`` is not supported when ``replace=False``.

    Args:
        a (1-D array-like or int):
            If an array-like,
            a random sample is generated from its elements.
            If an int, the random sample is generated as if ``a`` was
            ``cupy.arange(n)``
        size (int or tuple of ints): The shape of the array.
        replace (boolean): Whether the sample is with or without replacement.
        p (1-D array-like):
            The probabilities associated with each entry in ``a``.
            If not given the sample assumes a uniform distribution over all
            entries in ``a``.

    Returns:
        cupy.ndarray: An array of ``a`` values distributed according to
                      ``p`` or uniformly.

    .. seealso:: :func:`numpy.random.choice`

    """
    rs = generator.get_random_state()
    return rs.choice(a, size, replace, p)


def multinomial(n, pvals, size=None):
    """Returns an array from multinomial distribution.

    Args:
        n (int): Number of trials.
        pvals (cupy.ndarray): Probabilities of each of the ``p`` different
            outcomes. The sum of these values must be 1.
        size (int or tuple of ints or None): Shape of a sample in each trial.
            For example when ``size`` is ``(a, b)``, shape of returned value is
            ``(a, b, p)`` where ``p`` is ``len(pvals)``.
            If ``size`` is ``None``, it is treated as ``()``. So, shape of
            returned value is ``(p,)``.

    Returns:
        cupy.ndarray: An array drawn from multinomial distribution.

    .. note::
       It does not support ``sum(pvals) < 1`` case.

    .. seealso:: :func:`numpy.random.multinomial`
    """

    if size is None:
        m = 1
        size = ()
    elif isinstance(size, six.integer_types):
        m = size
        size = (size,)
    else:
        size = tuple(size)
        m = 1
        for x in size:
            m *= x

    p = len(pvals)
    shape = size + (p,)
    # atomicAdd only supports int32
    ys = basic.zeros(shape, 'i')
    if ys.size > 0:
        xs = choice(p, p=pvals, size=n * m)
        core.ElementwiseKernel(
            'int64 x, int32 p, int32 n', 'raw int32 ys',
            'atomicAdd(&ys[i / n * p + x], 1)',
            'cupy_random_multinomial')(xs, p, n, ys)
    return ys.astype('l')
