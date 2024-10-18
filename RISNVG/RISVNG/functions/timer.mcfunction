scoreboard players add @a randomtimer1 1
execute at @a[scores={randomtimer1=20}] run scoreboard players add @p randomtimer2 1
execute at @a[scores={randomtimer1=20}] run scoreboard players set @a randomtimer1 0
execute at @r[scores={randomtimer2=timedelay}] run function runrandompick