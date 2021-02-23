from flask import Flask, render_template, request, send_file, Response
import cv2
import numpy as np
import json
import requests
import base64
import matplotlib.pyplot as plt
import time
import os

app = Flask(__name__)
app.config['static'] = os.path.join('static', 'images')
app.config['upload_folder'] = os.path.join('static', 'results')

secret_file = "api_address.json"
with open(secret_file) as f:
    addresses = json.loads(f.read())


@app.route('/')
def home():
    return render_template('index.html')


########################################################

@app.route('/upload/strawberries')
def upload_straw():
    return render_template('uploadstrawberries.html')


@app.route('/upload/tomatoes')
def upload_tomato():
    return render_template('uploadtomatoes.html')


@app.route('/upload/paprika')
def upload_pap():
    return render_template('uploadpaprika.html')

@app.route('/upload/melon')
def upload_mel():
    return render_template('uploadmelon.html')


###########################################################

@app.route('/tomato', methods=['GET', 'POST'])
def result_toma():

    try:
        # Set content_type to header.
        content_type = 'application/json'
        headers = {'content-type': content_type}

        # upload image string array data.
        img_file = request.files['file'].stream.read()

        img = cv2.imdecode(np.fromstring(img_file, np.uint8), cv2.IMREAD_COLOR)

        # map to json.
        send = base64.b64encode(np.array(img))

        request_json = json.dumps({'input_img': send.decode(),
                                   'info': {
                                       'height': img.shape[0],
                                       'width': img.shape[1],
                                       'channel': img.shape[2]
                                   }
                                   })

        # http request.
        # print(request_json)
        response = requests.post(addresses["TOMATO_SERVER"], data=request_json, headers=headers)
        # print(response)

        # ['data', 'time', 'is_gpu']
        response_json = response.json()
        print(response_json)
        cost = response_json['time']
        is_gpu = response_json['is_gpu']

        # change to numpy array.
        r = base64.decodebytes(response_json['data'].encode())
        response_dat = np.fromstring(r, dtype=np.float)

        response_dat = response_dat.reshape((response_json['info']['height'],
                                             response_json['info']['width'],
                                             response_json['info']['channel']))

        # decodeed numpy image.
        plt.figure(figsize=(int(7 * (response_json['info']['width'] / response_json['info']['height'])), 7))
        plt.imshow(response_dat)
        timenow = str(time.time())
        fname = os.path.join('static', 'results', 'tomato', timenow + '.png')
        plt.axis('off')
        plt.savefig(fname)

        return render_template('tom_result.html', outimg=fname, timenow=timenow, cost=cost, is_gpu=is_gpu)

    except:
        return render_template('uploadtomatoes.html', alertflag="이미지가 너무 크거나 올바르지 않은 파일입니다.")


@app.route('/strawberry', methods=['GET', 'POST'])
def result_straw():

    try:
        # Set content_type to header.
        content_type = 'application/json'
        headers = {'content-type': content_type}

        # upload image string array data.
        img_file = request.files['file'].stream.read()

        img = cv2.imdecode(np.fromstring(img_file, np.uint8), cv2.IMREAD_COLOR)

        # map to json.
        send = base64.b64encode(np.array(img))

        request_json = json.dumps({'input_img': send.decode(),
                                   'info': {
                                       'height': img.shape[0],
                                       'width': img.shape[1],
                                       'channel': img.shape[2]
                                   }
                                   })

        # http request.
        response = requests.post(addresses["STRAWBERRY_SERVER"], data=request_json, headers=headers)
        # print(response)

        # ['data', 'time', 'is_gpu']
        response_json = response.json()
        cost = response_json['time']
        is_gpu = response_json['is_gpu']

        # change to numpy array.
        r = base64.decodebytes(response_json['data'].encode())
        response_dat = np.fromstring(r, np.float)

        response_dat = response_dat.reshape((response_json['info']['height'],
                                             response_json['info']['width'],
                                             response_json['info']['channel']))

        # decodeed numpy image.
        plt.figure(figsize=(7, 7))
        plt.imshow(response_dat)
        timenow = str(time.time())
        fname = os.path.join('static', 'results', 'strawberry', timenow + '.png')
        plt.axis('off')
        plt.savefig(fname)

        return render_template('str_result.html', outimg=fname, timenow=timenow, cost=cost, is_gpu=is_gpu)

    except:
        return render_template('uploadstrawberries.html', alertflag="이미지가 너무 크거나 올바르지 않은 파일입니다.")


