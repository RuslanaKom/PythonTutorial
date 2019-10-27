from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.template import loader
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import generic
from django.core.mail import EmailMessage
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.utils.translation import ugettext_lazy as _

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def mail(request):
    context = {'header': _('Contact us'), 'buttonText': _('Send'), 'label': _('Your message')}
    return render(request, 'polls/mail.html', context)
    
def processmail(request):
    subject = 'Message from Contact us form'
    text = request.POST['yourtext']
    addressFrom = 'stuffost@gmail.com'
    addressesTo = ['stuffost@gmail.com']

    email = EmailMessage(
    subject,
    text,
    addressFrom,
    addressesTo,
    [],
    reply_to=[],
    headers={'Message-ID': 'foo'},
    )

    email.send(fail_silently=False)
    return HttpResponseRedirect(reverse('polls:mail', args=()))
    
def pdf(request):
    return render(request, 'polls/pdf.html')
    
def createpdf(request):

    pdftext = request.POST['pdftext']

    sample_style_sheet = getSampleStyleSheet()
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(pdf_buffer)  
    paragraph_1 = Paragraph("Message", sample_style_sheet['Heading1'])
    paragraph_2 = Paragraph(pdftext,sample_style_sheet['BodyText'])
    flowables = []
    flowables.append(paragraph_1)
    flowables.append(paragraph_2)
    my_doc.build(flowables)
    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="some_file.pdf"'
    
    response.write(pdf_value)
    return response

def txt(request):
    return render(request, 'polls/txt.html')   
    
def createtxt(request):
    filename = "some_file.txt"
    plaintext = request.POST['plaintext']
    response = HttpResponse(plaintext, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
    

#-----OLD VARIANT-----------

#def index(request):
#   latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return HttpResponse(template.render(context, request))
    
def index(request):
    latest_question_list = get_list_or_404(Question.objects.order_by('-pub_date'))[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    
#def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'polls/detail.html', {'question': question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))