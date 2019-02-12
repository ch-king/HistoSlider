import sys

from histoslider.app import App
from histoslider.ui.main_window import MainWindow


def main():
    app = App(sys.argv)

    mw = MainWindow(app.report_error)
    mw.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
