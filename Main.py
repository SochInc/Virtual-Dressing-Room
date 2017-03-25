import tkinter as tk
from PIL import ImageTk

import detect_circle as cp
import cv2


def main():
    root = tk.Tk()

    # Code to add widgets will go here...
    def callback():
        cp.capture()

    canvas = tk.Canvas(root, width=1220, height=1000)
    canvas.pack()
    tk_img = ImageTk.PhotoImage(file="ecommerce.png")
    canvas.create_image(610, 500, image=tk_img)
    image = ImageTk.PhotoImage(file="phon.png")

    button = tk.Button(root, image=image, command=callback, activebackground="#33B5E5")
    button_window = canvas.create_window(500, 500, anchor='nw', window=button)
    root.mainloop()


if __name__ == '__main__':
    main()
