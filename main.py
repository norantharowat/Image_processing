from PyQt5 import QtWidgets
from PyQt5 import *
from gui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from copy import copy
from modesEnum import Modes
from imageModel import ImageModel
import logging

logging.basicConfig(filename= 'Log_File.log')
logging.root.setLevel(20)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.img_1 = ''
        self.img_2 = ''
        self.height2 = 0
        self.width2 = 0
        self.components = [self.ui.graphicsView_2 ,self.ui.graphicsView_4]
        self.Scales = [self.ui.s1 , self.ui.s2]
        self.comboBoxes =[self.ui.comboBox,self.ui.comboBox_2,self.ui.comboBox_3,self.ui.comboBox_4,self.ui.comboBox_5,self.ui.comboBox_6,self.ui.comboBox_7]
        self.ui.load1.triggered.connect(lambda: self.open_file(  0 , self.ui.graphicsView))
        self.ui.load2.triggered.connect(lambda: self.open_file( 1, self.ui.graphicsView_3))



    def open_file(self, img_number, viewBox):

        self.file_name = QFileDialog().getOpenFileName(self,'Open file', '/home',"signals(*.png , *.jpg )")
        
        if self.file_name[0] != '' :
            if img_number == 0 :
                logging.info('load image 1 from file menu was clicked')

                self.img_1 = copy(self.file_name[0]) 
                self.plot(ImageModel(self.img_1).imgByte,viewBox )
                self.plot_components(0, self.img_1)
                self.comboBoxes[0].currentIndexChanged.connect(lambda: self.plot_components(0, self.img_1))
                
            else :
                logging.info('load image 2 from file menu was clicked')

                self.img_2 = copy(self.file_name[0]) 
                self.plot(ImageModel(self.img_2).imgByte,viewBox )

                self.plot_components(1, self.img_2)
                self.comboBoxes[1].currentIndexChanged.connect(lambda: self.plot_components(1, self.img_2))


            self.compare_size( self.img_1 , self.img_2 )

            self.control_options()
            
            for i in range(2,6) : 
                self.comboBoxes[i].currentIndexChanged.connect(lambda: self.control_options())
            

        else :
            logging.info('load image 1 or load image 2 was clicked but no image was added')
            
            # pass
        


    def compare_size (self, img_1 , img_2):
     
        if img_1 != '' and img_2 == '':
            for i in range(2,7):
                    self.comboBoxes[i].setDisabled(True)
            for i in range(2):
                self.Scales[i].setDisabled(True)
            
        
        elif img_1 != '' and img_2 != '':
            imgobject1 = ImageModel(img_1)
            imgobject2 = ImageModel(img_2)
            
            if (imgobject2.height == imgobject1.height) & (imgobject2.width == imgobject1.width) :
                for i in range(7):
                    self.comboBoxes[i].setDisabled(False)
                for i in range(2):
                    self.Scales[i].setDisabled(False)
                logging.info('pass the comare size test')

            else :
                QMessageBox.about(self,"Warning","please load images of the same size" )
                logging.warning('user tried to add two images of diffrent sizes')

                for i in range(7):
                    self.comboBoxes[i].setDisabled(True)
                for i in range(2):
                    self.Scales[i].setDisabled(True)


    def plot_components(self , imageNum , Image) :
        
        self.imgobject = ImageModel(Image)

        if self.comboBoxes[imageNum].currentText() == "Magnitude" :
            self.plot(20*np.log(self.imgobject.magnitude) , self.components[imageNum] )
            logging.info("'Plot magnitude component of image',{0}".format(imageNum+1))
       
        elif self.comboBoxes[imageNum].currentText() == "Phase" :
            self.plot(self.imgobject.phase , self.components[imageNum] )
            logging.info("'Plot phase component of image',{0}".format(imageNum+1))
            
        elif self.comboBoxes[imageNum].currentText() == "Real" :
            self.plot(self.imgobject.real , self.components[imageNum] )
            logging.info("'Plot Real component of image',{0}".format(imageNum+1))
           
        elif self.comboBoxes[imageNum].currentText() == "Imaginary" :
            self.plot(self.imgobject.imaginary , self.components[imageNum] )
            logging.info("'Plot Imaginary component of image',{0}".format(imageNum+1))

            


    def plot(self  , data , widget):
        widget.canvas.axes.imshow(data, cmap = 'gray')
        widget.canvas.draw()

    def control_options(self):
        if self.ui.comboBox_5.currentText() == "Magnitude"  :
            self.ui.comboBox_7.clear()
            self.ui.comboBox_7.addItem("Phase")
            self.ui.comboBox_7.addItem("Uniform Phase")
            logging.info('user picked magnitude of component 1 ')
           
        elif self.ui.comboBox_5.currentText() == "Phase"  :
            self.ui.comboBox_7.clear()
            self.ui.comboBox_7.addItem("Magnitude")
            self.ui.comboBox_7.addItem("Uniform magnitude")
            logging.info('user picked phase of component 1 ')

        elif self.ui.comboBox_5.currentText() == "Imaginary"  :
            self.ui.comboBox_7.clear()
            self.ui.comboBox_7.addItem("Real")
            logging.info('user picked Imaginary of component 1 ')
            
        else :
            self.ui.comboBox_7.clear()
            self.ui.comboBox_7.addItem("Imaginary")
            logging.info('user picked Real of component 1 ')

        if self.img_1 != '' and self.img_2 != '':
            logging.info('Mixing was performed ')

            self.show_mix()
            self.ui.comboBox_7.currentTextChanged.connect(self.dummy_function)
            for sliderNum in range(2) :
                self.Scales[sliderNum].sliderPressed.connect(self.sldDisconnect)
                self.Scales[sliderNum].sliderReleased.connect(self.show_mix)
            
    def dummy_function(self):
        if self.ui.comboBox_7.currentText() =="Uniform magnitude" or self.ui.comboBox_7.currentText() =="Uniform Phase" :
            logging.info('component 2 comboBox was Clicked and mixing performed ')

            self.show_mix()
        else :
            pass
    def sldDisconnect(self):
        pass
    
    

    def get_Mode(self):

        if self.ui.comboBox_5.currentText() == "Magnitude" and self.ui.comboBox_7.currentText() == "Phase" :
            logging.info("'Magnitude of component 1 with ratio ',{0},' and phase of component 2 with ratio',{1},'was mixed'".format(self.ui.s1.value() /100, self.ui.s2.value() /100))

            self.ui.s2.setDisabled(False)
            return(self.ui.s1.value() /100, 1- self.ui.s2.value()/100 ,Modes.magnitudeAndPhase)

            
        elif self.ui.comboBox_5.currentText() == "Phase" and self.ui.comboBox_7.currentText() == "Magnitude" :
            logging.info("'Phase of component 1 with ratio ',{0},' and magnitude of component 2 with ratio',{1},'was mixed'".format(self.ui.s1.value() /100, self.ui.s2.value() /100))

            self.ui.s2.setDisabled(False)
            return(1- self.ui.s2.value()/100, self.ui.s1.value()/100 ,Modes.magnitudeAndPhase)
            
        elif self.ui.comboBox_5.currentText() == "Real" and self.ui.comboBox_7.currentText() == "Imaginary" :
            logging.info("'Real of component 1 with ratio ',{0},' and Imaginary of component 2 with ratio',{1},'was mixed'".format(self.ui.s1.value() /100, self.ui.s2.value() /100))
            
            self.ui.s2.setDisabled(False)
            return(self.ui.s1.value() /100, 1 - self.ui.s2.value() /100 , Modes.realAndImaginary)
            
        elif self.ui.comboBox_5.currentText() == "Imaginary" and self.ui.comboBox_7.currentText() == "Real" :
            logging.info("'Imaginary of component 1 with ratio ',{0},' and Real of component 2 with ratio',{1},'was mixed'".format(self.ui.s1.value() /100, self.ui.s2.value() /100))

            self.ui.s2.setDisabled(False)
            return(1- self.ui.s2.value() /100, self.ui.s1.value() /100 ,Modes.realAndImaginary)
            
        elif self.ui.comboBox_5.currentText() == "Magnitude" and self.ui.comboBox_7.currentText() == "Uniform Phase" :
            logging.info("'Magnitude of component 1 with ratio ',{0},' and Uniform phase was mixed'".format(self.ui.s1.value() /100))

            self.ui.s2.setDisabled(True)
            return(self.ui.s1.value() /100, self.ui.s1.value() /100 ,Modes.magnitudeAndUniformphase)
            
        elif self.ui.comboBox_5.currentText() == "Phase" and self.ui.comboBox_7.currentText() == "Uniform magnitude" :
            logging.info("'Phas of component 1 with ratio ',{0},' and Uniform magnitude was mixed'".format(self.ui.s1.value() /100))

            self.ui.s2.setDisabled(True)
            return(self.ui.s1.value() /100, self.ui.s1.value() /100 ,Modes.phaseAndUniformmagnitude)
            
    def show_mix(self):
        if  self.ui.comboBox_4.currentText() == "Image 1" and self.ui.comboBox_6.currentText() == "Image 2" :
            image1object = ImageModel(self.img_1)
            s1 , s2 , mode = self.get_Mode()
            data = image1object.mix( ImageModel(self.img_2) , s1 , s2 , mode )
        
        elif  self.ui.comboBox_4.currentText() == "Image 2" and self.ui.comboBox_6.currentText() == "Image 1" :
            image1object = ImageModel(self.img_2)
            s1 , s2 , mode = self.get_Mode()
            data = image1object.mix( ImageModel(self.img_1) , s1 , s2 , mode )
        
        elif  self.ui.comboBox_4.currentText() == "Image 1" and self.ui.comboBox_6.currentText() == "Image 1" :
            image1object = ImageModel(self.img_1)
            s1 , s2 , mode = self.get_Mode()
            data = image1object.mix( ImageModel(self.img_1) , s1 , s2 , mode )
        
        elif  self.ui.comboBox_4.currentText() == "Image 2" and self.ui.comboBox_6.currentText() == "Image 2" :
            image1object = ImageModel(self.img_2)
            s1 , s2 , mode = self.get_Mode()
            data = image1object.mix( ImageModel(self.img_2) , s1 , s2 , mode )

        if self.ui.comboBox_3.currentText()  == "Output 1" :
            logging.info("mixing output showed on output 1")

            self.plot(data , self.ui.graphicsView_5 )
        else :
            logging.info("mixing output showed on output 2")

            self.plot(data , self.ui.graphicsView_6 )

            




def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()

if __name__ == "__main__":
    main()