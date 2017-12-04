# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grr/client/minicomm/config.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='grr/client/minicomm/config.proto',
  package='grr',
  syntax='proto2',
  serialized_pb=_b('\n grr/client/minicomm/config.proto\x12\x03grr\"\xdd\x02\n\x13\x43lientConfiguration\x12\x13\n\x0b\x63ontrol_url\x18\x01 \x03(\t\x12\x14\n\x0cproxy_server\x18\x02 \x03(\t\x12\x13\n\x0b\x63\x61_cert_pem\x18\x03 \x01(\t\x12\x1e\n\x16\x63lient_private_key_pem\x18\x04 \x01(\t\x12&\n\x1elast_server_cert_serial_number\x18\x05 \x01(\x05\x12\x1a\n\x12writeback_filename\x18\x06 \x01(\t\x12\x44\n\x11subprocess_config\x18\x07 \x01(\x0b\x32).grr.ClientConfiguration.SubprocessConfig\x12\x1b\n\x13temporary_directory\x18\x08 \x01(\t\x1a?\n\x10SubprocessConfig\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04\x61rgv\x18\x02 \x03(\t\x12\x0b\n\x03\x65nv\x18\x03 \x03(\t')
)




_CLIENTCONFIGURATION_SUBPROCESSCONFIG = _descriptor.Descriptor(
  name='SubprocessConfig',
  full_name='grr.ClientConfiguration.SubprocessConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='grr.ClientConfiguration.SubprocessConfig.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='argv', full_name='grr.ClientConfiguration.SubprocessConfig.argv', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='env', full_name='grr.ClientConfiguration.SubprocessConfig.env', index=2,
      number=3, type=9, cpp_type=9, label=3,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=328,
  serialized_end=391,
)

_CLIENTCONFIGURATION = _descriptor.Descriptor(
  name='ClientConfiguration',
  full_name='grr.ClientConfiguration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='control_url', full_name='grr.ClientConfiguration.control_url', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proxy_server', full_name='grr.ClientConfiguration.proxy_server', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ca_cert_pem', full_name='grr.ClientConfiguration.ca_cert_pem', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='client_private_key_pem', full_name='grr.ClientConfiguration.client_private_key_pem', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_server_cert_serial_number', full_name='grr.ClientConfiguration.last_server_cert_serial_number', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='writeback_filename', full_name='grr.ClientConfiguration.writeback_filename', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subprocess_config', full_name='grr.ClientConfiguration.subprocess_config', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='temporary_directory', full_name='grr.ClientConfiguration.temporary_directory', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CLIENTCONFIGURATION_SUBPROCESSCONFIG, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=391,
)

_CLIENTCONFIGURATION_SUBPROCESSCONFIG.containing_type = _CLIENTCONFIGURATION
_CLIENTCONFIGURATION.fields_by_name['subprocess_config'].message_type = _CLIENTCONFIGURATION_SUBPROCESSCONFIG
DESCRIPTOR.message_types_by_name['ClientConfiguration'] = _CLIENTCONFIGURATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ClientConfiguration = _reflection.GeneratedProtocolMessageType('ClientConfiguration', (_message.Message,), dict(

  SubprocessConfig = _reflection.GeneratedProtocolMessageType('SubprocessConfig', (_message.Message,), dict(
    DESCRIPTOR = _CLIENTCONFIGURATION_SUBPROCESSCONFIG,
    __module__ = 'grr.client.minicomm.config_pb2'
    # @@protoc_insertion_point(class_scope:grr.ClientConfiguration.SubprocessConfig)
    ))
  ,
  DESCRIPTOR = _CLIENTCONFIGURATION,
  __module__ = 'grr.client.minicomm.config_pb2'
  # @@protoc_insertion_point(class_scope:grr.ClientConfiguration)
  ))
_sym_db.RegisterMessage(ClientConfiguration)
_sym_db.RegisterMessage(ClientConfiguration.SubprocessConfig)


# @@protoc_insertion_point(module_scope)
