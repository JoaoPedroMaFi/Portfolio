import time
import winsound

morse_code = {"A": ".-", "N": "-.",
              "B": "-...", "O": "---",
              "C": "-.-.", "P": ".--.",
              "D": "-..", "Q": "--.-",
              "E": ".", "R": ".-.",
              "F": "..-.", "S": "...",
              "G": "--.", "T": "-",
              "H": "....", "U": "..-",
              "I": "..", "V": "...-",
              "J": ".---", "W": ".--",
              "K": "-.-", "X": "-..-",
              "L": ".-..", "Y": "-.--",
              "M": "--", "Z": "--..", ".": "·-·-·-",
              ",": "--··--",
              "?": "··--··",
              "'": "·----·",
              "!": "-·-·--",
              "/": "-··-·",
              "(": "-·--·",
              ")": "-·--·-",
              "&": "·-···",
              ":": "---···",
              ";": "-·-·-·",
              "=": "-···-",
              "-": "-····-",
              "_": "··--·-",
              "\"": "·-··-·",
              "$": "···-··-",
              "@": "·--·-·",
              "1": "·----",
              "2": "··---",
              "3": "···--",
              "4": "····-",
              "5": "·····",
              "6": "-····",
              "7": "--···",
              "8": "---··",
              "9": "----·",
              "0": "-----"
              }
numbers = {
    1: "·----",
    2: "··---",
    3: "···--",
    4: "····-",
    5: "·····",
    6: "-····",
    7: "--···",
    8: "---··",
    9: "----·",
    0: "-----"}

punctuation = {
    ".": "·-·-·-",
    ",": "--··--",
    "?": "··--··",
    "'": "·----·",
    "!": "-·-·--",
    "/": "-··-·",
    "(": "-·--·",
    ")": "-·--·-",
    "&": "·-···",
    ":": "---···",
    ";": "-·-·-·",
    "=": "-···-",
    "-": "-····-",
    "_": "··--·-",
    "\"": "·-··-·",
    "$": "···-··-",
    "@": "·--·-·",
    ' ': "/"}


def find_value(char):
    if char in morse_code:
        return morse_code[char]
    if char in numbers:
        return numbers[char]
    if char in punctuation:
        return punctuation[char]


text = input("Insert your sentence: ")
morse_message = ""
for letter in range(len(text)):
    print(text[letter].upper())
    value = text[letter].upper()
    print(find_value(value))
    morse_message += find_value(value) + " "

print(morse_message)
# Play Morse Code
for char in morse_message:
    if char == ".":
        winsound.Beep(1000, 50)  # frequency, duration in ms for a dot
    elif char == "-":
        winsound.Beep(1000, 100)  # frequency, duration in ms for a dash
    elif char == " ":
        time.sleep(0.5)  # pause for space
    time.sleep(0.1)  # short pause between each signal
