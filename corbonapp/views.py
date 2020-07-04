from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .forms import FileForm
from .models import File
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sendgrid import SendGridAPIClient
from django.template.loader import get_template
from sendgrid.helpers.mail import *
from corbonmain.settings import SENDGRID_API_KEY
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.
def download_zip(request):
    files = File.objects.all()
    return render(request, "download.html", {
        "files":files
    })

def upload_zip(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("download")
    else:
        form = FileForm()
    return render(request, "zip_file.html",{
        'form': form
    })

# delete view
def delete_zip(request,id):
    context = {}

    zipfile = get_object_or_404(File, id = id)

    if request.method == "POST":
        zipfile.delete()

        return redirect("download")

    return render(request, "delete_zip.html")






def home(request):
    return render(request, 'home.html')

def log_in(request):
    if request.method == 'POST':
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        email = request.POST.get('email')
        if User.objects.filter(email__iexact=email).count() == 1:
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Email Confirmation'
            to_email = email
            print(to_email)
            message = get_template('email_verification_template.html').render({
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
            content = Content("text/html", message)
            mail = Mail('akinsolaademolatemitope@gmail.com', to_email, mail_subject, content)
            sg.send(mail)

            return HttpResponse('Please confirm your email address to complete the registration')

    return render(request, 'login.html')

def activate(request, uidb64, token):
    user = User()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')
