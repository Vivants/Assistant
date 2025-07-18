import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(
        #     Qt.CustomizeWindowHint |
        #     Qt.FramelessWindowHint
        # )

        self.initUI()

    def initUI(self):
        self.statusBar().setVisible(False)
        self.browser = QWebEngineView()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("请输入网址………")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # 添加按钮到布局
        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(300, 600, 1080, 600)
        # self.setWindowTitle('桌面管理')
        self.show()
        self.browser.hide()

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()
        self.url_bar.hide()  # 隐藏地址栏
        self.browser.show()

    def toggleStatusBar(self, status):
        self.statusBar().setVisible(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BrowserWindow()
    sys.exit(app.exec_())