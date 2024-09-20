from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Author,BookInstance,Language,Genre
from django.views.generic import CreateView, DetailView,TemplateView, ListView
from django.urls import reverse, reverse_lazy
from .forms import BookCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.contrib.auth.forms import UserCreationForm
# Create your views here.

#View for index page 
def index(request):
  num_book=Book.objects.all().count()
  num_instances=BookInstance.objects.all().count()
  num_instance_avail=BookInstance.objects.filter(status__exact='a').count()

  context={
    'num_book':num_book,
    'num_instances':num_instances,
    'num_instance_avail':num_instance_avail,
  }
  return render(request,'catalog/index.html',context=context)

# View to create new book and save in database, --> it looks for model_form.html
class BookCreate(LoginRequiredMixin,CreateView):
  # model=Book
  # fields="__all__"
  # success_url = reverse_lazy('book_detail')

  form_class = BookCreateForm
  template_name = 'catalog/book_form.html'
  def post(self,request,*args,**kwargs):
    form = self.form_class(request.POST)
    print(form)

    if form.is_valid():
      print('form valid')
      form.save()
      obj = form.instance
      print('form saved')
      return render(request,self.template_name,{'obj':obj,'form':self.form_class})
      
    else:
      print('form is not valid')
    return render(request,self.template_name)


#Subitting CreateView by default looks for name book_detail.html
#View to create detail view --> looks for model_detail.html
class BookDetail(DetailView):
  # model=Book
  template_name = 'catalog/book_detail.html'
  pass

# View which can be seen by authenticated user only
@login_required
def my_view(request):
  return render(request, 'catalog/my_view.html')


class SignUpView(CreateView):
  form_class=UserCreationForm
  success_url=reverse_lazy('login')
  template_name= 'catalog/signup.html'

class BorrowedByUserView(LoginRequiredMixin,ListView):
  model=BookInstance
  template_name='catalog/profile.html'
  paginate_by: 5
  def get_quueryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).all()