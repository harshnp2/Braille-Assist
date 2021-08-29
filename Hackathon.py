import cv2 as cv
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\harsh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
from PIL import Image
from gtts import gTTS
import os
import time
from threading import Thread
from pyfirmata import Arduino, util

# accessing the port and the arduino board
port = 'COM3'
board = Arduino(port)
time.sleep(0.25)

it = util.Iterator(board)
it.start()

arduino = {
    'digital': tuple(x for x in range(14)),
    'analog': tuple(x for x in range(6)),
    'pwm': (3, 5, 6, 9, 10, 11),
    'use_ports': True,
    'disabled': (0, 1)
}

# setting specific values needed to make the motor (such as pin value and the time it takes for one rotation)
left_motor = board.get_pin('d:3:p')
right_motor = board.get_pin('d:6:p')

rRot = 0.46
lRot = 0.545

Pre_r_Pos = 0
Pre_l_Pos = 0

l_pos = 0
r_pos = 0

plus = 0.1

count = 0

# makes the right motor move
def right_mot(right, n):
    right.write(0.5)
    time.sleep(n)
    right.write(0)
    time.sleep(0.1)


# makes the left motor move
def left_mot(left, m):
    left.write(0.5)
    time.sleep(m)
    left.write(0)
    time.sleep(0.1)


# the function that does the math to calculate how much it needs to rotate to get to the side of the octagon which has specific braille dots
def math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot, rRot, plus, count):
    print(count)

    New_l_pos = (lRot / 8) * l_num
    print("Moving to l position" + str(New_l_pos))
    l_pos = New_l_pos - Pre_l_Pos
    if l_pos < 0:
        l_pos = 1 + l_pos

    if 1 <= count < 3 and New_l_pos != Pre_l_Pos:
        l_pos += 0.1

    if count == 3 and New_l_pos != Pre_l_Pos:
        l_pos += 0.02

    print("My previous l position is " + str(Pre_l_Pos) + " I have to move " + str(l_pos))

    New_r_pos = (rRot / 8) * r_num
    print("Moving to r position" + str(New_r_pos))
    r_pos = New_r_pos - Pre_r_Pos
    if r_pos < 0:
        r_pos = 1 + r_pos

    if count == 2 and New_r_pos != Pre_r_Pos:
        r_pos += 0.02

    if count == 1 and New_r_pos != Pre_r_Pos:
        r_pos -= 0.07

    if count == 3:
        r_pos += 0.1

    print("My previous r position is " + str(Pre_r_Pos) + " I have to move " + str(r_pos))

    Pre_l_Pos = New_l_pos
    Pre_r_Pos = New_r_pos

    print("My previous l position is now" + str(Pre_l_Pos))
    print("My previous r position is now" + str(Pre_r_Pos))

    count += 1
    print(count)

    return Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus

cap = cv.VideoCapture(0)
language = 'en'
again = "try again"
captured = "Picture has been taken"
num = 0

mode = input("Which mode do you choose, text to braille (1) or text to speech (2): ")

