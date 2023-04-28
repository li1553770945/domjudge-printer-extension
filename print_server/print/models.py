from django.db import models
import os
import uuid
def rename_file(instance, filename):
    if not os.path.exists("files"):
        os.mkdir("files")
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid.uuid1().hex}{ext}"
    return f"files/{new_filename}"

# Create your models here.
class PrintModel(models.Model):
    team_id = models.CharField(max_length=30,default="")
    team_name = models.CharField(max_length=100,default="")
    language = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(choices=(
        ("pending","pending"),
        ("processing","processing"),
        ("done","done")),
        max_length=10,
        default = "pending"
    )
    original_name = models.CharField(max_length=100)
    submit_time = models.DateTimeField(auto_now_add=True,null=True)
    process_start_time = models.DateTimeField(null=True)
    done_time = models.DateTimeField(null=True)
    file = models.FileField(upload_to=rename_file)

