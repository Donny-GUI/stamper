from typing import Literal, Optional, Tuple, Union
from typing_extensions import Literal
import customtkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage
import os
import datetime

from customtkinter.windows.widgets.font import CTkFont

Label = tk.CTkLabel
Canvas = tk.CTkCanvas
Button = tk.CTkButton
Frame = tk.CTkFrame
Root = tk.CTk
Combo = tk.CTkComboBox
Entry = tk.CTkEntry


class UpdateBox(tk.CTkScrollableFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, scrollbar_fg_color: str | Tuple[str, str] | None = None, scrollbar_button_color: str | Tuple[str, str] | None = None, scrollbar_button_hover_color: str | Tuple[str, str] | None = None, label_fg_color: str | Tuple[str, str] | None = None, label_text_color: str | Tuple[str, str] | None = None, label_text: str = "", label_font: tuple | CTkFont | None = None, label_anchor: str = "center", orientation: Literal['vertical', 'horizontal'] = "vertical"):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, scrollbar_fg_color, scrollbar_button_color, scrollbar_button_hover_color, label_fg_color, label_text_color, label_text, label_font, label_anchor, orientation)
        self.width = width
        self.height = height
        self.lines = []
        self.configure(fg_color="black", bg_color="black")
        self.configure(label_text="Updates", width=1200, label_text_color="springgreen", label_fg_color="black")
        
    def write_message(self, message: str, font_size=12, message_color="green", font="Verdana", time_font_color="cyan"):
        t = datetime.datetime.now()
        frame = Frame(self, fg_color="black", bg_color="black")
        frame.pack(fill="x", anchor="nw", side="bottom")
        hour = t.strftime("%H")
        minute = t.strftime("%M")
        time = f"[ {hour}:{minute} ] ⋙"
        time_label = Label(frame, text=time, bg_color="black", fg_color="black", text_color=time_font_color)
        time_label.pack(side="left")
        message_label = Label(frame, text=message, font=(font, font_size), width=self.width-10, bg_color="black", fg_color="black", text_color=message_color)
        message_label.pack(side="left")
        self.lines.append((time_label, message_label))
        
    
      
