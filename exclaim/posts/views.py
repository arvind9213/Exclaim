# from urllib import quote
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



# Create your views here.
def post_create(request):
    #manual validation
    # form=PostForm()
    # # if request.method == "POST":
    # #     print (request.POST.get("content"))
    # #     print (request.POST.get("title"))
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.user = request.user
        print (form.cleaned_data.get("title"))
        instance.save()
        messages.success(request,"succssfully created")
        return HttpResponseRedirect(instance.get_absolute_url())


    context={"form":form}
    return render(request,"post_form.html",context)

def post_detail(request,slug):
    instance = get_object_or_404(Post,slug=slug)
    # share_string = quote(instance.content)
    query = request.GET.get("q")
    print(query)
    context = {
    "title":instance.title,
    "instance":instance,
    # "share_string":share_string,
    }
    return render(request,"post_detail.html",context)

def post_list(request):
    # queryset_list = Post.objects.all() #.order_by("-timestamp")
    queryset_list = Post.objects.filter(draft=False)
    query = request.GET.get("q")
    if query:

        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)
            ).distinct()

    paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    users_list = User.objects.all()  
      

    context = {'object_list':queryset,'title':"list",'page_request_var':page_request_var,'users_list':users_list}
    return render(request,"post_list.html",context)



def post_update(request,slug= None):
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit = False)
        print (form.cleaned_data.get("title"))
        instance.save()
        messages.success(request,"Item saved")

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
    "title":instance.title,
    "instance":instance,
    "form":form
    }
    return render(request,"post_form.html",context)

def post_delete(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request,"Sucessfully deleted")
    return redirect("posts:list")

def user_register(request):
    form = UserCreationForm(request.POST or None,)
    if form.is_valid():
        instance = form.save(commit = False)
        
        instance.save()
        messages.success(request,"succssfully created")
        # user = authenticate(username=request.POST["username"], password=request.POST["password1"])
        # if user is not None:
        #     login(request, user)
        return redirect("posts:list")
    
    context = {
        "form":form
    }    
    return render(request, 'registration/register.html', context)