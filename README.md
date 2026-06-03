# Python-OpenGL-3D-Maze-Game
An interactive 3D maze and crystal collector application utilizing PyOpenGL for hardware-accelerated rendering and custom AABB collision algorithms.

A fully functional, custom-built 3D graphics rendering engine and interactive application developed entirely in Python using **Pygame** and **PyOpenGL**.

Instead of relying on modern, pre-packaged game engines (like Unity, Unreal, or Godot) to handle the heavy lifting, this project was developed to demonstrate a deep understanding of core computer graphics, 3D mathematics, spatial matrix transformations, and hardware-accelerated rendering pipelines.

## ⚙️ Core Architecture & Technical Features

### 1. Custom 3D Rendering Pipeline

* **Geometric Primitives from Scratch:** The engine does not load pre-made 3D models. Every entity in the game—from the structural walls of the maze to the interactive rotating pyramids—is drawn by manually defining vertices in 3D space (`glVertex3fv`) and connecting them via OpenGL primitives (`GL_QUADS`, `GL_TRIANGLES`).
* **Hardware-Accelerated UV Mapping:** Features explicit texture coordinate mapping (`glTexCoord2f`) applied directly to the geometric faces, allowing the GPU to seamlessly render seamless, repeating textures (like grass and brick walls) using `GL_TEXTURE_2D`.
* **Dynamic Projection Matrices:** The architecture seamlessly transitions between a 3D Perspective Matrix (`gluPerspective`) for the spatial environment rendering, and a 2D Orthographic Matrix (`gluOrtho2D`) to draw the HUD and UI elements directly onto the screen space.

### 2. Advanced First-Person Camera System

* **Mathematical View Orientation:** The first-person camera is completely custom-built. It translates mouse movement inputs into Euler angles (Yaw and Pitch), applying trigonometric functions (`math.cos`, `math.sin`) to calculate exact look-direction vectors and update the `gluLookAt` matrix in real-time.
* **Vector-Based Kinematics:** Player movement is calculated using cross products (`np.cross`) between the camera's forward vector and the world's 'up' vector. This ensures highly accurate strafing (left/right) and forward/backward movement relative to the player's current perspective.

### 3. Collision Detection Mathematics

* **AABB Intersection Algorithm:** Implements a custom Axis-Aligned Bounding Box (AABB) collision detection system. The engine constantly calculates the Euclidean distance and proximity vectors between the player's spatial radius and the surrounding grid boxes, effectively preventing the camera from clipping through solid geometry.
* **Interactive State Management:** Built-in event loops handle the state of the world dynamically. As the player's collision radius intersects with a collectible item's bounding box, the engine updates the inventory state and removes the entity from the rendering queue.

## 🛠️ Technical Stack & Dependencies

* **Programming Language:** Python 3.8+
* **Graphics API:** PyOpenGL / PyOpenGL_accelerate (Direct hardware interface)
* **Windowing & Input Management:** Pygame
* **Mathematics:** NumPy (For matrix and vector calculations)

## 🚀 How to Run the Source Code

1. Ensure your system's graphics drivers support OpenGL hardware acceleration.
2. Install the necessary Python dependencies via pip:
`pip install pygame pyopengl numpy`
3. Ensure the project directory maintains the following structure, with your assets located in the `textures/` folder:
* README.md
* jogo_opengl.py
* textures/
* chao_grama.jpg
* parede_tijolo.jpg
* cristl.png




4. Execute the application:
`python jogo_opengl.py`

## 🎮 Controls

* **Mouse:** Free-look camera (360-degree first-person view).
* **W / A / S / D:** Move Forward / Strafe Left / Move Backward / Strafe Right.
* **ESC:** Exit the application and unlock the mouse cursor.
