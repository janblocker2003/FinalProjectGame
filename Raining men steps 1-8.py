import pygame, simpleGE, random

""" it's raining men 1-6 steps
    Build your roster!
"""

class Men(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Men.png")
        self.setSize(25, 35)
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class BadGuy(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)
        self.colorRect("white", (25, 35))
        self.reset()
    
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)
    
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Guy(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Guy.gif")
        self.setSize(35, 45)
        self.position = (320, 400)
        self.moveSpeed = 7
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed

class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)

class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"
        self.center = (500, 30)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Beach.png")
        self.sndMen = simpleGE.Sound("DohSound.wav")
        self.numMens = 10
        
        self.numBadGuys = 3
        self.sndBadGuy = simpleGE.Sound("scream.mp3")
        
        self.score = 0
        self.lblScore = LblScore()
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 20
        self.lblTime = LblTime()
        
        self.guy = Guy(self)
        
        self.mens = []
        for i in range(self.numMens):
            self.mens.append(Men(self))
            
        self.badGuys = []
        for i in range(self.numBadGuys):
            self.badGuys.append(BadGuy(self))
        
        self.sprites = [self.guy,
                        self.mens,
                        self.lblScore,
                        self.lblTime,
                        self.badGuys]

    def process(self):
        for men in self.mens:
            if men.collidesWith(self.guy):
                self.sndMen.play()
                men.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
        
        for badGuy in self.badGuys:
            if badGuy.collidesWith(self.guy):
                self.sndBadGuy.play()
                badGuy.reset()
                self.score -= 1
                self.lblScore.text = f"Score: {self.score}"
        
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            self.stop()

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        
        self.prevScore = prevScore
        
        self.setImage("Beach.png")
        self.response = "Quit"
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are a guy on vacation.",
        "Move with the left and right arrow keys.",
        "Build your roster by catching as many men",
        "as possible in your time provided.",
        "",
        "Good Luck!"]
        
        self.directions.center = (320, 200)
        self.directions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last Score: 0"
        self.lblScore.center = (320,400)
        
        self.lblScore.text = f"Last score: {self.prevScore}"
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
    
    
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()

def main():
    
    keepGoing = True
    lastScore = 0
    
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False
    
if __name__ == "__main__":
    main()