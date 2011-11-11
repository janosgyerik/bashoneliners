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

class CommonOneLinerForm(forms.ModelForm):
    user = None

    def __init__(self, user, *args, **kwargs):
	self.user = user
	super(CommonOneLinerForm, self).__init__(*args, **kwargs)

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


class PostOneLinerForm(CommonOneLinerForm):
    title = 'Post a one-liner'
    actions = ('Post one-liner',)

    def save(self):
	self.instance.user = self.user
	return super(PostOneLinerForm, self).save()


class EditOneLinerForm(CommonOneLinerForm):
    title = 'Edit one-liner'
    actions = ('Save one-liner', 'Delete one-liner',)
    edit = True

    def clean(self):
	if self.instance.user != self.user:
	    raise forms.ValidationError('User %s is not the owner of this OneLiner' % self.user)

	return self.cleaned_data


class SearchOneLinerForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 60}))


# eof
