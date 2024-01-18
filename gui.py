from pathlib import Path
from tkinter import *
# from tkinter.ttk import *
import tkinter.font as tkFont
from time import strftime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets")

# COLORS
dark = '#121212'
semi_dark = '#1e1e1e'
semi_semi_dark = '#2e2e2e'
purple = '#bb86fc'
light = '#bfbfbf'
semi_light = '#a8a8a8'
semi_semi_light = '#595959'
blue = '#397791'

# CONSTANTS
x_devices = [50, 350]
y_devices = [150, 650]
padding = 25
devices_titles = ["CLOCK", "IRRIGATION", "SOCKETS"]

# VARIABLES
active_devices = [0, 0, 1]
active_sockets = [1, 1, 0, 1]
water_level = 5
initial_zero = 0
initial_one = 1
initial_water_level = 0


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# LOGO
def draw_logo(image_home):
    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0, 0,
        950, 80,
        fill=purple,
        outline="")

    canvas.create_image(60, 40, image=image_home)

    canvas.create_text(
        100, 25,
        anchor="nw",
        text="PiHoMi",
        fill="#000000",
        font=("Inter Bold", 30 * -1)
    )

# DEVICES
def draw_devices(x_reference, y_reference, padding, devices_titles, active_devices, draw_image_icon, draw_image_checkbox):
    def toggle_device(index):
        active_devices[index] = 1 - active_devices[index]
        update_window()

    canvas.create_rectangle(
        x_reference[0], y_reference[0],
        x_reference[1], y_reference[1],
        fill=semi_dark,
        outline=""
    )
    canvas.create_text(
        x_reference[0] + padding + 10, y_reference[0] + padding + 10,
        anchor="nw",
        text="Devices",
        fill=light,
        font=tkFont.Font(family='Inter',
            size=30, weight='bold')
    )

    height_device = 60
    gap_after_text = 110

    icon_image_files = ["clock-light25x25.png", "water-light30x30.png", "socket-light-light-bcg30x30.png"]
    icon_image_disabled_files = ["clock-dark25x25.png", "water-dark30x30.png", "socket-dark-light-bcg30x30.png"]

    for i in range(3):
        def on_button_click(event, index=i):
            toggle_device(index)

        rectangle = canvas.create_rectangle(
            x_reference[0] + padding, y_reference[0] + gap_after_text + i * height_device + i * padding,
            x_reference[1] - padding, y_reference[0] + gap_after_text + (i+1) * height_device + i * padding,
            fill=semi_semi_dark,
            outline="",
            activefill=dark
        )

        draw_image_icon.append(PhotoImage(
            file=relative_to_assets(icon_image_files[i] if active_devices[i] == 1 else icon_image_disabled_files[i])))
        canvas.create_image(
            x_reference[0] + padding + 30, y_reference[0] + gap_after_text + i * height_device + i * padding + 30,
            image=draw_image_icon[i]
        )

        canvas.create_text(
            x_reference[0] + padding + 62, y_reference[0] + i * height_device + i * padding + gap_after_text + 23,
            anchor="nw",
            text=devices_titles[i],
            fill=semi_light if active_devices[i] == 1 else semi_semi_light,
            font=tkFont.Font(family='Inter', size=13, weight='bold')
        )
        draw_image_checkbox.append(PhotoImage(
            file=relative_to_assets("checkbox-yes15x15.png" if active_devices[i] == 1 else "checkbox-no15x15.png")))
        canvas.create_image(
            x_reference[0] + padding + 225, y_reference[0] + gap_after_text + i * height_device + i * padding + 30,
            image=draw_image_checkbox[i]
        )

        canvas.tag_bind(rectangle, '<Button-1>', on_button_click)


# SOCKETS
def draw_sockets(x_reference, y_reference, padding, active_sockets):
    def toggle_sockets(index):
        active_sockets[index] = 1 - active_sockets[index]
        update_window()

    sockets_height = 200
    canvas.create_rectangle(
        x_reference[1] + 2 * padding, y_reference[0],
        window_size[0] - 2 * padding, y_reference[0] + sockets_height,
        fill=semi_dark,
        outline=""
    )

    canvas.create_text(
        x_reference[1] + 100, y_reference[0] + padding,
        anchor="nw",
        text="Sockets",
        fill=light,
        font=tkFont.Font(family='Inter',
                         size=30, weight='bold')
    )

    for i in range(4):
        def on_button_click(event, index=i):
            toggle_sockets(index)

        draw_image_socket.append(PhotoImage(
            file=relative_to_assets("socket-light75x75.png" if active_sockets[i] == 1 else "socket-dark75x75.png")))
        image = canvas.create_image(
            x_reference[1] + i * (padding-10) + i * 90 + 140, y_reference[0] + 4*padding + 20,
            image=draw_image_socket[i]
        )
        canvas.tag_bind(image, '<Button-1>', on_button_click)

        text = canvas.create_text(
            x_reference[1] + i * (padding-10) + i * 90 + 107, y_reference[0] + 4*padding + 55,
            anchor="nw",
            text="{i}. enabled".format(i=i+1) if active_sockets[i] == 1 else "{i}. disabled".format(i=i+1),
            fill=semi_light if active_sockets[i] == 1 else semi_semi_light,
            font=tkFont.Font(family='Inter', size=10, weight='bold')
        )
        canvas.tag_bind(text, '<Button-1>', on_button_click)

    return sockets_height

