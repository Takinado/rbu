from django import forms


class ImportForm(forms.Form):
    file = forms.CharField(widget=forms.HiddenInput())
    # def __init__(self, *args, **kwargs):
    #     super(ImportForm, self).__init__(*args, **kwargs)
    #
    # class Meta:
    #     model = Post
    #
    #     widgets = {
    #         'file': forms.HiddenInput()
    #     }
    #     fields = '__all__'
    #     fields = ['title', 'text',]
    #     exclude = ['author']
    #     labels = {
    #         'name': _('Writer'),
    #     }
    #     help_texts = {
    #         'name': _('Some useful help text.'),
    #     }
    #     error_messages = {
    #         'name': {
    #             'max_length': _("This writer's name is too long."),
    #         },
    #     }

    # def clean(self):
    #     somefield = self.cleaned_data.get('somefield')
    #     if not somefield:
    #         if not self._errors.has_key('somefield'):
    #             from django.forms.util import ErrorList
    #             self._errors['somefield'] = ErrorList()
    #         self._errors['somefield'].append('Some field is blank')

    # def clean(self):
    #     f = self.cleaned_data.get('file')
    #
    #     if not f:
    #         if not self._errors.has_key('file'):
    #             from django.forms.util import ErrorList
    #             self._errors['file'] = ErrorList()
    #             print('OK')
    #         self._errors['file'].append('Some field is blank')

    def is_valid(self):

        # run the parent validation first
        valid = super(ImportForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        if not self.cleaned_data['file'].endswith('.csv'):
            print("Form not valid")
            return False

            # all good
        return True


from bootstrap3_datetime.widgets import DateTimePicker


class ToDoForm(forms.Form):
    todo = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    date = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD"}))
    reminder = forms.DateTimeField(required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))
