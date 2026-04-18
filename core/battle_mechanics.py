import random


def calculate_base_damage(attack_power):
    """
    Calculate base damage (uniform).
    
    Args:
        attack_power: Base attack power of the attacker
        
    Returns:
        int: Base damage value
    """
    return attack_power


def calculate_final_damage(base_damage, multiplier=1.0):
    """
    Calculate final damage after applying multiplier.
    
    Args:
        base_damage: Base damage before modifications
        multiplier: Damage multiplier (default 1.0)
        
    Returns:
        int: Final damage (minimum 1)
    """
    dmg = int(base_damage * multiplier)
    return max(1, dmg)


def process_action_interaction(player_action, enemy_action, 
                               player_hp, enemy_hp,
                               player_attack, enemy_attack):
    """
    Process the interaction between player and enemy actions.
    
    Action Interaction Rules:
    - attack to attack = both deal damage
    - attack to defense = ignore full damage (no damage)
    - attack to break armor = attack deals damage, break misses
    - defense to defense = skip the turn
    - break armor to defense = deal half the damage
    - break armor to break armor = both deal full damage
    
    Args:
        player_action: Player's action ('attack', 'defense', 'break')
        enemy_action: Enemy's action ('attack', 'defense', 'break')
        player_hp: Current player HP
        enemy_hp: Current enemy HP
        player_attack: Player's attack power
        enemy_attack: Enemy's attack power
        
    Returns:
        tuple: (new_player_hp, new_enemy_hp, battle_message)
    """
    battle_msg = ""
    
    # attack to attack = both deal damage
    if player_action == "attack" and enemy_action == "attack":
        player_dmg = calculate_final_damage(calculate_base_damage(enemy_attack))
        enemy_dmg = calculate_final_damage(calculate_base_damage(player_attack))
        player_hp -= player_dmg
        enemy_hp -= enemy_dmg
        battle_msg = f"Player attacks! {enemy_dmg} DMG! | Enemy attacks! {player_dmg} DMG!"
    
    # attack to defense = ignore full damage (no damage)
    elif player_action == "attack" and enemy_action == "defense":
        battle_msg = "Player attacks! Enemy defends! No damage dealt!"
    
    # defense to attack = ignore full damage (no damage)
    elif player_action == "defense" and enemy_action == "attack":
        battle_msg = "Player defends! Enemy attacks! No damage dealt!"
    
    # attack to break armor = attack deals damage, break misses
    elif player_action == "attack" and enemy_action == "break":
        enemy_dmg = calculate_final_damage(calculate_base_damage(player_attack))
        enemy_hp -= enemy_dmg
        battle_msg = f"Player attacks! {enemy_dmg} DMG! | Enemy tries to break... missed!"
    
    # break armor to attack = attack deals damage, break misses
    elif player_action == "break" and enemy_action == "attack":
        player_dmg = calculate_final_damage(calculate_base_damage(enemy_attack))
        player_hp -= player_dmg
        battle_msg = f"Player tries to break... missed! | Enemy attacks! {player_dmg} DMG!"
    
    # defense to defense = skip the turn
    elif player_action == "defense" and enemy_action == "defense":
        battle_msg = "Both defend! Turn skipped!"
    
    # break armor to defense = deal half the damage
    elif player_action == "break" and enemy_action == "defense":
        enemy_dmg = calculate_final_damage(calculate_base_damage(player_attack), multiplier=0.5)
        enemy_hp -= enemy_dmg
        battle_msg = f"Player breaks defense! {enemy_dmg} DMG!"
    
    # defense to break armor = deal half the damage
    elif player_action == "defense" and enemy_action == "break":
        player_dmg = calculate_final_damage(calculate_base_damage(enemy_attack), multiplier=0.5)
        player_hp -= player_dmg
        battle_msg = f"Enemy breaks defense! {player_dmg} DMG!"
    
    # break armor to break armor = both deal full damage
    elif player_action == "break" and enemy_action == "break":
        player_dmg = calculate_final_damage(calculate_base_damage(enemy_attack))
        enemy_dmg = calculate_final_damage(calculate_base_damage(player_attack))
        player_hp -= player_dmg
        enemy_hp -= enemy_dmg
        battle_msg = f"Player breaks! {enemy_dmg} DMG! | Enemy breaks! {player_dmg} DMG!"
    
    return player_hp, enemy_hp, battle_msg


def generate_enemy_actions(num_turns=3):
    """
    Generate enemy actions for all turns at once.
    
    Args:
        num_turns: Number of turns to generate actions for (default 3)
        
    Returns:
        list: List of enemy actions for each turn
    """
    enemy_actions = []
    for _ in range(num_turns):
        enemy_action = random.choice(["attack", "attack", "defense", "break"])
        enemy_actions.append(enemy_action)
    return enemy_actions


def process_queued_turn(action_queue, turn_index, player_hp, enemy_hp,
                         player_attack, enemy_attack,
                         enemy_action=None):
    """
    Process a single turn from the action queue using action interaction logic.
    
    Args:
        action_queue: List of player actions
        turn_index: Current turn index
        player_hp: Current player HP
        enemy_hp: Current enemy HP
        player_attack: Player's attack power
        enemy_attack: Enemy's attack power
        enemy_action: Pre-generated enemy action (optional, generates randomly if None)
        
    Returns:
        tuple: (new_player_hp, new_enemy_hp, battle_message)
    """
    if turn_index >= len(action_queue):
        return player_hp, enemy_hp, "Round complete!"

    player_action = action_queue[turn_index]
    
    # Normalize action names
    if player_action == "defend":
        player_action = "defense"

    # Use provided enemy action or generate randomly
    if enemy_action is None:
        enemy_action = random.choice(["attack", "attack", "defense", "break"])

    # Process the action interaction
    new_player_hp, new_enemy_hp, battle_msg = process_action_interaction(
        player_action, enemy_action,
        player_hp, enemy_hp,
        player_attack, enemy_attack
    )

    return new_player_hp, new_enemy_hp, battle_msg
