from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError


class User(AbstractUser):
    first_name = models.CharField(max_length=64, blank=False, default='')


class Listing(models.Model):
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=False)
    starting_bid = models.IntegerField(
        blank=False, validators=[MinValueValidator(1)])
    current_bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, null=True, blank=True, related_name="current_bid",)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_DEFAULT, default='NA', related_name="listings")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.starting_bid} - {self.category} - {self.user} - {self.active}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="bids", blank=False)
    listing = models.ForeignKey(
        Listing, on_delete=models.SET_NULL, null=True, related_name="bids", blank=False)
    bid = models.IntegerField(blank=False)

    def delete(self, *args, **kwargs):
        # Check if the associated Listing is active
        if self.listing.current_bid == self:
            raise ProtectedError(
                "Cannot delete Bid associated with an active Listing.", self)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.bid} by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(blank=False)

    def __str__(self):
        return f"{self.user} - {self.listing} - {self.comment}"


class Category(models.Model):
    category = models.CharField(max_length=64, blank=False, unique=True)

    def __str__(self):
        return f"{self.category}"
