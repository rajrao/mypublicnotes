from pybricks.hubs import InventorHub
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Button

def do_menu(hub, menu_options, cur_menu_index):
    """
    provides a mechanism for presenting single character menu options on
    the hub. 
    Selection is by the Center Button
    Bluetooth button stops the code
    Left and Right arrow keys pick the next menu item

    hub: instance of the hub.
    menu_options: a list/tuple of single characters displayed as menu items
    cur_menu_index: the currently selected menu-index

    example: the following code is called in a loop
    selected, cur_menu_index = do_menu(hub, ("1","2"), cur_menu_index)
    """
    num_options = len(menu_options)
    # Normally, the center button stops the program. But we want to use the
    # center button for our menu. So we can disable the stop button.
    hub.system.set_stop_button(None)
    while True:
        hub.display.char(menu_options[cur_menu_index])
        # Wait for any button.
        pressed = ()
        while not pressed:
            pressed = hub.buttons.pressed()
            wait(10)    
        print(f"pressed: {pressed}")
        # and then wait for the button to be released.
        while hub.buttons.pressed():
            wait(10)

        if Button.BLUETOOTH in pressed:
            # This is the exit key!
            return "X", None
  
        # Now check which button was pressed.
        if Button.CENTER in pressed:
            # Center button, this is the selection button, so we can exit the
            # selection loop
            print(f"Selected Index: {cur_menu_index}")
            break
        elif Button.LEFT in pressed:
            # Left button, so decrement menu menu_index.
            cur_menu_index -= 1
            if (cur_menu_index < 0): #roll over!
                cur_menu_index = num_options - 1
        elif Button.RIGHT in pressed:
            # Right button, so increment menu menu_index.
            cur_menu_index += 1
            if (cur_menu_index >= num_options):
                cur_menu_index = 0
        print(f"menu_index:{cur_menu_index}")
    
    # Now we want to use the Center button as the stop button again.
    hub.system.set_stop_button(Button.CENTER)
    selected = menu_options[cur_menu_index]
    print(f"menu option selected {selected}")
    
    return selected, cur_menu_index
