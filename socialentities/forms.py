from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SocialEntity

class SocialEntityCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SocialEntity
        fields = ('email',)

class SocialEntityChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = SocialEntity
        fields = ('email', 'first_name', 'last_name', 'cpf', 'role', 'imagem', 
                  'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    def __init__(self, *args, **kwargs):
        super(SocialEntityChangeForm, self).__init__(*args, **kwargs)
        # Torna os campos obrigatórios no formulário de edição
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['cpf'].required = True
        self.fields['role'].required = True

    def clean_cpf(self):
        """
        Garante que o CPF, se fornecido, seja único entre todos os usuários.
        Esta é a validação que substitui o 'unique=True' do modelo.
        """
        cpf = self.cleaned_data.get('cpf')
        # 'self.instance' é o objeto de usuário que está sendo editado.
        # Excluímos o próprio usuário da verificação para que ele possa ser salvo sem alterações.
        if cpf and SocialEntity.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Um usuário com este CPF já existe.")
        return cpf
