import django.forms as forms
from django.db.models import Count
from django.forms.utils import ErrorList

from medgis.settings import MIN_DOCS_PER_AUTHOR, MIN_DOCS_PER_TAG
from massmedia.models import *
from massmedia.services import get_user_group


class DocumentSearchForm(forms.Form):
    id = forms.CharField(label="ID", required=False)
    corpuses = forms.ModelMultipleChoiceField(queryset=Corpus.objects.all(), label="Корпусы", required=True)
    sources = forms.ModelMultipleChoiceField(queryset=Source.objects.all(), label="Источники", required=False)
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.annotate(num_docs=Count('document')).filter(num_docs__gte=MIN_DOCS_PER_AUTHOR),
        label="Авторы", required=False)
    title = forms.CharField(label="Заголовок", required=False)
    text = forms.CharField(label="Текст", required=False)

    num_views_from = forms.IntegerField(label="Количество просмотров - больше чем", required=False)
    num_views_to = forms.IntegerField(label="Количество просмотров - меньше чем", required=False)
    num_shares_from = forms.IntegerField(label="Количество репостов - больше чем", required=False)
    num_shares_to = forms.IntegerField(label="Количество репостов - меньше чем", required=False)
    num_comments_from = forms.IntegerField(label="Количество комментариев - больше чем", required=False)
    num_comments_to = forms.IntegerField(label="Количество комментариев - меньше чем", required=False)
    num_likes_from = forms.IntegerField(label="Количество лайков - больше чем", required=False)
    num_likes_to = forms.IntegerField(label="Количество лайков - меньше чем", required=False)

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.annotate(num_docs=Count('document')).filter(num_docs__gte=MIN_DOCS_PER_TAG), label="Теги",
        required=False)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label="Категории", required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                 renderer=None, user=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)
        if not user.is_superuser:
            group = get_user_group(user)
            self.fields['corpuses'].queryset = self.fields['corpuses'].queryset.filter(usergroup=group)
            self.fields['sources'].queryset = self.fields['sources'].queryset.filter(corpus__usergroup=group)
            self.fields['authors'].queryset = self.fields['authors'].queryset.filter(corpus__usergroup=group)
