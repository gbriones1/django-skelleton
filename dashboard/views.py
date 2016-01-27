from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from mysite.configurations import *


@login_required
def dashboard(request):


    return render_to_response('pages/dashboard.html', dict(locals(), **globals()), context_instance=RequestContext(request))
