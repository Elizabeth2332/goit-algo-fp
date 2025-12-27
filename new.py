import turtle

t = turtle.Turtle()
t.speed(0)
t.pensize(2)
t.color("#b22222")
t.hideturtle()


def y_tree(length, depth):
    if depth == 0:
        return

    # draw trunk
    t.forward(length)

    # save split point
    pos = t.position()
    heading = t.heading()

    # LEFT branch
    t.left(45)
    y_tree(length * 0.7, depth - 1)

    # return to split
    t.penup()
    t.goto(pos)
    t.setheading(heading)
    t.pendown()

    # RIGHT branch
    t.right(45)
    y_tree(length * 0.7, depth - 1)

    # return and go back down trunk
    t.penup()
    t.goto(pos)
    t.setheading(heading)
    t.pendown()
    t.backward(length)


# Start at TOP, pointing DOWN
t.penup()
t.goto(0, -250)
t.setheading(90)   # ⬅ THIS is the key line
t.pendown()

depth = int(input("Recursion depth (try 6–9): ") or "7")
y_tree(80, depth)

turtle.done()
