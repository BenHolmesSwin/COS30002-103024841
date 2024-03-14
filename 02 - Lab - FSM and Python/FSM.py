# variables

work = 0
energy = 0

states = ['playing','working','resting']
current_state = 'resting'

running = True
max_limit = 100
game_time = 0

while running:
    game_time += 1

    if current_state == 'playing':
        print('Having a great time!!')
        energy -= 1
        work += 1
        if energy < 5:
            current_state = 'resting'
        elif work > 7:
            current_state = 'working'

    elif current_state == 'working':
        print('The Boring thing that must be done')
        energy -= 1
        work -= 2
        if energy < 5:
            current_state = 'resting'
        elif work < 3:
            current_state = 'playing'

    elif current_state == 'resting':
        print('Sleepy')
        energy += 2
        work += 1
        if energy > 5:
            if work < 7:
                current_state = 'playing'
            else:
                current_state = 'working'

    if game_time > max_limit:
        running = False


print('-- The End --')