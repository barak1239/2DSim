from entity import Entity
import random as rnd
class Plant(Entity):
    def __init__(self,steps,x,y):
        super().__init__(x,y)
        self.steps = steps
    def spawn(self,grid):
        for _ in range(10):
            spawned = False
            i = 0
            while(not spawned and i< 900):
                newx = rnd.randint(0, grid.height - 1)
                newy = rnd.randint(0, grid.width - 1)
                if grid.grid[newx][newy] is None:
                    spawned = True
                    newsteps = self.steps
                    newPlant = Plant(newsteps,newx,newy)
                    grid.addentity(newPlant)
                i+=1
    def update(self,grid):
        self.steps -= 1
        if (self.steps <= 0):
            grid.remove(self)






