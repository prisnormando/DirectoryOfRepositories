from django import forms
from django.contrib.auth.models import User

from dor import models


class JournalSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Journal
        fields = "__all__"
        labels = {
            'name': "Name*",
            'url': 'Url*',
            'repos_endorsed': "Endorsed Repositories"
        }
        widgets = {
            'repos_endorsed': forms.CheckboxSelectMultiple(),
        }
        exclude = ('owner', 'is_visible',)

    def save(self, user=None, commit=True):
        inst = super(JournalSubmissionForm, self).save(commit=False)
        if user:
            inst.owner = user
        else:
            inst.owner = User.objects.filter(is_superuser=True)[0]
        if commit:
            try:
                user.userprofile.maintains_obj = True
                user.userprofile.save()
            except:
                pass
            inst.save()
            self.save_m2m()
        return inst

class RepoSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Repository
        fields = "__all__"
        labels = {
            'name': "Name*",
            'alt_names': 'Alternate Names',
            'url': 'Url*',
            'persistent_url': 'Persistent Url',
            'accepted_taxonomy': 'Accepted Taxonomy*',
            'accepted_content': 'Accepted Data-Types*',
            'standards': 'Standards',
            'hosting_institution': 'Hosting Institution',
            'institution_country': 'Institution Country',
            'metadataInformationURL': 'Metadata Information URL',
            'metadataRemarks': 'Metadata Remarks',
            'size': 'Size*',
            'date_operational': 'Date Operational',
            'remarks': 'Remarks',
            'db_certifications': 'Repository Certificaions',
        }
        widgets = {
            'accepted_content': forms.CheckboxSelectMultiple(),
            'db_certifications': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'metadataRemarks': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'remarks': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
        exclude = ('owner', 'embargoed')

    def __init__(self, *args, **kwargs):
        csrf = kwargs.pop('csrf')
        repo = kwargs.get('instance', None)

        super(RepoSubmissionForm, self).__init__(*args, **kwargs)

        self.fields['accepted_content'].queryset = (
            models.ContentType.objects.filter(associated_repo=None) &
            models.ContentType.objects.filter(token_id='')
        ) | (models.ContentType.objects.filter(token_id=str(csrf)))

        if repo:
            self.fields['accepted_content'].queryset = self.fields['accepted_content'].queryset | (
                models.ContentType.objects.filter(associated_repo=repo))

        self.fields['accepted_content'].queryset = self.fields['accepted_content'].queryset.order_by('obj_name', 'id')

    def save(self, user=None, commit=True):
        inst = super(RepoSubmissionForm, self).save(commit=False)
        inst.owner = user or inst.owner or User.objects.filter(is_superuser=True)[0]
        if commit:
            try:
                user.userprofile.maintains_obj = True
                user.userprofile.save()
            except:
                pass
            inst.save()
            self.save_m2m()
            for datatype in inst.accepted_content.all():
                if datatype.token_id:
                    datatype.token_id = ''
                    datatype.associated_repo = inst
                    datatype.save()
        return inst

class AnonymousRepoSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Repository
        labels = {
            'name': "Name*",
            'alt_names': 'Alternate Names',
            'url': 'Url*',
            'persistent_url': 'Persistent Url',
            'accepted_taxonomy': 'Accepted Taxonomy*',
            'accepted_content': 'Accepted Data-Types*',
            'standards': 'Standards',
            'hosting_institution': 'Hosting Institution',
            'institution_country': 'Institution Country',
            'metadataInformationURL': 'Metadata Information URL',
            'metadataRemarks': 'Metadata Remarks',
            'size': 'Size*',
            'date_operational': 'Date Operational',
            'remarks': 'Remarks',
            'db_certifications': 'Repository Certificaions',
        }
        widgets = {
            'accepted_content': forms.CheckboxSelectMultiple(),
            'db_certifications': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'metadataRemarks': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'remarks': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
        exclude = ('owner', 'embargoed',)

    def __init__(self, *args, **kwargs):
        csrf = kwargs.pop('csrf')
        super(AnonymousRepoSubmissionForm, self).__init__(*args, **kwargs)

        self.fields['accepted_content'].queryset = (
            models.ContentType.objects.filter(associated_repo=None) &
            models.ContentType.objects.filter(token_id='')
        ) | (
            models.ContentType.objects.filter(token_id=str(csrf))
        )

        self.fields['accepted_content'].queryset = self.fields['accepted_content'].queryset.order_by('obj_name', 'id')


    def save(self, user=None, commit=True):
        inst = super(AnonymousRepoSubmissionForm, self).save(commit=False)
        inst.owner = User.objects.filter(is_superuser=True)[0]
        if commit:
            inst.save()
            self.save_m2m()
            for datatype in inst.accepted_content.all():
                if datatype.token_id:
                    datatype.token_id = ''
                    datatype.associated_repo = inst
                    datatype.save()
        return inst


class TaxSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Taxonomy
        labels = {
            'obj_name': 'Name*',
            'associated_content': 'Associated Content',
        }
        exclude = ('lft', 'rght', 'tree_id', 'level', 'embargoed', 'tax_id')


class ContentSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.ContentType
        labels = {
            'obj_name': 'Name*',
            'position': 'Position*'
        }
        exclude = ('lft', 'rght', 'tree_id', 'level')


class CertificationSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Certification
        labels = {
            'obj_name': 'Name*',
            'position': 'Position*'
        }
        exclude = ('lft', 'rght', 'tree_id', 'level')


class StandardSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Standards
        fields = "__all__"


class UserSubmissionForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_again = forms.CharField(max_length=30, widget=forms.PasswordInput())
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=[('Repository Representative', 'Repository Representative'), ('Journal Representative', 'Journal Representative')])

    class Meta:
        model = User
        fields = "__all__"
        labels = {
            'username': "Username",
            'first_name': "First Name",
            'last_name': "Last Name",
            'password': "Password",
            'password_again': "Password Again",
            'email': "Email",
            'user_type': "User Type",
        }
        exclude = ('maintains_obj')

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is taken.")

    def clean_password(self):
        if 'password' in self.cleaned_data and 'password_again' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_again']:
                raise forms.ValidationError("Passwords must match.")
        return self.cleaned_data['password']

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.clean_password(),
                                        email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.user_type = self.cleaned_data['user_type']
        new_user.save()
        new_profile = models.UserProfile.objects.create(user=new_user, user_type=self.cleaned_data['user_type'])
        new_profile.save()
