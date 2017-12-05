# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: matrix_io/malos/v1/driver.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from matrix_io.proto.malos.v1 import comm_pb2 as matrix__io_dot_malos_dot_v1_dot_comm__pb2
from matrix_io.proto.malos.v1 import io_pb2 as matrix__io_dot_malos_dot_v1_dot_io__pb2
from matrix_io.proto.malos.v1 import maloseye_pb2 as matrix__io_dot_malos_dot_v1_dot_maloseye__pb2
from matrix_io.proto.malos.v1 import sense_pb2 as matrix__io_dot_malos_dot_v1_dot_sense__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='matrix_io/malos/v1/driver.proto',
  package='matrix_io.malos.v1.driver',
  syntax='proto3',
  serialized_pb=_b('\n\x1fmatrix_io/malos/v1/driver.proto\x12\x19matrix_io.malos.v1.driver\x1a\x1dmatrix_io/malos/v1/comm.proto\x1a\x1bmatrix_io/malos/v1/io.proto\x1a!matrix_io/malos/v1/maloseye.proto\x1a\x1ematrix_io/malos/v1/sense.proto\"\xfd\x04\n\x0c\x44riverConfig\x12\x1d\n\x15\x64\x65lay_between_updates\x18\x01 \x01(\x02\x12\x1f\n\x17timeout_after_last_ping\x18\x02 \x01(\x02\x12\x33\n\x05image\x18\x03 \x01(\x0b\x32$.matrix_io.malos.v1.io.EverloopImage\x12\x45\n\x10malos_eye_config\x18\x04 \x01(\x0b\x32+.matrix_io.malos.v1.maloseye.MalosEyeConfig\x12:\n\x0ezigbee_message\x18\x05 \x01(\x0b\x32\".matrix_io.malos.v1.comm.ZigBeeMsg\x12\x31\n\x04lirc\x18\x06 \x01(\x0b\x32#.matrix_io.malos.v1.comm.LircParams\x12\x31\n\x05servo\x18\x07 \x01(\x0b\x32\".matrix_io.malos.v1.io.ServoParams\x12/\n\x04gpio\x18\x08 \x01(\x0b\x32!.matrix_io.malos.v1.io.GpioParams\x12:\n\x08humidity\x18\t \x01(\x0b\x32(.matrix_io.malos.v1.sense.HumidityParams\x12\x37\n\x08micarray\x18\n \x01(\x0b\x32%.matrix_io.malos.v1.io.MicArrayParams\x12\x30\n\x05zwave\x18\x0b \x01(\x0b\x32!.matrix_io.malos.v1.comm.ZWaveMsg\x12\x37\n\x08wakeword\x18\x0c \x01(\x0b\x32%.matrix_io.malos.v1.io.WakeWordParams\"\xbc\x01\n\nDriverInfo\x12\x13\n\x0b\x64river_name\x18\x01 \x01(\t\x12\x11\n\tbase_port\x18\x02 \x01(\x05\x12\x18\n\x10provides_updates\x18\x03 \x01(\x08\x12\x1d\n\x15\x64\x65lay_between_updates\x18\x04 \x01(\x05\x12\x13\n\x0bneeds_pings\x18\x05 \x01(\x08\x12\x1f\n\x17timeout_after_last_ping\x18\x06 \x01(\x05\x12\x17\n\x0fnotes_for_human\x18\x07 \x01(\t\"F\n\x0fMalosDriverInfo\x12\x33\n\x04info\x18\x01 \x03(\x0b\x32%.matrix_io.malos.v1.driver.DriverInfoBA\n\x15\x63om.matrixio.malos.v1B\x0b\x44riverProtoP\x01\xaa\x02\x18MatrixIO.Malos.Driver.V1b\x06proto3')
  ,
  dependencies=[matrix__io_dot_malos_dot_v1_dot_comm__pb2.DESCRIPTOR,matrix__io_dot_malos_dot_v1_dot_io__pb2.DESCRIPTOR,matrix__io_dot_malos_dot_v1_dot_maloseye__pb2.DESCRIPTOR,matrix__io_dot_malos_dot_v1_dot_sense__pb2.DESCRIPTOR,])




_DRIVERCONFIG = _descriptor.Descriptor(
  name='DriverConfig',
  full_name='matrix_io.malos.v1.driver.DriverConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='delay_between_updates', full_name='matrix_io.malos.v1.driver.DriverConfig.delay_between_updates', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timeout_after_last_ping', full_name='matrix_io.malos.v1.driver.DriverConfig.timeout_after_last_ping', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='image', full_name='matrix_io.malos.v1.driver.DriverConfig.image', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='malos_eye_config', full_name='matrix_io.malos.v1.driver.DriverConfig.malos_eye_config', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zigbee_message', full_name='matrix_io.malos.v1.driver.DriverConfig.zigbee_message', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lirc', full_name='matrix_io.malos.v1.driver.DriverConfig.lirc', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='servo', full_name='matrix_io.malos.v1.driver.DriverConfig.servo', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gpio', full_name='matrix_io.malos.v1.driver.DriverConfig.gpio', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='humidity', full_name='matrix_io.malos.v1.driver.DriverConfig.humidity', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='micarray', full_name='matrix_io.malos.v1.driver.DriverConfig.micarray', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zwave', full_name='matrix_io.malos.v1.driver.DriverConfig.zwave', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='wakeword', full_name='matrix_io.malos.v1.driver.DriverConfig.wakeword', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=827,
)


