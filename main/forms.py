''' Kind reminders, (please review before editing!)
    - Forms are for validating input, NOT business logic.
    - Only include model specific logic in forms if it is required for input.
      Example: user should be able to select only the groups it is member of.
    '''

from django import forms

from bashoneliners.main.models import OneLiner, HackerProfile, User, Question

''' constants '''

#


''' forms '''

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
    actions = ('Post One-Liner',)

    def save(self):
	self.instance.user = self.user
	return super(PostOneLinerForm, self).save()


class EditOneLinerForm(CommonOneLinerForm):
    title = 'Edit one-liner'
    action_save = 'Save one-liner'
    action_delete = 'Delete one-liner'
    actions = (action_save, action_delete,)
    edit = True
    is_save = False
    is_delete = False

    def clean_action(self):
	action = self.cleaned_data['action']
	if action == self.action_save:
	    self.is_save = True
	elif action == self.action_delete:
	    self.is_delete = True
	return action

    def clean(self):
	if self.instance.user != self.user:
	    raise forms.ValidationError('User %s is not the owner of this OneLiner' % self.user)

	return self.cleaned_data


class SearchOneLinerForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 'search-query', }))


class EditUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
	super(EditUserForm, self).__init__(*args, **kwargs)
	self.fields['password'].required = False

    def save(self):
	user = super(EditUserForm, self).save(commit=False)
	new_password = self.cleaned_data['password']
	if new_password is not None:
	    user.set_password(new_password)
	user.save()
	return user

    class Meta:
	model = User

	fields = (
		'username',
		'password',
		)


class EditHackerProfileForm(forms.ModelForm):
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
    actions = ('Post question',)

    def save(self):
	self.instance.user = self.user
	return super(PostQuestionForm, self).save()


class EditQuestionForm(CommonQuestionForm):
    title = 'Edit question'
    action_save = 'Save question'
    action_delete = 'Delete question'
    actions = (action_save, action_delete,)
    edit = True
    is_save = False
    is_delete = False

    def clean_action(self):
	action = self.cleaned_data['action']
	if action == self.action_save:
	    self.is_save = True
	elif action == self.action_delete:
	    self.is_delete = True
	return action

    def clean(self):
	if self.instance.user != self.user:
	    raise forms.ValidationError('User %s is not the owner of this Question' % self.user)

	return self.cleaned_data


# eof
