import os
import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *


class AboutDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel('PyQT Browser')
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel('Version 0.1'))
        layout.addWidget(QLabel('Copyright Me'))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.setCentralWidget(self.browser)

        self.show()

        # Nav Bar
        navtb = QToolBar('Navigation')
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # Back Button
        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), 'Back', self)
        back_btn.setStatusTip('Back to previous page')
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # Reload Button
        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), 'Reload', self)
        reload_btn.setStatusTip('Reload Page')
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # Next Button
        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), 'Forward', self)
        next_btn.setStatusTip('Forward to the next page')
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # Home Button
        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), 'Home', self)
        home_btn.setStatusTip('Go Home')
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # Stop Button
        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), 'Stop', self)
        stop_btn.setStatusTip('Stop loading current page')
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # HTTPS Icon
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-noss1.png')))
        navtb.addWidget(self.httpsicon)

        # URL Bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        ## Url Status
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        # File Menu
        self.menuBar().setNativeMenuBar(False)
        file_menu = self.menuBar().addMenu('&File')

        # Open File
        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), 'Open file...', self)
        open_file_action.setStatusTip('Open from file')
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        # Save File
        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), 'Save Page As...', self)
        save_file_action.setStatusTip('Save current page to file')
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        # Help Menu
        help_menu = self.menuBar().addMenu('&Help')

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), 'About', self)
        about_action.setStatusTip('Find out more')
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_browser_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')), 'Navigate', self)
        navigate_browser_action.setStatusTip('Go to Homepage')
        navigate_browser_action.triggered.connect(self.navigate_browser)
        help_menu.addAction(navigate_browser_action)


    # Slot for Navigate Home
    def navigate_home(self):
        self.browser.setUrl(QUrl('http://www.google.com'))

    # Slot for URL Navigation
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        
        self.browser.setUrl(q)

    # Slot for Url Status
    def update_urlbar(self, q):
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-noss1.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # Slot for Title
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f'{title} - PyQT Browser')

    # Open File
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', '',
                                                  'Hypertext Markup Language (*.htm *.html);;'
                                                  'All files (*.*)')
        
        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Page As', '',
                                                  'Hypertext Markup Language (*.htm *.html);;'
                                                  'All files (*.*)')
        
        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def navigate_browser(self):
        self.browser.setUrl(QUrl('https://www.pythonguis.com/courses/example-browser/'))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()


app = QApplication(sys.argv)
window = MainWindow()

app.exec()
