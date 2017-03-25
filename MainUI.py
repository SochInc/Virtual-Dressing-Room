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
    image = Image.open("ecommerce.png")
    image = image.resize((w,h), Image.ANTIALIAS)
    tk_img = ImageTk.PhotoImage(image)
    canvas.create_image(w/2, h/2, image=tk_img)
    image = ImageTk.PhotoImage(file="phon.png")

    button = tk.Button(root, image=image, command=callback, activebackground="#33B5E5")
    button_window = canvas.create_window(500, 500, anchor='nw', window=button)
    root.mainloop()


if __name__ == '__main__':
    main()
