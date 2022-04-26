import glob
import cv2
import argparse
import os.path
import sys
# simple right now, just displays images one after the other and prompt on the terminal for a label

# from the example zip
symbols = ["advance to contact", "ambush", "attack", "attack by fire", "block", "breach",
           "bypass", "clear", "counterattack", "cover", "delay", "destroy", "disrupt",
           "fix", "follow_and_assume", "follow_and_support", "guard", "isolate",
           "main_attack", "neutralize", "occupy", "penetrate", "retain", "retirement",
           "screen", "secure", "seize", "support_by_fire", "suppress", "turn", "withdrawal"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='labeling tool')
    parser.add_argument('dir', type=str, help="Directory containing images to be labeled.")
    args = parser.parse_args(sys.argv[1:])

    args.dir = os.path.abspath(args.dir)
    if not os.path.isdir(args.dir):
        print(f"Nonexisting directory {args.dir} passed. Quitting.")
        exit()

    # grab image filenames form directory
    images = glob.glob(args.dir + "/*.jpg")
    images += glob.glob(args.dir + "/*.png")

    cv2.namedWindow("imgdisplay")
    for i, symb in enumerate(symbols):
        print(f"{i}. {symb}")
    for imname in images:
        imgbasename, ext = os.path.basename(imname).split(".")
        img = cv2.imread(imname)
        h, w, _ = img.shape
        if w*h > 480_000:  # if image is greater than a 800x600 img resize into something sane
            factor = 800/max(w, h)
            img = cv2.resize(img, (int(w*factor), int(h*factor)))

        cv2.setWindowTitle("imgdisplay", imgbasename)
        cv2.imshow("imgdisplay", img)
        cv2.waitKey(1)
        while True:
            label = input()
            # you can type the label or use the number
            if label.isdigit() and int(label) < len(symbols):

                break
            elif label.strip().replace(" ", "_").lower() in symbols:

                break
            else:
                print(f"Invalid input: {label}")

        # incomplete atm
        # with open(os.path.join(args.dir, f"{imgbasename}.txt"), "w") as f:
        #     f.write(ch)
