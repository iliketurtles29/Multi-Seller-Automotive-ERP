from django.shortcuts import redirect, render
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import Profile, User
from userauths.forms import VendorRegistrationForm, ProfileForm
from django.contrib.auth.models import Group

#User = settings.AUTH_USER_MODEL
# Create your views here.
def register_view(request):

    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your Account is Registered")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect("core:index")
    else:
        print("cannot")
        form = UserRegistrationForm()

    context ={
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey you are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You're logged in")
                return redirect("core:index")
            
            else:
                messages.warning(request, "User does not exist or Password incorrect")
        except:
            messages.warning(request, f"User { email } does not exist")

    return render(request, "userauths/sign-in.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out of your account.")
    return redirect("userauths:sign-in")

def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            user = request.user  # Get the logged-in user

            # Assign the logged-in user to the vendor
            vendor.user = user
            vendor.save()

            # Add the user to the 'Seller' group and mark as staff
            seller_group, created = Group.objects.get_or_create(name='Seller')
            user.is_staff = True
            user.groups.add(seller_group)
            user.save()

            messages.success(request, "You are now a Vendor")
            return redirect("core:index")
            # return redirect('vendor_detail', vendor_id=vendor.id)  # Redirect to vendor detail page or any other page
    else:
        form = VendorRegistrationForm()
    return render(request, 'userauths/vendor_registration.html', {'form': form})


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile updated Successfully.")
            return redirect("core:dashboard")
 
    else:
        form = ProfileForm(instance=profile)

    context =  {
        "form": form,
        "profile": profile,

    }
    return render(request, 'userauths/profile-edit.html', context)
