import sys
import os
import threading
import webbrowser
import uvicorn

# When bundled by PyInstaller, extracted files live in sys._MEIPASS.
# Set the working directory there so relative imports in main.py resolve correctly.
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
    # console=False in the .spec means Windows gives the process no console window,
    # so sys.stdout and sys.stderr are None.  Uvicorn's log formatter calls
    # stream.isatty() during startup and crashes with AttributeError / ValueError
    # if either stream is None.  Redirect both to the null device so they are
    # valid (but silent) file objects before uvicorn initialises logging.
    _null = open(os.devnull, 'w')
    sys.stdout = _null
    sys.stderr = _null

def _open_browser():
    import time
    time.sleep(2)
    webbrowser.open('http://localhost:8000')

if __name__ == '__main__':
    from main import app  # import the app object directly — string-based imports
                          # ('main:app') are unreliable inside a PyInstaller bundle
                          # because the frozen importer does not behave like a normal
                          # sys.path lookup.
    threading.Thread(target=_open_browser, daemon=True).start()
    # log_config=None tells uvicorn to skip its dictConfig call entirely,
    # which is a second layer of protection against the formatter crash.
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='error', log_config=None)
