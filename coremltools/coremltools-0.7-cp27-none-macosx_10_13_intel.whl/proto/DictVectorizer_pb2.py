# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: DictVectorizer.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import DataStructures_pb2 as DataStructures__pb2
try:
  FeatureTypes__pb2 = DataStructures__pb2.FeatureTypes__pb2
except AttributeError:
  FeatureTypes__pb2 = DataStructures__pb2.FeatureTypes_pb2

from .DataStructures_pb2 import *

DESCRIPTOR = _descriptor.FileDescriptor(
  name='DictVectorizer.proto',
  package='CoreML.Specification',
  syntax='proto3',
  serialized_pb=_b('\n\x14\x44ictVectorizer.proto\x12\x14\x43oreML.Specification\x1a\x14\x44\x61taStructures.proto\"\x8f\x01\n\x0e\x44ictVectorizer\x12;\n\rstringToIndex\x18\x01 \x01(\x0b\x32\".CoreML.Specification.StringVectorH\x00\x12\x39\n\x0cint64ToIndex\x18\x02 \x01(\x0b\x32!.CoreML.Specification.Int64VectorH\x00\x42\x05\n\x03MapB\x02H\x03P\x00\x62\x06proto3')
  ,
  dependencies=[DataStructures__pb2.DESCRIPTOR,],
  public_dependencies=[DataStructures__pb2.DESCRIPTOR,])




_DICTVECTORIZER = _descriptor.Descriptor(
  name='DictVectorizer',
  full_name='CoreML.Specification.DictVectorizer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stringToIndex', full_name='CoreML.Specification.DictVectorizer.stringToIndex', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='int64ToIndex', full_name='CoreML.Specification.DictVectorizer.int64ToIndex', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='Map', full_name='CoreML.Specification.DictVectorizer.Map',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=69,
  serialized_end=212,
)

_DICTVECTORIZER.fields_by_name['stringToIndex'].message_type = DataStructures__pb2._STRINGVECTOR
_DICTVECTORIZER.fields_by_name['int64ToIndex'].message_type = DataStructures__pb2._INT64VECTOR
_DICTVECTORIZER.oneofs_by_name['Map'].fields.append(
  _DICTVECTORIZER.fields_by_name['stringToIndex'])
_DICTVECTORIZER.fields_by_name['stringToIndex'].containing_oneof = _DICTVECTORIZER.oneofs_by_name['Map']
_DICTVECTORIZER.oneofs_by_name['Map'].fields.append(
  _DICTVECTORIZER.fields_by_name['int64ToIndex'])
_DICTVECTORIZER.fields_by_name['int64ToIndex'].containing_oneof = _DICTVECTORIZER.oneofs_by_name['Map']
DESCRIPTOR.message_types_by_name['DictVectorizer'] = _DICTVECTORIZER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DictVectorizer = _reflection.GeneratedProtocolMessageType('DictVectorizer', (_message.Message,), dict(
  DESCRIPTOR = _DICTVECTORIZER,
  __module__ = 'DictVectorizer_pb2'
  # @@protoc_insertion_point(class_scope:CoreML.Specification.DictVectorizer)
  ))
_sym_db.RegisterMessage(DictVectorizer)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\003'))
# @@protoc_insertion_point(module_scope)
