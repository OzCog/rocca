#!/usr/bin/env python3

# Experiment to communicate with Minetest via Miney.
#
# Requirements:
#
# - Minetest and Miney, see
#   https://miney.readthedocs.io/en/latest/index.html
#
# Usage:
#
# 1. Run minetest
# 2. Create game with mineysocket enabled
# 3. Run that script
#
# Acknowledgment:
#
# A lot of understanding (especially the end of the script) comes from
# studying https://github.com/MaikePaetzel/minetest-agent

import miney

# Connect Minetest
mt = miney.Minetest()
print("mt = {}".format(mt))

# We set the time to midnight
print("mt.time_of_day = {}".format(mt.time_of_day))
mt.time_of_day = 0.5
print("mt.time_of_day = {}".format(mt.time_of_day))

# Set Lua interpreter
lua = miney.Lua(mt)
print("lua = {}".format(lua))

# Convert Python data into lua string.
#
# List of supported Python constructs (so far):
# - list
#
# List of unsupported Python constructs (so far):
# - set
# - tuple
data = ["123", "abc"]
data_dumps = lua.dumps(data)
print("data_dumps = {}".format(data_dumps))

# Run simple lua code
simple_lua_code = "return 1 + 2"
simple_lua_result = lua.run(simple_lua_code)
print("simple_lua_result = {}".format(simple_lua_result))

# Run lua code to trigger play action, inspired from
# minetest-agent/agent/Rob/atomic_actions.py
#
# Additionally here is a list of potentially useful methods from
# https://minetest.org/modbook/lua_api.html
#
# minetest.player_exists(name)
# minetest.get_player_by_name(name)
# minetest.get_objects_inside_radius(pos, radius)
# minetest.find_node_near(pos, radius, nodenames)
# minetest.find_nodes_in_area_under_air(minp, maxp, nodenames)
# minetest.emerge_area(pos1, pos2, [callback], [param])
# minetest.delete_area(pos1, pos2)
# minetest.line_of_sight(pos1, pos2, stepsize)
# minetest.find_path(pos1,pos2,searchdistance,max_jump,max_drop,algorithm)
# minetest.get_inventory(location)
# minetest.dir_to_yaw(dir)
# minetest.yaw_to_dir(yaw)
# minetest.item_drop(itemstack, dropper, pos)
# minetest.item_eat(hp_change, replace_with_item)
# minetest.node_punch(pos, node, puncher, pointed_thing)
# minetest.node_dig(pos, node, digger)
#
# ObjectRef methods:
# - move_to(pos, continuous=false)
# - punch(puncher, time_from_last_punch, tool_capabilities, direction)
# - get_player_name()
# - set_look_vertical(radians)
# - set_look_horizontal(radians)

# Chat
chat = """
return minetest.chat_send_all(\"Hello Minetest\")
"""
chat_result = lua.run(chat)
print("chat_result = {}".format(chat_result))

# Testing player
player_name = "singleplayer"

# Check that the player exists
player_exists = """
return minetest.player_exists(\"{}\")
""".format(player_name)
player_exists_result = lua.run(player_exists)
print("player_exists = {}".format(player_exists_result))

# Retrieve the name of the player (given its name, hehe)
player_retrieve_name = """
local player = minetest.get_player_by_name(\"{}\")
local player_name = player:get_player_name()
return player_name
""".format(player_name)
player_retrieve_name_result = lua.run(player_retrieve_name)
print("player_retrieve_name_result = {}".format(player_retrieve_name_result))

# Get player position
get_player_pos = """
local player = minetest.get_player_by_name(\"{}\")
return player:get_pos()
""".format(player_name)
get_player_pos_result = lua.run(get_player_pos)
print("get_player_pos_result = {}".format(get_player_pos_result))

# Move player to new position
# NEXT
move_player_to = """
local player = minetest.get_player_by_name(\"{}\")
return player:move_to({})
""".format(player_name, lua.dumps(get_player_pos_result))
print("move_player_to = {}".format(move_player_to))
move_player_to_result = lua.run(move_player_to)
print("get_player_to_result = {}".format(move_player_to_result))

# # Starts mining
# player = "singleplayer"
# lua_mine = """
# local npc = npcf:get_luaentity(\"""" + player + """\")
# local move_obj = npcf.movement.getControl(npc)
# move_obj:mine()
# return true
# """
# mine_result = lua.run(lua_mine)
# print("mine_result = {}".format(mine_result))

# # Stop mining
# lua_stop = """
# move_obj:mine_stop()
# return true
# """
# stop_result = lua.run(lua_stop)
# print("stop_result = {}".format(stop_result))
