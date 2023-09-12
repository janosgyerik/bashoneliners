''' Kind reminders, (please review before editing!)
    - Forms are for validating input, NOT business logic.
    - Only include model specific logic in forms if it is required for input.
      Example: user should be able to select only the groups it is member of.
    '''

from django import forms

from oneliners.models import OneLiner, HackerProfile


def common_text_input():
    return forms.TextInput(attrs={'class': 'form-control', })


def common_checkbox_input():
    return forms.CheckboxInput(attrs={'class': 'form-check-input', })


class CommonOneLinerForm(forms.ModelForm):
    user = None
    action = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CommonOneLinerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = OneLiner

        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control', }),
            'line': forms.TextInput(attrs={'class': 'form-control', }),
            'explanation': forms.Textarea(attrs={'rows': 10, 'class': 'form-control col-md-6', }),
            'limitations': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', }),
            'is_published': common_checkbox_input(),
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
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', }))
    is_advanced = forms.BooleanField(required=False)
    match_summary = forms.BooleanField(initial=True, required=False, widget=common_checkbox_input())
    match_line = forms.BooleanField(initial=True, required=False, widget=common_checkbox_input())
    match_explanation = forms.BooleanField(initial=True, required=False, widget=common_checkbox_input())
    match_limitations = forms.BooleanField(initial=True, required=False, widget=common_checkbox_input())
    match_whole_words = forms.BooleanField(initial=False, required=False, widget=common_checkbox_input())


class EditHackerProfileForm(forms.ModelForm):

    def clean(self):
        super().clean()

        for name in self.fields:
            cleaned_value = self.cleaned_data.get(name)
            if not cleaned_value and not self.data.get(name) or cleaned_value == self.data.get(name):
                self.fields[name].widget.attrs.update({'class': 'form-control is-valid'})
            else:
                self.fields[name].widget.attrs.update({'class': 'form-control is-invalid'})

        return self.cleaned_data

    class Meta:
        model = HackerProfile

        widgets = {
            'display_name': common_text_input(),
            'twitter_name': common_text_input(),
            'blog_url': common_text_input(),
            'homepage_url': common_text_input(),
        }

        exclude = (
            'user',
        )

