from django.shortcuts import render_to_response


def internal_error(request):
    return render_to_response('internal_error.html')
