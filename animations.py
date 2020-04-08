def checkframe(direction, handstate, rframe, velocity, frame, maxrframe, legs = False):

    if legs == True: #drawing the legs of the player
        if direction[0] == -1:
            if direction[1] != 0:
                return -102
            if velocity[0] == 0:
                return -100
            if rframe <= (maxrframe/8) and velocity[0] < 0:
                return -104
            if (maxrframe*2/8) >= rframe > (maxrframe/8) and velocity[0] < 0:
                return -106
            if (maxrframe*3/8) >= rframe > (maxrframe*2/8) and velocity[0] < 0:
                return -108
            if (maxrframe*4/8) >= rframe > (maxrframe*3/8) and velocity[0] < 0:
                return -110
            if (maxrframe*5/8) >= rframe > (maxrframe*4/8) and velocity[0] < 0:
                return -112
            if (maxrframe*6/8) >= rframe > (maxrframe*5/8) and velocity[0] < 0:
                return -114
            if (maxrframe*7/8) >= rframe > (maxrframe*6/8) and velocity[0] < 0:
                return -116
            if rframe > (maxrframe*7/8) and velocity[0] < 0:
                return -118
        if direction[0] == 1:
            if direction[1] != 0:
                return -103
            if velocity[0] == 0:
                return -101
            if rframe <= (maxrframe/8) and velocity[0] > 0:
                return -105
            if (maxrframe*2/8) >= rframe > (maxrframe/8) and velocity[0] > 0:
                return -107
            if (maxrframe*3/8) >= rframe > (maxrframe*2/8) and velocity[0] > 0:
                return -109
            if (maxrframe*4/8) >= rframe > (maxrframe*3/8) and velocity[0] > 0:
                return -111
            if (maxrframe*5/8) >= rframe > (maxrframe*4/8) and velocity[0] > 0:
                return -113
            if (maxrframe*6/8) >= rframe > (maxrframe*5/8) and velocity[0] > 0:
                return -115
            if (maxrframe*7/8) >= rframe > (maxrframe*6/8) and velocity[0] > 0:
                return -117
            if rframe > (maxrframe*7/8) and velocity[0] > 0:
                return -119
        

    if direction[1] == 1 and direction[0] == -1:
        return 4
    if direction[1] == 1 and direction[0] == 1:
        return 5
    if direction[1] == -1 and direction[0] == -1: #if the player is falling and facing left
        return 4
    if direction[1] == -1 and direction[0] == 1: #if the player is falling and facing right
        return 5

    if direction[0] == -1 and direction[1] >= 0 and handstate == 0 and frame%120 < 60 and velocity[0] == 0: #if the player is facing left, not falling, has no handstate, is not moving
        return 0
    if direction[0] == -1 and direction[1] >= 0 and handstate == 0 and frame%120 >= 60 and velocity[0] == 0: #if the player is facing left, not falling, has no handstate, is not moving
        #placeholder, replace with idle animation state 1 facing left.
        return 10
    if direction[0] == 1 and direction[1] >= 0 and handstate == 0 and  frame%120 < 60 and velocity[0] == 0: #if the player is facing right not falling, has no handstate, is not moving
        return 1
    if direction[0] == 1 and direction[1] >= 0 and handstate == 0 and frame%120 >= 60 and velocity[0] == 0: #if the player is facing right, not falling, has no handstate, is not moving
        #placeholder, replace with idle animation state 1 facing right.
        return 11

    if direction[1] == 0 and handstate == 0 and rframe <= (maxrframe/8) and velocity[0] > 0: #if the player is moving right and not falling and has no handstate
        return 3
    if direction[1] == 0 and handstate == 0 and rframe <= (maxrframe/8) and velocity[0] < 0: #if the player is moving left and not falling and has no handstate
        return 2
    if direction[1] == 0 and handstate == 0 and (maxrframe*2/8) >= rframe > (maxrframe/8) and velocity[0] > 0: #2
        return 7 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and (maxrframe*2/8) >= rframe > (maxrframe/8) and velocity[0] < 0: #etc
        return 6 #placeholder, replace with running animation state n facing left
    if direction[1] == 0 and handstate == 0 and (maxrframe*3/8) >= rframe > (maxrframe*2/8) and velocity[0] > 0: #etc
        return 9 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and (maxrframe*3/8) >= rframe > (maxrframe*2/8) and velocity[0] < 0: #etc
        return 8 #placeholder, replace with running animation state n facing left
    if direction[1] == 0 and handstate == 0 and (maxrframe*4/8) >= rframe > (maxrframe*3/8) and velocity[0] > 0: #etc
        return 23 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and (maxrframe*4/8) >= rframe > (maxrframe*3/8) and velocity[0] < 0: #etc
        return 18 #placeholder, replace with running animation state n facing left
    if direction[1] == 0 and handstate == 0 and (maxrframe*5/8) >= rframe > (maxrframe*4/8) and velocity[0] > 0: #etc
        return 24 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and (maxrframe*5/8) >= rframe > (maxrframe*4/8) and velocity[0] < 0: #etc
        return 19 #placeholder, replace with running animation state n facing left
    if direction[1] == 0 and handstate == 0 and (maxrframe*6/8) >= rframe > (maxrframe*5/8) and velocity[0] > 0: #etc
        return 25 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and (maxrframe*6/8) >= rframe > (maxrframe*5/8) and velocity[0] < 0: #etc
        return 20 #placeholder, replace with running animation state n facing left
    if direction[1] == 0 and handstate == 0 and (maxrframe*7/8) >= rframe > (maxrframe*6/8) and velocity[0] > 0: #etc
        return 26 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and (maxrframe*7/8) >= rframe > (maxrframe*6/8) and velocity[0] < 0: #etc
        return 21 #placeholder, replace with running animation state n facing left
    if direction[1] == 0 and handstate == 0 and rframe > (maxrframe*7/8) and velocity[0] > 0: #etc
        return 27 #placeholder, replace with running animation state n facing right
    if direction[1] == 0 and handstate == 0 and rframe > (maxrframe*7/8) and velocity[0] < 0: #etc
        return 22 #placeholder, replace with running animation state n facing left


    if handstate == 1 and direction[0] == -1: #mining
        return 12
    if handstate == 2 and direction[0] == -1:
        return 13
    if handstate == 3 and direction[0] == -1:
        return 14
    if handstate == 4 and direction[0] == -1:
        return 28
    if handstate == 5 and direction[0] == -1:
        return 29
    if handstate == 6 and direction[0] == -1:
        return 30
    if handstate == 7 and direction[0] == -1:
        return 31
    if handstate == 1 and direction[0] == 1:
        return 15
    if handstate == 2 and direction[0] == 1:
        return 16
    if handstate == 3 and direction[0] == 1:
        return 17
    if handstate == 4 and direction[0] == 1:
        return 32
    if handstate == 5 and direction[0] == 1:
        return 33
    if handstate == 6 and direction[0] == 1:
        return 34
    if handstate == 7 and direction[0] == 1:
        return 35

    return -1
