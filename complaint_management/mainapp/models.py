from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Complaint(models.Model):

    Status_choices = (
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed"),
    )


    title = models.CharField(max_length=155, blank=False, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    description = models.TextField(blank=False, null=False)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    status = models.CharField(choices=Status_choices, default="New", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    complaint = models.ForeignKey(Complaint, null=False, related_name="comments", blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " " + self.complaint + " " + self.comment
    




