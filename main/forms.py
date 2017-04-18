from django.forms import ModelForm
from main.models import Albums, Images



class AddAlbum(ModelForm):
    class Meta:
        model = Albums
        fields = ['title', 'text']


class AddImage(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'tag', 'text', 'image']


class EditAlbum(ModelForm):
    class Meta:
        model = Albums
        fields = ['title', 'text']


class EditImage(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'tag', 'text']
