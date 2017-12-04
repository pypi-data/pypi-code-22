"""
Plans that might be useful at the APS using BlueSky

.. autosummary::
   
   ~nscan
   ~TuneAxis

"""

# Copyright (c) 2017-, UChicago Argonne, LLC.  See LICENSE file.

from collections import OrderedDict
import logging
import numpy as np 
from bluesky import preprocessors as bpp
from bluesky import plan_stubs as bps
from bluesky import plans as bp
from bluesky.callbacks.fitting import PeakStats
import datetime


logger = logging.getLogger(__name__).addHandler(logging.NullHandler())


def nscan(detectors, *motor_sets, num=11, per_step=None, md=None):
    """
    Scan over ``n`` variables moved together, each in equally spaced steps.

    PARAMETERS

    detectors : list
        list of 'readable' objects
    motor_sets : list
        sequence of one or more groups of: motor, start, finish
    motor : object
        any 'settable' object (motor, temp controller, etc.)
    start : float
        starting position of motor
    finish : float
        ending position of motor
    num : int
        number of steps (default = 11)
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step)
        Expected signature: ``f(detectors, step_cache, pos_cache)``
    md : dict, optional
        metadata
    """
    def take_n_at_a_time(args, n=2):
        yield from zip(*[iter(args)]*n)
        
    if len(motor_sets) < 3:
        raise ValueError("must provide at least one movable")
    if len(motor_sets) % 3 > 0:
        raise ValueError("must provide sets of movable, start, finish")

    motors = OrderedDict()
    for m, s, f in take_n_at_a_time(motor_sets, n=3):
        if not isinstance(s, (int, float)):
            msg = "start={} ({}): is not a number".format(s, type(s))
            raise ValueError(msg)
        if not isinstance(f, (int, float)):
            msg = "finish={} ({}): is not a number".format(f, type(f))
            raise ValueError(msg)
        motors[m.name] = dict(motor=m, start=s, finish=f, 
                              steps=np.linspace(start=s, stop=f, num=num))

    _md = {'detectors': [det.name for det in detectors],
           'motors': [m for m in motors.keys()],
           'num_points': num,
           'num_intervals': num - 1,
           'plan_args': {'detectors': list(map(repr, detectors)), 
                         'num': num,
                         'motors': repr(motor_sets),
                         'per_step': repr(per_step)},
           'plan_name': 'nscan',
           'plan_pattern': 'linspace',
           'hints': {},
           'iso8601': datetime.datetime.now(),
           }
    _md.update(md or {})

    try:
        m = list(motors.keys())[0]
        dimensions = [(motors[m]["motor"].hints['fields'], 'primary')]
    except (AttributeError, KeyError):
        pass
    else:
        _md['hints'].setdefault('dimensions', dimensions)

    if per_step is None:
        per_step = bps.one_nd_step

    @bpp.stage_decorator(list(detectors) 
                         + [m["motor"] for m in motors.values()])
    @bpp.run_decorator(md=_md)
    def inner_scan():
        for step in range(num):
            step_cache, pos_cache = {}, {}
            for m in motors.values():
                next_pos = m["steps"][step]
                m = m["motor"]
                pos_cache[m] = m.read()[m.name]["value"]
                step_cache[m] = next_pos
            yield from per_step(detectors, step_cache, pos_cache)

    return (yield from inner_scan())


# def sscan(*args, md=None, **kw):        # TODO: planned
#     """
#     gather data form the sscan record and emit documents
#     
#     Should this operate a complete scan using the sscan record?
#     """
#     raise NotImplemented("this is only planned")


