from .models import Listing, Bid, Comment
from django import forms
from django.core.exceptions import ValidationError


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description',
                  'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title of the listing', 'autofocus': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the description of the listing'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the starting bid of the listing'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter the image URL of the listing'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select the category of the listing'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'starting_bid': 'Starting Bid',
            'image_url': 'Image URL',
            'category': 'Category',
        }
        error_messages = {
            'title': {
                'max_length': "This title is too long.",
            },
        }


class BidFrontendForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your bid greater than the current bid/starting bid'}),
        }
        labels = {
            'bid': 'Bid',
        }

    def clean(self):
        cleaned_data = super().clean()
        bid = cleaned_data.get('bid')
        listing = self.instance.listing

        if bid is not None:
            if not listing.current_bid and bid > listing.starting_bid:
                return cleaned_data
            elif listing.current_bid and bid > listing.current_bid.bid:
                return cleaned_data
            elif listing.current_bid and bid <= listing.current_bid.bid:
                raise ValidationError("Bid must be greater than the current bid.")
            else:
                raise ValidationError("Bid must be greater than the starting bid.")

        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"
    
    def clean(self):
        try:
            user = self.cleaned_data['user']
            listing = self.cleaned_data['listing']
            bid = self.cleaned_data['bid']
            if user == listing.user:
                raise ValidationError(
                    {'user': 'You cannot bid on your own listing.'})
            if not listing.current_bid and bid <= listing.starting_bid:
                raise ValidationError(
                    {'bid': 'Bid must be greater than the starting bid.'})
            elif listing.current_bid and bid <= listing.current_bid.bid:
                raise ValidationError(
                    {'bid': 'Bid must be greater than the current bid.'})
            else:
                return self.cleaned_data
        except KeyError:
            pass


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comment', 'maxlength': '1100', 'minlength': '10', 'rows': '4'}),
        }
        labels = {
            'comment': 'Comment',
        }