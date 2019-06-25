import spritesheet, pygame
 
class SpriteStripAnim(object):
    """ sprite strip animator
    This class provides an iterator (iter(), next(), and stop(), methods), 
    and a __add__() method for joining strips which comes in handy when a
    strip wraps to the next row. """
    
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        #-- Class Globals --#
        """ self is the SpriteStripAnim class """
        self.filename = filename
        ss = spritesheet.spritesheet(filename) # spritesheet.py module method
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
        
        #-- Class Methods --#
    def iter(self):
        """ advances to the next image """
        self.i = 0
        self.f = self.frames
        return self
    
    def next(self):
        """ returns the next image from the spritesheet """
        """ the clock is not part of the original code but
        was added because the game loop in the main module 
        has keyboard controlled movement and it requires a
        different speed for the keypress than it does for the 
        animation frame rate """
        clock = pygame.time.Clock() 
        clock.tick(60)
        if self.i >= len(self.images):
            if not self.loop: #loop is a boolean
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    
    def stop(self):
        """ lands on the first image of the spritesheet
        helpful when we are doing a character animation
        and don't want animation frames to run when the 
        character should be still """
        self.i = 1
        image = self.images[self.i]
        return image
    
    def __add__(self, ss):
        """ allows you to join strips.  This comes in 
        handy when you are joining images from more
        than one row """
        self.images.extend(ss.images)
        return self

