import tkinter as tk
from PIL import ImageTk, Image
import MainCam as cp


def main():
    root = tk.Tk()

    # Code to add widgets will go here...
    def callback():
        cp.capture()

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack()

    image = Image.open("bgtry.png")
    image = image.resize((w, h), Image.ANTIALIAS)
    tk_img = ImageTk.PhotoImage(image)
    bgcanvas = canvas.create_image(w / 2, h / 2, image=tk_img)

    image = ImageTk.PhotoImage(file="trial.png")
    button = tk.Button(root, image=image, command=callback, bd=0)
    button_window = canvas.create_window((w / 2) - 360, (h / 2) - (66 / 2) + 160, anchor='nw', window=button)

    next = ImageTk.PhotoImage(file="next.png")
    button1 = tk.Button(root, image=next, command=callback, bd=0)
    button_window = canvas.create_window(w - (w / 15), (h / 2), window=button1)

    prev = ImageTk.PhotoImage(file="prev.png")
    button1 = tk.Button(root, image=prev, command=callback, bd=0)
    button_window = canvas.create_window((w / 15), (h / 2), window=button1)

    root.mainloop()


if __name__ == '__main__':
    main()
