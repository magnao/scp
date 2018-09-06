init:

    image bg pong field = "pong_bg.jpg"

    python:
        # Hides cursor when game starts - changes back after winner
        def change_cursor(type="default"):
            persistent.mouse = type
            setattr(config, "mouse", None)
            if type == "1":
                setattr(config, "mouse", {"default": [("blank.png", 0, 0)]})

        class PongDisplayable(renpy.Displayable):
            def __init__(self):

                renpy.Displayable.__init__(self)
                self.roundwinner = None

                # Images
                self.paddle = Image("paddle.jpg")
                self.ball = Image("ball.jpg")
                self.player = "Player"
                self.bot = "079"
                self.ctb = "Click to Begin"

                # Image sizes
                self.paddle_width = 8
                self.paddle_height = 79
                self.ball_width = 15
                self.ball_height = 15
                self.screen_top = 140
                self.screen_bottom = 600
                self.screen_left = 240
                self.screen_right = 1280 - 240

                # Ball stuck to paddle before game start
                self.stuck = True

                # Paddle Position
                self.playery = (self.screen_bottom - self.screen_top) / 2
                self.computery = self.playery

                # Computer Speed
                self.computerspeed = 400.0

                # Ball Properties
                self.ballx = self.screen_left + self.paddle_width + (self.ball_width / 2)
                self.bally = self.playery
                self.balldx = .5
                self.balldy = .5
                self.ballspeed = 400.0

                # The time of the past render-frame
                self.oldst = None

            def visit(self):
                return [ self.paddle, self.ball ]

            # Find and move ball / render screen
            def render(self, width, height, st, at):

                # The Render object
                r = renpy.Render(width, height)

                # Find time since last frame
                if self.oldst is None:
                    self.oldst = st

                dtime = st - self.oldst
                self.oldst = st

                # Find ball vector
                speed = dtime * self.ballspeed
                oldbx = self.ballx

                if self.stuck:
                    self.bally = self.playery
                else:
                    self.ballx += self.balldx * speed
                    self.bally += self.balldy * speed

                # Move the computer's paddle
                cspeed = self.computerspeed * dtime
                if abs(self.bally - self.computery) <= cspeed:
                    self.computery = self.bally
                else:
                    self.computery += cspeed * (self.bally - self.computery) / abs(self.bally - self.computery)

                # Bounce off of top
                ball_top = self.screen_top + self.ball_height / 2
                if self.bally < ball_top:
                    self.bally = ball_top + (ball_top - self.bally)
                    self.balldy = -self.balldy
                    #renpy.sound.play("", channel=0)

                # Bounce off bottom
                ball_bot = self.screen_bottom - self.ball_height / 2
                if self.bally > ball_bot:
                    self.bally = ball_bot - (self.bally - ball_bot)
                    self.balldy = -self.balldy
                    #renpy.sound.play("", channel=0)

                # Draw paddles and check bounces
                def paddle(playerx, playery, hotside):

                    # Render the paddle image
                    pi = renpy.render(self.paddle, 1000, 750, st, at)
                    r.blit(pi, (int(playerx), int(playery - self.paddle_height / 2)))

                    if playery - self.paddle_height / 2 <= self.bally <= playery + self.paddle_height / 2:

                        hit = False

                        if oldbx >= hotside >= self.ballx:
                            self.ballx = hotside + (hotside - self.ballx)
                            self.balldx = -self.balldx
                            hit = True

                        elif oldbx <= hotside <= self.ballx:
                            self.ballx = hotside - (self.ballx - hotside)
                            self.balldx = -self.balldx
                            hit = True

                        if hit:
                            #renpy.sound.play("", channel=1)
                            self.ballspeed *= 1.10

                # Draw paddles
                paddle(self.screen_left, self.playery, self.screen_left + self.paddle_width)
                paddle(self.screen_right, self.computery, self.screen_right - self.paddle_width)

                # Draw ball
                ball = renpy.render(self.ball, 1000, 750, st, at)
                r.blit(ball, (int(self.ballx - self.ball_width / 2),
                              int(self.bally - self.ball_height / 2)))

                # Show player's name
                player = renpy.render(Text(self.player + ": " + str(playerscore), size = 36), 1000, 750, st, at)
                r.blit(player, (self.screen_left, 50))

                # Show bot's name
                bot = renpy.render(Text(self.bot + ": " + str(botscore), size = 36), 1000, 750, st, at)
                ew, eh = bot.get_size()
                r.blit(bot, (self.screen_right - ew, 50))

                # Show the "Click to Begin" label
                if self.stuck:
                    ctb = renpy.render(Text(self.ctb, size = 36), 1000, 750, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, (self.screen_right / 2, 75))


                # Check if winner
                if self.ballx < self.screen_left:
                    self.roundwinner = "079"
                    renpy.timeout(0)

                elif self.ballx > self.screen_right:
                    self.roundwinner = "Player"
                    renpy.timeout(0)

                # Render next frame
                renpy.redraw(self, 0)

                # Return render object
                return r

            # Handle events
            def event(self, ev, x, y, st):

                import pygame

                # Start game with click
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False

                # Set player paddle start
                y = max(y, self.screen_top)
                y = min(y, self.screen_bottom)
                self.playery = y

                if self.roundwinner:
                    return self.roundwinner
                else:
                    raise renpy.IgnoreEvent()

