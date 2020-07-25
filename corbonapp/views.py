from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .forms import FileForm, CreateUsersForm
from .models import Files, PrivateDocument
from django.http import HttpResponse
from s3fs.core import S3FileSystem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sendgrid import SendGridAPIClient
from django.template.loader import get_template
from sendgrid.helpers.mail import *
from corbonmain.settings import SENDGRID_API_KEY
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
import pandas as pd
import xlrd
import os
# Create your views here.

@login_required
def download_zip(request):
    files = PrivateDocument.objects.all()
    return render(request, "download.html", {
        "files":files
    })

@staff_member_required
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
@staff_member_required
def delete_zip(request,id):
    zipfile = get_object_or_404(PrivateDocument, id = id)

    context = {
        "object":zipfile
    }

    if request.method == "POST":
        zipfile.upload.delete(save=False)
        zipfile.delete()

        return redirect("download")

    return render(request, "delete_zip.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')


@staff_member_required
def create_new_users(request):
    if request.method == "POST":
        form = CreateUsersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        excel_file = request.FILES.get("file")
        excel_file_name = excel_file.name

        if excel_file_name[-3:] == 'xls' or excel_file_name[-4:] == 'xlsx':

            try:
                # reading the excel file
                s3 = S3FileSystem(anon=False)
                key = f'media/public/excel_file/{excel_file}'
                bucket = 'corbon2'

                df = pd.read_excel(s3.open('{}/{}'.format(bucket, key),
                                         mode='rb')
                                 )
                for f in Files.objects.all():
                    f.delete()
                # Dropping the unnecessary columns
                data2 = df.dropna(axis=0, how="any")

                data2.columns = data2.columns.map(lambda x: x.replace('\n', ''))


                # here is final_data, the list of dictionaries that can be easily stored in the database
                final_data = data2.to_dict(orient="records")

                # code to store into the DB goes here, data is in variable final_data
                for row in final_data:
                    if not User.objects.filter(username__iexact=row['email']).exists():
                        User.objects.create_user(username=row['email'])
            except KeyError:
                return HttpResponse('excel file could not be processed')

            return redirect('download')
    else:
        form = CreateUsersForm()
    return render(request, 'store_users.html',{
        'form': form
    })



def home(request):
    return render(request, 'home.html')

def log_in(request):
    if request.method == 'POST':
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        email = request.POST.get('email')
        if User.objects.filter(username__iexact=email).count() == 1:
            user = User.objects.get(username=email)
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

            return render(request, 'email_sent.html', {'sent':True})
        return render(request, 'email_sent.html', {'sent': False})

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
        return HttpResponse('Confirmation link is invalid!')

