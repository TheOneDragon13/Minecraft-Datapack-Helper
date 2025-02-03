import sublime
import sublime_plugin
import json
import os

class McFunctionAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.mcfunction"):
            return None

        completions = [
            ("advancement\tAdvancement Command", "advancement ${1:grant|revoke} @s ${2:only|until|everything} ${3:advancement}"),
            ("attribute\tAttribute Command", "attribute @s ${1:attribute} ${2:get|base|get_modifier|add_modifier|remove_modifier} ${3:args}"),
            ("bossbar\tBossbar Command", "bossbar ${1:add|get|list|remove|set} ${2:args}"),
            ("clear\tClear Inventory", "clear @s ${1:item} ${2:maxCount}"),
            ("clone\tClone Blocks", "clone ${1:startX} ${2:startY} ${3:startZ} ${4:endX} ${5:endY} ${6:endZ} ${7:destinationX} ${8:destinationY} ${9:destinationZ} ${10:replace|masked} ${11:normal|force|move}"),
            ("data\tData Command", "data ${1:get|merge|modify|remove} ${2:args}"),
            ("datapack\tDatapack Command", "datapack ${1:disable|enable|list} ${2:args}"),
            ("debug\tDebug Command", "debug ${1:start|stop|function} ${2:args}"),
            ("defaultgamemode\tSet Default Gamemode", "defaultgamemode ${1:survival|creative|adventure|spectator}"),
            ("difficulty\tSet Difficulty", "difficulty ${1:peaceful|easy|normal|hard}"),
            ("effect\tApply Effect", "effect give @s minecraft:${1:effect} ${2:30} ${3:1}"),
            ("execute\tExecute Command", "execute as @s at @s run ${1:command}"),
            ("fill\tFill Blocks", "fill ${1:startX} ${2:startY} ${3:startZ} ${4:endX} ${5:endY} ${6:endZ} ${7:block} ${8:replace|destroy|hollow|keep|outline}"),
            ("forceload\tForceload Command", "forceload ${1:add|remove|query} ${2:args}"),
            ("function\tCall Function", "function ${1:namespace}:${2:filename}"),
            ("gamemode\tChange Gamemode", "gamemode ${1:survival|creative|adventure|spectator} @s"),
            ("gamerule\tSet Gamerule", "gamerule ${1:rule} ${2:value}"),
            ("give\tGive Item", "give @s minecraft:${1:item} ${2:1}"),
            ("kill\tKill Entity", "kill @e[type=${1:entity}]"),
            ("locate\tLocate Structure", "locate ${1:structure}"),
            ("me\tChat Command", "me ${1:message}"),
            ("msg\tPrivate Message", "msg @a ${1:message}"),
            ("particle\tParticle Command", "particle ${1:name} ${2:x} ${3:y} ${4:z} ${5:dx} ${6:dy} ${7:dz} ${8:speed} ${9:count} ${10:force|normal}"),
            ("playsound\tPlay Sound", "playsound minecraft:${1:sound} master @a ${2:x} ${3:y} ${4:z} ${5:1.0} ${6:1.0} ${7:1.0}"),
            ("say\tSay Message", "say ${1:message}"),
            ("scoreboard\tScoreboard Command", "scoreboard objectives add ${1:name} ${2:criteria}"),
            ("setblock\tSet Block", "setblock ${1:x} ${2:y} ${3:z} ${4:block} ${5:replace|destroy|keep}"),
            ("spawnpoint\tSet Spawn Point", "spawnpoint @s ${1:x} ${2:y} ${3:z}"),
            ("summon\tSummon Entity", "summon minecraft:${1:entity} ${2:x} ${3:y} ${4:z}"),
            ("team\tTeam Command", "team ${1:add|empty|join|leave|list|modify|remove} ${2:args}"),
            ("teleport\tTeleport", "tp @s ${1:x} ${2:y} ${3:z}"),
            ("time\tTime Command", "time set ${1:day|night|noon|midnight}"),
            ("tp\tTeleport", "tp @s ${1:x} ${2:y} ${3:z}"),
            ("title\tTitle Command", "title @a title {\"text\":\"${1:message}\",\"color\":\"${2:red}\"}"),
            ("weather\tWeather Command", "weather ${1:clear|rain|thunder}"),
            ("xp\tXP Command", "xp add @s ${1:amount} ${2:levels}"),
        ]

        return completions

class McFunctionSyntaxHighlight(sublime_plugin.EventListener):
    def on_load(self, view):
        if view.file_name() and view.file_name().endswith(".mcfunction"):
            view.set_syntax_file("Packages/User/mcfunction.sublime-syntax")

class McFunctionSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit, snippet):
        self.view.run_command("insert_snippet", {"contents": snippet})

SYNTAX_FILE = "Packages/User/mcfunction.sublime-syntax"
SYNTAX_CONTENT = """
%YAML 1.2
---
name: Minecraft Function
file_extensions:
  - mcfunction
scope: source.mcfunction
contexts:
  main:
    - match: '(#.*)'
      scope: comment.line.mcfunction
    - match: '\b(tp|give|summon|effect|kill|execute|say|scoreboard|fill|locate|particle|playsound|spawnpoint|team|weather|xp)\b'
      scope: keyword.control.mcfunction
"""

def plugin_loaded():
    if not os.path.exists(SYNTAX_FILE):
        with open(SYNTAX_FILE, "w") as f:
            f.write(SYNTAX_CONTENT)
