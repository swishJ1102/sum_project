import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QGroupBox, QVBoxLayout, \
    QFileDialog, QTableWidget, QTableWidgetItem, QWidget, QComboBox, QCheckBox, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件管理器")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        # 上半部分
        self.upperGroupBox = QGroupBox("选择文件夹和文件类型")
        upperLayout = QHBoxLayout()

        self.folderLabel = QLabel("选择文件夹:")
        self.folderInput = QLineEdit()
        self.folderInput.setPlaceholderText("点击按钮选择文件夹")
        self.folderButton = QPushButton("选择")
        self.folderButton.clicked.connect(self.selectFolder)

        self.fileTypeLabel = QLabel("选择文件类型:")
        self.fileTypeComboBox = QComboBox()
        self.fileTypeComboBox.addItems(
            ["All Files (*.*)", "Text Files (*.txt)", "Python Files (*.py)", "Java Files (*.java)"])

        upperLayout.addWidget(self.folderLabel)
        upperLayout.addWidget(self.folderInput)
        upperLayout.addWidget(self.folderButton)
        upperLayout.addWidget(self.fileTypeLabel)
        upperLayout.addWidget(self.fileTypeComboBox)

        self.upperGroupBox.setLayout(upperLayout)

        # 中间部分
        self.middleGroupBox = QGroupBox("文件列表")
        middleLayout = QVBoxLayout()

        self.fileTable = QTableWidget()
        self.fileTable.setColumnCount(4)
        self.fileTable.setHorizontalHeaderLabels(["选择", "文件名", "目录", "类型"])

        middleLayout.addWidget(self.fileTable)

        self.middleGroupBox.setLayout(middleLayout)

        # 下半部分
        self.lowerGroupBox = QGroupBox("操作按钮")
        lowerLayout = QHBoxLayout()

        self.convertButton = QPushButton("转换")
        self.convertButton.clicked.connect(self.showConversionWindow)  # 修改这里，连接到显示子窗口的方法
        self.reportButton = QPushButton("报告")
        self.reportButton.clicked.connect(self.generateReport)
        self.exitButton = QPushButton("退出")
        self.exitButton.clicked.connect(self.confirmExit)

        lowerLayout.addWidget(self.convertButton)
        lowerLayout.addWidget(self.reportButton)
        lowerLayout.addWidget(self.exitButton)

        self.lowerGroupBox.setLayout(lowerLayout)

        # 整体布局
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.upperGroupBox)
        mainLayout.addWidget(self.middleGroupBox)
        mainLayout.addWidget(self.lowerGroupBox)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # 信号连接
        self.fileTable.itemClicked.connect(self.selectFile)

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folderPath:
            self.folderInput.setText(folderPath)
            # 列出文件夹下的文件
            self.listFiles(folderPath)

    def listFiles(self, folderPath):
        # 清空表格
        self.fileTable.setRowCount(0)
        # 获取文件类型
        fileTypeFilter = self.fileTypeComboBox.currentText()
        # 遍历文件夹及其子文件夹中的文件
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                if fileTypeFilter == "All Files (*.*)":
                    filePath = os.path.join(root, file)
                    self.addFileToTable(filePath, root)
                else:
                    fileExtension = fileTypeFilter.split(" ")[-1][2:-1]
                    if file.endswith(fileExtension):
                        filePath = os.path.join(root, file)
                        self.addFileToTable(filePath, root)

    def addFileToTable(self, filePath, directory):
        rowPosition = self.fileTable.rowCount()
        self.fileTable.insertRow(rowPosition)
        checkBoxItem = QTableWidgetItem()
        checkBoxItem.setFlags(checkBoxItem.flags() | Qt.ItemIsUserCheckable)
        checkBoxItem.setCheckState(Qt.Unchecked)
        checkBoxItem.filePath = filePath  # 保存文件路径信息
        self.fileTable.setItem(rowPosition, 0, checkBoxItem)
        fileNameItem = QTableWidgetItem(os.path.basename(filePath))
        if checkBoxItem.checkState() == Qt.Checked:
            fileNameItem.setFont(Qt.Bold)
        self.fileTable.setItem(rowPosition, 1, fileNameItem)
        self.fileTable.setItem(rowPosition, 2, QTableWidgetItem(directory))
        self.fileTable.setItem(rowPosition, 3, QTableWidgetItem(filePath.split(".")[-1]))

    def selectFile(self, item):
        if item.column() == 0:  # 只处理复选框列
            checked = item.checkState() == Qt.Checked
            filePath = item.filePath
            if os.path.isdir(filePath):  # 如果是目录，则递归设置子目录下的文件复选框状态
                self.setChildrenCheckState(filePath, checked)
            else:  # 如果是文件，则设置同目录下的文件复选框状态
                self.setSiblingCheckState(filePath, checked)

    def setChildrenCheckState(self, folderPath, checked):
        for root, _, files in os.walk(folderPath):
            for file in files:
                index = self.getIndexFromPath(os.path.join(root, file))
                if index is not None:
                    checkBoxItem = self.fileTable.item(index, 0)
                    checkBoxItem.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def setSiblingCheckState(self, filePath, checked):
        directory = os.path.dirname(filePath)
        for root, _, files in os.walk(directory):
            for file in files:
                index = self.getIndexFromPath(os.path.join(root, file))
                if index is not None:
                    checkBoxItem = self.fileTable.item(index, 0)
                    checkBoxItem.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def getIndexFromPath(self, filePath):
        for i in range(self.fileTable.rowCount()):
            item = self.fileTable.item(i, 1)
            if item.text() == os.path.basename(filePath):
                return i
        return None

    def generateReport(self):
        # 生成报告的逻辑
        pass

    def confirmExit(self):
        reply = QMessageBox.question(self, '确认退出', '确定要退出吗？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def showConversionWindow(self):
        self.conversionWindow = ConversionWindow(self)
        self.conversionWindow.show()
        self.setEnabled(False)  # 主窗口非活化


class ConversionWindow(QDialog):
    def __init__(self, selectedFiles):
        super().__init__()
        self.setWindowTitle("转换窗口")
        self.selectedFiles = selectedFiles
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        self.conversionLabel = QLabel("请选择要进行的转换操作：")

        self.upperGroupBox = QGroupBox("选项")
        upperLayout = QVBoxLayout()

        self.option1CheckBox = QCheckBox("选项1")
        self.option2CheckBox = QCheckBox("选项2")
        self.option3CheckBox = QCheckBox("选项3")

        upperLayout.addWidget(self.option1CheckBox)
        upperLayout.addWidget(self.option2CheckBox)
        upperLayout.addWidget(self.option3CheckBox)

        self.upperGroupBox.setLayout(upperLayout)

        self.convertButton = QPushButton("转换")
        self.convertButton.clicked.connect(self.convertFiles)

        mainLayout.addWidget(self.conversionLabel)
        mainLayout.addWidget(self.upperGroupBox)
        mainLayout.addWidget(self.convertButton)

        self.setLayout(mainLayout)

    def convertFiles(self):
        selectedOptions = []
        if self.option1CheckBox.isChecked():
            selectedOptions.append("选项1")
        if self.option2CheckBox.isChecked():
            selectedOptions.append("选项2")
        if self.option3CheckBox.isChecked():
            selectedOptions.append("选项3")

        # 处理选中的文件和选项
        print(f"选中的文件: {self.selectedFiles}")
        print(f"选中的转换选项: {selectedOptions}")


class ReportWindow(QDialog):
    def __init__(self, reportData):
        super().__init__()
        self.setWindowTitle("报告窗口")
        self.reportData = reportData
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        self.reportLabel = QLabel("生成的报告数据：")
        self.reportTextEdit = QTextEdit()
        self.reportTextEdit.setReadOnly(True)

        generateReportButton = QPushButton("生成报告")
        generateReportButton.clicked.connect(self.generateReportText)

        mainLayout.addWidget(self.reportLabel)
        mainLayout.addWidget(self.reportTextEdit)
        mainLayout.addWidget(generateReportButton)

        self.setLayout(mainLayout)

    def generateReportText(self):
        # 生成报告文本并显示在文本框中
        self.reportTextEdit.clear()
        for file, data in self.reportData.items():
            self.reportTextEdit.append(f"文件: {file}")
            for key, value in data.items():
                self.reportTextEdit.append(f"{key}: {value}")
            self.reportTextEdit.append("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
