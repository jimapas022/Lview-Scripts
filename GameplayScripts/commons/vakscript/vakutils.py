from struct import unpack as unpack_st
from recordclass import recordclass


Node = recordclass('Node', 'address, next')

def linked_insert(current_node, next_address):
    next_node = Node(next_address, current_node.next)
    current_node.next = next_node


def int_from_buffer(data, offset):
    return int.from_bytes(data[offset:offset + 4], 'little')


def float_from_buffer(data, offset):
    f, = unpack_st('f', data[offset:offset + 4])
    return f


def double_from_buffer(data, offset):
    d, = unpack_st('d', data[offset:offset + 8])
    return d


def bool_from_buffer(data, offset):
    return data[offset:offset + 1] != b'\x00'