_DRIVERINFO = _descriptor.Descriptor(
  name='DriverInfo',
  full_name='matrix_io.malos.v1.driver.DriverInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='driver_name', full_name='matrix_io.malos.v1.driver.DriverInfo.driver_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='base_port', full_name='matrix_io.malos.v1.driver.DriverInfo.base_port', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='provides_updates', full_name='matrix_io.malos.v1.driver.DriverInfo.provides_updates', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='delay_between_updates', full_name='matrix_io.malos.v1.driver.DriverInfo.delay_between_updates', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='needs_pings', full_name='matrix_io.malos.v1.driver.DriverInfo.needs_pings', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timeout_after_last_ping', full_name='matrix_io.malos.v1.driver.DriverInfo.timeout_after_last_ping', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='notes_for_human', full_name='matrix_io.malos.v1.driver.DriverInfo.notes_for_human', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=830,
  serialized_end=1018,
)


_MALOSDRIVERINFO = _descriptor.Descriptor(
  name='MalosDriverInfo',
  full_name='matrix_io.malos.v1.driver.MalosDriverInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='matrix_io.malos.v1.driver.MalosDriverInfo.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1020,
  serialized_end=1090,
)

_DRIVERCONFIG.fields_by_name['image'].message_type = matrix__io_dot_malos_dot_v1_dot_io__pb2._EVERLOOPIMAGE
_DRIVERCONFIG.fields_by_name['malos_eye_config'].message_type = matrix__io_dot_malos_dot_v1_dot_maloseye__pb2._MALOSEYECONFIG
_DRIVERCONFIG.fields_by_name['zigbee_message'].message_type = matrix__io_dot_malos_dot_v1_dot_comm__pb2._ZIGBEEMSG
_DRIVERCONFIG.fields_by_name['lirc'].message_type = matrix__io_dot_malos_dot_v1_dot_comm__pb2._LIRCPARAMS
_DRIVERCONFIG.fields_by_name['servo'].message_type = matrix__io_dot_malos_dot_v1_dot_io__pb2._SERVOPARAMS
_DRIVERCONFIG.fields_by_name['gpio'].message_type = matrix__io_dot_malos_dot_v1_dot_io__pb2._GPIOPARAMS
_DRIVERCONFIG.fields_by_name['humidity'].message_type = matrix__io_dot_malos_dot_v1_dot_sense__pb2._HUMIDITYPARAMS
_DRIVERCONFIG.fields_by_name['micarray'].message_type = matrix__io_dot_malos_dot_v1_dot_io__pb2._MICARRAYPARAMS
_DRIVERCONFIG.fields_by_name['zwave'].message_type = matrix__io_dot_malos_dot_v1_dot_comm__pb2._ZWAVEMSG
_DRIVERCONFIG.fields_by_name['wakeword'].message_type = matrix__io_dot_malos_dot_v1_dot_io__pb2._WAKEWORDPARAMS
_MALOSDRIVERINFO.fields_by_name['info'].message_type = _DRIVERINFO
DESCRIPTOR.message_types_by_name['DriverConfig'] = _DRIVERCONFIG
DESCRIPTOR.message_types_by_name['DriverInfo'] = _DRIVERINFO
DESCRIPTOR.message_types_by_name['MalosDriverInfo'] = _MALOSDRIVERINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DriverConfig = _reflection.GeneratedProtocolMessageType('DriverConfig', (_message.Message,), dict(
  DESCRIPTOR = _DRIVERCONFIG,
  __module__ = 'matrix_io.malos.v1.driver_pb2'
  # @@protoc_insertion_point(class_scope:matrix_io.malos.v1.driver.DriverConfig)
  ))
_sym_db.RegisterMessage(DriverConfig)

DriverInfo = _reflection.GeneratedProtocolMessageType('DriverInfo', (_message.Message,), dict(
  DESCRIPTOR = _DRIVERINFO,
  __module__ = 'matrix_io.malos.v1.driver_pb2'
  # @@protoc_insertion_point(class_scope:matrix_io.malos.v1.driver.DriverInfo)
  ))
_sym_db.RegisterMessage(DriverInfo)

MalosDriverInfo = _reflection.GeneratedProtocolMessageType('MalosDriverInfo', (_message.Message,), dict(
  DESCRIPTOR = _MALOSDRIVERINFO,
  __module__ = 'matrix_io.malos.v1.driver_pb2'
  # @@protoc_insertion_point(class_scope:matrix_io.malos.v1.driver.MalosDriverInfo)
  ))
_sym_db.RegisterMessage(MalosDriverInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\025com.matrixio.malos.v1B\013DriverProtoP\001\252\002\030MatrixIO.Malos.Driver.V1'))
try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
