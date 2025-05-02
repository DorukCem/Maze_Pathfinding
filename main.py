import os
import threading
from app import App
from file_count import *
from grid import Grid
from manager import Manager
from settings import *
import pygame
from utility import *
from watchdog.observers import Observer

os.makedirs("saved_grids", exist_ok=True)
pygame.init()
pygame.font.init()

app = App()

mouse_is_held = False
item_being_held = None
grid_needs_reset = False
current_thread: threading.Thread | None = None
is_start_screen = True
alerts = AlertManager()

# Monitor number of files is saved_grids
# (We go to the toruble of watching the directory so that external events can also be handled)
event_handler = FileCountHandler("saved_grids")
observer = Observer()
observer.schedule(event_handler, path="saved_grids", recursive=False)
observer.start()

while True:
    if current_thread is not None and not current_thread.is_alive():
        current_thread = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if is_start_screen:
                is_start_screen = False
                continue

        # Only process inputs if no algorithm is running
        if current_thread is None:
            # --- Mouse Inputs ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    cell = app.grid.get_cell_being_clicked(pygame.mouse.get_pos())
                    item_being_held = cell.flag
                    mouse_is_held = True

                    if grid_needs_reset:
                        app.grid.reset_grid()
                        grid_needs_reset = False

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                app.grid.cell_that_switched_last = None
                mouse_is_held = False

            elif event.type == pygame.MOUSEWHEEL:
                app.scroll("up" if event.y == 1 else "down")

            # --- Keyboard Inputs ---
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    th = threading.Thread(target=lambda: app.run_algorithm())
                    th.start()
                    current_thread = th
                    grid_needs_reset = True

                elif event.key == pygame.K_s:
                    save_grid(app.grid, alerts)

                elif event.key == pygame.K_c:
                    app.grid.reset_grid()
                    grid_needs_reset = False

                elif event.key == pygame.K_d:
                    delete_saves(alerts)

                elif event.key == pygame.K_UP:
                    app.scroll("up")

                elif event.key == pygame.K_DOWN:
                    app.scroll("down")

                elif pygame.K_0 <= event.key <= pygame.K_9:
                    number_pressed = event.key - pygame.K_0
                    app.grid = load_grid(number_pressed, alerts) or app.grid

                elif pygame.K_KP0 <= event.key <= pygame.K_KP9:
                    number_pressed = event.key - pygame.K_KP0
                    app.grid = load_grid(number_pressed, alerts) or app.grid
        else:
            # Stop algorithm
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Grid is accesed by the algorithm that is executed which will check on each iteration if this is true
                app.grid.kill_thread = True
                app.grid.reset_grid()

    if is_start_screen:
        app.draw_start_screen()

    else:
        if mouse_is_held:
            app.handle_mouse(item_being_held)

        app.screen.fill(BLACK)
        app.grid.draw(app.screen)
        app.draw_algorithm_text(app.font)
        app.draw_num_files_saved(saved_file_count, app.alert_font)
        alerts.filter_alerts()
        alerts.draw_alerts(app.screen, app.alert_font)

        saved_file_count = event_handler.get_file_count()

    pygame.display.update()
    app.clock.tick(60)
