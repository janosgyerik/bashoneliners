''' Kind reminders, (please review before editing!)
    - Forms are for validating input, NOT business logic.
    - Only include model specific logic in forms if it is required for input.
      Example: user should be able to select only the groups it is member of.
    '''

from django import forms
from django.contrib.comments.forms import CommentForm

from bashoneliners.main.models import OneLiner, HackerProfile, User, Question


class CommonOneLinerForm(forms.ModelForm):
    user = None
    next_url = forms.URLField(required=False)
    action = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CommonOneLinerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = OneLiner

        widgets = {
                'summary': forms.TextInput(attrs={'class': 'span6', }),
                'line': forms.TextInput(attrs={'class': 'span6', }),
                'explanation': forms.Textarea(attrs={'rows': 10, 'class': 'span6', }),
                'limitations': forms.Textarea(attrs={'rows': 3, 'class': 'span6', }),
                }

        fields = (
                'line',
                'summary',
                'explanation',
                'limitations',
                'is_published',
                )


class PostOneLinerForm(CommonOneLinerForm):
    title = 'Post a One-Liner'
    actions = ({'name': 'Post one-liner', 'cssclass': 'btn-primary'},)

    def save(self):
        self.instance.user = self.user
        return super(PostOneLinerForm, self).save()


class EditOneLinerForm(CommonOneLinerForm):
    title = 'Edit one-liner'
    action_save = {'name': 'Save one-liner', 'cssclass': 'btn-primary'}
    action_delete = {'name': 'Delete one-liner', 'cssclass': 'btn-danger'}
    actions = (action_save, action_delete)
    edit = True
    is_save = False
    is_delete = False

    def clean_action(self):
        action = self.cleaned_data['action']
        if action == self.action_save['name']:
            self.is_save = True
        elif action == self.action_delete['name']:
            self.is_delete = True
        return action

    def clean(self):
        if self.instance.user != self.user:
            raise forms.ValidationError('User %s is not the owner of this OneLiner' % self.user)
        return self.cleaned_data


class SearchOneLinerForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'span4', }))
    is_advanced = forms.BooleanField(required=False)
    match_summary = forms.BooleanField(initial=True, required=False)
    match_line = forms.BooleanField(initial=True, required=False)
    match_explanation = forms.BooleanField(initial=True, required=False)
    match_limitations = forms.BooleanField(initial=True, required=False)
    match_whole_words = forms.BooleanField(initial=False, required=False)


class EditHackerProfileForm(forms.ModelForm):
    next_url = forms.URLField(required=False)

    def clean_display_name(self):
        display_name = self.cleaned_data['display_name']
        if display_name == '':
            display_name = None
        return display_name

    class Meta:
        model = HackerProfile

        widgets = {
                'display_name': forms.TextInput(attrs={'class': '', }),
                'twitter_name': forms.TextInput(attrs={'class': '', }),
                'blog_url': forms.TextInput(attrs={'class': 'span6', }),
                'homepage_url': forms.TextInput(attrs={'class': 'span6', }),
                }

        exclude = (
                'user',
                )


class CommonQuestionForm(forms.ModelForm):
    user = None
    next_url = forms.URLField(required=False)
    action = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CommonQuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question

        widgets = {
                'summary': forms.TextInput(attrs={'class': 'span6', }),
                'explanation': forms.Textarea(attrs={'rows': 5, 'class': 'span6', }),
                }

        fields = (
                'summary',
                'explanation',
                'is_published',
                'is_answered',
                )


class PostQuestionForm(CommonQuestionForm):
    title = 'Post a question'
    actions = ({'name': 'Post question', 'cssclass': 'btn-primary'},)

    def save(self):
        self.instance.user = self.user
        return super(PostQuestionForm, self).save()


class EditQuestionForm(CommonQuestionForm):
    title = 'Edit question'
    action_save = {'name': 'Save question', 'cssclass': 'btn-primary'}
    action_delete = {'name': 'Delete question', 'cssclass': 'btn-danger'}
    actions = (action_save, action_delete)
    edit = True
    is_save = False
    is_delete = False

    def clean_action(self):
        action = self.cleaned_data['action']
        if action == self.action_save['name']:
            self.is_save = True
        elif action == self.action_delete['name']:
            self.is_delete = True
        return action

    def clean(self):
        if self.instance.user != self.user:
            raise forms.ValidationError('User %s is not the owner of this Question' % self.user)
        return self.cleaned_data


class PostCommentOnOneLinerForm(CommentForm):
    next_url = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super(PostCommentOnOneLinerForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.Textarea(attrs={'rows': 5, 'class': 'span6', })


# eof
