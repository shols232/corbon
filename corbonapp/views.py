from django.shortcuts import render, redirect
from .forms import FileForm
from .models import File
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


