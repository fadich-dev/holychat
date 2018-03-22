from gui import windows
import signal


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    main_win = windows.MainWindow(title='Roflin')

    main_win.init()
    main_win.destroy()