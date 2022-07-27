
from cv2 import CV_32F
import numpy as np
import cv2 as cv
from PIL import Image , ImageChops , ImageMath ,ImageEnhance


numpy_file = np.load('./models/pts_in_hull.npy')
Caffe_net = cv.dnn.readNetFromCaffe("./models/colorization_deploy_v2.prototxt", "./models/colorization_release_v2.caffemodel")
numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)


def gray2clor(image):
    frame =  image #cv.imread(image)
 
    Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [numpy_file.astype(np.float32)]
    Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]
    
    input_width = 224
    input_height = 224
    rgb_img = (frame[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
    lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
    l_channel = lab_img[:,:,0] 

    l_channel_resize = cv.resize(l_channel, (input_width, input_height)) 
    l_channel_resize -= 50
    Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
    ab_channel = Caffe_net.forward()[0,:,:,:].transpose((1,2,0)) 

    (original_height,original_width) = rgb_img.shape[:2] 
    ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
    lab_output = np.concatenate((l_channel[:,:,np.newaxis],ab_channel_us),axis=2) 
    bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)

    
    bgr_output = (bgr_output*255).astype(np.uint8)

    img = cv.cvtColor(bgr_output, cv.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)

    return enchanment(im_pil)
   

def enchanment(image):
    
    ori = image
    ychannel = Image.new('RGB', (ori.width, ori.height), (255, 255, 220))
    rA, gA, bA = ori.split()
    rB, gB, bB = ychannel.split()
    rTmp = ImageMath.eval("int(a/((float(b)+1)/256))", a=rA, b=rB).convert('L')
    gTmp = ImageMath.eval("int(a/((float(b)+1)/256))", a=gA, b=gB).convert('L')
    bTmp = ImageMath.eval("int(a/((float(b)+1)/256))", a=bA, b=bB).convert('L')
    Clrcorect = Image.merge("RGB", (rTmp, gTmp , bTmp))
    shpfct = 1.5
    sharpn = ImageEnhance.Sharpness(Clrcorect)
    fn=sharpn.enhance(shpfct)
    fn = cv.cvtColor(np.array(fn), cv.COLOR_RGB2BGR)
    return fn


def vcont(video):

    video_name = video.split(".")
    video_out = video_name[0] + "-cont." + video_name[-1]
    vid = cv.VideoCapture(video)
    v_wid = int(vid.get(3))
    v_height= int(vid.get(4))
    fps = int(vid.get(5))
    output = cv.VideoWriter(video_out, cv.VideoWriter_fourcc('D','I','V','X'), fps, (v_wid , v_height))
    i = 0
    while(True):
        ret , frame = vid.read()
        i+=1
        print(i)
   
        if ret:
            color = gray2clor(frame)
            cv.imshow("frame" , color)
            key = cv.waitKey(20)
            if key == ord('q'):
                break
            output.write(color)
        else:
            break

    output.release()
    vid.release()


def imageconverion(image):
    img = image.split(".")
    output = img[0] + "-cont." + img[-1]
    imgcv = cv.imread(image)
    cvtimg = gray2clor(imgcv)
    cv.imwrite(output , cvtimg)
