from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Meep
from django.contrib import messages

from .form import MeepForm,SignUp, ProfilePicForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User



# Create your views here.

def home(request):
    meeps = {}
    
    
    meeps = Meep.objects.all().order_by('-created_at')
    if request.user.is_authenticated:

        
        form = MeepForm

        if request.method == "POST":
            form = MeepForm(request.POST)

            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()

                messages.success(request, ("Meep Published!"))
                return redirect('home')
        
        return render(request, 'home.html', {"meeps":meeps, "form":form})
    else:
        return render(request, 'home.html', {"meeps":meeps})

def profile_list(request):
    if request.user.is_authenticated:
        print("user ",request.user)
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request, ("User must Logged in to view this page"))
        return redirect('home')

def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)

        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, (f"You have successfully unfollowed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, ("User must Logged in to view this page"))
        return redirect('home')

def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)

        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request, (f"You have successfully followed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, ("User must Logged in to view this page"))
        return redirect('home')


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            # print("len of profiles ",len(profiles))
            return render(request, 'followers.html',{"profiles":profiles})
        else:
            messages.success(request, ("You dont have access to this page... "))
            return redirect('home')
    else:
        messages.success(request, ("User must Logged in to view this page"))
        return redirect('home')
    

def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html',{"profiles":profiles})
        else:
            messages.success(request, ("You dont have access to this page... "))
            return redirect('home')
    else:
        messages.success(request, ("User must Logged in to view this page"))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by('-created_at')
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            print("action ",action)
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)

        return render(request, 'profile.html',{"profile":profile, "meeps": meeps})
    else:
        messages.success(request, ("User must Logged in to view this page"))
        return redirect('home')
    

def login_user(request):

    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been loggedin!!"))
        else:
            messages.success(request, ("The given username and password doesnot match"))

        return redirect('home')
    
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = SignUp
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("The Register is successful"))
            return redirect('home')
        else:
            print("invalid form")

    return render(request, 'register.html',{ "form":form })


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id= request.user.id)
        user_form = SignUp(request.POST or None, request.FILES or None , instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None , instance=profile_user)

        # if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request,current_user)
            return redirect('home')
        return render(request, 'update_profile.html',{"user_form":user_form , "profile_form": profile_form  })
    else:
        messages.success(request, ("You must logged In to access this page"))
        return redirect('home')
    
def like_meep(request, pk):

    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        
        if meep.like.filter(id= request.user.id):
            meep.like.remove(request.user)
        else:
            meep.like.add(request.user)
        print("refer page ",)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ("You must logged In to access this page"))
        return redirect('home')

def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, 'meep_show.html',{"meep": meep })
    else:
        messages.success(request, ("You must logged In to access this page"))
        return redirect('home')
    
def delete_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.user.username == request.user.username:
            meep.delete()
            messages.success(request, ("Meep deleted successfully"))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, ("You are not the owner of the Meep"))
            return redirect('home')
    else:
        messages.success(request, ("You must logged In to access this page"))
        return redirect('home')
    
def edit_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.user.username == request.user.username:
            # form = MeepForm
            form = MeepForm(request.POST or None, instance=meep)

            if request.method == "POST":
                

                if form.is_valid():
                    meep = form.save(commit=False)
                    meep.user = request.user
                    meep.save()
                    messages.success(request, ("Meep Updated!"))
                    return redirect('home')
            else:
                return render(request, 'meep_edit.html',{"meep": meep, "form": form })

        else:
            messages.success(request, ("You are not the owner of the Meep"))
            return redirect('home')
    else:
        messages.success(request, ("You must logged In to access this page"))
        return redirect('home')
    
def search(request):
    if request.method == "POST":
        search = request.POST['search']
        searched = Meep.objects.filter(body__contains=search) 
        return render(request, 'search.html', {'search' :search, "searched":searched})


    else:
        return render(request, 'search.html', {})