from utils import AlgoContext, Int

ctx = AlgoContext()
x = Int(int(input("Erste Zahl: ")), ctx)
y = Int(int(input("Zweite Zahl: ")), ctx)

while x > 0:
    if x < y:
        x, y = y, x
    x -= y
print(y)

print(f"Insgesamt gab es {ctx.subtractions} Subtraktionen.")
