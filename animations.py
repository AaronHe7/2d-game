def checkframe(direction, handstate, frame, velocity):
    print(direction, handstate, frame, velocity)

    if direction[1] == -1 and direction[0] == 0: #if the player is falling and facing left
        return 4
    if direction[1] == -1 and direction[0] == 1: #if the player is falling and facing right
        return 5

    if direction[0] == 0 and direction[1] >= 0 and handstate == 0 and frame <= 60 and velocity[0] == 0: #if the player is facing left, not falling, has no handstate, is not moving
        return 0
    if direction[0] == 0 and direction[1] >= 0 and handstate == 0 and frame > 60 and velocity[0] == 0: #if the player is facing left, not falling, has no handstate, is not moving
        #placeholder, replace with idle animation state 1 facing left.
        return 0
    if direction[0] == 1 and direction[1] >= 0 and handstate == 0 and frame <= 60 and velocity[0] == 0: #if the player is facing right not falling, has no handstate, is not moving
        return 1
    if direction[0] == 1 and direction[1] >= 0 and handstate == 0 and frame > 60 and velocity[0] == 0: #if the player is facing right, not falling, has no handstate, is not moving
        #placeholder, replace with idle animation state 1 facing right.
        return 1

    if direction[1] == 0 and handstate == 0 and frame <= 60 and velocity[0] > 0: #if the player is moving right and not falling and has no handstate
        return 3
    if direction[1] == 0 and handstate == 0 and frame <= 60 and velocity[0] < 0: #if the player is moving left and not falling and has no handstate
        return 2
    if direction[1] == 0 and handstate == 0 and frame > 60 and velocity[0] > 0: #etc
        return 3 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and frame > 60 and velocity[0] < 0: #etc
        return 2 #placeholder, replace with running animation state n facing left

    return 1
