from __future__ import absolute_import

import os
from io import BytesIO

from django.conf import settings
from django.utils.functional import cached_property

from PIL import Image

from ckeditor_uploader import utils

import io
from django.core.files.storage import default_storage as storage

THUMBNAIL_SIZE = getattr(settings, "CKEDITOR_THUMBNAIL_SIZE", (75, 75))


class PillowBackend(object):
    def __init__(self, storage_engine, file_object):
        self.file_object = file_object
        self.storage_engine = storage_engine

    @cached_property
    def is_image(self):
        try:
            Image.open(BytesIO(self.file_object.read())).verify()  # verify closes the file
            return True
        except IOError:
            return False
        finally:
            self.file_object.seek(0)

    def _compress_image(self, image):
        quality = getattr(settings, "CKEDITOR_IMAGE_QUALITY", 50)
        basewidth = 600
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth,hsize), Image.ANTIALIAS).convert('RGB')
        in_mem_file = io.BytesIO()
        img.save(in_mem_file, format='JPEG')
        img_write = storage.open(self.image.name, 'w+')
        img_write.write(in_mem_file.getvalue())
        img_write.close()



        # image_tmp = BytesIO()
        # image.save(image_tmp, format="JPEG", quality=quality, optimize=True)
        return image_tmp

    def save_as(self, filepath):
        if not self.is_image:
            saved_path = self.storage_engine.save(filepath, self.file_object)
            return saved_path

        # image = Image.open(self.file_object)
        # img_read = storage.open(self.image.name, 'r')
        img_read = storage.open(self.file.name, 'r')
        image = Image.open(img_read)

        should_compress = getattr(settings, "CKEDITOR_FORCE_JPEG_COMPRESSION", True)
        is_animated = hasattr(image, 'is_animated') and image.is_animated
        if should_compress and not is_animated:
            file_object = self._compress_image(image)
            filepath = "{}.jpg".format(os.path.splitext(filepath)[0])
            saved_path = self.storage_engine.save(filepath, file_object)
        else:
            file_object = self.file_object
            saved_path = self.storage_engine.save(filepath, self.file_object)
        

        img_read.close()
        # if not is_animated:
            # self.create_thumbnail(file_object, saved_path)
        return saved_path

    def create_thumbnail(self, file_object, file_path):
        thumbnail_filename = utils.get_thumb_filename(file_path)
        thumbnail_io = BytesIO()
        image = Image.open(file_object).convert('RGB')
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        image.save(thumbnail_io, format='JPEG', optimize=True)
        return self.storage_engine.save(thumbnail_filename, thumbnail_io)
