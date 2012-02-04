from django.shortcuts import render_to_response
from django.contrib.auth.decorators import *

from bashoneliners.main.models import WishListQuestion, OneLiner

@login_required
def question_answered(request, question_pk, oneliner_pk):
    question = WishListQuestion.objects.get(pk=question_pk, user=request.user)
    oneliner = OneLiner.objects.get(pk=oneliner_pk)
    question.accept_answer(oneliner)

    return render_to_response('json.js')


# eof
