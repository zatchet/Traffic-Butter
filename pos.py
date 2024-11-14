class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(x: {self.x}, y: {self.y})"
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Pos):
            return self.x == value.x and self.y == value.y
        return False