from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    brewery_id  = models.CharField(max_length=100)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    rating      = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review      = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BreweryID: {self.brewery_id}   User: {str(self.user)}   Rating: {str(self.rating)}   Review: {str(self.review)}"