# Copyright (c) 2016-2017 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Autogenerated python message buffer code.
Source: clad/types/robotStatusAndActions.clad
Full command line: ../tools/message-buffers/emitters/Python_emitter.py -C ../robot/clad/src/ -o ../generated/cladPython// clad/types/robotStatusAndActions.clad
"""

from __future__ import absolute_import
from __future__ import print_function

def _modify_path():
  import inspect, os, sys
  search_paths = [
    '../..',
    '../../../../tools/message-buffers/support/python',
  ]
  currentpath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
  for search_path in search_paths:
    search_path = os.path.normpath(os.path.abspath(os.path.realpath(os.path.join(currentpath, search_path))))
    if search_path not in sys.path:
      sys.path.insert(0, search_path)
_modify_path()

import msgbuffers

Anki = msgbuffers.Namespace()
Anki.Cozmo = msgbuffers.Namespace()
Anki.Cozmo.RobotInterface = msgbuffers.Namespace()

from clad.types.imu import Anki as _Anki
Anki.update(_Anki.deep_clone())

from clad.types.proxMessages import Anki as _Anki
Anki.update(_Anki.deep_clone())

class RobotStatusFlag(object):
  "Automatically-generated uint_32 enumeration."
  NoneRobotStatusFlag   = 0
  IS_MOVING             = 0x1
  IS_CARRYING_BLOCK     = 0x2
  IS_PICKING_OR_PLACING = 0x4
  IS_PICKED_UP          = 0x8
  IS_BODY_ACC_MODE      = 0x10
  IS_FALLING            = 0x20
  IS_ANIMATING          = 0x40
  IS_PATHING            = 0x80
  LIFT_IN_POS           = 0x100
  HEAD_IN_POS           = 0x200
  IS_ANIM_BUFFER_FULL   = 0x400
  IS_ANIMATING_IDLE     = 0x800
  IS_ON_CHARGER         = 0x1000
  IS_CHARGING           = 0x2000
  CLIFF_DETECTED        = 0x4000
  ARE_WHEELS_MOVING     = 0x8000
  IS_CHARGER_OOS        = 0x10000

Anki.Cozmo.RobotStatusFlag = RobotStatusFlag
del RobotStatusFlag


class DockAction(object):
  "Automatically-generated uint_8 enumeration."
  DA_PICKUP_LOW      = 0
  DA_PICKUP_HIGH     = 1
  DA_PLACE_HIGH      = 2
  DA_PLACE_LOW       = 3
  DA_PLACE_LOW_BLIND = 4
  DA_ROLL_LOW        = 5
  DA_DEEP_ROLL_LOW   = 6
  DA_POST_DOCK_ROLL  = 7
  DA_FACE_PLANT      = 8
  DA_POP_A_WHEELIE   = 9
  DA_ALIGN           = 10
  DA_ALIGN_SPECIAL   = 11
  DA_RAMP_ASCEND     = 12
  DA_RAMP_DESCEND    = 13
  DA_CROSS_BRIDGE    = 14

Anki.Cozmo.DockAction = DockAction
del DockAction


class CarryState(object):
  "Automatically-generated uint_8 enumeration."
  CARRY_NONE       = 0
  CARRY_1_BLOCK    = 1
  CARRY_2_BLOCK    = 2
  NUM_CARRY_STATES = 3

Anki.Cozmo.CarryState = CarryState
del CarryState


class CarryStateUpdate(object):
  "Generated message-passing message."

  __slots__ = (
    '_state', # Anki.Cozmo.CarryState
  )

  @property
  def state(self):
    "Anki.Cozmo.CarryState state struct property."
    return self._state

  @state.setter
  def state(self, value):
    self._state = msgbuffers.validate_integer(
      'CarryStateUpdate.state', value, 0, 255)

  def __init__(self, state=Anki.Cozmo.CarryState.CARRY_NONE):
    self.state = state

  @classmethod
  def unpack(cls, buffer):
    "Reads a new CarryStateUpdate from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('CarryStateUpdate.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new CarryStateUpdate from the given BinaryReader."
    _state = reader.read('B')
    return cls(_state)

  def pack(self):
    "Writes the current CarryStateUpdate, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current CarryStateUpdate to the given BinaryWriter."
    writer.write(self._state, 'B')

  def __eq__(self, other):
    if type(self) is type(other):
      return self._state == other._state
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._state, 'B'))

  def __str__(self):
    return '{type}(state={state})'.format(
      type=type(self).__name__,
      state=self._state)

  def __repr__(self):
    return '{type}(state={state})'.format(
      type=type(self).__name__,
      state=repr(self._state))

Anki.Cozmo.CarryStateUpdate = CarryStateUpdate
del CarryStateUpdate


class RobotPose(object):
  "Generated message-passing structure."

  __slots__ = (
    '_x',           # float_32
    '_y',           # float_32
    '_z',           # float_32
    '_angle',       # float_32
    '_pitch_angle', # float_32
  )

  @property
  def x(self):
    "float_32 x struct property."
    return self._x

  @x.setter
  def x(self, value):
    self._x = msgbuffers.validate_float(
      'RobotPose.x', value, 'f')

  @property
  def y(self):
    "float_32 y struct property."
    return self._y

  @y.setter
  def y(self, value):
    self._y = msgbuffers.validate_float(
      'RobotPose.y', value, 'f')

  @property
  def z(self):
    "float_32 z struct property."
    return self._z

  @z.setter
  def z(self, value):
    self._z = msgbuffers.validate_float(
      'RobotPose.z', value, 'f')

  @property
  def angle(self):
    "float_32 angle struct property."
    return self._angle

  @angle.setter
  def angle(self, value):
    self._angle = msgbuffers.validate_float(
      'RobotPose.angle', value, 'f')

  @property
  def pitch_angle(self):
    "float_32 pitch_angle struct property."
    return self._pitch_angle

  @pitch_angle.setter
  def pitch_angle(self, value):
    self._pitch_angle = msgbuffers.validate_float(
      'RobotPose.pitch_angle', value, 'f')

  def __init__(self, x=0.0, y=0.0, z=0.0, angle=0.0, pitch_angle=0.0):
    self.x = x
    self.y = y
    self.z = z
    self.angle = angle
    self.pitch_angle = pitch_angle

  @classmethod
  def unpack(cls, buffer):
    "Reads a new RobotPose from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('RobotPose.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new RobotPose from the given BinaryReader."
    _x = reader.read('f')
    _y = reader.read('f')
    _z = reader.read('f')
    _angle = reader.read('f')
    _pitch_angle = reader.read('f')
    return cls(_x, _y, _z, _angle, _pitch_angle)

  def pack(self):
    "Writes the current RobotPose, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current RobotPose to the given BinaryWriter."
    writer.write(self._x, 'f')
    writer.write(self._y, 'f')
    writer.write(self._z, 'f')
    writer.write(self._angle, 'f')
    writer.write(self._pitch_angle, 'f')

  def __eq__(self, other):
    if type(self) is type(other):
      return (self._x == other._x and
        self._y == other._y and
        self._z == other._z and
        self._angle == other._angle and
        self._pitch_angle == other._pitch_angle)
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._x, 'f') +
      msgbuffers.size(self._y, 'f') +
      msgbuffers.size(self._z, 'f') +
      msgbuffers.size(self._angle, 'f') +
      msgbuffers.size(self._pitch_angle, 'f'))

  def __str__(self):
    return '{type}(x={x}, y={y}, z={z}, angle={angle}, pitch_angle={pitch_angle})'.format(
      type=type(self).__name__,
      x=self._x,
      y=self._y,
      z=self._z,
      angle=self._angle,
      pitch_angle=self._pitch_angle)

  def __repr__(self):
    return '{type}(x={x}, y={y}, z={z}, angle={angle}, pitch_angle={pitch_angle})'.format(
      type=type(self).__name__,
      x=repr(self._x),
      y=repr(self._y),
      z=repr(self._z),
      angle=repr(self._angle),
      pitch_angle=repr(self._pitch_angle))

Anki.Cozmo.RobotPose = RobotPose
del RobotPose


class RobotState(object):
  "Generated message-passing structure."

  __slots__ = (
    '_timestamp',              # uint_32
    '_pose_frame_id',          # uint_32
    '_pose_origin_id',         # uint_32
    '_pose',                   # Anki.Cozmo.RobotPose
    '_lwheel_speed_mmps',      # float_32
    '_rwheel_speed_mmps',      # float_32
    '_headAngle',              # float_32
    '_liftAngle',              # float_32
    '_accel',                  # Anki.Cozmo.AccelData
    '_gyro',                   # Anki.Cozmo.GyroData
    '_batteryVoltage',         # float_32
    '_status',                 # uint_32
    '_cliffDataRaw',           # uint_16[4]
    '_backpackTouchSensorRaw', # uint_16
    '_currPathSegment',        # int_8
  )

  @property
  def timestamp(self):
    "uint_32 timestamp struct property."
    return self._timestamp

  @timestamp.setter
  def timestamp(self, value):
    self._timestamp = msgbuffers.validate_integer(
      'RobotState.timestamp', value, 0, 4294967295)

  @property
  def pose_frame_id(self):
    "uint_32 pose_frame_id struct property."
    return self._pose_frame_id

  @pose_frame_id.setter
  def pose_frame_id(self, value):
    self._pose_frame_id = msgbuffers.validate_integer(
      'RobotState.pose_frame_id', value, 0, 4294967295)

  @property
  def pose_origin_id(self):
    "uint_32 pose_origin_id struct property."
    return self._pose_origin_id

  @pose_origin_id.setter
  def pose_origin_id(self, value):
    self._pose_origin_id = msgbuffers.validate_integer(
      'RobotState.pose_origin_id', value, 0, 4294967295)

  @property
  def pose(self):
    "Anki.Cozmo.RobotPose pose struct property."
    return self._pose

  @pose.setter
  def pose(self, value):
    self._pose = msgbuffers.validate_object(
      'RobotState.pose', value, Anki.Cozmo.RobotPose)

  @property
  def lwheel_speed_mmps(self):
    "float_32 lwheel_speed_mmps struct property."
    return self._lwheel_speed_mmps

  @lwheel_speed_mmps.setter
  def lwheel_speed_mmps(self, value):
    self._lwheel_speed_mmps = msgbuffers.validate_float(
      'RobotState.lwheel_speed_mmps', value, 'f')

  @property
  def rwheel_speed_mmps(self):
    "float_32 rwheel_speed_mmps struct property."
    return self._rwheel_speed_mmps

  @rwheel_speed_mmps.setter
  def rwheel_speed_mmps(self, value):
    self._rwheel_speed_mmps = msgbuffers.validate_float(
      'RobotState.rwheel_speed_mmps', value, 'f')

  @property
  def headAngle(self):
    "float_32 headAngle struct property."
    return self._headAngle

  @headAngle.setter
  def headAngle(self, value):
    self._headAngle = msgbuffers.validate_float(
      'RobotState.headAngle', value, 'f')

  @property
  def liftAngle(self):
    "float_32 liftAngle struct property."
    return self._liftAngle

  @liftAngle.setter
  def liftAngle(self, value):
    self._liftAngle = msgbuffers.validate_float(
      'RobotState.liftAngle', value, 'f')

  @property
  def accel(self):
    "Anki.Cozmo.AccelData accel struct property."
    return self._accel

  @accel.setter
  def accel(self, value):
    self._accel = msgbuffers.validate_object(
      'RobotState.accel', value, Anki.Cozmo.AccelData)

  @property
  def gyro(self):
    "Anki.Cozmo.GyroData gyro struct property."
    return self._gyro

  @gyro.setter
  def gyro(self, value):
    self._gyro = msgbuffers.validate_object(
      'RobotState.gyro', value, Anki.Cozmo.GyroData)

  @property
  def batteryVoltage(self):
    "float_32 batteryVoltage struct property."
    return self._batteryVoltage

  @batteryVoltage.setter
  def batteryVoltage(self, value):
    self._batteryVoltage = msgbuffers.validate_float(
      'RobotState.batteryVoltage', value, 'f')

  @property
  def status(self):
    "uint_32 status struct property."
    return self._status

  @status.setter
  def status(self, value):
    self._status = msgbuffers.validate_integer(
      'RobotState.status', value, 0, 4294967295)

  @property
  def cliffDataRaw(self):
    "uint_16[4] cliffDataRaw struct property."
    return self._cliffDataRaw

  @cliffDataRaw.setter
  def cliffDataRaw(self, value):
    self._cliffDataRaw = msgbuffers.validate_farray(
      'RobotState.cliffDataRaw', value, 4,
      lambda name, value_inner: msgbuffers.validate_integer(
        name, value_inner, 0, 65535))

  @property
  def backpackTouchSensorRaw(self):
    "uint_16 backpackTouchSensorRaw struct property."
    return self._backpackTouchSensorRaw

  @backpackTouchSensorRaw.setter
  def backpackTouchSensorRaw(self, value):
    self._backpackTouchSensorRaw = msgbuffers.validate_integer(
      'RobotState.backpackTouchSensorRaw', value, 0, 65535)

  @property
  def currPathSegment(self):
    "int_8 currPathSegment struct property."
    return self._currPathSegment

  @currPathSegment.setter
  def currPathSegment(self, value):
    self._currPathSegment = msgbuffers.validate_integer(
      'RobotState.currPathSegment', value, -128, 127)

  def __init__(self, timestamp=0, pose_frame_id=0, pose_origin_id=0, pose=Anki.Cozmo.RobotPose(), lwheel_speed_mmps=0.0, rwheel_speed_mmps=0.0, headAngle=0.0, liftAngle=0.0, accel=Anki.Cozmo.AccelData(), gyro=Anki.Cozmo.GyroData(), batteryVoltage=0.0, status=0, cliffDataRaw=(0,) * 4, backpackTouchSensorRaw=0, currPathSegment=0):
    self.timestamp = timestamp
    self.pose_frame_id = pose_frame_id
    self.pose_origin_id = pose_origin_id
    self.pose = pose
    self.lwheel_speed_mmps = lwheel_speed_mmps
    self.rwheel_speed_mmps = rwheel_speed_mmps
    self.headAngle = headAngle
    self.liftAngle = liftAngle
    self.accel = accel
    self.gyro = gyro
    self.batteryVoltage = batteryVoltage
    self.status = status
    self.cliffDataRaw = cliffDataRaw
    self.backpackTouchSensorRaw = backpackTouchSensorRaw
    self.currPathSegment = currPathSegment

  @classmethod
  def unpack(cls, buffer):
    "Reads a new RobotState from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('RobotState.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new RobotState from the given BinaryReader."
    _timestamp = reader.read('I')
    _pose_frame_id = reader.read('I')
    _pose_origin_id = reader.read('I')
    _pose = reader.read_object(Anki.Cozmo.RobotPose.unpack_from)
    _lwheel_speed_mmps = reader.read('f')
    _rwheel_speed_mmps = reader.read('f')
    _headAngle = reader.read('f')
    _liftAngle = reader.read('f')
    _accel = reader.read_object(Anki.Cozmo.AccelData.unpack_from)
    _gyro = reader.read_object(Anki.Cozmo.GyroData.unpack_from)
    _batteryVoltage = reader.read('f')
    _status = reader.read('I')
    _cliffDataRaw = reader.read_farray('H', 4)
    _backpackTouchSensorRaw = reader.read('H')
    _currPathSegment = reader.read('b')
    return cls(_timestamp, _pose_frame_id, _pose_origin_id, _pose, _lwheel_speed_mmps, _rwheel_speed_mmps, _headAngle, _liftAngle, _accel, _gyro, _batteryVoltage, _status, _cliffDataRaw, _backpackTouchSensorRaw, _currPathSegment)

  def pack(self):
    "Writes the current RobotState, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current RobotState to the given BinaryWriter."
    writer.write(self._timestamp, 'I')
    writer.write(self._pose_frame_id, 'I')
    writer.write(self._pose_origin_id, 'I')
    writer.write_object(self._pose)
    writer.write(self._lwheel_speed_mmps, 'f')
    writer.write(self._rwheel_speed_mmps, 'f')
    writer.write(self._headAngle, 'f')
    writer.write(self._liftAngle, 'f')
    writer.write_object(self._accel)
    writer.write_object(self._gyro)
    writer.write(self._batteryVoltage, 'f')
    writer.write(self._status, 'I')
    writer.write_farray(self._cliffDataRaw, 'H', 4)
    writer.write(self._backpackTouchSensorRaw, 'H')
    writer.write(self._currPathSegment, 'b')

  def __eq__(self, other):
    if type(self) is type(other):
      return (self._timestamp == other._timestamp and
        self._pose_frame_id == other._pose_frame_id and
        self._pose_origin_id == other._pose_origin_id and
        self._pose == other._pose and
        self._lwheel_speed_mmps == other._lwheel_speed_mmps and
        self._rwheel_speed_mmps == other._rwheel_speed_mmps and
        self._headAngle == other._headAngle and
        self._liftAngle == other._liftAngle and
        self._accel == other._accel and
        self._gyro == other._gyro and
        self._batteryVoltage == other._batteryVoltage and
        self._status == other._status and
        self._cliffDataRaw == other._cliffDataRaw and
        self._backpackTouchSensorRaw == other._backpackTouchSensorRaw and
        self._currPathSegment == other._currPathSegment)
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._timestamp, 'I') +
      msgbuffers.size(self._pose_frame_id, 'I') +
      msgbuffers.size(self._pose_origin_id, 'I') +
      msgbuffers.size_object(self._pose) +
      msgbuffers.size(self._lwheel_speed_mmps, 'f') +
      msgbuffers.size(self._rwheel_speed_mmps, 'f') +
      msgbuffers.size(self._headAngle, 'f') +
      msgbuffers.size(self._liftAngle, 'f') +
      msgbuffers.size_object(self._accel) +
      msgbuffers.size_object(self._gyro) +
      msgbuffers.size(self._batteryVoltage, 'f') +
      msgbuffers.size(self._status, 'I') +
      msgbuffers.size_farray(self._cliffDataRaw, 'H', 4) +
      msgbuffers.size(self._backpackTouchSensorRaw, 'H') +
      msgbuffers.size(self._currPathSegment, 'b'))

  def __str__(self):
    return '{type}(timestamp={timestamp}, pose_frame_id={pose_frame_id}, pose_origin_id={pose_origin_id}, pose={pose}, lwheel_speed_mmps={lwheel_speed_mmps}, rwheel_speed_mmps={rwheel_speed_mmps}, headAngle={headAngle}, liftAngle={liftAngle}, accel={accel}, gyro={gyro}, batteryVoltage={batteryVoltage}, status={status}, cliffDataRaw={cliffDataRaw}, backpackTouchSensorRaw={backpackTouchSensorRaw}, currPathSegment={currPathSegment})'.format(
      type=type(self).__name__,
      timestamp=self._timestamp,
      pose_frame_id=self._pose_frame_id,
      pose_origin_id=self._pose_origin_id,
      pose=self._pose,
      lwheel_speed_mmps=self._lwheel_speed_mmps,
      rwheel_speed_mmps=self._rwheel_speed_mmps,
      headAngle=self._headAngle,
      liftAngle=self._liftAngle,
      accel=self._accel,
      gyro=self._gyro,
      batteryVoltage=self._batteryVoltage,
      status=self._status,
      cliffDataRaw=msgbuffers.shorten_sequence(self._cliffDataRaw),
      backpackTouchSensorRaw=self._backpackTouchSensorRaw,
      currPathSegment=self._currPathSegment)

  def __repr__(self):
    return '{type}(timestamp={timestamp}, pose_frame_id={pose_frame_id}, pose_origin_id={pose_origin_id}, pose={pose}, lwheel_speed_mmps={lwheel_speed_mmps}, rwheel_speed_mmps={rwheel_speed_mmps}, headAngle={headAngle}, liftAngle={liftAngle}, accel={accel}, gyro={gyro}, batteryVoltage={batteryVoltage}, status={status}, cliffDataRaw={cliffDataRaw}, backpackTouchSensorRaw={backpackTouchSensorRaw}, currPathSegment={currPathSegment})'.format(
      type=type(self).__name__,
      timestamp=repr(self._timestamp),
      pose_frame_id=repr(self._pose_frame_id),
      pose_origin_id=repr(self._pose_origin_id),
      pose=repr(self._pose),
      lwheel_speed_mmps=repr(self._lwheel_speed_mmps),
      rwheel_speed_mmps=repr(self._rwheel_speed_mmps),
      headAngle=repr(self._headAngle),
      liftAngle=repr(self._liftAngle),
      accel=repr(self._accel),
      gyro=repr(self._gyro),
      batteryVoltage=repr(self._batteryVoltage),
      status=repr(self._status),
      cliffDataRaw=repr(self._cliffDataRaw),
      backpackTouchSensorRaw=repr(self._backpackTouchSensorRaw),
      currPathSegment=repr(self._currPathSegment))

Anki.Cozmo.RobotState = RobotState
del RobotState


class BodyRadioMode(object):
  "Automatically-generated int_8 enumeration."
  BODY_BLUETOOTH_OPERATING_MODE = 0x0
  BODY_ACCESSORY_OPERATING_MODE = 0x1
  BODY_LOW_POWER_OPERATING_MODE = 0x2
  BODY_FORCE_RECOVERY           = 0x3
  BODY_STARTUP                  = 0x4
  BODY_DTM_OPERATING_MODE       = 0x20
  BODY_OTA_MODE                 = 0x40
  BODY_BATTERY_CHARGE_TEST_MODE = 0x78

Anki.Cozmo.BodyRadioMode = BodyRadioMode
del BodyRadioMode


class SetBodyRadioMode(object):
  "Generated message-passing message."

  __slots__ = (
    '_radioMode',   # Anki.Cozmo.BodyRadioMode
    '_wifiChannel', # uint_8
  )

  @property
  def radioMode(self):
    "Anki.Cozmo.BodyRadioMode radioMode struct property."
    return self._radioMode

  @radioMode.setter
  def radioMode(self, value):
    self._radioMode = msgbuffers.validate_integer(
      'SetBodyRadioMode.radioMode', value, -128, 127)

  @property
  def wifiChannel(self):
    "uint_8 wifiChannel struct property."
    return self._wifiChannel

  @wifiChannel.setter
  def wifiChannel(self, value):
    self._wifiChannel = msgbuffers.validate_integer(
      'SetBodyRadioMode.wifiChannel', value, 0, 255)

  def __init__(self, radioMode=Anki.Cozmo.BodyRadioMode.BODY_BLUETOOTH_OPERATING_MODE, wifiChannel=0):
    self.radioMode = radioMode
    self.wifiChannel = wifiChannel

  @classmethod
  def unpack(cls, buffer):
    "Reads a new SetBodyRadioMode from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('SetBodyRadioMode.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new SetBodyRadioMode from the given BinaryReader."
    _radioMode = reader.read('b')
    _wifiChannel = reader.read('B')
    return cls(_radioMode, _wifiChannel)

  def pack(self):
    "Writes the current SetBodyRadioMode, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current SetBodyRadioMode to the given BinaryWriter."
    writer.write(self._radioMode, 'b')
    writer.write(self._wifiChannel, 'B')

  def __eq__(self, other):
    if type(self) is type(other):
      return (self._radioMode == other._radioMode and
        self._wifiChannel == other._wifiChannel)
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._radioMode, 'b') +
      msgbuffers.size(self._wifiChannel, 'B'))

  def __str__(self):
    return '{type}(radioMode={radioMode}, wifiChannel={wifiChannel})'.format(
      type=type(self).__name__,
      radioMode=self._radioMode,
      wifiChannel=self._wifiChannel)

  def __repr__(self):
    return '{type}(radioMode={radioMode}, wifiChannel={wifiChannel})'.format(
      type=type(self).__name__,
      radioMode=repr(self._radioMode),
      wifiChannel=repr(self._wifiChannel))

Anki.Cozmo.SetBodyRadioMode = SetBodyRadioMode
del SetBodyRadioMode


class PowerState(object):
  "Generated message-passing structure."

  __slots__ = (
    '_VBatFixed',     # int_32
    '_VExtFixed',     # int_32
    '__unused',       # int_32
    '_batteryLevel',  # uint_8
    '_onCharger',     # bool
    '_isCharging',    # bool
    '_operatingMode', # Anki.Cozmo.BodyRadioMode
    '_chargerOOS',    # bool
  )

  @property
  def VBatFixed(self):
    "int_32 VBatFixed struct property."
    return self._VBatFixed

  @VBatFixed.setter
  def VBatFixed(self, value):
    self._VBatFixed = msgbuffers.validate_integer(
      'PowerState.VBatFixed', value, -2147483648, 2147483647)

  @property
  def VExtFixed(self):
    "int_32 VExtFixed struct property."
    return self._VExtFixed

  @VExtFixed.setter
  def VExtFixed(self, value):
    self._VExtFixed = msgbuffers.validate_integer(
      'PowerState.VExtFixed', value, -2147483648, 2147483647)

  @property
  def _unused(self):
    "int_32 _unused struct property."
    return self.__unused

  @_unused.setter
  def _unused(self, value):
    self.__unused = msgbuffers.validate_integer(
      'PowerState._unused', value, -2147483648, 2147483647)

  @property
  def batteryLevel(self):
    "uint_8 batteryLevel struct property."
    return self._batteryLevel

  @batteryLevel.setter
  def batteryLevel(self, value):
    self._batteryLevel = msgbuffers.validate_integer(
      'PowerState.batteryLevel', value, 0, 255)

  @property
  def onCharger(self):
    "bool onCharger struct property."
    return self._onCharger

  @onCharger.setter
  def onCharger(self, value):
    self._onCharger = msgbuffers.validate_bool(
      'PowerState.onCharger', value)

  @property
  def isCharging(self):
    "bool isCharging struct property."
    return self._isCharging

  @isCharging.setter
  def isCharging(self, value):
    self._isCharging = msgbuffers.validate_bool(
      'PowerState.isCharging', value)

  @property
  def operatingMode(self):
    "Anki.Cozmo.BodyRadioMode operatingMode struct property."
    return self._operatingMode

  @operatingMode.setter
  def operatingMode(self, value):
    self._operatingMode = msgbuffers.validate_integer(
      'PowerState.operatingMode', value, -128, 127)

  @property
  def chargerOOS(self):
    "bool chargerOOS struct property."
    return self._chargerOOS

  @chargerOOS.setter
  def chargerOOS(self, value):
    self._chargerOOS = msgbuffers.validate_bool(
      'PowerState.chargerOOS', value)

  def __init__(self, VBatFixed=0, VExtFixed=0, _unused=0, batteryLevel=0, onCharger=False, isCharging=False, operatingMode=Anki.Cozmo.BodyRadioMode.BODY_BLUETOOTH_OPERATING_MODE, chargerOOS=False):
    self.VBatFixed = VBatFixed
    self.VExtFixed = VExtFixed
    self._unused = _unused
    self.batteryLevel = batteryLevel
    self.onCharger = onCharger
    self.isCharging = isCharging
    self.operatingMode = operatingMode
    self.chargerOOS = chargerOOS

  @classmethod
  def unpack(cls, buffer):
    "Reads a new PowerState from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('PowerState.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new PowerState from the given BinaryReader."
    _VBatFixed = reader.read('i')
    _VExtFixed = reader.read('i')
    __unused = reader.read('i')
    _batteryLevel = reader.read('B')
    _onCharger = bool(reader.read('b'))
    _isCharging = bool(reader.read('b'))
    _operatingMode = reader.read('b')
    _chargerOOS = bool(reader.read('b'))
    return cls(_VBatFixed, _VExtFixed, __unused, _batteryLevel, _onCharger, _isCharging, _operatingMode, _chargerOOS)

  def pack(self):
    "Writes the current PowerState, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current PowerState to the given BinaryWriter."
    writer.write(self._VBatFixed, 'i')
    writer.write(self._VExtFixed, 'i')
    writer.write(self.__unused, 'i')
    writer.write(self._batteryLevel, 'B')
    writer.write(int(self._onCharger), 'b')
    writer.write(int(self._isCharging), 'b')
    writer.write(self._operatingMode, 'b')
    writer.write(int(self._chargerOOS), 'b')

  def __eq__(self, other):
    if type(self) is type(other):
      return (self._VBatFixed == other._VBatFixed and
        self._VExtFixed == other._VExtFixed and
        self.__unused == other.__unused and
        self._batteryLevel == other._batteryLevel and
        self._onCharger == other._onCharger and
        self._isCharging == other._isCharging and
        self._operatingMode == other._operatingMode and
        self._chargerOOS == other._chargerOOS)
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._VBatFixed, 'i') +
      msgbuffers.size(self._VExtFixed, 'i') +
      msgbuffers.size(self.__unused, 'i') +
      msgbuffers.size(self._batteryLevel, 'B') +
      msgbuffers.size(self._onCharger, 'b') +
      msgbuffers.size(self._isCharging, 'b') +
      msgbuffers.size(self._operatingMode, 'b') +
      msgbuffers.size(self._chargerOOS, 'b'))

  def __str__(self):
    return '{type}(VBatFixed={VBatFixed}, VExtFixed={VExtFixed}, _unused={_unused}, batteryLevel={batteryLevel}, onCharger={onCharger}, isCharging={isCharging}, operatingMode={operatingMode}, chargerOOS={chargerOOS})'.format(
      type=type(self).__name__,
      VBatFixed=self._VBatFixed,
      VExtFixed=self._VExtFixed,
      _unused=self.__unused,
      batteryLevel=self._batteryLevel,
      onCharger=self._onCharger,
      isCharging=self._isCharging,
      operatingMode=self._operatingMode,
      chargerOOS=self._chargerOOS)

  def __repr__(self):
    return '{type}(VBatFixed={VBatFixed}, VExtFixed={VExtFixed}, _unused={_unused}, batteryLevel={batteryLevel}, onCharger={onCharger}, isCharging={isCharging}, operatingMode={operatingMode}, chargerOOS={chargerOOS})'.format(
      type=type(self).__name__,
      VBatFixed=repr(self._VBatFixed),
      VExtFixed=repr(self._VExtFixed),
      _unused=repr(self.__unused),
      batteryLevel=repr(self._batteryLevel),
      onCharger=repr(self._onCharger),
      isCharging=repr(self._isCharging),
      operatingMode=repr(self._operatingMode),
      chargerOOS=repr(self._chargerOOS))

Anki.Cozmo.PowerState = PowerState
del PowerState


class BodyColor(object):
  "Automatically-generated int_8 enumeration."
  UNKNOWN   = -1
  WHITE_v10 = 0
  RESERVED  = 1
  WHITE_v15 = 2
  CE_LM_v15 = 3
  COUNT     = 4

Anki.Cozmo.BodyColor = BodyColor
del BodyColor


class AnimationState(object):
  "Generated message-passing message."

  __slots__ = (
    '_timestamp',            # uint_32
    '_numAnimBytesPlayed',   # int_32
    '_numAudioFramesPlayed', # int_32
    '_enabledAnimTracks',    # uint_8
    '_tag',                  # uint_8
  )

  @property
  def timestamp(self):
    "uint_32 timestamp struct property."
    return self._timestamp

  @timestamp.setter
  def timestamp(self, value):
    self._timestamp = msgbuffers.validate_integer(
      'AnimationState.timestamp', value, 0, 4294967295)

  @property
  def numAnimBytesPlayed(self):
    "int_32 numAnimBytesPlayed struct property."
    return self._numAnimBytesPlayed

  @numAnimBytesPlayed.setter
  def numAnimBytesPlayed(self, value):
    self._numAnimBytesPlayed = msgbuffers.validate_integer(
      'AnimationState.numAnimBytesPlayed', value, -2147483648, 2147483647)

  @property
  def numAudioFramesPlayed(self):
    "int_32 numAudioFramesPlayed struct property."
    return self._numAudioFramesPlayed

  @numAudioFramesPlayed.setter
  def numAudioFramesPlayed(self, value):
    self._numAudioFramesPlayed = msgbuffers.validate_integer(
      'AnimationState.numAudioFramesPlayed', value, -2147483648, 2147483647)

  @property
  def enabledAnimTracks(self):
    "uint_8 enabledAnimTracks struct property."
    return self._enabledAnimTracks

  @enabledAnimTracks.setter
  def enabledAnimTracks(self, value):
    self._enabledAnimTracks = msgbuffers.validate_integer(
      'AnimationState.enabledAnimTracks', value, 0, 255)

  @property
  def tag(self):
    "uint_8 tag struct property."
    return self._tag

  @tag.setter
  def tag(self, value):
    self._tag = msgbuffers.validate_integer(
      'AnimationState.tag', value, 0, 255)

  def __init__(self, timestamp=0, numAnimBytesPlayed=0, numAudioFramesPlayed=0, enabledAnimTracks=0, tag=0):
    self.timestamp = timestamp
    self.numAnimBytesPlayed = numAnimBytesPlayed
    self.numAudioFramesPlayed = numAudioFramesPlayed
    self.enabledAnimTracks = enabledAnimTracks
    self.tag = tag

  @classmethod
  def unpack(cls, buffer):
    "Reads a new AnimationState from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('AnimationState.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new AnimationState from the given BinaryReader."
    _timestamp = reader.read('I')
    _numAnimBytesPlayed = reader.read('i')
    _numAudioFramesPlayed = reader.read('i')
    _enabledAnimTracks = reader.read('B')
    _tag = reader.read('B')
    return cls(_timestamp, _numAnimBytesPlayed, _numAudioFramesPlayed, _enabledAnimTracks, _tag)

  def pack(self):
    "Writes the current AnimationState, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current AnimationState to the given BinaryWriter."
    writer.write(self._timestamp, 'I')
    writer.write(self._numAnimBytesPlayed, 'i')
    writer.write(self._numAudioFramesPlayed, 'i')
    writer.write(self._enabledAnimTracks, 'B')
    writer.write(self._tag, 'B')

  def __eq__(self, other):
    if type(self) is type(other):
      return (self._timestamp == other._timestamp and
        self._numAnimBytesPlayed == other._numAnimBytesPlayed and
        self._numAudioFramesPlayed == other._numAudioFramesPlayed and
        self._enabledAnimTracks == other._enabledAnimTracks and
        self._tag == other._tag)
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._timestamp, 'I') +
      msgbuffers.size(self._numAnimBytesPlayed, 'i') +
      msgbuffers.size(self._numAudioFramesPlayed, 'i') +
      msgbuffers.size(self._enabledAnimTracks, 'B') +
      msgbuffers.size(self._tag, 'B'))

  def __str__(self):
    return '{type}(timestamp={timestamp}, numAnimBytesPlayed={numAnimBytesPlayed}, numAudioFramesPlayed={numAudioFramesPlayed}, enabledAnimTracks={enabledAnimTracks}, tag={tag})'.format(
      type=type(self).__name__,
      timestamp=self._timestamp,
      numAnimBytesPlayed=self._numAnimBytesPlayed,
      numAudioFramesPlayed=self._numAudioFramesPlayed,
      enabledAnimTracks=self._enabledAnimTracks,
      tag=self._tag)

  def __repr__(self):
    return '{type}(timestamp={timestamp}, numAnimBytesPlayed={numAnimBytesPlayed}, numAudioFramesPlayed={numAudioFramesPlayed}, enabledAnimTracks={enabledAnimTracks}, tag={tag})'.format(
      type=type(self).__name__,
      timestamp=repr(self._timestamp),
      numAnimBytesPlayed=repr(self._numAnimBytesPlayed),
      numAudioFramesPlayed=repr(self._numAudioFramesPlayed),
      enabledAnimTracks=repr(self._enabledAnimTracks),
      tag=repr(self._tag))

Anki.Cozmo.RobotInterface.AnimationState = AnimationState
del AnimationState


