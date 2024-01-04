from numpy import array,matmul
from pymem.exception import MemoryReadError
from collections import namedtuple
from win32api import GetSystemMetrics
import commons.vakscript.vakoffsets
from commons.vakscript.vakutils import float_from_buffer, int_from_buffer, bool_from_buffer, linked_insert, Node


Object = namedtuple('Object', 'name, ability_power, armor, attack_range, attack_speed_multiplier, base_attack, bonus_attack, health, network_id, magic_resist, mana, max_health, size_multiplier, x, y, z, level, team, spawn_count, targetable, visibility')

def read_object(mem, address):
    data = mem.read_bytes(address, commons.vakscript.vakoffsets.OBJECT_SIZE)

    params = {}
    params['name'] = mem.read_string(int_from_buffer(data, commons.vakscript.vakoffsets.oObjectName), 50)
    params['ability_power'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectAbilityPower)
    params['armor'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectArmor)
    params['attack_range'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectAtkRange)
    params['attack_speed_multiplier'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectAtkSpeedMulti)
    params['base_attack'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectBaseAtk)
    params['bonus_attack'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectBonusAtk)
    params['magic_resist'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectMagicRes)
    params['mana'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectMana)
    params['health'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectHealth)
    params['max_health'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectMaxHealth)
    params['size_multiplier'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectSizeMultiplier)
    params['x'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectX)
    params['y'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectY)
    params['z'] = float_from_buffer(data, commons.vakscript.vakoffsets.oObjectZ)

    params['network_id'] = int_from_buffer(data, commons.vakscript.vakoffsets.oObjectNetworkID)
    params['level'] = int_from_buffer(data, commons.vakscript.vakoffsets.oObjectLevel)
    params['team'] = int_from_buffer(data, commons.vakscript.vakoffsets.oObjectTeam)
    params['spawn_count'] = int_from_buffer(data, commons.vakscript.vakoffsets.oObjectSpawnCount)

    params['targetable'] = bool_from_buffer(data, commons.vakscript.vakoffsets.oObjectTargetable)
    params['visibility'] = bool_from_buffer(data, commons.vakscript.vakoffsets.oObjectVisibility)

    return Object(**params)

def find_object_pointers(mem, max_count=800):
    object_pointers = mem.read_uint(mem.base_address + commons.vakscript.vakoffsets.oObjectManager)
    root_node = Node(mem.read_uint(object_pointers + commons.vakscript.vakoffsets.oObjectMapRoot), None)
    addresses_seen = set()
    current_node = root_node
    pointers = set()
    count = 0
    while current_node is not None and count < max_count:
        if current_node.address in addresses_seen:
            current_node = current_node.next
            continue
        addresses_seen.add(current_node.address)
        try:
            data = mem.read_bytes(current_node.address, 0x18)
            count += 1
        except MemoryReadError:
            pass
        else:
            for i in range(3):
                child_address = int_from_buffer(data, i * 4)
                if child_address in addresses_seen:
                    continue
                linked_insert(current_node, child_address)
            net_id = int_from_buffer(data, commons.vakscript.vakoffsets.oObjectMapNodeNetId)
            if net_id - 0x40000000 <= 0x100000:
                pointers.add(int_from_buffer(data, commons.vakscript.vakoffsets.oObjectMapNodeObject))
        current_node = current_node.next
    return pointers


def find_champion_pointers(mem, champion_names):
    pointers = find_object_pointers(mem)
    champion_pointers = set()
    for pointer in pointers:
        try:
            o = read_object(mem, pointer)
        except (MemoryReadError, UnicodeDecodeError):
            pass
        else:
            if o.name.lower() in champion_names:
                champion_pointers.add(pointer)
    assert len(champion_pointers) >= len(champion_names), "CP %s CN %s" % (len(champion_pointers), len(champion_names))
    return champion_pointers

def find_local_net_id(mem):
    local_player = mem.read_uint(mem.base_address + commons.vakscript.vakoffsets.oLocalPlayer)
    return mem.read_int(local_player + commons.vakscript.vakoffsets.oObjectNetworkID)

def find_game_time(mem):
    return mem.read_float(mem.base_address + commons.vakscript.vakoffsets.oGameTime)

def list_to_matrix(floats):
    m = array(floats)
    return m.reshape(4, 4)

def find_view_proj_matrix(mem):

    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)

    data = mem.read_bytes(mem.base_address + commons.vakscript.vakoffsets.oViewProjMatrices, 128)
    view_matrix = list_to_matrix([float_from_buffer(data, i * 4) for i in range(16)])
    proj_matrix = list_to_matrix([float_from_buffer(data, 64 + (i * 4)) for i in range(16)])
    view_proj_matrix = matmul(view_matrix, proj_matrix)
    return view_proj_matrix.reshape(16), width, height

def world_to_screen(view_proj_matrix, width, height, x, y, z):
    
    clip_coords_x = x * view_proj_matrix[0] + y * view_proj_matrix[4] + z * view_proj_matrix[8] + view_proj_matrix[12]
    clip_coords_y = x * view_proj_matrix[1] + y * view_proj_matrix[5] + z * view_proj_matrix[9] + view_proj_matrix[13]
    clip_coords_w = x * view_proj_matrix[3] + y * view_proj_matrix[7] + z * view_proj_matrix[11] + view_proj_matrix[15]

    if clip_coords_w < 1.:
        clip_coords_w = 1.

    M_x = clip_coords_x / clip_coords_w
    M_y = clip_coords_y / clip_coords_w

    out_x = (width / 2. * M_x) + (M_x + width / 2.)
    out_y = -(height / 2. * M_y) + (M_y + height / 2.)

    if 0 <= out_x <= width and 0 <= out_y <= height:
        return out_x, out_y

    return None, None
