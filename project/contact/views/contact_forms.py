from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from contact.models import Contact
from django.contrib.auth.decorators import login_required

from django import forms
from django.core.exceptions import ValidationError



from contact.models import Contact

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
         widget=forms.FileInput(
              attrs={
                   'accept': 'image/*',
              }
         ) 
         ,required=False
    )
   
    first_name = forms.CharField(
           widget=forms.TextInput(
               attrs={ 
                   'class': 'classe-a classe-b',
                   
                   
               }
           ),
    )
   
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone',
                  'email', 'description', 'category',
                  'picture'
                  
                  )

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
             msg = ValidationError(
                                    'Primeiro Nome Não Pode Ser Igual Ao Ultimo Nome',
                                    code='invalid'
                               )
             self.add_error('first_name', msg)
             self.add_error('last_name',  msg)
             

        
        return super().clean()
    def clean_first_name(self):
                first_name = self.cleaned_data.get('first_name')
        
                if first_name == 'ABC':

                    self.add_error(
                              'first_name',
                               ValidationError(
                                   'Veio do add_error',
                                   code='invalid'
                               )
                           )
                
                return first_name

        
@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        context = {
          'form': form,
          'form_action': form_action,
        }

        if form.is_valid():
             contact = form.save()
             return redirect('contact:update', contact_id=contact.id)
        
        return render(
                request,
                'contact/create.html',
                context
            )

    context = {
      'form': ContactForm(),
      'form_action': form_action,
    }

    
    return render(
        request,
        'contact/create.html',
        context
    )

@login_required(login_url='contact:login')
def Update(request, contact_id):
    contact = get_object_or_404(
         Contact,pk=contact_id, show=True, owner=request.user
         )
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST,instance=contact)

        context = {
          'form': form,
          'form_action': form_action,
        }

        if form.is_valid():
             contact = form.save(commit=False)
             contact.owner = request.user
             contact.save()
             return redirect('contact:update', contact_id=contact.id)
        
        return render(
                request,
                'contact/create.html',
                context
            )

    context = {
      'form': ContactForm(instance=contact),
      'form_action': form_action,
    }

    
    return render(
        request,
        'contact/create.html',
        context
    )
@login_required(login_url='contact:login')
def Delete(request, contact_id):
    contact = get_object_or_404(
         Contact,pk=contact_id, show=True, owner=request.user
         )
    confirmation = request.POST.get('confirmation', 'no')
    print('Confirmation:',confirmation)

    if confirmation == "yes":
        contact.delete()
        return redirect('contact:index')
         
    # contact.delete()
    # return redirect('contact:index')

    return render(
         request,
         "contact/contact.html",
         {
              'contact': contact,
              'confirmation': confirmation
         }
    )