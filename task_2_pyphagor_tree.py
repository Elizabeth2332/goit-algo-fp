import turtle

screen = turtle.Screen()
t = turtle.Turtle()
t.speed(0)
t.left(90)      # look upwards
t.penup()
t.goto(0, -250)
t.pendown()


def pythagoras_tree(length, level):
    if level == 0:
        return

    # draw square
    t.forward(length)

    # left branch
    t.left(45)
    pythagoras_tree(length * 0.7, level - 1)

    # right branch
    t.right(90)
    pythagoras_tree(length * 0.7, level - 1)

    # tuern back to original position and angle
    t.left(45)
    t.backward(length)


# get recursion level from user
level = int(input("Enter recursion level (e.g. 8–12): "))

pythagoras_tree(100, level)

screen.mainloop()
