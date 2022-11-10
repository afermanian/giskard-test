from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm
from .utils import handle_uploaded_file
from .compute_odds import compute_final_odds


def form(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            empire_dict = handle_uploaded_file(request.FILES['file'])
            probability = f'{compute_final_odds(empire_dict): .2f} %'
            return render(request, 'odds/form.html',
                          {'form': form, 'probability': probability})
    else:
        form = UploadFileForm()
    return render(request, 'odds/form.html', {'form': form})


