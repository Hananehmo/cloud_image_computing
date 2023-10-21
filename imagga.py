import requests

api_key = 'acc_38c6a3591fef108'
api_secret = '054704a78d16b43bd27665126e3644b3'


def detection_face(image_path):
    response = requests.post(
        'https://api.imagga.com/v2/faces/detections?return_face_id=1',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')})
    print(response.json())
    # return response.json().result.faces[0].face_id
    return response.json()['result']['faces'][0]['face_id']


def check_similarity(face_id1, face_id2):
    response = requests.get(
        'https://api.imagga.com/v2/faces/similarity?face_id=%s&second_face_id=%s' % (face_id1, face_id2),
        auth=(api_key, api_secret))
    print(response.json())
    return response.json()['result']['score']
