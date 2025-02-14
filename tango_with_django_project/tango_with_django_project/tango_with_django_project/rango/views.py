from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime, timedelta

# ✅ Helper function to safely get a session variable
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# ✅ Function to track visits using sessions
def visitor_cookie_handler(request):
    # Retrieve visits count, default to 1 if not found
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # Retrieve the last visit timestamp
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # Check if a day has passed since last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())  # Update last visit
    else:
        request.session['last_visit'] = last_visit_cookie  # Maintain last visit

    request.session['visits'] = visits  # Update visits count


# ✅ Restricted View - Redirects Non-Authenticated Users
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


# ✅ Logout Function - Redirects to Home
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


# ✅ User Login - Shows Error Messages if Login Fails
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return render(request, 'rango/login.html', {'error_message': "Invalid login details supplied."})

    return render(request, 'rango/login.html')


# ✅ User Registration - Registers & Logs in User
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True  # ✅ Mark registration as successful

            # 🚀 Instead of redirecting, render the register page with a success message
            return render(request, 'rango/register.html', {
                'user_form': UserForm(),  # Empty form after success
                'profile_form': UserProfileForm(),  # Empty form after success
                'registered': registered  # ✅ This ensures the success message is shown
            })

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })




# ✅ Add Category - Requires Login
@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


# ✅ Add Page - Requires Login & Handles Invalid Category
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})


# ✅ Index Page - Shows Categories, Pages & User Greeting
# ✅ Index Page - Shows Categories, Pages & User Greeting
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    user_greeting = "Hey there, partner!"
    if request.user.is_authenticated:
        user_greeting = f"Howdy {request.user.username}!"

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
        'user_greeting': user_greeting
    }

    # ✅ Call function to update session-based cookies (but do NOT pass visits to template)
    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context=context_dict)


# ✅ About Page - Now Displays `visits`
def about(request):
    visitor_cookie_handler(request)  # ✅ Ensure visits count is updated

    context_dict = {
        'visits': request.session['visits']  # ✅ Pass `visits` to template
    }

    return render(request, 'rango/about.html', context=context_dict)




# ✅ Show Category - Lists Pages Sorted by Views
def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['category'] = category
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)



