# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/17 11:19 
@Author : qinhanluo
@File : tasks.py 
@Software: PyCharm
@Description ： TODO
'''
import os
from celery import Celery
from PIL import Image
import io
import oss2

from Image_enhance.ttypes import *
from Image_enhance import ImageUploadService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

ALIYUN_END_POINT = os.environ.get('ALIYUN_END_POINT', 'http://oss-cn-hangzhou.aliyuncs.com')
ALIYUN_ACCESS_KEY = os.environ.get('ALIYUN_ACCESS_KEY', 'LTAI4GFfg1CGXXcPLFuEmNoE')
ALIYUN_SECRET = os.environ.get('ALIYUN_SECRET', 'GXqXK7cyG1WzX6VGVZiAHChxmt5uA3')
ALIYUN_BUCKET_NAME = os.environ.get('ALIYUN_BUCKET_NAME', 'adacloud')
ALIYUN_OSS_IMAGE_SIZE = os.environ.get('ALIYUN_OSS_IMAGE_SIZE', 256)

ADASPACE_IMAGE_ENHANCE_SERVICE_END_POINT = os.environ.get('ADASPACE_IMAGE_ENHANCE_SERVICE_END_POINT', '182.150.116.28')
ADASPACE_IMAGE_ENHANCE_SERVICE_PORT = os.environ.get('ADASPACE_IMAGE_ENHANCE_SERVICE_PORT', 9090)

celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)

auth = oss2.Auth(ALIYUN_ACCESS_KEY, ALIYUN_SECRET)
bucket = oss2.Bucket(auth, ALIYUN_END_POINT, ALIYUN_BUCKET_NAME)
bucket_update = oss2.Bucket(auth, ALIYUN_END_POINT, 'lqh-cv')

@celery.task(name='mytasks.process')
def download(left_top_y, left_top_x, right_bottom_y, right_bottom_x, z):
    x_range = range(left_top_x, right_bottom_x + 1)
    y_range = range(left_top_y, right_bottom_y + 1)

    total_image = Image.new('RGB', (ALIYUN_OSS_IMAGE_SIZE*len(y_range), ALIYUN_OSS_IMAGE_SIZE*len(x_range)))
    url_address = '2019_06_03/{z}/{y}/{x}.jpg'

    for x in x_range:
        for y in y_range:
            t_address = url_address.format(z=z, y=y, x=x)
            print t_address
            object_stream = bucket.get_object(t_address)
            t_bytes = object_stream.read()
            t_image = Image.open(io.BytesIO(t_bytes))
            total_image.paste(t_image, ((y-y_range[0])*ALIYUN_OSS_IMAGE_SIZE, (x-x_range[0])*ALIYUN_OSS_IMAGE_SIZE))

    # Continue the processing ask the thrift server
    img_bytes = io.BytesIO()
    total_image.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()

    total_name = '{z}_{lt_y}_{lt_x}_{rb_y}_{rb_x}.jpg'.format(z=z, lt_y=left_top_y, lt_x=left_top_x, rb_y=right_bottom_y, rb_x=right_bottom_x)
    thrift_byte = ImageData(total_name, img_bytes, '')

    transport = TSocket.TSocket(ADASPACE_IMAGE_ENHANCE_SERVICE_END_POINT, ADASPACE_IMAGE_ENHANCE_SERVICE_PORT)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = ImageUploadService.Client(protocol)

    '''
    TODO, some more efficient way
    '''
    transport.open()
    ret = client.uploadImage(thrift_byte)
    transport.close()
    '''
    TODO, upload the returned Image into oss2
    '''
    ret_image = Image.open(io.BytesIO(ret.data))
    ret_image.save('test.jpg')

    object_update_location = '{z}/{y}/{x}.jpg'

    for x_update in x_range:
        for y_update in y_range:
            box = ((x_update-x_range[0])*256, (y_update-y_range[0])*256, (x_update-x_range[0]+1)*256, (y_update-y_range[0] + 1)*256)
            t_image = ret_image.crop(box)

            t_img_bytes = io.BytesIO()
            t_image.save(t_img_bytes, format='JPEG')
            t_img_bytes = t_img_bytes.getvalue()
            t_object_location = object_update_location.format(z=18, y=y_update, x=x_update)
            bucket_update.put_object(t_object_location, t_img_bytes)

    # bucket_update.put_object_from_file('test.jpg', 'test.jpg')
    return 'Succeess'
