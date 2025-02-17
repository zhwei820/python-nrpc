# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: alloptions.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nrpc import nrpc_pb2 as nrpc_dot_nrpc__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='alloptions.proto',
  package='main',
  syntax='proto3',
  serialized_pb=_b('\n\x10\x61lloptions.proto\x12\x04main\x1a\x0fnrpc/nrpc.proto\"\x19\n\tStringArg\x12\x0c\n\x04\x61rg1\x18\x01 \x01(\t\"\"\n\x11SimpleStringReply\x12\r\n\x05reply\x18\x01 \x01(\t2\xe7\x02\n\x10SvcCustomSubject\x12N\n\rMtSimpleReply\x12\x0f.main.StringArg\x1a\x17.main.SimpleStringReply\"\x13\x82\xb2\x19\x0fmt_simple_reply\x12,\n\x0bMtVoidReply\x12\x0f.main.StringArg\x1a\n.nrpc.Void\"\x00\x12\x39\n\x0bMtNoRequest\x12\x0f.nrpc.NoRequest\x1a\x17.main.SimpleStringReply\"\x00\x12\x41\n\x0fMtStreamedReply\x12\x0f.main.StringArg\x1a\x17.main.SimpleStringReply\"\x04\x90\xb2\x19\x01\x12\x43\n\x16MtVoidReqStreamedReply\x12\n.nrpc.Void\x1a\x17.main.SimpleStringReply\"\x04\x90\xb2\x19\x01\x1a\x12\xc2\xf3\x18\x0e\x63ustom_subject2\xdf\x01\n\x10SvcSubjectParams\x12J\n\x13MtWithSubjectParams\x12\n.nrpc.Void\x1a\x17.main.SimpleStringReply\"\x0e\x8a\xb2\x19\x03mp1\x8a\xb2\x19\x03mp2\x12(\n\tMtNoReply\x12\n.nrpc.Void\x1a\r.nrpc.NoReply\"\x00\x12G\n\x12MtNoRequestWParams\x12\x0f.nrpc.NoRequest\x1a\x17.main.SimpleStringReply\"\x07\x8a\xb2\x19\x03mp1\x1a\x0c\xca\xf3\x18\x08\x63lientid2M\n\x10NoRequestService\x12\x39\n\x0bMtNoRequest\x12\x0f.nrpc.NoRequest\x1a\x17.main.SimpleStringReply\"\x00\x42\x1c\x82\xb5\x18\x04root\x8a\xb5\x18\x08instance\x90\xb5\x18\x01\x98\xb5\x18\x01\x62\x06proto3')
  ,
  dependencies=[nrpc_dot_nrpc__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_STRINGARG = _descriptor.Descriptor(
  name='StringArg',
  full_name='main.StringArg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arg1', full_name='main.StringArg.arg1', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=43,
  serialized_end=68,
)


_SIMPLESTRINGREPLY = _descriptor.Descriptor(
  name='SimpleStringReply',
  full_name='main.SimpleStringReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reply', full_name='main.SimpleStringReply.reply', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=70,
  serialized_end=104,
)

DESCRIPTOR.message_types_by_name['StringArg'] = _STRINGARG
DESCRIPTOR.message_types_by_name['SimpleStringReply'] = _SIMPLESTRINGREPLY

StringArg = _reflection.GeneratedProtocolMessageType('StringArg', (_message.Message,), dict(
  DESCRIPTOR = _STRINGARG,
  __module__ = 'alloptions_pb2'
  # @@protoc_insertion_point(class_scope:main.StringArg)
  ))
_sym_db.RegisterMessage(StringArg)

SimpleStringReply = _reflection.GeneratedProtocolMessageType('SimpleStringReply', (_message.Message,), dict(
  DESCRIPTOR = _SIMPLESTRINGREPLY,
  __module__ = 'alloptions_pb2'
  # @@protoc_insertion_point(class_scope:main.SimpleStringReply)
  ))
_sym_db.RegisterMessage(SimpleStringReply)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\202\265\030\004root\212\265\030\010instance\220\265\030\001\230\265\030\001'))
# @@protoc_insertion_point(module_scope)