class App:
    onehundred = range(0,100)
    
    def __init__(self) -> None:
        
        self.stamp_width = 16
        self.stamp_height = 16
        self.mousex = 0
        self.mousey = 0
        self.image = None
        self.photoimage = None
        self.image_height = None 
        self.image_width = None
        self.centerh = None
        self.centerw = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.tempfile = "tempimage"
        self.resize_factor = 8
        self.image_loaded = False
        self.subimages_saved = 0
        self.current_output_directory = "OUTPUT"
        self.image_is_hovered = False
        
        # Window Root
        self.root = Root()
        self.root.geometry("1200x900")
        self.root.title = "Stamper"
        self.root.bind("<Left>", self.move_subimage_left)
        self.root.bind("<Right>", self.move_subimage_right)
        self.root.bind("<KeyPress-Down>", self.move_subimage_down)
        self.root.bind("<KeyPress-Up>", self.move_subimage_up)
        self.root.bind("<Motion>", self.main_canvas_hovered)
        self.root.bind("<space>", self.save_subimage)
        
        
        # top Frame
        self.loading_frame = Frame(self.root, width=800, height=200, border_width=3)
        self.loading_frame.pack(fill="both", ipady=3)
        
        # Browse Button
        self.browse_button = Button(self.loading_frame, width=100, text="Browse")
        self.browse_button.pack(side="right")
        self.browse_button.bind("<Button-1>", self.browse_for_file)
        
        # filepath label
        self.filepath_label = Label(self.loading_frame, width=100, text="No File Loaded", bg_color="black", fg_color="green")
        self.filepath_label.pack(side="right", ipadx=4)
        
        
        # Frame For Main Canvas
        self.image_frame = Frame(self.root, width=1100, height=800)
        self.image_frame.pack(fill="both")
        
        # Main Canvas
        self.main_image = Canvas(self.image_frame, 
                                 width=800, 
                                 height=600)
        self.main_image.pack(side="left", padx=(0, 10))
        self.main_image.bind("<Enter>", self.set_is_hovered_image)
        self.main_image.bind("<Leave>", self.set_is_not_hovered_image)
        
        # Subimage Canvas
        self.sub_image_canvas = Canvas(self.image_frame, 
                                 width=round(self.stamp_width*self.resize_factor), 
                                 height=round(self.stamp_height*self.resize_factor))
        self.sub_image_canvas.pack(side="left", padx=(0,10))
        
        # SubImage Canvas Frame
        self.subimage_settings_frame = Frame(self.loading_frame, width=800, height=200)
        self.subimage_settings_frame.pack(side="left", padx=5)
        
        # Directory Ouput Label
        self.directory_output_label = Label(self.subimage_settings_frame, text="Output Directory: ")
        self.directory_output_label.pack(side="left", padx=1, pady=1)
        
        # Direcotry Output Entrybox
        self.directory_output_entry = Entry(self.subimage_settings_frame, width=100, placeholder_text=self.current_output_directory)
        self.directory_output_entry.pack(side="left", padx=1, pady=1)
        
        # Directory Output Button
        self.directory_output_button = Button(self.subimage_settings_frame, width=100, text="Set Directory")
        self.directory_output_button.pack(side="right", padx=1, pady=1)
        
        # Frame for Box Width Combo
        self.loading_width_frame = Frame(self.loading_frame, width=800, height=200)
        self.loading_width_frame.pack(side="left")
        
        
        # Width combo Label
        self.width_label = Label(self.loading_width_frame, 
                                 text="Width: ")
        self.width_label.pack(fill="both")
        
        # Width Combo
        self.stamp_width_combo = Combo(self.loading_width_frame, 
                                       width=100, 
                                       values=[str(x) for x in self.onehundred],
                                       command=self.width_chosen)
        self.stamp_width_combo.pack(fill="both") 
        self.stamp_width_combo.set(self.stamp_width)
        self.stamp_width_combo.bind("<<ComboboxSelected>>", self.width_chosen)
        
        # Frame For Height Combo
        self.loading_height_frame = Frame(self.loading_frame, 
                                          width=800, 
                                          height=200)
        self.loading_height_frame.pack(side="left")
        
        # Height Combo Label
        self.height_label = Label(self.loading_height_frame, 
                                  text="Height: ")
        self.height_label.pack(fill="both")
        
        # Height Combo
        self.stamp_height_combo = Combo(self.loading_height_frame, 
                                        width=100, 
                                        values=[str(x) for x in self.onehundred],
                                        command=self.height_chosen)
        self.stamp_height_combo.pack(fill="both")
        self.stamp_height_combo.set(self.stamp_height)
        
        self.updates_box = UpdateBox(self.root)
        self.updates_box.pack(side="bottom", padx=5, pady=10)
        
        self.updates_box.write_message("Application Loaded")
        self.root.after(1000, lambda: self.updates_box.write_message("Select a File to Get to work with the Browse button at the top right", font_size=20))
        self.root.after(2000, lambda: self.updates_box.write_message("use Arrow Keys to move the box once you have clicked your desired image", font_size=20, message_color="red"))
    
    
    def set_is_not_hovered_image(self, *args):
        self.image_is_hovered = False
    
    def set_is_hovered_image(self, *args):
        self.image_is_hovered = True
    
    def create_rectangle_coordinates(self):
        self.centerh = round(self.stamp_height/2)
        self.centerw = round(self.stamp_width/2)
        self.x1 = self.mousex - self.centerh
        self.y1 = self.mousey + self.centerw
        self.x2 = self.mousex + self.centerw
        self.y2 = self.mousey - self.centerh
    
    def main_canvas_hovered(self, *args):
        self.get_mouse_position(args[0])
        if self.image != None:
            if self.image_is_hovered is True:
                self.draw_image()
                self.create_rectangle_coordinates()
                self.main_image.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline="blue")
                
                
    def save_rectangle_location(self):
        self.rectangle_x1 = self.x1
        self.rectangle_x2 = self.x2 
        self.rectangle_y1 = self.y1 
        self.rectangle_y2 = self.y2
        self.updates_box.write_message(f"Area Selected [ {self.x1} {self.y1} {self.x2} {self.y2} ] ")
    
    def browse_for_file(self, *args):
        self.updates_box.write_message("File Browse")
        filedialog = tk.filedialog.askopenfilename()
        if filedialog != None:
            self.filepath_label.configure(text=filedialog)
            self.root.bind("<Button-1>", self.get_subimage)
            self.image_loaded = True
            self.image_extension = os.path.splitext(filedialog)[1]
            self.image_format = self.image_extension.split('.')[1].upper()
            self.image = filedialog
            self.photoimage = PhotoImage(file=self.image)
            self.image_height = self.photoimage.height()
            self.image_width = self.photoimage.width()
            self.main_image.configure(width=self.image_width, height=self.image_height)
            self.draw_image()
            self.updates_box.write_message(f"Image Loaded [ {filedialog} ]")
        else:
             self.updates_box.write_message("File Browse Cancelled")
    
    def draw_image(self):
        self.main_image.create_image(0, 0, anchor="nw", image=self.photoimage)
    
    def get_mouse_position(self, event, *args):
        self.mousex = event.x
        self.mousey = event.y
    
    def get_subimage(self, *args):
        self.get_mouse_position(args[0])
        self.create_rectangle_coordinates()
        self.save_rectangle_location()
        self.extract_subimage()
        self.draw_subimage()
        self.updates_box.write_message("Subimage Selected")
    
    def extract_subimage(self):
        self._subimage = Image.open(self.image)
        self.tempfile = os.path.join(os.getcwd(), "tempfile" + self.image_extension)
        self.subimage = self._subimage.crop((self.x1, self.y2, self.x2, self.y1))
        
        self.subimage = self.subimage.resize(
            (round(self.stamp_width*self.resize_factor), round(self.stamp_height*self.resize_factor)))
        
        self.subimage.save(self.tempfile, format=self.image_format)
        self.sub_photoimage = PhotoImage(file=self.tempfile)
    
    def move_rectangle_right(self):
        self.updates_box.write_message("Moving right")
        self.rectangle_x1+=1
        self.rectangle_x2+=1
    
    def move_rectangle_left(self):
        self.updates_box.write_message("Moving left")
        self.rectangle_x1 -= 1
        self.rectangle_x2 -= 1
    
    def move_rectangle_down(self):
        self.updates_box.write_message("Moving down")
        self.rectangle_y1 += 1
        self.rectangle_y2 += 1
    
    def move_rectangle_up(self):
        self.updates_box.write_message("Moving Up")
        self.rectangle_y1 -= 1
        self.rectangle_y2 -= 1
    
    def move_subimage_up(self, *args):
        if self.image_loaded:
            self.move_rectangle_up()
            self.extract_subimage_from_rectangle()
            self.draw_subimage()
    
    def move_subimage_down(self, *args):
        if self.image_loaded:
            self.move_rectangle_down()
            self.extract_subimage_from_rectangle()
            self.draw_subimage()
    
    def move_subimage_right(self, *args):
        if self.image_loaded:
            self.move_rectangle_right()
            self.extract_subimage_from_rectangle()
            self.draw_subimage()
    
    def move_subimage_left(self, *args):
        print("Left")
        if self.image_loaded:
            self.move_rectangle_left()
            self.extract_subimage_from_rectangle()
            self.draw_subimage()
    
    def extract_subimage_from_rectangle(self):
        self._subimage = Image.open(self.image)
        self.tempfile = os.path.join(os.getcwd(), "tempfile" + self.image_extension)
        self.subimage = self._subimage.crop((self.rectangle_x1, self.rectangle_y2, self.rectangle_x2, self.rectangle_y1))
        
        self.subimage = self.subimage.resize(
            (round(self.stamp_width*self.resize_factor), round(self.stamp_height*self.resize_factor)))
        
        self.subimage.save(self.tempfile, format=self.image_format)
        self.sub_photoimage = PhotoImage(file=self.tempfile)
        
    def draw_subimage(self):
        self.sub_image_canvas.create_image(0,0, anchor="nw", image=self.sub_photoimage)
    
    def save_subimage(self, *args):
        self._saved_subimage = Image.open(self.image)
        self._saved_subimage_name = f"{self.subimages_saved}.{self.image_format}"
        self._saved_subimage_path = os.path.join(self.current_output_directory, self._saved_subimage_name)
        os.makedirs(self.current_output_directory, exist_ok=True)
        self.subimage = self._subimage.crop((self.rectangle_x1, self.rectangle_y2, self.rectangle_x2, self.rectangle_y1))
        self.subimage.save(self._saved_subimage_path, format=self.image_format)
        self.updates_box.write_message(f"SubImage  Saved @ [ {os.getcwd()}{os.sep}{self._saved_subimage_path} ]")
    
    def height_chosen(self, *args):
        self.stamp_height = int(self.stamp_height_combo.get())
        self.updates_box.write_message(f"height adjusted {self.stamp_height}")
        self.y2 = self.y1 + self.stamp_height
        self.sub_image_canvas.configure(height=self.stamp_height*self.resize_factor)
        self.create_rectangle_coordinates()
        self.save_rectangle_location()
        self.extract_subimage()
    
    def width_chosen(self, *args):
        self.stamp_width = int(self.stamp_width_combo.get())
        self.updates_box.write_message(f"width adjusted {self.stamp_width}")
        self.x2 = self.x1 + self.stamp_width
        self.sub_image_canvas.configure(width=self.stamp_width*self.resize_factor)
        self.create_rectangle_coordinates()
        self.save_rectangle_location()
        self.extract_subimage()
        
app = App()
app.root.mainloop()