class TuneAxis(object):
    """
    tune an axis with a signal
    
    This class provides a tuning object so that a Device or other entity
    may gain its own tuning process, keeping track of the particulars
    needed to tune this device again.  For example, one could add
    a tuner to a motor stage::
    
        motor = EpicsMotor("xxx:motor", "motor")
        motor.tuner = TuneAxis([det], motor)
    
    Then the ``motor`` could be tuned individually::
    
        RE(motor.tuner.tune(md={"activity": "tuning"}))
    
    or the :meth:`tune()` could be part of a plan with other steps.
    
    Example::
    
        tuner = TuneAxis([det], axis)
        live_table = LiveTable(["axis", "det"])
        RE(tuner.multi_pass_tune(width=2, num=9), live_table)
        RE(tuner.tune(width=0.05, num=9), live_table)

    .. autosummary::
       
       ~tune
       ~multi_pass_tune
       ~peak_detected

    """
    
    def __init__(self, signals, axis, signal_name=None):
        self.signals = signals
        self.signal_name = signal_name or signals[0].name
        self.axis = axis
        self.stats = {}
        self.tune_ok = False
        self.peaks = None
        self.center = None
        self.stats = []
        
        # defaults
        self.width = 1
        self.num = 10
        self.step_factor = 4
        self.pass_max = 6
        self.snake = True
    
    def tune(self, width=None, num=None, md=None):
        """
        BlueSky plan to execute one pass through the current scan range
        
        Scan self.axis centered about current position from
        ``-width/2`` to ``+width/2`` with ``num`` steps.
        If a peak was detected (default check is that max >= 4*min), 
        then set ``self.tune_ok = True``.

        PARAMETERS
    
        width : float
            width of the tuning scan in the units of ``self.axis``
            Default value in ``self.width`` (initially 1)
        num : int
            number of steps
            Default value in ``self.num`` (initially 10)
        md : dict, optional
            metadata
        """
        width = width or self.width
        num = num or self.num

        initial_position = self.axis.position
        start = initial_position - width/2
        finish = initial_position + width/2
        self.tune_ok = False

        _md = {'tune_width': width,
               'tune_center_initial': self.axis.position,
               'plan_name': self.__class__.__name__ + '.tune',
               'time_iso8601': str(datetime.datetime.now()),
               }
        _md.update(md or {})
        if "pass_max" not in _md:
            self.stats = []
        self.peaks = PeakStats(x=self.axis.name, y=self.signal_name)
        
        @bpp.subs_decorator(self.peaks)
        def _scan():
            yield from bp.scan(
                self.signals, self.axis, start, finish, num=num, md=_md)
            
            if self.peak_detected():
                self.tune_ok = True
                self.center = self.peaks.cen
            
            if self.center is not None:
                self.axis.move(self.center)
            else:
                self.axis.move(initial_position)
            self.stats.append(self.peaks)
    
        return (yield from _scan())
        
    
    def multi_pass_tune(self, width=None, step_factor=None, 
                        num=None, pass_max=None, snake=None, md=None):
        """
        BlueSky plan for tuning this axis with this signal
        
        Execute multiple passes to refine the centroid determination.
        Each subsequent pass will reduce the width of scan by ``step_factor``.
        If ``snake=True`` then the scan direction will reverse with
        each subsequent pass.

        PARAMETERS
    
        width : float
            width of the tuning scan in the units of ``self.axis``
            Default value in ``self.width`` (initially 1)
        num : int
            number of steps
            Default value in ``self.num`` (initially 10)
        step_factor : float
            This reduces the width of the next tuning scan by the given factor.
            Default value in ``self.step_factor`` (initially 4)
        pass_max : int
            Maximum number of passes to be executed (avoids runaway
            scans when a centroid is not found).
            Default value in ``self.pass_max`` (initially 10)
        snake : bool
            If ``True``, reverse scan direction on next pass.
            Default value in ``self.snake`` (initially True)
        md : dict, optional
            metadata
        """
        width = width or self.width
        num = num or self.num
        step_factor = step_factor or self.step_factor
        snake = snake or self.snake
        pass_max = pass_max or self.pass_max
        
        self.stats = []

        def _scan(width=1, step_factor=10, num=10, snake=True):
            for _pass_number in range(pass_max):
                _md = {'pass': _pass_number+1,
                       'pass_max': pass_max,
                       'plan_name': self.__class__.__name__ + '.multi_pass_tune',
                       }
                _md.update(md or {})
            
                yield from self.tune(width=width, num=num, md=_md)

                if not self.tune_ok:
                    return
                width /= step_factor
                if snake:
                    width *= -1
        
        return (
            yield from _scan(
                width=width, step_factor=step_factor, num=num, snake=snake))
    
    def peak_detected(self):
        """
        returns True if a peak was detected, otherwise False
        
        The default algorithm identifies a peak when the maximum
        value is four times the minimum value.  Change this routine
        by subclassing :class:`TuneAxis` and override :meth:`peak_detected`.
        """
        if self.peaks is None:
            return False
        self.peaks.compute()
        if self.peaks.max is None:
            return False
        
        ymax = self.peaks.max[-1]
        ymin = self.peaks.min[-1]
        return ymax > 4*ymin        # this works for USAXS
