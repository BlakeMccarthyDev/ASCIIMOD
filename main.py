from PIL import Image, ImageEnhance
from nicegui import ui, app, events
import base64
from io import BytesIO

#region ImageInput
outim = Image.open("input.jpg")
uploaded = False
uploadedlabel = ui.label(text="Not Uploaded")
def displayup():
    uploadedlabel.text = "Uploaded"

def handleInputs(e : events.UploadEventArguments):
    displayup()
    b64 = base64.b64encode(e.content.read())
    xim = BytesIO(base64.b64decode(b64))
    outim = Image.open(xim)
    ImtoAscii(outim)

imageupload = ui.upload(multiple=False, on_upload=handleInputs)
#endregion ImageInput
#region ImagetoAscii

nl = ui.label("")

def pixtoSTR(inp: int) -> str:
    if inp > 204:
        return "@"
    elif inp > 153:
        return "X"
    elif inp > 102:
        return ";"
    elif inp > 51:
        return ","
    else:
        return " "

pix = []

def ImtoAscii(im: Image.Image):
    x = im.resize([64, 64])
    y = ImageEnhance.Color(x)
    x = y.enhance(0.0)
    for ix in range(64):
        for iy in range(64):
            gpx = x.getpixel([ix, iy])[0]
            pix.append(pixtoSTR(gpx))
            for i in range(len(pix)):
                if i % 64 == 0:
                    nl.text += "\n"
                else:
                    nl.text += pix[i]


#endregion ImagetoAscii

app.on_disconnect(app.shutdown)
ui.run()