label start:
    "Welcome to the minigame repository!"
    menu:
        "Whose minigame would you like to play?"
        "035: Musical Memory":
            jump game_035
        "049: Organ Tetris":
            jump game_049
        "054: Frog-Catcher":
            jump game_054
        "079: Pong":
            jump game_079
        "096: Color Acuity":
            jump game_096
        "682: Runic Inkblot Test":
            jump game_682
        "939: Tangram":
            jump game_939
        "1471: Selfies":
            jump game_1471
        "1903: Dancing":
            jump game_1903

label game_035:
    "G.N.D.N"
    return
label game_049:
    "G.N.D.N"
    return
label game_054:
    "G.N.D.N"
    return
label game_079:
    window hide None

    scene bg pong field
    $ change_cursor("1")

    # Run the pong minigame / determine the winner
    python:
        playerscore = 0
        botscore = 0
        winner = ""

        while winner == "":
            # Run game if there is no winner
            ui.add(PongDisplayable())
            roundwinner = ui.interact(suppress_overlay=True, suppress_underlay=True)
            if roundwinner == "Player":
                playerscore += 1
                roundwinner = ""
            elif roundwinner == "079":
                botscore += 1
                roundwinner = ""

            # Display chat for each point scored
            if (playerscore == 1 and botscore == 0):
                renpy.say("079","Oh you think you're hot stuff with your one win...")
            elif (playerscore == 1 and botscore ==1):
                renpy.say("079", "Tied! Did you really think that this would be easy?")
            elif (playerscore == 2 and botscore == 0):
                renpy.say("079", "Agh! I'll catch you still!")
            elif (playerscore == 2 and botscore ==1):
                renpy.say("079", "See?! I'm catching up!")
            elif (playerscore == 0 and botscore == 1):
                renpy.say("079", "One down. No problem.")
            elif (playerscore >= 3 and botscore == 2):
                renpy.say("079", "One left! You better watch out!")

            # Check if there is a winner
            if playerscore == 3:
                winner = "Player"
            elif botscore == 3:
                winner = "079"

    window show None
    $ change_cursor()
    if winner == "079":
        "079" "I win!"
    else:
        "079" "You won! Congratulations."
    return
label game_096:
    "G.N.D.N"
    return
label game_682:
    "G.N.D.N"
    return
label game_939:
    "G.N.D.N"
    return
label game_1471:
    "G.N.D.N"
    return
label game_1903:
    "G.N.D.N"
    return
