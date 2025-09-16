from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    amount_left = models.PositiveIntegerField(null=True, blank=True)  # optional field

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    def clean(self):
        # Prevent admin from changing amount_left when it's already 0
        if self.pk:  # check if movie already exists
            old_instance = Movie.objects.get(pk=self.pk)
            if old_instance.amount_left == 0 and self.amount_left != 0:
                raise ValidationError("You cannot modify 'amount left' once it has reached 0.")

    def save(self, *args, **kwargs):
        self.full_clean()  # run clean() before saving
        super().save(*args, **kwargs)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
