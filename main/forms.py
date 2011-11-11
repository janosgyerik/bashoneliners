''' Kind reminders, (please review before editing!)
    - Forms are for validating input, NOT business logic.
    - Only include model specific logic in forms if it is required for input.
      Example: user should be able to select only the groups it is member of.
    '''

from django import forms

from bashoneliners.main.models import OneLiner

''' constants '''

#


''' forms '''

class PostOneLinerForm(forms.ModelForm):
    title = 'Post a one-liner'
    actions = ('Post one-liner',)

    def save(self, user):
	self.instance.user = user
	return super(PostOneLinerForm, self).save()

    class Meta:
	model = OneLiner

	widgets = {
		'line': forms.Textarea(attrs={'cols': 80, 'rows': 3, }),
		'summary': forms.TextInput(attrs={'size': 100, }),
		'explanation': forms.Textarea(attrs={'cols': 80, 'rows': 10, }),
		'caveats': forms.Textarea(attrs={'cols': 80, 'rows': 3, }),
		}

	fields = (
		'line',
		'summary',
		'explanation',
		'caveats',
		#'is_published',
		)


class EditOneLinerForm(forms.ModelForm):
    title = 'Edit one-liner'
    actions = ('Save one-liner', 'Delete one-liner',)
    edit = True
    user = None

    def __init__(self, user, *args, **kwargs):
	self.user = user
	super(EditOneLinerForm, self).__init__(*args, **kwargs)

    def clean(self):
	if self.instance.user != self.user:
	    raise forms.ValidationError('User %s is not the owner of this OneLiner' % self.user)

	return self.cleaned_data

    class Meta:
	model = OneLiner

	widgets = {
		'line': forms.Textarea(attrs={'cols': 80, 'rows': 3, }),
		'summary': forms.TextInput(attrs={'size': 100, }),
		'explanation': forms.Textarea(attrs={'cols': 80, 'rows': 10, }),
		'caveats': forms.Textarea(attrs={'cols': 80, 'rows': 3, }),
		}

	fields = (
		'line',
		'summary',
		'explanation',
		'caveats',
		'is_published',
		)


class SearchOneLinerForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 60}))


# eof
