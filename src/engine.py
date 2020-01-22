import tcod as libtcod

# imports
from input_handlers import handle_keys

def main():
    # Set screen size
    screen_width = 80
    screen_height = 50

    # Player infos
    player_x = int(screen_width/2)
    player_y = int(screen_height/2)

    # Assign custom tileset/fonts & init console
    libtcod.console_set_custom_font('./src/assets/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'my-py-roguelike', False)

    con = libtcod.console_new(screen_width, screen_height)

    # Mouse & keys infos
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        libtcod.console_flush() # Update window to display current state

        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        # Get action from key presses
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
