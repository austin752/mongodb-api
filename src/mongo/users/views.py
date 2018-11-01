from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, FormView
from django.utils.http import is_safe_url
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, LoginForm
from .signals import user_logged_in


def home_page(request):
	content = {
	    'title': 'Home',
        'home_content': 'Home Content'
    }

	if request.user.is_authenticated:
		email = request.user.email
		print(email)
		content = {
            'user_email': email,
			'home_content': 'logged in content'
        }
	return render(request, 'home.html', content)

class RegisterView(generic.CreateView):
	form_class = CustomUserCreationForm
	template_name = 'users/register.html'
	success_url = '/login'


class LoginView(FormView):
	form_class = LoginForm
	template_name = 'users/login.html'
	success_url = '/'

	def form_valid(self, form):
		request = self.request
		next_ = request.GET.get('next')
		next_page = request.POST.get('next')
		redirect_path = next_ or next_page or None
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(username=email, password=password)
		print(user)
		if user is not None:
			login(request, user)
			user_logged_in.send(user.__class__, instance=user, request=request)
			try:
				del request.session['guest_email']
			except:
				pass
			if is_safe_url(redirect_path, request.get_host()):
				return redirect('/')
			else:
				return redirect('/')
		return super(LoginView, self).form_invalid(form)
