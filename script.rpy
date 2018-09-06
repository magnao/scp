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
            #new
            (0, 0), ConditionSwitch(
                "color == 0", "base.png",
                "color == 1", "base1.png"),
            #new long end
            (0, 0), "glasses%d.png"%glasses, # (0, 0) is the position of a dressup item. Because these images are saved with spacing around them, we don't need to position them.
            (0, 0), "hair%d.png"%hair,
            (0, 0), "tie%d.png"%tie,
            ),.1

    def draw_char_clothes(st, at): # same as above, but with clothing overlay
        return LiveComposite(
            (361, 702), # image size
            (0, 0), ConditionSwitch(
                "color == 0", "base.png",
                "color == 1", "base1.png"),
            (0, 0), "glasses%d.png"%glasses, # (0, 0) is the position of a dressup item. Because these images are saved with spacing around them, we don't need to position them.
            (0, 0), "hair%d.png"%hair,
            (0, 0), "overlay.png",
            (0, 0), "tie%d.png"%tie
            ),.1

    def draw_char_side(st, at): # same thing as above, just scaled and positioned for the sideimage; there's probably more elegant solution than this...
        return LiveComposite(
            (361, 702),
            (10, 550), ConditionSwitch(
                "color == 0", im.FactorScale("base.png", .45, .45),
                "color == 1", im.FactorScale("base1.png", .45, .45)
                ),
            (10, 550), im.FactorScale("glasses%d.png"%glasses, .45, .45),
            (10, 550), im.FactorScale("hair%d.png"%hair, .45, .45),
            (10, 550), im.FactorScale("overlay.png", .45, .45),
            (10, 550), im.FactorScale("tie%d.png"%tie, .45, .45)
            ),.1

init:
    image char = DynamicDisplayable(draw_char) # using DynamicDisplayable ensures that any changes are visible immedietly
    image char_clothes = DynamicDisplayable(draw_char_clothes)
    define character = Character('[playername]', color="#c8ffc8", window_left_padding=180, show_side_image=DynamicDisplayable(draw_char_side))

label start:
   show screen dressup_button
   #changed to false
   $ dressup_button_show = False
label cont:
    $ color = 0
    show char
    #new
    $ playername = renpy.input("What is your name?")
    $ playername = playername.strip()
    if playername == "xXRaz0rXx":
        "This name is invalid. A new name has been assigned."
        $ playername = "Alexx"
        jump cont2
    while not playername:
        "You need to choose a name!"
        $ playername =renpy.input("What is your name?")
        $ playername = playername.strip()
        if playername == "xXRaz0rXx":
            "This name is invalid. A new name has been assigned."
            $ playername = "Alexx"
            jump cont2
label cont2:
    #end new
    $ dressup_button_show = True
    character "This is the main character!"
    #changed from jump cont to return
    return

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
        ui.textbutton("Return", clicked=ui.returns("goback")) # image button version: ui.imagebutton("return.png", "return_hover.png", clicked=ui.returns("goback"), ypos=0, xpos=0)
        ui.textbutton("Confirm appearance", clicked=ui.returns("confirmation"),  ypos=0, xpos=770)
        ui.textbutton("Light", clicked=ui.returns("lightskin"), ypos=100, xpos=700)
        ui.textbutton("Dark", clicked=ui.returns("darkskin"), ypos=100, xpos=600)
        ui.textbutton("Kiwi", clicked=ui.returns("kiwiload"), ypos=200, xpos = 700)

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

    if picked == "lightskin":
        $ color = 0
    if picked == "darkskin":
        $ color = 1

    if picked == "kiwiload":
        $ color = 0
        $ hair = 4
        $ glasses = 2
        $ tie = 2

    if picked == "confirmation":
        menu:
            "Are you sure this is the character you want?"
            "Yes":
                hide char
                with fade
                show char_clothes
                with fade
                character "This is the main character!"
                return
            "No":
                return

    if picked == "goback":
        return
    jump dressup # we don't want to return on every click, this jump loops until we click on "back" button

    return
