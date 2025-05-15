from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Category(models.Model):
    """
    Модель категорий товаров.
    """
    title = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.title}"

class Ad(models.Model):
    """
    Модель товаров.
    """
    class Condition(models.TextChoices):
        NEW = "Новый"
        USED = "Б/У"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    # image_url = models.ImageField(upload_to="images/", null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    condition = models.CharField(choices=Condition, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse(
            "ads:detail",
            kwargs={"pk": self.id}
        )

    def __str__(self):
        return f"{self.title}"