@app.route('/paprika', methods=['GET', 'POST'])
def result_pap():

    try:
        # Set content_type to header.
        content_type = 'application/json'
        headers = {'content-type': content_type}

        # upload image string array data.
        img_file = request.files['file'].stream.read()

        img = cv2.imdecode(np.fromstring(img_file, np.uint8), cv2.IMREAD_COLOR)

        # map to json.
        send = base64.b64encode(np.array(img))

        request_json = json.dumps({'input_img': send.decode(),
                                   'info': {
                                       'height': img.shape[0],
                                       'width': img.shape[1],
                                       'channel': img.shape[2]
                                   }
                                   })


        # http request.
        response = requests.post(addresses["PAPRIKA_SERVER"], data=request_json, headers=headers)
        # print(response)

        # ['data', 'time', 'is_gpu']
        response_json = response.json()
        cost = response_json['time']
        is_gpu = response_json['is_gpu']

        # change to numpy array.
        r = base64.decodebytes(response_json['data'].encode())
        response_dat = np.fromstring(r, dtype=np.float)

        response_dat = response_dat.reshape((response_json['info']['height'],
                                             response_json['info']['width'],
                                             response_json['info']['channel']))

        # decodeed numpy image.
        plt.figure(figsize=(7, 7))
        plt.imshow(response_dat)
        timenow = str(time.time())
        fname = os.path.join('static', 'results', 'paprika', timenow + '.png')
        plt.axis('off')
        plt.savefig(fname)

        return render_template('pap_result.html', outimg=fname, timenow=timenow, cost=cost, is_gpu=is_gpu)

    except:
        return render_template('uploadpaprika.html', alertflag="이미지가 너무 크거나 올바르지 않은 파일입니다.")

@app.route('/melon', methods=['GET', 'POST'])
def result_mel():
    """ 아직 모델이 없는 관계로 파프리카 모델 임시 사용 """
    try:
        # Set content_type to header.
        content_type = 'application/json'
        headers = {'content-type': content_type}

        # upload image string array data.
        img_file = request.files['file'].stream.read()

        img = cv2.imdecode(np.fromstring(img_file, np.uint8), cv2.IMREAD_COLOR)

        # map to json.
        send = base64.b64encode(np.array(img))

        request_json = json.dumps({'input_img': send.decode(),
                                   'info': {
                                       'height': img.shape[0],
                                       'width': img.shape[1],
                                       'channel': img.shape[2]
                                   }
                                   })


        # http request.
        response = requests.post(addresses["PAPRIKA_SERVER"], data=request_json, headers=headers)
        # print(response)

        # ['data', 'time', 'is_gpu']
        response_json = response.json()
        cost = response_json['time']
        is_gpu = response_json['is_gpu']

        # change to numpy array.
        r = base64.decodebytes(response_json['data'].encode())
        response_dat = np.fromstring(r, dtype=np.float)

        response_dat = response_dat.reshape((response_json['info']['height'],
                                             response_json['info']['width'],
                                             response_json['info']['channel']))

        # decodeed numpy image.
        plt.figure(figsize=(7, 7))
        plt.imshow(response_dat)
        timenow = str(time.time())
        fname = os.path.join('static', 'results', 'paprika', timenow + '.png')
        plt.axis('off')
        plt.savefig(fname)

        return render_template('mel_result.html', outimg=fname, timenow=timenow, cost=cost, is_gpu=is_gpu)

    except:
        return render_template('uploadmelon.html', alertflag="이미지가 너무 크거나 올바르지 않은 파일입니다.")


################################################################################

@app.route('/delete_file', methods=['POST'])
def delete():
    if request.method == "POST":
        filename = request.form['filename']
        if os.path.isfile(filename):
            os.remove(filename)

    return Response(status="ok")


################################################################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
