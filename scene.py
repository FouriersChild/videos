from sys import builtin_module_names, modules
from typing_extensions import runtime
from manim import *
import numpy as np
import math

config["max_files_cached"] = 1000

class NumberPlaneExample(MovingCameraScene):
    def construct(self):
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
        mouseVelocityBrace = Brace(Line(mouseDot.get_center(), 0.25*LEFT), direction=Line(mouseDot.get_center(), 0.25*LEFT).rotate(PI/2).get_unit_vector())
        mouseVelocityText = mouseVelocityBrace.get_tex(r"\vec{m}")
        catVelocityBrace = Brace(Line(2*UP, 2*UP + LEFT), direction=Line(2*UP, 2*UP+LEFT).rotate(PI/2).get_unit_vector())
        catVelocityText = catVelocityBrace.get_tex(r"\vec{c}")
        catVelocityText2 = catVelocityBrace.get_tex(r"\vec{c} = 4 \vec{m}")
        catVelocity = Arrow(start=2*UP, end=2*UP+LEFT, buff=0)
        mouseVelocity = Arrow(start=[0,0,0], end=0.25*LEFT, buff=0)
        self.play(Write(catVelocity), Write(mouseVelocity))
        
        self.play(Write(mouseVelocityBrace), Write(catVelocityBrace))

        self.wait()

        self.play(Write(mouseVelocityText))

        self.wait()

        self.play(Write(catVelocityText))

        self.wait()

        self.play(Transform(catVelocityText, catVelocityText2))

        self.wait(3)

        self.play(FadeOut(catVelocity), FadeOut(mouseVelocity), FadeOut(mouseVelocityText), FadeOut(catVelocityText), FadeOut(mouseVelocityBrace), FadeOut(catVelocityBrace))
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
        self.play(lineEquationAt0.animate.shift(UP*1.5 + RIGHT*3).scale(0.5))
        self.wait()

        #moves mouseDot 2 units down
        self.play(mouseDot.animate(rate_func=linear).shift(2*DOWN), run_time=2)
        
        self.wait(4)

        circleEquation = MathTex(r"y^2 + x^2 = r^2", font_size=48)
        circleEquationEqualToY = MathTex(r"y = \pm\sqrt{r^2 - x^2}", font_size=48)
        self.play(Write(circleEquation))
        self.wait()
        self.play(TransformMatchingShapes(circleEquation, circleEquationEqualToY))
        self.play(circleEquationEqualToY.animate.shift(UP*0.5 + RIGHT*3).scale(0.5))
        self.wait()

        topArc = Arc(radius=2, start_angle=0, angle=PI, arc_center=np.array([0,0,0]))
        self.play(Write(topArc))
        self.wait()
        self.play(ApplyWave(topArc))

        #circleEquationToY and lineEquationAt0
        #y = \sqrt{r^2 - x^2} and y = \frac{m_y}{m_x}x
        
        equalEquations = MathTex(r"\frac{m_y}{m_x}x = \sqrt{r^2 - x^2}", font_size=48)
        solutionX = MathTex(r"x = \sqrt{\frac{r^2}{(\frac{m_y}{m_x})^2+1}}", font_size=48)
        solutionY = MathTex(r"y = \frac{m_y}{m_x} \sqrt{\frac{r^2}{(\frac{m_y}{m_x})^2+1}}", font_size=48)
        self.play(TransformMatchingShapes(circleEquationEqualToY, equalEquations), TransformMatchingShapes(lineEquationAt0, equalEquations))
        self.wait()
        self.play(TransformMatchingShapes(equalEquations,solutionX))
        self.wait()
        blah = solutionX.copy()
        self.play(TransformMatchingShapes(solutionX, solutionY.shift(DOWN)), blah.animate.shift(UP))

        solution1Dot = Dot(point=np.array([-math.sqrt(2),math.sqrt(2),0]))
        self.play(Write(solution1Dot))

        self.wait()

        self.play(Transform(solutionY, solution1Dot),TransformMatchingShapes(blah, solution1Dot))
        self.wait()

        #self.play(FadeOut(solution1Dot))
        #self.play(FadeOut(solutionY))
        self.play(FadeOut(solutionY), FadeOut(topArc))
        
        self.wait()

        #self.play(FadeOut(solution1Dot))

        #negative equal Equations
        equalEquations = MathTex(r"\frac{m_y}{m_x}x = -\sqrt{r^2 - x^2}", font_size=48)
        bottomArc = Arc(radius=2, start_angle=PI, angle=PI, arc_center=np.array([0,0,0]))
        self.play(Write(bottomArc))
        self.wait()
        self.play(ApplyWave(bottomArc))

        self.wait()

        self.play(Write(equalEquations))

        self.wait(3)

        solutionX = MathTex(r"x = -\sqrt{\frac{r^2}{(\frac{m_y}{m_x})^2+1}}", font_size=48)
        solutionY = MathTex(r"y = -\frac{m_y}{m_x} \sqrt{\frac{r^2}{(\frac{m_y}{m_x})^2+1}}", font_size=48)
        self.play(TransformMatchingShapes(equalEquations,solutionX))
        self.wait()
        blah = solutionX.copy()
        self.play(TransformMatchingShapes(solutionX, solutionY.shift(DOWN)), blah.animate.shift(UP))
        
        self.wait()
        

        solution2Dot = Dot(point=np.array([math.sqrt(2), -math.sqrt(2),0]))
        self.play(Write(solution2Dot))

        self.wait()

        self.play(Transform(solutionY, solution2Dot), TransformMatchingShapes(blah, solution2Dot))
        self.wait()

        self.play(FadeOut(solutionY), FadeOut(bottomArc))

        d1 = Brace(Line(mouseDot.get_center(), solution1Dot.get_center()),direction=Line(mouseDot.get_center(), solution1Dot.get_center()).rotate(PI/2).get_unit_vector())
        d1Text = d1.get_tex("d_1")

        d2 = Brace(Line(solution2Dot.get_center(), mouseDot.get_center()), direction=Line(mouseDot.get_center(), solution2Dot.get_center()).rotate(PI/2).get_unit_vector())
        d2Text = d2.get_tex("d_2")

        self.play(Write(d1))

        self.wait()

        self.play(Write(d1Text))

        self.wait()

        temp = d1.get_center()
        self.play(FadeOut(d1), d1Text.animate.move_to(temp).scale(0.6))

        self.wait()

        self.play(Write(d2))

        self.wait()

        self.play(Write(d2Text))

        self.wait()

        temp = d2.get_center()
        self.play(FadeOut(d2), d2Text.animate.move_to(temp).scale(0.6))

        self.wait()

        inequality = MathTex(r"d_1 < d_2", font_size=36).move_to(np.array([3,1.5,0]))
        self.play(TransformMatchingShapes(d2Text,inequality),TransformMatchingShapes(d1Text,inequality))

        self.play(FadeOut(d2Text), FadeOut(inequality))

        self.wait(3)

        self.play(Circumscribe(solution2Dot))

        self.wait()

        self.play(FadeOut(solution2Dot), FadeOut(solution1Dot))

        self.wait()

        #moves mouse two units to the left
        self.play(mouseDot.animate(rate_func=linear).shift(2*LEFT), run_time=2)

        self.wait()

        solution2Dot = Dot(point=np.array([-math.sqrt(2), -math.sqrt(2),0]), z_index=2)
        solution1Dot = Dot(point=np.array([math.sqrt(2), math.sqrt(2),0]))

        self.play(Write(solution2Dot), Write(solution1Dot))

        self.wait()

        self.play(Circumscribe(solution2Dot))

        self.wait(3)

        self.play(FadeOut(solution1Dot))
        #catDirection

        self.wait()

        catDot = Dot([0,2,0], z_index=2)

        self.play(Write(catDot))

        self.wait()

        self.play(Circumscribe(solution2Dot))

        self.wait()

        self.play(Circumscribe(catDot))

        self.wait()

        #render quadrants
        quadrant1 = Square(color=GREEN, fill_opacity=0.4, stroke_opacity=0, z_index=5).set(height=6, width=6)
        quadrant1.move_to([quadrant1.width/2, quadrant1.height/2, 0])

        quadrant3 = Square(color=GREEN, fill_opacity=0.4, stroke_opacity=0, z_index=5).set(height=6, width=6)
        quadrant3.move_to([-quadrant3.width/2, -quadrant3.height/2, 0])

        self.play(FadeIn(quadrant1), FadeIn(quadrant3))

        self.wait()

        topArc = Arc(color=BLUE, radius=2, start_angle=PI/4, angle=PI, arc_center=ORIGIN, z_index=1)
        bottomArc = Arc(color=BLUE, radius=2, start_angle=5*PI/4, angle=PI, arc_center=ORIGIN, z_index=1)

        self.play(Write(topArc))

        self.wait()

        self.play(Wiggle(quadrant1))

        clockwise = MarkupText(f'clockwise', font_size=18, z_index=6).shift(1.5*UP + 2.75*RIGHT)
        counterclockwise = MarkupText(f'counterclockwise', font_size=18, z_index=6).shift(1.5*UP + 2.75*RIGHT)
        #return clockwise
        rotation = clockwise.copy()
        self.play(Write(rotation))

        self.wait()

        self.play(Wiggle(quadrant3))

        #return counterclockwise
        self.play(Transform(rotation,counterclockwise))

        self.play(FadeOut(catDot), Unwrite(topArc),FadeOut(rotation))

        self.wait()

        catDot = Dot([0,-2,0], z_index=2)

        self.play(Write(catDot))

        self.wait()

        self.play(Write(bottomArc))

        self.wait()

        self.play(Wiggle(quadrant1))

        #return counterclockwise
        rotation = counterclockwise.copy()
        self.play(Write(rotation))

        self.wait()

        self.play(Wiggle(quadrant3))

        #return clockwise
        self.play(Transform(rotation,clockwise))

        self.wait()

        self.play(Unwrite(bottomArc), FadeOut(quadrant1), FadeOut(quadrant3), FadeOut(rotation))

        self.play(Unwrite(solution2Dot), Unwrite(catDot))

        self.wait()

        self.play(mouseDot.animate(rate_func=linear).shift(2*UP), run_time=2)
        
        self.wait()

        solutionDot = Dot(point=np.array([-math.sqrt(2), math.sqrt(2),0]), z_index=2)
        self.play(Write(solutionDot))

        quadrant2 = Square(color=GREEN, fill_opacity=0.4, stroke_opacity=0, z_index=5).set(height=6, width=6)
        quadrant2.move_to([quadrant2.width/2, -quadrant2.height/2, 0])

        quadrant4 = Square(color=GREEN, fill_opacity=0.4, stroke_opacity=0, z_index=5).set(height=6, width=6)
        quadrant4.move_to([-quadrant4.width/2, quadrant4.height/2, 0])

        catDot = Dot([0,2,0], z_index=2)

        self.play(Write(catDot))

        self.wait()

        self.play(FadeIn(quadrant2), FadeIn(quadrant4))

        self.wait()

        topArc = Arc(color=BLUE, radius=2, start_angle=-PI/4, angle=PI, arc_center=ORIGIN, z_index=1)
        bottomArc = Arc(color=BLUE, radius=2, start_angle=3*PI/4, angle=PI, arc_center=ORIGIN, z_index=1)

        self.play(Write(topArc))

        self.wait()

        self.play(Wiggle(quadrant2))

        #return clockwise
        rotation = clockwise.copy()
        self.play(Write(rotation))

        self.wait()

        self.play(Wiggle(quadrant4))

        #return counterclockwise
        self.play(Transform(rotation, counterclockwise))

        self.play(FadeOut(catDot), Unwrite(topArc), FadeOut(rotation))

        catDot = Dot([0,-2,0], z_index=2)

        self.play(Write(catDot))

        self.wait()

        self.play(Write(bottomArc))

        self.wait()

        self.play(Wiggle(quadrant2))

        #return counterclockwise
        rotation = counterclockwise.copy()
        self.play(Write(rotation))

        self.wait()

        self.play(Wiggle(quadrant4))

        #return clockwise
        self.play(Transform(rotation, clockwise))

        self.wait()
