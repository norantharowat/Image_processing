## This is the abstract class that the students should implement  

from modesEnum import Modes
import numpy as np
import cv2

class ImageModel():
    def __init__(self):
        pass

    def __init__(self, imgPath: str):
        self.imgPath = imgPath

        self.imgByte = cv2.imread(self.imgPath ,0)
        self.height, self.width = self.imgByte.shape
        self.dft = cv2.dft(np.float32(self.imgByte),flags = cv2.DFT_COMPLEX_OUTPUT)
        self.magnitude = cv2.magnitude(self.dft[:,:,0],self.dft[:,:,1])
        self.uniformMagnitude = np.full((self.magnitude.shape[0] , self.magnitude.shape[1]) , 1)
        self.phase = cv2.phase(self.dft[:,:,0],self.dft[:,:,1])
        self.uniformPhase = np.full((self.phase.shape[0] , self.phase.shape[1]) , 0)
        self.real = self.dft[:,:,0]
        self.imaginary = self.dft[:,:,1]
        
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        
        if mode == Modes.magnitudeAndPhase :
            self.mix = (magnitudeOrRealRatio * self.magnitude + (1 - magnitudeOrRealRatio) * imageToBeMixed.magnitude) * (np.exp(1j*( (1-phaesOrImaginaryRatio) * imageToBeMixed.phase + phaesOrImaginaryRatio * self.phase)))

        elif mode == Modes.realAndImaginary:
            self.mix = (magnitudeOrRealRatio * self.real + (1 - magnitudeOrRealRatio) * imageToBeMixed.real) + 1j * ( (1-phaesOrImaginaryRatio) * imageToBeMixed.imaginary + (phaesOrImaginaryRatio) * self.imaginary )
        elif mode == Modes.magnitudeAndUniformphase:
            self.mix = (magnitudeOrRealRatio * self.magnitude + (1 - magnitudeOrRealRatio) * imageToBeMixed.magnitude)* (np.exp(1j*( self.uniformPhase)))
        elif mode == Modes.phaseAndUniformmagnitude:
            self.mix = (self.uniformMagnitude )* (np.exp(1j*( (1-phaesOrImaginaryRatio) * imageToBeMixed.phase + phaesOrImaginaryRatio * self.phase)))

        self.mix = np.array(np.dstack([self.mix.real,self.mix.imag]))
        self.mix = cv2.idft(self.mix)
        self.mix = cv2.magnitude(self.mix[:,:,0],self.mix[:,:,1])

        return self.mix
