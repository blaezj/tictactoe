from guizero import App, Box, TextBox, PushButton, Picture
from PIL import Image

IMAGEPATH="x.png"
TEMPIMAGEPATH="temp_resized.png"

def resize_button_image():
    buttonboxwidth = int(app.width/3)
    buttonboxheight = int(app.height/3)
    buttonwidth = int(buttonboxwidth/3)
    buttonheight = int(buttonboxheight/3)
    
    wid = buttonwidth
    hei = buttonheight

    resized = make_scaled_image(IMAGEPATH, wid, hei, TEMPIMAGEPATH)
    
    button_box1.width=buttonboxwidth
    button_box1.height=buttonboxheight 
    button_box2.width=buttonboxwidth
    button_box2.height=buttonboxheight
    button_box3.width=buttonboxwidth
    button_box3.height=buttonboxheight

    btn1.image = resized
    btn2.image = resized
    btn3.image = resized
    btn4.image = resized
    btn5.image = resized
    btn6.image = resized
    btn7.image = resized
    btn8.image = resized
    btn9.image = resized

def make_scaled_image(path, width, height, savePath=TEMPIMAGEPATH):
    img = Image.open(path)
    img = img.resize((width, height))
    img.save(savePath)
    return savePath


app = App(width=500, height=500, bg="lightblue")
buttonboxholder = Box(app, align="top", height="fill", width="fill")

# creates the width and height of the buttons and button boxes
#buttonboxwidth = int(app.width/3)
#buttonboxheight = int(app.height/3)
#buttonwidth = int(buttonboxwidth/3)
#buttonheight = int(buttonboxheight/3)


button_box1 = Box(buttonboxholder, align="top", width="fill")
btn1 = PushButton(button_box1, align="left", image="x.png", bg=app.bg)
btn2 = PushButton(button_box1, align="left", image="x.png", bg=app.bg)
btn3 = PushButton(button_box1, align="left", image="x.png", bg=app.bg)

button_box2 = Box(buttonboxholder, align="top", width="fill")
btn4 = PushButton(button_box2, align="left", image="x.png", bg=app.bg)
btn5 = PushButton(button_box2, align="left", image="x.png", bg=app.bg)
btn6 = PushButton(button_box2, align="left", image="x.png", bg=app.bg)

button_box3 = Box(buttonboxholder, align="top", width="fill")
btn7 = PushButton(button_box3, align="left", image="x.png", bg=app.bg)
btn8 = PushButton(button_box3, align="left", image="x.png", bg=app.bg)
btn9 = PushButton(button_box3, align="left", image="x.png", bg=app.bg)

#scaled_img_path = make_scaled_image(IMAGEPATH, buttonwidth, buttonheight)
#app.when_resized = resize_button_image
app.display()
