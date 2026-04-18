import random


def process_attack(attacker, defender, is_break, defender_is_defending, attacker_attack=15, defender_defense=5):
    """
    Process an attack action between two entities
    
    Args:
        attacker: Name of the attacking entity
        defender: Name of the defending entity
        is_break: Whether the attack is a break attack
        defender_is_defending: Whether the defender is defending
        attacker_attack: Attack power of the attacker
        defender_defense: Defense power of the defender
        
    Returns:
        tuple: (damage, message)
    """
    # Calculate base damage
    dmg_base = random.randint(attacker_attack - 5, attacker_attack + 5)

    if is_break:
        # Break attack
        if defender_is_defending:
            # Defender is defending, so break is more effective
            dmg = int(dmg_base * 1.5) - defender_defense
            dmg = max(1, dmg)  # Minimum 1 damage
            msg = f"{attacker} BROKE defense! {dmg} DMG!"
        else:
            # Defender is not defending, so break is less effective
            dmg = int(dmg_base * 0.5) - int(defender_defense * 0.5)
            dmg = max(1, dmg)  # Minimum 1 damage
            msg = f"{attacker} tried to break... missed! {dmg} DMG."
    else:
        if defender_is_defending:
            
            dmg = int(dmg_base * 0.3) - defender_defense
            dmg = max(1, dmg)  # Minimum 1 damage
            msg = f"{defender} blocked! {dmg} DMG."
        else:
            dmg = dmg_base - int(defender_defense * 0.5)
            dmg = max(1, dmg)  # Minimum 1 damage
            msg = f"{attacker} attacks! {dmg} DMG!"

    return dmg, msg


def process_queued_turn(action_queue, turn_index, player_hp, enemy_hp, player_defending, enemy_defending,
                         player_attack=15, player_defense=5, enemy_attack=12, enemy_defense=4):
    """
    Process a single turn from the action queue.
    Returns: (new_player_hp, new_enemy_hp, new_player_defending, new_enemy_defending, battle_msg)
    """
    if turn_index >= len(action_queue):
        return player_hp, enemy_hp, player_defending, enemy_defending, "Round complete!"

    player_action = action_queue[turn_index]

    # Process Player Action
    if player_action == "defend":
        player_defending = True
        battle_msg = "Player defends!"
    elif player_action == "attack":
        dmg, msg = process_attack("Player", "Enemy", False, enemy_defending, player_attack, enemy_defense)
        enemy_hp -= dmg
        battle_msg = msg
    elif player_action == "break":
        dmg, msg = process_attack("Player", "Enemy", True, enemy_defending, player_attack, enemy_defense)
        enemy_hp -= dmg
        battle_msg = msg

    # Check if enemy is defeated before enemy turn
    if enemy_hp <= 0:
        return player_hp, enemy_hp, player_defending, enemy_defending, battle_msg

    # Process Enemy Turn (after player action)
    action_choice = random.choice(["attack", "attack", "defend", "break"])
    if action_choice == "defend":
        enemy_defending = True
        battle_msg += " | Enemy defends!"
    else:
        dmg, msg = process_attack("Enemy", "Player", action_choice == "break", player_defending, enemy_attack, player_defense)
        player_hp -= dmg
        battle_msg += f" | {msg}"

    return player_hp, enemy_hp, player_defending, enemy_defending, battle_msg
