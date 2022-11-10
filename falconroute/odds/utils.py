import json
from django.conf import settings


def handle_uploaded_file(f):
    file_path = settings.BASE_DIR / 'odds/files/empire.json'
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    saved_f = open(file_path)
    empire_dict = json.load(saved_f)
    return empire_dict


def lists_sum(length, total_sum):
    # Create all possible lists of a certain length which elements are positive
    # integers summing to total_sum
    out = []
    if length == 1:
        return [[total_sum]]
    else:
        for value in range(total_sum + 1):
            for permutation in lists_sum(length - 1, total_sum - value):
                out.append([value] + permutation)
        return out
