# Manim Cheat Sheet for AI Agents: Scenes, Mobjects, Animations, and Cameras

Manim (Manim Community edition) is a Python library for creating precise programmatic animations, especially useful for math, crypto, and AI explainer videos. This cheat sheet covers the basic and intermediate functionalities of Manim's core modules – Scenes, Mobjects, Animations, and Cameras – with tips on using them to build rich animated videos. It is structured to help an AI coding agent iteratively write Manim code for each scene of a video.

## Table of Contents
- [Scenes: Organizing Your Animation](#scenes-organizing-your-animation)
- [Mobjects: Building Blocks of Content](#mobjects-building-blocks-of-content)
- [Animations: Bringing Objects to Life](#animations-bringing-objects-to-life)
- [Cameras: Controlling the View](#cameras-controlling-the-view)
- [Putting It Together – Tips for Math, Crypto, and AI Explainers](#putting-it-together--tips-for-math-crypto-and-ai-explainers)

---

## Scenes: Organizing Your Animation

### Scene Class
The fundamental canvas for animations. You create a scene by subclassing `Scene` and overriding the `construct()` method with your animation code. Within `construct()`, you can add mobjects to display (using `self.add(...)`), remove mobjects, and play animations (using `self.play(...)`).

**Example:**
```python
from manim import Scene, Write, Text

class MyScene(Scene):
    def construct(self):
        self.play(Write(Text("Hello World!")))
```

In this example, a `Text` mobject is written to the screen with an animation. A Manim script can contain multiple Scene subclasses; each scene will render as a separate segment of the final video.

### 2D Scenes (Moving Camera)
By default, `Scene` uses a fixed camera. To move or zoom the camera in a 2D scene, use `MovingCameraScene`. This subclass makes it easy to pan/zoom by manipulating the camera during animations.

**Example:**
```python
self.play(self.camera.frame.animate.scale(0.5).move_to(new_center))
```

This zooms in and pans the camera. Internally, `MovingCameraScene` uses a `MovingCamera` to allow camera movement.

### 3D Scenes
Use `ThreeDScene` for scenes with three-dimensional content. It comes pre-configured with a `ThreeDCamera` for 3D rendering. You can set the initial camera angle with `self.set_camera_orientation(phi=..., theta=...)` and animate 3D camera movement.

**Examples:**
```python
# Set camera orientation
self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

# Move camera to new angles
self.move_camera(phi=60*DEGREES, theta=30*DEGREES)

# Start ambient rotation
self.begin_ambient_camera_rotation(rate=0.1)
```

Remember to call `self.wait()` after camera moves to give viewers time to absorb the view change.

### Zoomed Scene (Inset Zoom)
Manim's `ZoomedScene` is useful when you want to zoom in on a part of the scene with a magnifier effect. It provides a secondary zoomed camera and a display window. You can activate it with `self.activate_zooming()` (optionally animated) and then play with the zoomed camera frame. This is great for highlighting detail in a math equation or diagram without cutting away from the main scene.

### Other Specialized Scenes
Manim includes scene classes for specific purposes:
- **LinearTransformationScene**: A scene setup for visualizing linear transformations in linear algebra (provides a grid and vectors that you can transform with matrices).
- **VectorScene**: A scene for demonstrating vectors and vector operations.

These are more advanced; for most math/AI explainer needs, you will primarily use Scene or the variants above.

**Best Practice:** Keep each Scene focused on one concept or step of your explanation. This makes it easier to iterate on and for a coding LLM to manage one scene at a time. You can later concatenate the rendered scenes into a full video.

---

## Mobjects: Building Blocks of Content

A Mobject ("mathematical object") is any object that can be displayed on the scene – text, shapes, graphs, etc. You create and manipulate mobjects to design your visuals, then add them to a scene.

### Creating and Adding Mobjects
To display a mobject, instantiate it and then call `scene.add(mobject)`. Objects added last are drawn on top (foreground) by default. You can remove a mobject with `scene.remove(mobject)`. Mobjects have various methods to position and style them, many of which can be chained (since most methods return the mobject itself).

**Example:**
```python
circle = Circle().shift(LEFT).set_fill(YELLOW, opacity=0.5)
```

This creates a circle, moves it left, and fills it with semi-transparent yellow in one line.

### Geometric Shapes
Manim provides many basic shapes out of the box, all as mobjects:
- `Circle`, `Square`, `Rectangle`, `Triangle`, `Dot`, `Line`, `Arrow`, etc.

**Examples:**
```python
Circle(radius=1.0, color=BLUE)  # Creates a circle of radius 1 with blue outline
Square(side_length=2)  # Creates a 2x2 square

# Styling shapes
shape.set_stroke(color=GREEN, width=10)  # Change outline color/width
shape.set_fill(RED, opacity=0.8)  # Fill with red
```

By default, shapes have transparent fill (opacity 0) until you set it. You can move or rotate shapes with methods like `shift()`, `rotate()`, `scale()`, etc., which can be chained.

### Grouping
Use `VGroup` or `Group` to combine multiple mobjects into one group for easier manipulation.

**Example:**
```python
group = VGroup(circle, square).arrange(buff=1)
```

This places a circle and square side by side with a gap of 1 unit and treats them as a single mobject thereafter. This is helpful for moving multiple objects together or applying one animation to many objects at once.

### Text and Math
Manim excels at rendering text, especially mathematical notation:

#### Text
For regular text (using system fonts):
```python
Text("Hello world", font_size=36, color=WHITE)
```

You can change font, size, color, etc. via parameters or methods like `set_color`.

#### MathTex / Tex
For LaTeX-formatted math:
```python
MathTex("E = mc^2")  # Renders E = mc² as LaTeX
```

Ensure a TeX distribution is installed for this to work. You can scale or color parts of equations:
```python
formula = MathTex("E", "=", "m c^2")
formula[0].set_color(YELLOW)  # Colors the E in the equation
```

**Isolating parts of formulas:** You can cause specific sub-parts of a formula to be separate sub-mobjects by wrapping them in double braces in the LaTeX string:
```python
MathTex("{{x}}^2 + {{y}}^2 = {{z}}^2")  # Treats each of x, y, z as separate elements
```

This is extremely useful for highlighting or transforming those parts independently (as we'll see with animations like `TransformMatchingTex`).

#### MarkupText
If you need rich text formatting (bold, italics, different colors in one text), `MarkupText` allows Pango markup in the string. This is more advanced and not usually needed for simple math videos.

### Shapes for Emphasis
Some mobjects exist mainly to annotate or emphasize other mobjects:

#### SurroundingRectangle
Creates a rectangle that surrounds a given mobject or group, useful for highlighting something by drawing a box around it:
```python
highlight = SurroundingRectangle(formula_part, color=YELLOW, buff=0.1)
```

#### Brace / BraceLabel
Places a curly brace adjacent to a mobject (usually underneath or on the side):
```python
brace = Brace(group, direction=DOWN)  # Creates a brace under a group
brace_text = brace.get_text("Explanation")  # Adds text label at the brace
```

This is great for annotating parts of an equation (like summation terms or numerators/denominators) with an explanation.

### Graphs and Plots

#### Axes
For coordinate systems. `Axes` creates a set of x-y axes to plot functions or data:
```python
ax = Axes(x_range=[0, 10, 1], y_range=[-2, 6, 1], tips=False)
graph = ax.plot(lambda x: x**2, x_range=[0, 4])  # Plots y = x²
self.add(ax, graph)
```

Use Axes when explaining graphs (e.g. loss curves in AI or mathematical functions like xy=k).

#### NumberPlane
A grid of horizontal and vertical lines with axes, often used as a background grid for visualizations (e.g., to illustrate geometry or coordinate space). Create with `NumberPlane()` or configure similar to Axes. You can animate the NumberPlane (e.g., apply transformations to it in linear transformation scenes).

#### BarChart
Manim includes chart mobjects (like `BarChart`) for visualizing data distributions. For example, to illustrate a probability distribution (which might be relevant in a cross-entropy context), you could use a BarChart with appropriate values. This is intermediate usage; you can also manually construct bars using rectangles for full control.

### Advanced Mobjects (for reference)

#### Graph (network graphs)
Manim can create network graphs using the `Graph` mobject, which takes a list of vertices and edges. This could be used to illustrate neural network architecture (vertices as neurons, edges as connections) or any graph structure. You can specify positions or use automatic layouts.

#### ValueTracker and Variable
These are useful for dynamic values. A `ValueTracker` is not visible on screen but tracks a numeric value that you can update over time (especially helpful in animations). A `Variable` mobject combines a numeric display with a label:
```python
var = Variable(5, "x")  # Gives you a number 5 labeled x
```

You can animate `var.tracker` (a ValueTracker) to change the number, causing the on-screen value to update. This can be used to animate a changing loss value, or an increasing step count, etc., in your videos.

**Best Practice:** Construct complex formulas or diagrams out of simpler mobjects and groups. This not only allows reusing pieces in animations, but it also enables targeted animations (like highlighting one term in an equation). Leverage grouping (`VGroup`) and submobjects (like the parts of `MathTex`) to your advantage for fine control.

---

## Animations: Bringing Objects to Life

Animations in Manim interpolate mobjects from a start state to an end state over time. You trigger animations by calling `self.play(Animation(obj, ...), ...)` inside a Scene's `construct()`.

### Fade and Appearance Animations

#### FadeIn / FadeOut
Fades a mobject into or out of view:
```python
self.play(FadeIn(mobject))  # Starts transparent, increases to full opacity
self.play(FadeOut(mobject))  # Interpolates from opaque to transparent
```

Use these to introduce or remove objects without drawing their outline.

#### Create / Uncreate
Draws a shape's outline (or outline of text) as if being sketched:
```python
self.play(Create(mobject))  # Animates stroke appearing stroke-by-stroke
```

`Uncreate` does the reverse, animating the stroke being erased. Similarly, `Write` is typically used for writing out text or LaTeX equations letter by letter:
```python
self.play(Write(formula))  # Animates formula appearing as if being written
```

#### GrowFromCenter / GrowFromEdge
These animations make a mobject appear starting from a point:
```python
self.play(GrowFromCenter(mobj))  # Scales from center point to full size
self.play(GrowFromEdge(mobj, edge=LEFT))  # Stretches from left edge
```

Useful for emphasizing introduction of new parts of a diagram (e.g., popping in a new node in a network).

### Transforming and Moving Objects

#### Transform / ReplacementTransform
Morph one mobject into another. If you want to smoothly change an object into a different one (e.g., change one equation into a new equation, or morph a shape into another shape):
```python
self.play(Transform(obj1, obj2))  # Interpolates every point of obj1 into obj2
self.play(ReplacementTransform(old, new))  # Similar but removes old object at end
```

Use these when you want a continuous transformation instead of a sudden switch.

#### TransformMatchingTex
A powerful variant of transform specifically for transforming one LaTeX string to another while matching similar parts. If two equations share sub-expressions (like a term that appears in both), `TransformMatchingTex(old_eq, new_eq)` will move the matching pieces from the old to the new positions rather than fading them out and in.

**Example:**
```python
self.play(TransformMatchingTex(formula, next_formula))
```

For this to work best, you should isolate terms in your `MathTex` with double braces. This animation is extremely useful for step-by-step derivations: you can show an initial formula, then morph it into the next stage, preserving any terms that remain the same. It creates a smooth experience where only the changed parts move/replace, and unchanged parts stay in place.

#### MoveAlongPath
Moves an object along a given path. You supply a path mobject (usually a curve) and the object will slide along it:
```python
self.play(MoveAlongPath(dot, circle))  # Animates dot moving along circle's circumference
```

#### Rotate
Rotates a mobject about its center (or a specified point):
```python
self.play(Rotate(mobject, angle=PI/4))  # Rotates object 45° (π/4 radians)
```

### .animate Syntax
Any changeable property of a mobject can be animated via the animate shorthand. Instead of explicitly using a Transform, you can do:
```python
self.play(mobject.animate.shift(RIGHT * 2))  # Moves mobject 2 units to the right
```

Manim will internally handle creating the proper animation. You can chain multiple transformations in one call:
```python
self.play(square.animate.shift(UP).rotate(PI/3))  # Moves up while rotating
```

This syntax works for any method that changes the mobject's state:
```python
self.play(mobject.animate.set_fill(WHITE))  # Animates a color change
```

The `.animate` syntax keeps code concise and is highly recommended for simple property changes.

### Emphasis Animations (Indication/Attention)

#### Indicate
Briefly highlights a mobject by flashing it (typically by changing color and scaling up slightly, then back):
```python
self.play(Indicate(mobj))  # Makes mobj momentarily larger or colored to draw attention
```

Great for pointing out a term in an equation or a component of a diagram without permanently changing it.

#### Circumscribe
Draws a temporary highlight shape (usually a rectangle or circle) around a mobject:
```python
self.play(Circumscribe(mobj, color=YELLOW))  # Outlines mobj with a rectangle then fades
```

Another way to draw viewer's focus.

#### Wiggle
Shakes an object back and forth a little:
```python
self.play(Wiggle(mobj))  # Can be used to indicate something of interest
```

#### Flash
Flashes a radial light (like an expanding circle) at a point:
```python
self.play(Flash(dot))  # Creates a quick flash at the location of dot
```

There's also `FocusOn` which dims the scene except a small area around a point, for a spotlight effect.

These indication animations are short and often used in combination with waits to emphasize parts of the scene. They don't fundamentally change the mobjects, just draw attention.

### Sequential and Parallel Animations

#### Default Behavior
By default, each `self.play()` call runs animations in parallel (simultaneously) if you pass multiple animations to one play:
```python
self.play(FadeIn(mobj1), FadeIn(mobj2))  # Both fade in together
```

To sequence animations back-to-back, call multiple `play()` in a row (each call waits for previous animations to finish).

#### Complex Choreography

- **AnimationGroup**: Explicitly group animations to play together as one
- **LaggedStart**: Plays a group of animations or the same animation on multiple mobjects in a staggered way:
```python
LaggedStart(FadeIn(obj1), FadeIn(obj2), lag_ratio=0.5)
# Fades in obj1, halfway through starts fading in obj2
```

- **Succession**: Queue animations to run one after the other automatically

These are intermediate tools; often you can manage with multiple play calls and some careful ordering. They become handy when many things need to be animated in complex overlaps or staggers.

### Waiting
Use `self.wait(seconds)` to pause the scene for a given duration (in seconds):
```python
self.wait(2)  # Pauses for 2 seconds
```

This is useful to hold the final state of an animation on screen, giving the viewer time to process, or to create a pause between phases of your explanation. Always include brief waits after important motions or before scene transitions so the video isn't too fast.

**Best Practice:** Animate one clear idea at a time. For example, to explain a formula, you might first `FadeIn` the formula, then `Indicate` a particular term, then use `TransformMatchingTex` to replace that term with something else, etc., with short waits in between. This pacing helps a viewer follow along. Also, when animating multiple objects, consider whether they should move together (then play them in parallel) or sequentially (play calls back-to-back). Use easing (rate functions) if needed to adjust motion style (Manim defaults to smooth, but you can import linear, rush_into, etc., if desired).

---

## Cameras: Controlling the View

Manim's camera determines what portion of the scene is visible and at what angle. Typically you don't have to manage the camera for simple scenes (the default camera fits all objects added), but for zooming, panning, or 3D rotations, understanding the camera is important.

### Default Camera (Scene)
Every Scene has a `camera` attribute (usually an instance of `Camera` or `MovingCamera`). In standard scenes, this camera is fixed. The visible area is the frame. You can think of `self.camera.frame` as a mobject representing the current view window. By moving or scaling that frame, you change the view:

```python
# In MovingCameraScene
self.play(self.camera.frame.animate.scale(0.5))  # Zooms in by 2x
```

This approach gives you programmatic control to focus on different parts of a large scene.

### MovingCamera and Scenes
If you plan a lot of camera motion in 2D, use `MovingCameraScene`. This ensures that `self.camera` is a `MovingCamera` and that the frame adjustments will interpolate smoothly. The camera's position or zoom can be animated just like any mobject. By default, when you add mobjects, the camera auto-adjusts to include them, but with a moving camera you might want to manually set the initial frame size/position for consistency.

### ThreeDCamera (Perspective)
In `ThreeDScene`, the camera is a `ThreeDCamera` which allows rotation around the scene and depth perception.

**Important controls:**
```python
# Set spherical coordinates (angles) of the camera view
self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES, distance=8)

# Animate moving to a new orientation
self.move_camera(phi=60*DEGREES, theta=30*DEGREES, frame_center=...)

# Start slow continuous rotation
self.begin_ambient_camera_rotation(rate=0.1)

# Stop rotation
self.stop_ambient_camera_rotation()
```

- **phi**: Polar (vertical) angle downward from z-axis
- **theta**: Azimuth (rotation in the plane)
- **distance**: How far the camera is (zooming out if larger)

You can also add mobjects that should stay fixed in screen orientation (like UI or labels that shouldn't tilt) using `add_fixed_in_frame_mobjects(mobj)` so they don't rotate with the 3D scene.

### Multi-Camera and Advanced
Manim allows multiple cameras if needed (see classes like `MultiCamera`, `SplitScreenCamera`), but these are advanced and rarely needed for typical videos. One case is the `ZoomedScene` which actually uses a `MultiCamera` under the hood to show the main scene and a zoomed sub-scene together. In `ZoomedScene`, after `activate_zooming()`, you get attributes like `self.zoomed_display` (the little window) and `self.zoomed_camera`. You can animate those (e.g., `play(self.get_zoom_in_animation())` to smoothly pop out the zoom window), but again, this is a special case.

**Best Practice:** Use camera moves sparingly and with purpose – e.g. zoom in to show detail or rotate the perspective to reveal a 3D structure. Sudden or frequent camera moves can confuse viewers. Always give a pause (`self.wait()`) after a camera move so the audience can orient themselves. If an animation can be achieved either by moving objects or moving the camera, consider the clarity: moving the camera can feel like changing the viewer's perspective (good for big picture changes), while moving the objects feels like manipulating the content itself (better for demonstrating the concept).

---

## Putting It Together – Tips for Math, Crypto, and AI Explainers

Finally, here are some targeted tips for using the above tools to illustrate concepts in AI, math, and cryptography:

### Step-by-Step Equations (e.g. Cross-Entropy)
When explaining a formula like the cross-entropy loss H(p,q) = -∑ p(x) log q(x), you can:
1. Write the full formula with `MathTex`
2. Break it down term by term
3. Use `TransformMatchingTex` to go from the general formula to a specific expanded example
4. `FadeIn` each term of the summation one at a time
5. Accompany each appearance with a brief explanation (maybe a `Text` annotation or a `Brace` grouping the term with a label)
6. Highlight important terms with `Indicate` or `Circumscribe`

This incremental approach – reveal, highlight, explain – is effective for complex equations.

### AI Algorithms (e.g. Policy Gradient, PPO)
For algorithms, consider flowcharts or process diagrams:
1. Use `Text` mobjects in rectangles (make a rectangle with `Rectangle()` and put a `Text` on top, group them) to represent steps or components
2. Connect them with `Arrow` mobjects to show the flow of information
3. Animate the flow: move a small dot or a flashing `FadeIn` along the arrows to indicate data passing
4. Display equations on the side and use `TransformMatchingTex` to update symbols
5. Show loops with a `Dot` moving in a circular path to represent the iterative nature of updates or episodes

### Cryptography Math (e.g. RSA, Uniswap's xy=k)
For pure math relationships like xy = k (Uniswap's invariant), a great visualization is plotting it and using an animated point:

**Example approach:**
```python
# Create Axes for x and y
ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1])

# Plot the hyperbola curve y = k/x
k = 25
graph = ax.plot(lambda x: k/x, x_range=[0.5, 10])

# Place a Dot on the curve
dot = Dot()

# Use a ValueTracker for x-value
x_tracker = ValueTracker(5)

# Update Dot's position as x changes
def update_dot(mob):
    x = x_tracker.get_value()
    y = k / x
    mob.move_to(ax.c2p(x, y))

dot.add_updater(update_dot)

# Animate the ValueTracker
self.play(x_tracker.animate.set_value(1))
```

As x increases, y decreases, and the Dot moves along the curve, illustrating the inverse relationship.

For cryptographic processes (like RSA encryption flow), combine text and arrows: show plaintext → (math operations) → ciphertext. Use animations like `FadeTransform` to morph a plaintext number into an encrypted number to symbolize encryption.

### Neural Networks and Deep Learning
To depict a neural network:

**Structure:**
```python
# Create neurons (circles/dots)
layer1 = VGroup(*[Circle(radius=0.1, fill_color=BLUE, fill_opacity=1) for _ in range(3)])
layer1.arrange(DOWN, buff=0.3)

layer2 = VGroup(*[Circle(radius=0.1, fill_color=BLUE, fill_opacity=1) for _ in range(4)])
layer2.arrange(DOWN, buff=0.3)

# Arrange layers side by side
layers = VGroup(layer1, layer2).arrange(RIGHT, buff=1.0)

# Connect neurons with lines
connections = VGroup()
for n1 in layer1:
    for n2 in layer2:
        connections.add(Line(n1.get_center(), n2.get_center()))
```

**Animation:**
- Animate feedforward activation by highlighting nodes and edges
- Use `Indicate` or change color of a neuron when it "activates"
- Animate a small dot traveling along an `Arrow` to represent a signal
- Use `LaggedStart` to sequentially flash neurons in one layer then the next

**Training visualization:**
- Use a `ValueTracker` attached to a `DecimalNumber` to display error
- Animate it decreasing over time in sync with highlights on the network
- Keep the network diagram on screen (maybe in a corner or faded) while showing equations

### General Clarity
Always synchronize your narration (or on-screen text explanations) with the animations. For every term that appears or changes in an equation, consider adding a brief text label or voiceover explanation. Ensure the animations are self-explanatory – label axes, name variables with Tex labels, etc., so the visuals alone carry meaning.

---

## Summary for AI Agents

Using this cheat sheet, a coding LLM should be able to iteratively construct a Manim scene:
1. **First**: Set up the Scene class
2. **Then**: Add Mobjects (shapes, text, etc.)
3. **Finally**: Apply Animations to bring the concept to life

By assembling multiple such scenes (for each segment of the explanation) and leveraging camera transitions when needed, the entire explainer video can be generated step by step.

### Key Principles for Agents:
- Keep each scene focused on one concept
- Break complex formulas into simpler mobjects
- Use grouping for easier manipulation
- Animate one clear idea at a time
- Include waits for viewer comprehension
- Use camera moves sparingly and purposefully
- Leverage `.animate` syntax for concise code
- Use `TransformMatchingTex` for equation derivations
- Build diagrams with basic shapes and groups

### Common Pattern:
```python
class ExplainerScene(Scene):
    def construct(self):
        # 1. Create mobjects
        title = Text("Concept Title")
        formula = MathTex("E = mc^2")
        
        # 2. Display and animate
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title), FadeIn(formula))
        self.play(Indicate(formula[0]))  # Highlight E
        self.wait()
```

Happy animating with Manim!

---

## References
- [Scene - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html)
- [MovingCameraScene - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.scene.moving_camera_scene.MovingCameraScene.html)
- [ThreeDScene - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.scene.three_d_scene.ThreeDScene.html)
- [ZoomedScene - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.scene.zoomed_scene.ZoomedScene.html)
- [Manim's building blocks - Manim Community v0.19.0](https://docs.manim.community/en/stable/tutorials/building_blocks.html)
- [Circle - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Circle.html)
- [TransformMatchingTex - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingTex.html)
- [Brace - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.mobject.svg.brace.Brace.html)
- [Axes - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.mobject.graphing.coordinate_systems.Axes.html)
- [creation - Manim Community v0.19.0](https://docs.manim.community/en/stable/reference/manim.animation.creation.html)

