from django.core.exceptions import ValidationError

def validate_image(image):
   file_size = image.size
   limit_kb = 500 # 500KB
   if file_size > limit_kb * 1024:
      raise ValidationError(f"The maximum file size that can be uploaded is {limit_kb}KB")
   
   valid_mime_types = ['image/jpeg', 'image/png']
   if image.content_type not in valid_mime_types:
      raise ValidationError(f"The file must be a JPEG or PNG image")

def validate_file_size(file):
   file_size = file.size
   limit_kb = 1024 # 1MB
   if file_size > limit_kb * 1024:
      raise ValidationError(f"The maximum file size that can be uploaded is {limit_kb}KB")
   
   

