execute unless entity @a[tag=timer] run spawnpoint @a[tag=!timer] 0 64 0
execute unless entity @a[tag=timer] run setworldspawn 0 64 0
execute unless entity @a[tag=timer] run tp @a[tag=!timer] 0 64 0
setblock 0 63 0 bedrock
execute unless entity @a[tag=timer] run scoreboard objectives add randomtimer1 dummy Ticks
execute unless entity @a[tag=timer] run scoreboard objectives add randomtimer2 dummy Seconds
execute unless entity @a[tag=timer] run scoreboard objectives add random dummy Random
execute unless entity @a[tag=timer] run tag @a add timer
execute as @a[tag=timer] run tag @a add timer
gamerule commandblockoutput false
gamerule sendcommandfeedback false
