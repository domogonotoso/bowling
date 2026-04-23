with open("text.txt", "a") as f:
    f.write("\ngallery" \
    "photo" \
    "\ndodo" \
    "du rapshindu")

with open("text.txt", "r") as f:  
    text = f.readlines()
    print(text)


print(help(open))