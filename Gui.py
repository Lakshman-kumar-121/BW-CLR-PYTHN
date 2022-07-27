from tkinter import *
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from turtle import width
from PIL import Image, ImageTk

from main import imageconverion, vcont


img_bw = "./models/Default_Image/image-bw.jpg"
img_clr = "./models/Default_Image/image-clr.png"
vid_bw = "./models/Default_Image/video-bw.png"
vid_clr = "./models/Default_Image/video-clr.png"


def browserfile(label ):
    
    if menu.get() == "Video":
        filename = filedialog.askopenfilename(initialdir='./' , 
        title="Open Gray scale Image" ,
        filetypes = (("Mp4",  "*.mp4*") , ("Mkv" , "*.mkv"),("Ts" , "*.Ts") ,("Webm" , "*.webm") ,("Avi" , "*.avi"),("MOV" , "*.mov")))
    else:
        menu.set("Image")
        filename = filedialog.askopenfilename(initialdir='./' , 
        title="Open Gray scale Image" ,
        filetypes = (("Jpg",  "*.jpg*") , ("Png" , "*.png") ,("Jpeg" , "*.jpeg")))

    
    global img1
    img1 = filename
    filename = filename.split('/')[-1]
    if(filename == ""):
        filename = "No File choosen"
        messagebox.showinfo("Select File", "No File is selected, Please select any file")
        if menu.get() != "Video":
            image1 = Image.open(img_bw)
            update_img(img_bw)
        else:
            update_img(vid_bw)
        cvtbtn['state'] = DISABLED

        return
    cvtbtn['state'] = NORMAL
    label['text'] = filename
    update_img(img1)
    
def update_img(name ):
    print(name)
    if menu.get() == "Image" or menu.get() == "Select Video or Image":
        image1 = Image.open(name)
        image1= image1.resize((400,300), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        Dis_pic_1.configure(image=test)
        Dis_pic_1.image=test
    else:
        image1 = Image.open(vid_bw)
        image1= image1.resize((400,300), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        Dis_pic_1.configure(image=test)
        Dis_pic_1.image=test





root = Tk()

menu= StringVar()
menu.set("Select Video or Image")
drop= OptionMenu(root, menu,"Image", "Video" )



img1= ImageTk.PhotoImage(Image.open(img_bw).resize((400,300), Image.ANTIALIAS))
Dis_pic_1= Label(root,image= img1)

img2= ImageTk.PhotoImage(Image.open(img_clr).resize((400,300), Image.ANTIALIAS))
Dis_pic_2= Label(root,image= img2)

mylabel = Label(root ,text="No File choosen" , width=20)
mylabel.place()
root.geometry("1200x800+10+20")
root.title("Grayscale to Color")

def conversion():
    if menu.get() == "Video":
        image1 = Image.open(vid_clr)
        image1= image1.resize((400,300), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        Dis_pic_2.configure(image=test)
        Dis_pic_2.image=test
        messagebox.showinfo("Alert !", "To Stop the Video process , Press Q key ")
        vcont(img1)
    else:
        imageconverion(img1)
        demo = img1.split('.')
        image2 = Image.open(demo[0] + "-cont." + demo[-1])
        image2= image2.resize((400,300), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image2)
        Dis_pic_2.configure(image=test)
        Dis_pic_2.image=test
        messagebox.showinfo("Alert !", "File is converted and saved in same directory!")
mylabel.pack(pady=20)


Dis_pic_1.place(x=200,y=70)
Dis_pic_2.place(x = 650 , y=70)
drop.pack(pady=355)
opnbtn = Button(root , text="Open File" , padx=50 , pady=5 , width=20 , command= lambda:browserfile(mylabel))
opnbtn.place (x=270, y = 500)
cvtbtn = Button(root , text="Convert To color" , padx=50 , pady=5 ,width=20, command=conversion , state=DISABLED)
cvtbtn.place(x=755, y = 500)
root.mainloop()

