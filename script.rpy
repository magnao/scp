init python:
    dressup_button_show = False
    hair, glasses, tie, shirt, pants = 1, 1, 1, 1, 1 # default dressup items
    hair_styles_num, glasses_styles_num, tie_styles_num, shirt_styles_num, pants_styles_num = 7, 4, 4, 3, 3 # number of styles (files) for each dressup item
    # define images as:
    # "base.png" for the base image
    # "hair1.png", "hair2.png", "hair3.png", ... - start with 1 and end with (hair_styles_num)
    # "glasses1.png", "glasses2.png", "glasses3.png", ... "tie1.png", "tie2.png", ... "shirt1.png", "shirt2.png", ... "shirt1.png", "pants2.png", ...

    def draw_char(st, at): # combine the dressup items into one displayable
        return LiveComposite(
            (361, 702), # image size
            (0, 0), "base.png",
            (0, 0), "glasses%d.png"%glasses, # (0, 0) is the position of a dressup item. Because these images are saved with spacing around them, we don't need to position them.
            (0, 0), "hair%d.png"%hair,
            (0, 0), "shirt%d.png"%shirt,
            (0, 0), "tie%d.png"%tie,
            (0, 0), "pants%d.png"%pants
            ),.1

    def draw_char_side(st, at): # same thing as above, just scaled and positioned for the sideimage; there's probably more elegant solution than this...
        return LiveComposite(
            (361, 702),
            (10, 550), im.FactorScale("base.png", .45, .45),
            (10, 550), im.FactorScale("glasses%d.png"%glasses, .45, .45),
            (10, 550), im.FactorScale("hair%d.png"%hair, .45, .45),
            (10, 550), im.FactorScale("shirt%d.png"%shirt, .45, .45),
            (10, 550), im.FactorScale("tie%d.png"%tie, .45, .45),            
            (10, 550), im.FactorScale("pants%d.png"%pants, .45, .45)
            ),.1

init:
    image char = DynamicDisplayable(draw_char) # using DynamicDisplayable ensures that any changes are visible immedietly
    $ character = Character('Koma', color="#c8ffc8", window_left_padding=180, show_side_image=DynamicDisplayable(draw_char_side))

label start:
   show screen dressup_button
   $ dressup_button_show = True
label cont:
    show char
    character "La, la, la!"
    jump cont

screen dressup_button: # a button to call the dressup game
    if dressup_button_show:
        vbox xalign 0.01 yalign 0.01:
            textbutton "Change look." action ui.callsinnewcontext("dressup")

label dressup:
    show char:
        xpos 250
    python:
        # display the arrows for changing the dress:
        y = 50
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns("hairL"), ypos=y, xpos=50)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns("hairR"), ypos=y, xpos=400)
        y += 80
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns("glassesL"), ypos=y, xpos=50)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns("glassesR"), ypos=y, xpos=400)
        y += 80
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns("tieL"), ypos=y, xpos=50)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns("tieR"), ypos=y, xpos=400)
        y += 80
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns("shirtL"), ypos=y+80, xpos=50)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns("shirtR"), ypos=y+80, xpos=400)
        y += 80
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns("pantsL"), ypos=y+160, xpos=50)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns("pantsR"), ypos=y+160, xpos=400)
        ui.textbutton("Return", clicked=ui.returns("goback")) # image button version: ui.imagebutton("return.png", "return_hover.png", clicked=ui.returns("goback"), ypos=0, xpos=0)
        
    $ picked = ui.interact()
    # based on the selection, we increase or decrease the index of the appropriate dress up item
    if picked == "hairL":
        $ hair -= 1 # previous hair
    if picked == "hairR":
        $ hair += 1 # next hair
    if hair < 1: # making sure we don't get out of index range (index 0 is not allowed)
        $ hair = hair_styles_num
    if hair > hair_styles_num: # making sure we don't get out of index range (index musn't be bigger than hair_styles_num)
        $ hair = 1

    if picked == "glassesL":
        $ glasses -= 1
    if picked == "glassesR":
        $ glasses += 1
    if glasses < 1:
        $ glasses = glasses_styles_num
    if glasses > glasses_styles_num:
        $ glasses = 1

    if picked == "tieL":
        $ tie -= 1
    if picked == "tieR":
        $ tie += 1
    if tie < 1:
        $ tie = tie_styles_num
    if tie > tie_styles_num:
        $ tie = 1

    if picked == "shirtL":
        $ shirt -= 1
    if picked == "shirtR":
        $ shirt += 1
    if shirt < 1:
        $ shirt = shirt_styles_num
    if shirt > shirt_styles_num:
        $ shirt = 1

    if picked == "pantsL":
        $ pants -= 1
    if picked == "pantsR":
        $ pants += 1
    if pants < 1:
        $ pants = pants_styles_num
    if pants > pants_styles_num:
        $ pants = 1
        
    if picked == "goback":
        return    
    jump dressup # we don't want to return on every click, this jump loops until we click on "back" button

    return
