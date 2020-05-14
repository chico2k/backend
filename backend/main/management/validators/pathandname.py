from django.utils.deconstruct import deconstructible
import uuid
import os

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # eg: filename = 'my uploaded file.jpg'
        ext = filename.split('.')[-1]  # eg: 'jpg'
        uid = uuid.uuid4().hex[:30]  # eg: '567ae32f97567ae32f97567ae32f97'

        # Concat new name
        filename = f'${uid}.${ext}'
        profile_id = str(instance.profile.id)

        # eg: '42/certificate/567ae32f97567ae32f97567ae32f97.jpg'
        return os.path.join(profile_id, self.sub_path, filename)
