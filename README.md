# UCSD_Energium_AI_Competition
1. Generate bot if #bots < #positive cells*0.618
2. Create a priority queue containing all the positions of positive cells, sorted by the energium at this location, break tie by the distance to the base. 
3. Using the greedy strategy, if a bot doesn't have a 'goal', set it to the best possible location according to the priority queue. 
4. Dodging: If an enemy is adjacent and can kill it, set its 'goal' to base and re-dispatch. 
5. Avoiding dead-end: The nearest path might lead the bot to a 'dead-end', which might end up with going back and forth infinitely. So this additional check is added.
