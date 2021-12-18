from threading import Thread

import app
import interface

# Create threads for server and window (interface)
t_server = Thread(target=app.serve)
t_gen_qr = Thread(target=interface.gen_qr)
t_window = Thread(target=interface.window)

# Set all threads as Deamon thread (die on program termination)
t_server.daemon = True
t_gen_qr.daemon = True
t_window.daemon = True

# Start server
t_server.start()

# Start QR code generation
t_gen_qr.start()

# Wait for QR code to be generated
t_gen_qr.join(timeout=2.0)

# Exit if QR code not generated within timeout
if t_gen_qr.is_alive():
    exit()

# Start window
t_window.start()

# Wait for window to close
t_window.join()