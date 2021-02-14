from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QTableWidgetItem,QTextEdit
from pyqtgraph import PlotWidget, plot
from arctic import Arctic
import matplotlib
import matplotlib.pyplot as plt
import sys, os, time

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('form.ui', self)

        '''set button functions'''
        self.pushButton.pressed.connect(self.mongo_party2)
        self.pushButton_2.pressed.connect(self.mongo_party3)
        self.pushButton_3.pressed.connect(self.start_process)
        self.textEdit.setReadOnly(True)

        '''start mongo server'''
        if os.system("systemctl status mongod | grep inactive") == 0:
            os.system("systemctl start mongod")
        else:
            pass

        '''access mongo server'''
        self.store = Arctic('localhost')
        # Create the library - defaults to VersionStore
        self.store.initialize_library('HISTORICAL_DATA')
        # Access the library
        self.library = self.store['HISTORICAL_DATA']

        '''table selection change'''
        self.tableWidget.doubleClicked.connect(self.on_click)
        
        '''set plot'''
    '''def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)'''
    
    def mongo_party2(self):
        self.items1=self.library.read('BTC')
        self.BTC=self.items1.data.head(1)['1a. open (USD)']
        self.btc_wig=int(self.BTC.iloc[0])
        self.tableWidget.setData(0, 3, QTableWidgetItem(self.btc_wig))
        self.items2=self.library.read('ETH')
        self.ETH=self.items2.data.head(1)['1a. open (USD)']
        self.eth_wig=int(self.ETH.iloc[0])
        self.tableWidget.setData(1, 3, QTableWidgetItem(self.eth_wig))
        self.items3 = self.library.read('LTC')
        self.LTC = self.items3.data.head(1)['1a. open (USD)']
        self.ltc_wig = int(self.LTC.iloc[0])
        self.tableWidget.setData(2, 3, QTableWidgetItem(self.ltc_wig))

    def mongo_party3(self):
        os.system("systemctl stop mongod")    

    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            if currentQTableWidgetItem.text() =="BIT":
                self.bit_plot=self.get_historic_bit()
                self.graphWidget.clear()

                self.graphWidget.plot(self.bit_plot)
            elif currentQTableWidgetItem.text()=="ETH":
                self.eth_plot=self.get_historic_eth()
                self.graphWidget.clear()

                self.graphWidget.plot(self.eth_plot)
            elif currentQTableWidgetItem.text()=="LTC":
                self.ltc_plot=self.get_historic_bit()
                self.graphWidget.clear()

                self.graphWidget.plot(self.ltc_plot)

    def message(self, s):
        self.textEdit.append(s)

    def get_historic_bit(self):
        self.items_btc = self.library.read('BTC')
        self.BTC1=self.items_btc.data['1a. open (USD)']
        self.BTC1=self.BTC1.iloc[::-1]
        return self.BTC1

    def get_historic_eth(self):
        self.items_eth = self.library.read('ETH')
        self.ETH1 = self.items_eth.data['1a. open (USD)']
        self.ETH1 = self.ETH1.iloc[::-1]
        return self.ETH1

    def get_historic_ltc(self):
        self.items_ltc = self.library.read('LTC')
        self.LTC1 = self.items_ltc.data['1a. open (USD)']
        self.LTC1 = self.LTC1.iloc[::-1]
        return self.LTC1

    def start_process(self):
        self.message("Sending it.")
        self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.p.start("python3", ['Alpha_vantage_trader.py'])
        self.p.finished.connect(self.process_finished)  # Clean up once complete.


    def process_finished(self):
        time.sleep(4)
        '''set table items'''
        self.set_table_values()
        self.message("Sent")
        self.p = None

    def set_table_values(self):
        self.items1=self.library.read('BTC')
        self.BTC=self.items1.data.head(1)['1a. open (USD)']
        self.btc_wig=str(self.BTC.iloc[0])
        self.tableWidget.setItem(0, 3, QTableWidgetItem(self.btc_wig))
        self.items2=self.library.read('ETH')
        self.ETH=self.items2.data.head(1)['1a. open (USD)']
        self.eth_wig=str(self.ETH.iloc[0])
        self.tableWidget.setItem(1, 3, QTableWidgetItem(self.eth_wig))
        self.items3 = self.library.read('LTC')
        self.LTC = self.items3.data.head(1)['1a. open (USD)']
        self.ltc_wig = str(self.LTC.iloc[0])
        self.tableWidget.setItem(2, 3, QTableWidgetItem(self.ltc_wig))


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':         
    main()