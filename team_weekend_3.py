from flask import Flask, jsonify, request
import base64
import skimage.draw
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2
import numpy as np
from scipy.spatial.qhull import ConvexHull
import videooverlay as video
import ffmpeg
import os
import glob
import wave, warnings

# tmp_image ==> 내얼굴과 영상의 합성되는 공간
# tmp==>tmp_image에서 합성된 사진을 mp4동영상으로 만들어 저장
# team ==> 프로필 원본
# team1 ==> 프로필에서 얼굴만 크롭하여 저장
# receive ==> 음성합성을위해 클라이언트로부터 받은 디렉토리 
# condition == > php 저장소
# final ==> 최종 합성 된 곳
# zzal ==> 짤로만든 영상
# upload ==> 짤 썸내일
# python3 team_weekend_3.py 로 실행해야한다 


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/var/www/html/shape_predictor_68_face_landmarks.dat")

predictor_model = "/var/www/html/shape_predictor_68_face_landmarks.dat"
fa = FaceAligner(predictor, desiredFaceWidth=546)

app = Flask(__name__)


@app.route('/')
def index():
    return 'aaaaa'


@app.route('/voiceupload', methods=['POST', 'GET'])
def abc():
    if request.method == 'POST':
        file = request.files['file']
        tmpname = file.filename
        tmpname1 = []
        tmpname2 = []
        tmpname3 = []
        tmpname1 = tmpname.split('.')
        tmpname2 = tmpname1[0]
        tmpname3 = tmpname2.split('_')
        user = tmpname3[1]
        num = tmpname3[0]
        voice = tmpname3[2]
        time = tmpname3[3]
        print(tmpname,user, num, voice, time)

        print('음성 전송 시작')
        # receive 음성 파일 저장하는 공간 
        file.save('/var/www/html/receive/' + user + time + '.mp4')
        print('음성 파일 저장, 비디오 합성 시작')
        video.choice(user, num)
        print('이미지 비디오 합치기 시작')

        makeVideo(user, time)
        print('비디오 만들기 완성')
        print('mp4로 합성된 이미지를 음성 변조를 위해 wav파일로 변환 ')
        os.system("rm -rf /var/www/html/receive/" + user + time + ".wav")
        os.system("ffmpeg -i /var/www/html/receive/" + user + time + ".mp4 -ac 2 -f wav /var/www/html/receive/" + user + time + ".wav")
        print('합성 이미지 삭제')
        os.system("rm -rf /var/www/html/tmp_image/" + user)
        print('업로드한 사용자 원본 목소리 파일 삭제')
        os.system("rm -rf /var/www/html/receive/" + user + time + ".mp4")

        
       
        print('변조없음')
        # wav 파일을 mp4 파일로 변환 
        os.system("ffmpeg -i /var/www/html/receive/" + user + time + ".wav -ac 2 -f mp4 /var/www/html/receive/" + user + time + ".mp4")
        os.system("rm -rf /var/www/html/receive/" + user + time + ".wav")
        os.system("rm -rf /var/www/html/final/" + user + time + ".mp4")
        os.system("ffmpeg -i /var/www/html/receive/" + user + time + ".mp4 -i " + "/var/www/html/tmp/" + user + time + ".mp4 -c copy /var/www/html/final/" + user + time + ".mp4")
        os.system("rm -rf /var/www/html/tmp/" + user + time + ".mp4")
        os.system("rm -rf /var/www/html/receive/" + user + time + ".mp4")
        print('최종 완료')
    
        return jsonify({'insert' : 'ok'}), 200


@app.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        user = request.form['id']
        file = request.files['file']
        # team 유저 프로필 이미지 
        # team1 유저 프로필에서 얼굴만 크롭하여 저장
        file.save('/var/www/html/team/' + user + '.jpg')

        file_name = '/var/www/html/team/' + user + '.jpg'
        image = cv2.imread(file_name)
        image = imutils.resize(image, width=1010)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 1)

        for rect in rects:
            (x, y, w, h) = rect_to_bb(rect)
            sp = predictor(image, rect)
            landmarks = np.array([[p.x, p.y] for p in sp.parts()])

            vertices = ConvexHull(landmarks).vertices
            Y, X = skimage.draw.polygon(landmarks[vertices, 1], landmarks[vertices, 0])
            cropped_img = np.zeros(image.shape, dtype=np.uint8)
            cropped_img[Y, X] = image[Y, X]

            image = imutils.resize(cropped_img, width=1000, height=1000)
            faceAligned = fa.align(image, gray, rect)

            cv2.imwrite("/var/www/html/team1/{}.jpg".format(user), faceAligned)

            src = cv2.imread("/var/www/html/team1/{}.jpg".format(user), 1)

            tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
            b, g, r = cv2.split(src)
            rgba = [b, g, r, alpha]
            dst = cv2.merge(rgba, 4)
            cv2.imwrite("/var/www/html/team1/{}.jpg".format(user), dst)
            cv2.waitKey(0)

    # return "success"
    return jsonify({'insert' : 'ok'}), 200

@app.route('/detect', methods=["POST"])
def detect():
    imgBytes = request.data
    imgdata = base64.b64decode(imgBytes)
    with open("test.mp4", 'wb') as f:
        f.write(imgdata)
    return 'success'


def makeVideo(user, time):
    count = 1
    img_array = []
    for tmp_image in glob.glob('/var/www/html/tmp_image/' + user + '/*.jpg'):
        img = cv2.imread('/var/www/html/tmp_image/' + user + '/' + str(count) + '.jpg')
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
        count += 1

    out = cv2.VideoWriter('/var/www/html/tmp/' + user + time + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    print("비디오 완성")
    out.release()


if __name__ == "__main__":
    app.run('0.0.0.0', port=11000)
