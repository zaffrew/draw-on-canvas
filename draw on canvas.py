# draw on a canvas

import tkinter as tk
from tkinter import colorchooser
import math
from PIL import Image


def reset_event_list(event):
    global event_list, event_count
    event_list = []
    event_count = 0

def get_brush_colour():
    global brush_hex
    rgb, new_hex = colorchooser.askcolor()
    brush_hex = new_hex
    
def clear_canvas():
    canvas.delete('all')

def draw_on_canvas(event):
    
##    print('Window coord:', event.x, event.y)
    
    # to use create_oval, canvas coordinates must be used
    # the ones abover are window coordinates
    
##    x = canvas.canvasx(event.x)
##    y = canvas.canvasy(event.y)

    global event_list, event_count, canvas_height, canvas_width, max_vel, sect_size
    global brush_hex

    x = event.x
    y = event.y
  
    event_list += [(x, y)]
    event_count += 1

    # event_list takes all the mouse click coords
    # event_count is used to access previous coords
    
##    print('Canvas coord:', x, y)

    prev_x, prev_y = x, y

    if event_count > 1:
        prev_x, prev_y = event_list[event_count - 2] # event_count - 1 will give current element
##        print(event_list)
##        print(event_count)
##        print('Previous', prev_x, prev_y)
##        print('Current', x, y)

    mouse_vel = (abs(x - prev_x) + abs(y - prev_y)) * 12

##    print('mouse_vel', mouse_vel)

    thickness_factor = 0

    # to make thickness reduce as speed increases
  
##    print('max vel', max_vel)
 
    for i in range(1, max_vel + 1, sect_size):
        # to get 10 sections out of 420
        if mouse_vel in range(i, i + sect_size):
            thickness_factor = mouse_vel // sect_size
            break
            # i want to bring thickness_factor between 0 and 9
            # it can go from 1 to around 423 so
            # we divide 420 into 10 parts of 42 size each
            # if the mouse_vel is in one of the parts
            # it gets a value 
            
    thickness = thickness_slider.get()
    if thickness > 1:
        thickness -= thickness_factor
    # if thickness becomes negative the negative sign is ignored?
    # so thickness increases with velocity. we dont want that.
    # at thickness 1, we cant decrease thickness further. 

##    print('Thickness', thickness)
    
    # get a circle/ellipse with x, y as centre
    ellipse_coord = (x + thickness, y + thickness, x - thickness, y - thickness)

    choice_val = radio_choice.get()
    if choice_val == 1:
        # Brush 1
        canvas.create_line(prev_x, prev_y, x, y, fill = brush_hex, width = thickness)
    elif choice_val == 2:
        # Brush 2
        canvas.create_oval(ellipse_coord, fill = brush_hex, width = 0)
    elif choice_val == 3:
        canvas.create_line(prev_x, prev_y, x, y, fill = 'white', width = thickness, smooth = 'TRUE', capstyle = 'ROUND')

app = tk.Tk()

event_list = []
event_count = 0

canvas_height = 500
canvas_width = 500

max_vel = int(((math.sqrt((canvas_height ** 2) + (canvas_width ** 2))) // 10)*5)

sect_size = max_vel // 10

canvas = tk.Canvas(app, width = canvas_width, height = canvas_height, bg = 'white')

canvas.bind('<B1-Motion>', draw_on_canvas) # button 1 is mouse left click
# when button 1 is clicked AND moved, the handler function is executed.
# events are passed as strings. the other arg is the handler function/callback

canvas.bind('<ButtonRelease-1>', reset_event_list)

# use '<Button-1>' for button 1 click only
# use '<Motion>' for motion of mouse
# use '<ButtonRelease-1>' for release of button 1

thickness_label = tk.Label(app, text = 'Thickness')
thickness_slider = tk.Scale(app, from_ = 1, to = 10, orient = 'horizontal')

brush_hex = 'black'
bg_hex = 'white'

colour_label = tk.Label(app, text = 'Colour')
colour_button = tk.Button(app, text = 'Brush Colour', command = get_brush_colour)

radio_choice = tk.IntVar()
radio_choice.set(1)

brush_label = tk.Label(app, text = 'Brush type')
brush_choice1 = tk.Radiobutton(app, text = 'Type 1', variable = radio_choice, value = 1)
brush_choice2 = tk.Radiobutton(app, text = 'Type 2', variable = radio_choice, value = 2)
brush_choice3 = tk.Radiobutton(app, text = 'Eraser', variable = radio_choice, value = 3)

clear_button = tk.Button(app, text = 'Clear canvas', command = clear_canvas)

canvas.grid(row = 0, column = 0, sticky = 'NSEW', columnspan = 4)
thickness_label.grid(row = 1, column = 0, sticky = 'SW')
thickness_slider.grid(row = 1, column = 1, sticky = 'SW')
colour_label.grid(row = 2, column = 0, sticky = 'SW')
colour_button.grid(row = 2, column = 1, sticky = 'SW')
brush_label.grid(row = 3, column = 0, sticky = 'SW')
brush_choice1.grid(row = 3, column = 1)
brush_choice2.grid(row = 3, column = 2)
brush_choice3.grid(row = 3, column = 3)
clear_button.grid(row = 4, column = 0, sticky = 'SW')


app.mainloop()
