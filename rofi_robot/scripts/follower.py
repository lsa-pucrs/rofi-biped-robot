import time
import rospy
from std_msgs.msg import String, Int32, Float64

class follower:
    def __init__(self):
        self.name = "follower"

        self.pubGOAL = rospy.Publisher('/follower/goal', String, queue_size = 10)

        self.memory = []

        self.quad, self.dist = None, None

        self.changeQuad = True
        self.changeDist = True
    # this functions takes the quadrant and the distance from the blob finder and returns a goal for the rofi class
    # quad, dist as variables accessed by other threads
    def setQuad(self, quad):
        if self.changeQuad:
            self.quad = quad
            self.changeQuad = False

    def setDist(self, dist):
        if self.changeDist:
            self.dist = dist
            self.changeDist = False

    def run(self):
        goal = String()

        while not rospy.is_shutdown():
            if self.quad == None or self.dist == None:
                continue

            # create memories of the last 25 quadrants the ball was
            if len(self.memory) < 25:
                self.memory.insert(0, quad)
            elif len(self.memory) > 25:
                while len(self.memory) > 25:
                    del self.memory[-1]

            # if the distance from the ball is less than 10(cm) then halts
            if self.dist < 10:
                goal.data = 'stay'
            else:
                if self.quad != 0:
                    if self.quad == 1 or self.quad == 4:
                        goal.data = 'left'
                    elif self.quad == 3 or self.quad == 6:
                        goal.data = 'right'
                    else:
                        goal.data = 'forward'
                else:
                    # search in memory the last quadrant the ball was
                    found = False

                    for m in self.memory:
                        if m != 0:
                            found = True

                            if m == 1 or m == 4:
                                goal.data = 'left'
                            elif m == 3 or m == 6:
                                goal.data = 'right'
                            else:
                                goal.data = 'forward'

                    # in case it haven't found anything
                    if not found:
                        goal.data = 'stay'

            self.pubGOAL.publish(goal)

            self.dist = None
            self.quad = None

            self.changeDist = True
            self.changeQuad = True

# ============================================================================ #

FOLLOWER = follower()

if __name__ == '__main__':
    rospy.init_node(FOLLOWER.name, anonymous = False)
    rospy.Subscriber('/follower/quad', Int32, FOLLOWER.setQuad)
    rospy.Subscriber('/follower/dist', Float64, FOLLOWER.setDist)
    FOLLOWER.run()
