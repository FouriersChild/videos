from sys import builtin_module_names
from manim import *
import numpy as np
import math

class NumberPlaneExample(MovingCameraScene):
    
    def construct(self):
        def trackMinDistancePoint(mobject, mouseDot):
            minDistancePoint = getMinDistancePoint(np.array([0,0]), 2, np.array([mouseDot.get_center()[0], mouseDot.get_center()[1]]))
            mobject.move_to([minDistancePoint[0],minDistancePoint[1],0])
        def trackLineThroughPoint(mobject, mouseDot):
            #thingLine = Line(start=mouseDot.get_center()*-5, end=mouseDot.get_center()*5)
            mobject.put_start_and_end_on(start=mouseDot.get_center()*-5, end=mouseDot.get_center()*5)
        #writes number plane
        number_plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 4,
                "stroke_opacity": 0.3
            }
        )
        self.play(Write(number_plane))

        #writes circle
        thing = Circle(radius=2,fill_opacity=0.5)
        self.play(Write(thing))
        #mouse
        mouseDot = Dot()
        self.play(Write(mouseDot))

        #catVector
        #,max_tip_length_to_length_ratio = 0.25
        
        catVelocity = Arrow(start=2*UP, end=2*UP+LEFT, buff=0)
        mouseVelocity = Arrow(start=[0,0,0], end=0.25*LEFT, buff=0)
        self.play(Write(catVelocity), Write(mouseVelocity))
        
        self.play(FadeOut(catVelocity), FadeOut(mouseVelocity))

        ## how the mouse moves
        # some max velocity
        # pythagorean theorem
        
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=thing.width*2).move_to(thing))


        ## how the cat moves
        # minDistancepoint

        self.play(mouseDot.animate.shift(UP+RIGHT))
        self.wait()

        thingLine = Line(start=mouseDot.get_center()*-5, end=mouseDot.get_center()*5)
        thingLine.add_updater(lambda mobject: trackLineThroughPoint(mobject, mouseDot))
        self.play(Write(thingLine))
        self.wait(3)

        slope = MathTex(r"\frac{m_y - c_y}{m_x - c_x}", font_size=48)
        slopeWithoutCenter = MathTex(r"\frac{m_y}{m_x}", font_size=48)

        self.play(Write(slope))
        self.play(Transform(slope,slopeWithoutCenter))
        
        lineEquation = MathTex(r"y = \frac{m_y}{m_x} (x - c_x) + c_y", font_size=48)
        lineEquationAt0 = MathTex(r"y = \frac{m_y}{m_x}x", font_size=48)
        self.play(TransformMatchingShapes(slope,lineEquation, path_arc=PI/2))
        self.wait(3)
        self.play(TransformMatchingShapes(lineEquation,lineEquationAt0, path_arc=PI/2))
        self.wait(3)

        #moves mouseDot 2 units down
        mouseDot.add_updater(lambda mobject, dt: mobject.shift(dt*DOWN))
        self.wait(2)
        mouseDot.clear_updaters()
        
        self.wait(4)

        circleEquation = MathTex(r"y^2 + x^2 = r^2", font_size=96)

        self.play(Write(circleEquation))
        self.play(circleEquation.animate.shift(UP*1.5 + RIGHT*3).scale(0.25))
        self.wait()

        bottomArc = Arc(radius=2, start_angle=PI, angle=PI, arc_center=np.array([0,0,0]))
        self.play(Write(bottomArc))
        self.wait()
        self.play(ApplyWave(bottomArc))

        self.wait(3)
        topArc = Arc(radius=2, start_angle=0, angle=PI, arc_center=np.array([0,0,0]))
        self.play(Write(topArc))
        self.wait()
        self.play(ApplyWave(topArc))

        



def getCatDirection(center, minDistancePoint, catPos):
    #returns 0 for clockwise, 1 for counterclockwise
    if center[0] == minDistancePoint[0]:
        if catPos[0] > center[0]:
            if minDistancePoint[1] > center[1]:
                return 0
            else:
                return 1
        else:
            if minDistancePoint[1] > center[1]:
                return 1
            else:
                return 0
    slope = (center[1] - minDistancePoint[1])/(center[0]-minDistancePoint[0])
    #equation is y = slope * (x - center[0]) + center[1]
    if slope >= 0:
        if catPos[1] < slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 0
            else:
                return 1
        elif catPos[1] > slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 1
            else:
                return 0
        else: 
            return 0
    else:
        if catPos[1] < slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 0
            else:
                return 1
        elif catPos[1] > slope * (catPos[0] - center[0]) + center[1]:
            if minDistancePoint[0] < center[0]:
                return 1
            else:
                return 0
        else:
            return 0
    

def getMinDistancePoint(center, radius, point):

    if center[0] == point[0]:
        if center[1] >= point[1]:
            return (center[0], center[1] - radius)
        else:
            return (center[0], center[1] + radius)
    
    slope = (point[1] - center[1])/(point[0] - center[0])

    point1x = math.sqrt(radius**2/(slope**2 + 1)) + center[0]
    point1y = slope * (point1x - center[0]) + center[1]

    point2x = -1 * math.sqrt(radius**2/(slope**2 + 1)) + center[0]
    point2y = slope * (point2x - center[0]) + center[1]

    dPoint1 = math.sqrt((point1y-point[1])**2+(point1x-point[0])**2)
    dPoint2 = math.sqrt((point2y-point[1])**2+(point2x-point[0])**2)
    if dPoint1 < dPoint2:
        return (point1x, point1y)
    else: 
        return (point2x, point2y)


def calculateThetaBasedOnPoint(center, point, radius):
    if point[0] == center[0]:
        if point[1] > center[1]:
            return 0
        else:
            return 180
    if point[1] == center[1]:
        if point[0] > center[0]:
            return 90
        else:
            return 270

    if point[0] >= center[0] and point[1] > center[1]:
        return math.degrees(math.asin(abs(point[0])/radius))
    elif point[0] > center[0] and point[1] <= center[1]:
        return math.degrees(math.acos(abs(point[0])/radius)) + 90
    elif point[0] <= center[0] and point[1] < center[1]:
        return math.degrees(math.asin(abs(point[0])/radius)) + 180
    else:
        return math.degrees(math.acos(abs(point[0])/radius)) + 270
#print(calculateThetaBasedOnPoint(np.array([0,0]), np.array([0,2]), 2))
#print(calculateThetaBasedOnPoint(np.array([0,0]), np.array([math.sqrt(2),math.sqrt(2)]), 2))