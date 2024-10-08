class CarGame(pyglet.window.Window):
    def __init__(self, agent):
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        # Initialize agent and other game components
        self.agent = agent
        self.batch = pyglet.graphics.Batch()
        self.static_lines = []  # Static lines for walls
        self.dynamic_lines = []  # Dynamic lines for car projections
        self.walls = []
        self.turnkeyspressed = [0, 0]
        
        # Initialize walls (track boundaries)
        self.init_walls()
        
        # Draw initial walls
        for wall in self.walls:
            self.static_lines.append(pyglet.shapes.Line(
                wall.start.x, wall.start.y, wall.end.x, wall.end.y, color=(0, 150, 150), batch=self.batch))

    def init_walls(self):
        # Initialize walls (similar to your original wall setup)
        self.walls.append(Wall((60, 235), (60, 130), self.agent))
        self.walls.append(Wall((60, 130), (169, 41), self.agent))
        # (Add more walls as needed...)

    def reset_game(self):
        # Reset the agent's state and clear all drawn elements
        self.agent.reset()
        self.dynamic_lines.clear()

    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.draw_game()
    
    def draw_game(self):
        # Clear old dynamic lines (projections)
        for line in self.dynamic_lines:
            line.delete()
        self.dynamic_lines.clear()

        # Draw the car, wheels, and other elements of the car environment
        x = self.agent.state[0]
        y = self.agent.state[1]
        th = self.agent.state[2]
        phi = self.agent.phi
        size = self.agent.size
        corners = self.agent.corners
        proj_angles = self.agent.projections[0]
        proj_lengths = self.agent.projections[1]
        st = self.agent.proj_start

        # Draw the car
        body = pyglet.shapes.Rectangle(x, y, size[0], size[1], color=self.agent.car_colour[:3], batch=self.batch)
        body.anchor_x = size[0] // 2
        body.rotation = 90 - th * 180 / pi

        # Draw car wheels
        wheel1 = pyglet.shapes.Rectangle(corners[3].x, corners[3].y, 3, 8, color=(255, 0, 0), batch=self.batch)
        wheel1.anchor_x = 3 // 2
        wheel1.anchor_y = 8 // 2
        wheel1.rotation = 90 - (th + phi) * 180 / pi

        wheel2 = pyglet.shapes.Rectangle(corners[2].x, corners[2].y, 3, 8, color=(255, 0, 0), batch=self.batch)
        wheel2.anchor_x = 3 // 2
        wheel2.anchor_y = 8 // 2
        wheel2.rotation = 90 - (th + phi) * 180 / pi

        # Draw Projections
        for i in range(len(proj_angles)):
            end_x = st.x + proj_lengths[i] * cos(proj_angles[i] + th)
            end_y = st.y + proj_lengths[i] * sin(proj_angles[i] + th)
            line = pyglet.shapes.Line(st.x, st.y, end_x, end_y, color=(255, 0, 0), batch=self.batch)
            self.dynamic_lines.append(line)

        # Draw other elements if necessary

        # Update wall distances for new state
        for wall in self.walls:
            wall.car_distance()
