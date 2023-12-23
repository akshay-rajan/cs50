import sys, random
from pyfiglet import Figlet

figlet = Figlet()

def main():
    list = figlet.getFonts()
    # Check for command line arguments
    error = 'Invalid usage'
    if (len(sys.argv) != 1 and len(sys.argv) != 3):
        sys.exit(error)

    # If there are command line arguments
    if (len(sys.argv) > 1):
        if (sys.argv[1] != '-f' and sys.argv[1] != '--font'):
            sys.exit(error)
        else:
            fontname = sys.argv[2]
            # If the font is valid
            if fontname in list:
                figlet.setFont(font=fontname)
            else:
                sys.exit(error)
    # Else pick the font randomly
    else:
        fontname = list[random.randint(0, len(list) - 1)]
        figlet.setFont(font=fontname)

    # Prompt the user for a string to FIGlet
    s = str(input('Input: '))

    # Print the rendered text
    print(figlet.renderText(s))

main()