from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class ProfileSettings(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="settings"
    )
    is_public = models.BooleanField(default=True)
    hide_email = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Settings"

class ProfileLink(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_links")

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Link(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=300)

    def __str__(self):
        return self.name

class Photo(models.Model):
    photo = CloudinaryField("image", folder="projects_photos", resource_type="image", blank=True, null=True)

    def __str__(self):
        return f"Photo {self.id}"

class Project(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    links = models.ManyToManyField(
        Link,
        blank=True,
        related_name="projects"
    )
    photos = models.ManyToManyField(
        Photo,
        blank=True,
        related_name="projects"
    )

    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="liked_projects"
    )

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Comment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.name}"


class Dashboard(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="dashboard"
    )
    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="dashboards"
    )

    def __str__(self):
        return f"{self.user.username}'s Dashboard"