while True:
    # ret checks if camera can be used and frame is the actual image
    ret, frame = cap.read()

    cv.imshow("frame", frame)

    if cv.waitKey(1) & 0xFF == ord('d'):
        # takes a piture of the text
        cv.imwrite('index.png', frame)
        img = Image.open("index.png")
        # detects the text in the picture
        message = tess.image_to_string(img)

        # speech messages
        repeat = gTTS(text=again, lang=language, slow=False)
        captured = gTTS(text=captured, lang=language, slow=False)
        output = gTTS(text=message, lang=language, slow=False)

        array = message.split()
        elements = len(array)

        for i in array:
            x = i.isalpha()
            if x is True:
                num += 1
                print(i)


        if elements == num:
            # if mode 1 was choden it goes through this if statement
            if mode == "1":
                print(message)
                captured.save("captured.mp3")
                os.system("start captured.mp3")
                # divides the string up into a list with each character
                char = list(message)
                print(char)
                # for loop goes through the list and sees if any of them are letters
                for check in char:
                    # if detects a certain letter it excutes the code inside the if statment which causes the motors to move to the specific side with the braille
                    if check == "a" or check == "A":
                        l_num = 1
                        r_num = 0

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()


                    elif check == "b" or check == "B":
                        l_num = 5
                        r_num = 0

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()



                    elif check == "c" or check == "C":
                        l_num = 1
                        r_num = 3

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "d" or check == "D":
                        l_num = 1
                        r_num = 7

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "e" or check == "E":
                        l_num = 1
                        r_num = 2

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "f" or check == "F":
                        l_num = 5
                        r_num = 3

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "g" or check == "G":
                        l_num = 5
                        r_num = 7

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "h" or check == "H":
                        l_num = 5
                        r_num = 2

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "i" or check == "I":
                        l_num = 2
                        r_num = 3

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "j" or check == "J":
                        l_num = 2
                        r_num = 7

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "k" or check == "K":
                        l_num = 6
                        r_num = 0

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "l" or check == "L":
                        l_num = 4
                        r_num = 0

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "m" or check == "M":
                        l_num = 6
                        r_num = 3

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "n" or check == "N":
                        l_num = 6
                        r_num = 7

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "o" or check == "O":
                        l_num = 6
                        r_num = 2

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "p" or check == "P":
                        l_num = 4
                        r_num = 3

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "q" or check == "Q":
                        l_num = 4
                        r_num = 7

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "r" or check == "R":
                        l_num = 4
                        r_num = 2

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "s" or check == "S":
                        l_num = 7
                        r_num = 1

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "t" or check == "T":
                        l_num = 7
                        r_num = 5

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "u" or check == "U":
                        l_num = 6
                        r_num = 3

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "v" or check == "V":
                        l_num = 4
                        r_num = 3

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "w" or check == "W":
                        l_num = 2
                        r_num = 4

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "x" or check == "X":
                        l_num = 6
                        r_num = 6

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "y" or check == "Y":
                        l_num = 6
                        r_num = 4

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == "z" or check == "Z":
                        l_num = 6
                        r_num = 7

                        Pre_l_Pos, Pre_r_Pos, l_pos, r_pos, count, plus = math(l_num, r_num, Pre_l_Pos, Pre_r_Pos, lRot,
                                                                               rRot, plus, count)
                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    elif check == " ":
                        l_num = 0
                        r_num = 0

                        New_l_pos = (lRot / 8) * l_num
                        print("Moving to l position" + str(New_l_pos))
                        l_pos = New_l_pos - Pre_l_Pos
                        if l_pos < 0 and New_l_pos != Pre_l_Pos:
                            l_pos = 1 + l_pos

                        l_pos = l_pos + ((lRot / 8) * 0.8)

                        print("My previous l position is " + str(Pre_l_Pos) + " I have to move " + str(l_pos))

                        New_r_pos = (rRot / 8) * r_num
                        print("Moving to r position" + str(New_r_pos))
                        r_pos = New_r_pos - Pre_r_Pos
                        if r_pos < 0 and New_r_pos != Pre_r_Pos:
                            r_pos = 1 + r_pos

                        print("My previous r position is " + str(Pre_r_Pos) + " I have to move " + str(r_pos))

                        Pre_l_Pos = New_l_pos
                        Pre_r_Pos = New_r_pos

                        print("My previous l position is now" + str(Pre_l_Pos))
                        print("My previous r position is now" + str(Pre_r_Pos))

                        rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                        lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                        lDelay = lThread.start()
                        rDelay = rThread.start()
                        rThread.join()
                        lThread.join()

                    time.sleep(4)

                reset = input("Do you want to reset back to space position, Y or N: ")


                # after it is done printing the message in braille it asks the user if it wants braille assist to go back to the space position
                if reset == "Y" or reset == "y":
                    l_num = 0
                    r_num = 0

                    New_l_pos = (lRot / 8) * l_num
                    print("Moving to l position" + str(New_l_pos))
                    l_pos = New_l_pos - Pre_l_Pos
                    if l_pos < 0:
                        l_pos = 1 + l_pos

                    if count >= 1 and New_l_pos != Pre_l_Pos:
                        l_pos = l_pos + ((lRot / 8) * 0.15)

                    print("My previous l position is " + str(Pre_l_Pos) + " I have to move " + str(l_pos))

                    New_r_pos = (rRot / 8) * r_num
                    print("Moving to r position" + str(New_r_pos))
                    r_pos = New_r_pos - Pre_r_Pos
                    if r_pos < 0:
                        r_pos = 1 + r_pos

                    if count >= 1:
                        r_pos = r_pos + ((rRot / 8) * 0.08)

                    print("My previous r position is " + str(Pre_r_Pos) + " I have to move " + str(r_pos))

                    Pre_l_Pos = New_l_pos
                    Pre_r_Pos = New_r_pos

                    print("My previous l position is now" + str(Pre_l_Pos))
                    print("My previous r position is now" + str(Pre_r_Pos))

                    rThread = Thread(target=right_mot, args=[right_motor, r_pos], daemon=True)
                    lThread = Thread(target=left_mot, args=[left_motor, l_pos], daemon=True)
                    lDelay = lThread.start()
                    rDelay = rThread.start()
                    rThread.join()
                    lThread.join()

            # text to speech
            elif mode == "2":
                print(message)
                output.save("output.mp3")
                os.system("start output.mp3")


    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# destroys windows after it breaks out of the while loop
cap.release()
cv.destroyAllWindows()
