execute unless entity @a[tag=timer] run scoreboard objectives add randomtimer1 dummy Ticks
execute unless entity @a[tag=timer] run scoreboard objectives add randomtimer2 dummy Seconds
execute unless entity @a[tag=timer] run scoreboard objectives add random dummy Random
execute unless entity @a[tag=timer] run tag @a add timer
execute as @a[tag=timer] run tag @a add timer
gamerule commandblockoutput false
gamerule sendcommandfeedback false