# IRIGATION
def draw_irrigation(x_reference, y_reference, padding, sockets_height, water_level=1):
    irrigation_width = 200
    canvas.create_rectangle(
        x_reference[1] + 2 * padding, y_reference[0] + sockets_height + padding,
        x_reference[1] + 2 * padding + irrigation_width, y_reference[1],
        fill=semi_dark,
        outline=""
    )
    canvas.create_text(
        x_reference[1] + 2 * padding + 30, y_reference[0] + sockets_height + padding + 20,
        anchor="nw",
        text="Water level",
        fill=semi_light,
        font=tkFont.Font(family='Inter', size=15, weight='bold')
    )
    canvas.create_text(
        x_reference[1] + 2 * padding + 30, y_reference[0] + sockets_height + padding + 40,
        anchor="nw",
        text="irrigation",
        fill=semi_semi_light,
        font=tkFont.Font(family='Inter', size=10, weight='bold')
    )

    canvas.create_rectangle(
        x_reference[1] + 2 * padding + 75, y_reference[0] + sockets_height + padding + 75,
        x_reference[1] + 2 * padding + irrigation_width - 75, y_reference[1] - 125,
        fill=semi_semi_dark,
        outline=""
    )
    canvas.create_rectangle(
        x_reference[1] + 2 * padding + 75, y_reference[0] + sockets_height + padding + 75 + (7 - water_level) * 10,
        x_reference[1] + 2 * padding + irrigation_width - 75, y_reference[1] - 125,
        fill=blue,
        outline=""
    )

    return irrigation_width


# CLOCK
def draw_clock(x_reference, y_reference, padding, irrigation_width, sockets_height):
    canvas.create_rectangle(
        x_reference[1] + 3 * padding + irrigation_width, y_reference[0] + sockets_height + padding,
        window_size[0] - 2 * padding, y_reference[1],
        fill=semi_dark,
        outline=""
    )
    canvas.create_text(
        x_reference[1] + 3 * padding + irrigation_width + padding, y_reference[0] + sockets_height + padding + 20,
        anchor="nw",
        text="Clock",
        fill=light,
        font=tkFont.Font(family='Inter',
                         size=30, weight='bold')
    )

    def time():
        string = strftime('%H:%M')
        lbl.config(text=string)
        lbl.after(1000, time)

    # Styling the label widget so that the clock
    # will look more attractive
    lbl = Label(window, font=('calibri', 40, 'bold'),
                background=semi_dark,
                foreground=semi_light)

    lbl.place(x=x_reference[1] + 3 * padding + irrigation_width + 3 * padding,
              y=y_reference[0] + sockets_height + 3 * padding + 20)
    time()


def update_window():
    global active_devices, active_sockets, water_level, draw_image_icon, draw_image_checkbox, draw_image_socket
    water_level = (water_level - 1) % 8 # Increment water_level in the range of 0 to 7

    draw_image_icon = []
    draw_image_checkbox = []
    draw_image_socket = []

    draw_devices(x_devices, y_devices, padding, devices_titles, active_devices, draw_image_icon, draw_image_checkbox)
    sockets_height = draw_sockets(x_devices, y_devices, padding, active_sockets)
    irrigation_width = draw_irrigation(x_devices, y_devices, padding, sockets_height, water_level)
    draw_clock(x_devices, y_devices, padding, irrigation_width, sockets_height)
    # window.after(1000, update_window)

    # print('Active devices: ', active_devices, '\nActive sockets: ', active_sockets)


draw_image_icon = []
draw_image_checkbox = []
draw_image_socket = []

window = Tk()
window.geometry("950x625")
window.configure(bg=dark)
window_size = [950, 625]

canvas = Canvas(
    window,
    bg=dark,
    height=550,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

image_home = PhotoImage(file=relative_to_assets("home.png"))
draw_logo(image_home)
window.resizable(False, False)

update_window()
window.mainloop()
