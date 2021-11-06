from telegram.ext import CommandHandler, MessageHandler, Updater
from io import BytesIO
import math

import brotherlabel

from PIL import Image, ImageFont

from label import Label
import items

from dotenv import dotenv_values

import qrcode

config = dotenv_values(".env")
token = config["SECRET"]
updater = Updater(token=token, use_context=True)

# Setup printer and create class MyLabel
backend = brotherlabel.USBBackend("usb://0x04f9:0x2085")
printer = brotherlabel.PTPrinter(backend)
printer.quality = brotherlabel.Quality.high_quality
printer.tape = brotherlabel.Tape.TZe36mm
printer.margin = 0

fontsize = 70
font = ImageFont.truetype("./arialbi.ttf", fontsize)

class MyLabel(Label):
        items = [
            [items.Text(font, pad_right=5, pad_left=5)]
        ]

height = printer.tape['print_area']

def main():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('qr', make_qr))
    dispatcher.add_handler(CommandHandler('print', print_text))
    dispatcher.add_handler(MessageHandler(Filters.photo, receive_images))

    updater.start_polling()

def print_text(update, context):
    if(len(context.args) == 0):
        context.bot.sendMessage(update.effective_chat.id, "Please specify the text you want to print")
        
    text = ' '.join(context.args)

    img = MyLabel(text).render(height=height)

    #Send message that it's printing
    context.bot.sendMessage(update.effective_chat.id, "Printing " + text)

    printer.print([img])

def make_qr(update, context):
    if(len(context.args) == 0):
        context.bot.sendMessage(update.effective_chat.id, "Please specify the text you want to print as a QrCode")

    text = ' '.join(context.args)

    #Generate qrcode and resize
    qrcode = qrcode.make(text)
    img = qrcode.resize((454, 454))

    #Send message that it's printing
    context.bot.sendMessage(update.effective_chat.id, "Printing as QrCode " + text)

    printer.print([img])
    
def receive_images(update, context):
    #Download the image and double the size
    downloaded_img = Image.open(BytesIO(context.bot.getFile(update.message.photo[-1].file_id).download_as_bytearray()))
    decode_img = downloaded_img.resize((downloaded_img.width*2, downloaded_img.height*2))

    #Confirm printing, split image by height strips and print
    context.bot.sendMessage(update.effective_chat.id, "Preparing scissors and glue...")
    for i in range(0, math.ceil(decode_img.height/height)):
        printer.print([decode_img.crop((0, height*i, decode_img.width, min(height*(i+1), decode_img.height))).convert('1')])

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="""Hey! Send me a message with a picture and I'll cut it out for you!""")

if __name__ == '__main__':
    main()