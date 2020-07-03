from django.shortcuts import render


# Create your views here.
def upload_zip(request):
    return render(request, "zip_file.html")
