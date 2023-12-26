from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from . import forms, models
from datetime import datetime
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    last_news = models.Blog.objects.order_by('-posted')[0:3]
    return render(
        request,
        'index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
            'last_news': last_news
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'about.html',
        {
            'title': 'О нас',
            'message': 'Сведения о нас',
            'year': datetime.now().year,
        }
    )

def registration(request):
    """Renders the registration page"""

    if request.method == "Post":
        regform = forms.RegistrationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect('home')
    else:
        regform = forms.RegistrationForm()

    assert isinstance(request,HttpRequest)
    return render(
        request,
        'registration.html',
        {
            'title': 'Регистрация пользователя',
            'regform': regform,
            'year' :datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page"""
    posts = models.Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )

def blogpost(request,parametr):
    assert isinstance(request, HttpRequest)
    post_1 = models.Blog.objects.get(id=parametr)
    comments = models.Comment.objects.filter(post=parametr)

    if request.method =="POST":
       form = forms.CommentForm(request.POST)
       if form.is_valid():
           comment_f = form.save(commit=False)
           comment_f.author = request.user
           comment_f.date = datetime.now()
           comment_f.post = models.Blog.objects.get(id=parametr)
           comment_f.save()

           return redirect('blogpost', parametr=post_1.id)
    else:
       form = forms.CommentForm()

    return render(
        request,
        'blogpost.html',
        {
            'post_1':post_1,

            'title': post_1.title,
            'comments': comments,
            'form': form,

            'year':datetime.now().year,
        }
)


def courses (request):
    assert isinstance(request, HttpRequest)

    courses = models.Course.objects.all()

    for course in courses:
        course.enrolled = request.user.is_authenticated and models.Enrollment.objects.filter(course=course, owner=request.user).exists()

    return render(
        request,
        'courses.html',
        {
            'title':'Курсы',
            'year':datetime.now().year,
            'courses': courses
        }
    )

def course (request, parametr):
    assert isinstance(request, HttpRequest)

    course = models.Course.objects.get(id=parametr)
    course.raw_sum = course.lessons_count * course.price

    return render(
        request,
        'course.html',
        {
            'title':'Курс ' + course.title,
            'year':datetime.now().year,
            'course': course,
            'enrolled': request.user.is_authenticated and models.Enrollment.objects.filter(course=course, owner=request.user).exists()
        }
    )


def enroll (request):
    assert isinstance(request, HttpRequest)

    if request.method != "POST": return redirect('courses')

    id = request.POST.get('course_id')
    phone = request.POST.get('phone')

    models.Enrollment.objects.create(
        owner = request.user,
        course = models.Course.objects.get(id=id),
        phone = phone,
    )

    return redirect('course', parametr=id)


def store (request):
    assert isinstance(request, HttpRequest)

    products = models.Product.objects.all()
    categories = models.Category.objects.all()

    if request.user.is_authenticated:
        try: cart = models.Cart.objects.get(owner=request.user)
        except: cart = models.Cart.objects.create(owner=request.user)

        for product in products:
            product.bought = cart.products.filter(id=product.id).exists()

    return render(
        request,
        'store.html',
        {
            'title':'Магазин',
            'year':datetime.now().year,
            'categories': categories,
            'products': products
        }
    )

def product (request, parametr):
    assert isinstance(request, HttpRequest)

    product = models.Product.objects.get(id=parametr)

    if request.user.is_authenticated:
        try: cart = models.Cart.objects.get(owner=request.user)
        except: cart = models.Cart.objects.create(owner=request.user)

    return render(
        request,
        'product.html',
        {
            'title':'Товар ' + product.title,
            'year':datetime.now().year,
            'product': product,
            'bought': request.user.is_authenticated and cart.products.filter(id=product.id).exists()
        }
    )


def store_buy (request):
    assert isinstance(request, HttpRequest)

    id = request.POST.get('product_id')

    cart = models.Cart.objects.get(owner=request.user)
    product = models.Product.objects.get(id=id)

    cart.products.add(product)

    return redirect('store')

def store_cancel (request):
    assert isinstance(request, HttpRequest)

    id = request.POST.get('product_id')

    cart = models.Cart.objects.get(owner=request.user)
    product = models.Product.objects.get(id=id)

    cart.products.remove(product)

    return redirect('store')

def store_inc (request):
    assert isinstance(request, HttpRequest)

    id = request.POST.get('product_id')

    cart = models.Cart.objects.get(owner=request.user)
    product = models.Product.objects.get(id=id)

    cart.data = json.loads(cart.data.replace("'", '"'))

    if str(product.id) not in cart.data: cart.data[str(product.id)] = 1
    cart.data[str(product.id)] = cart.data[str(product.id)] + 1

    cart.data = json.dumps(cart.data)

    cart.save(force_update=True)

    return redirect('store')

def store_dec (request):
    assert isinstance(request, HttpRequest)

    id = request.POST.get('product_id')

    cart = models.Cart.objects.get(owner=request.user)
    product = models.Product.objects.get(id=id)

    cart.data = json.loads(cart.data.replace("'", '"'))

    if str(product.id) not in cart.data: cart.data[str(product.id)] = 1
    cart.data[str(product.id)] = cart.data[str(product.id)] - 1

    cart.data = json.dumps(cart.data)

    cart.save(force_update=True)

    return redirect('store')


def cart (request):
    assert isinstance(request, HttpRequest)

    if request.user.is_authenticated:
        try: cart = models.Cart.objects.get(owner=request.user)
        except: cart = models.Cart.objects.create(owner=request.user)

    else: return redirect('login')

    cart.data = json.loads(cart.data.replace("'", '"'))

    for product in cart.products.all():
        if str(product.id) not in cart.data: cart.data[str(product.id)] = 1
        if cart.data[str(product.id)] <= 0:
            cart.products.remove(product)
            del cart.data[str(product.id)]
        elif cart.data[str(product.id)] > product.stock: cart.data[str(product.id)] = product.stock

    cart.data = json.dumps(cart.data)
    cart.save(force_update=True)
    data = json.loads(cart.data.replace("'", '"'))

    cart.data = {}
    cart.sum = 0
    for key in data:
        cart.data[int(key)] = int(data[key])
        cart.sum += models.Product.objects.get(id=int(key)).price * int(data[key])

    return render(
        request,
        'cart.html',
        {
            'title':'Корзина',
            'year':datetime.now().year,
            'cart': cart,
        }
    )

def store_place (request):
    assert isinstance(request, HttpRequest)

    cart = models.Cart.objects.get(owner=request.user)
    cart.data = json.loads(cart.data.replace("'", '"'))

    for product in cart.products.all():
        if str(product.id) not in cart.data: cart.data[str(product.id)] = 1
        if cart.data[str(product.id)] <= 0:
            cart.products.remove(product)
            del cart.data[str(product.id)]
        elif cart.data[str(product.id)] > product.stock: cart.data[str(product.id)] = product.stock

    order = models.Order.objects.create(
        buyer = request.user,
        data = cart.data
    )
    order.products.set(cart.products.all())

    cart.data = '{}'
    cart.products.clear()
    cart.save(force_update=True)

    return redirect('cart')


def profile (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')

    enrollments = models.Enrollment.objects.filter(owner=request.user)
    orders = models.Order.objects.filter(buyer=request.user)

    enrollment_state_choices = {
        "new": "Новый",
        "enrolled": "Записаный",
        "canceled": "Отмененный",
        "completed": "Завершенный",
    }

    enrollment_state_colors = {
        "new": "rgb(99, 177, 255)",
        "enrolled": "rgb(99, 255, 177)",
        "canceled": "rgb(255, 99, 99)",
        "completed": "rgb(99, 255, 99)",
    }

    for enrollment in enrollments:
        enrollment.status = enrollment_state_choices[enrollment.state]
        enrollment.color = enrollment_state_colors[enrollment.state]

    order_state_choices = {
        "new": "Новый",
        "confirmed": "Подтвержденный",
        "canceled": "Отмененный",
        "delivered": "Доставленный",
        "returned": "Возвратный",
        "completed": "Завершенный",
    }

    order_state_colors = {
        "new": "rgb(99, 177, 255)",
        "confirmed": "rgb(99, 255, 177)",
        "canceled": "rgb(255, 99, 99)",
        "delivered": "rgb(99, 99, 255)",
        "returned": "rgb(255, 177, 99)",
        "completed": "rgb(99, 255, 99)",
    }

    for order in orders:
        order.status = order_state_choices[order.state]
        order.color = order_state_colors[order.state]

        order.sum = 0
        for product in order.products.all():
            order.sum += product.price

    return render(
        request,
        'profile.html',
        {
            'title':'Профиль',
            'year':datetime.now().year,
            'enrollments': enrollments,
            'orders': orders
        }
    )


def management (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    return render(
        request,
        'management.html',
        {
            'title':'Управление',
            'year':datetime.now().year,
        }
    )

def manage_orders (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    orders = models.Order.objects.all()

    order_state_choices = {
        "new": "Новый",
        "confirmed": "Подтвержденный",
        "canceled": "Отмененный",
        "delivered": "Доставленный",
        "returned": "Возвратный",
        "completed": "Завершенный",
    }

    for order in orders:
        order.items = order.products.all()
        order.data = json.loads(order.data.replace("'", '"'))
        order.sum = 0
        order.status = order_state_choices[order.state]
        for product in order.items:
            order.sum += product.price
            product.quantity = order.data[str(product.id)]

    return render(
        request,
        'manage/orders.html',
        {
            'title':'Управление заказами',
            'year':datetime.now().year,
            'orders': orders,
            'statuses': order_state_choices
        }
    )

def manage_order_status (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    order_id = request.POST.get('order_id')
    order = models.Order.objects.get(id=order_id)
    order.state = request.POST.get('status')
    order.save()

    return redirect('manage_orders')

def manage_enrollments (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    enrollment_state_choices = {
        "new": "Новый",
        "enrolled": "Записаный",
        "canceled": "Отмененный",
        "completed": "Завершенный",
    }

    enrollments = models.Enrollment.objects.all()

    for enrollment in enrollments:
        enrollment.status = enrollment_state_choices[enrollment.state]

    return render(
        request,
        'manage/enrollments.html',
        {
            'title':'Управление записями',
            'year':datetime.now().year,
            'enrollments': enrollments,
            'statuses': enrollment_state_choices
        }
    )

def manage_enrollment_status (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    enrollment_id = request.POST.get('enrollment_id')
    enrollment = models.Enrollment.objects.get(id=enrollment_id)
    enrollment.state = request.POST.get('status')
    enrollment.save()

    return redirect('manage_enrollments')

def manage_blog (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    blog = models.Blog.objects.all()

    return render(
        request,
        'manage/blog.html',
        {
            'title':'Управление блогом',
            'year':datetime.now().year,
            'blog': blog,

        }
    )

def manage_blog_change (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    blog_id = parametr
    blog = models.Blog.objects.get(id=blog_id)
    blog.title = request.POST.get('title')
    blog.content = request.POST.get('content')
    blog.save()

    return redirect('manage_blog')

def manage_blog_delete (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    blog_id = parametr
    blog = models.Blog.objects.get(id=blog_id)
    blog.delete()

    return redirect('manage_blog')

def manage_new_post (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    if request.method =="POST":
        blogform = forms.BlogForm(request.POST,request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit= False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('manage_blog')
    else:
        blogform = forms.BlogForm()

    return render(
        request,
        'manage/new_post.html',
        {
           'form':blogform,
           'title': 'Добавить статью блога',
           'year':datetime.now().year,
        }
    )

def manage_products (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    products = models.Product.objects.all()

    for product in products:
        product.price = int(product.price)

    return render(
        request,
        'manage/products.html',
        {
            'title':'Управление товарами',
            'year':datetime.now().year,
            'products': products,
            'categories': models.Category.objects.all()
        }
    )

def manage_product_change (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    product = models.Product.objects.get(id=parametr)
    product.title = request.POST.get('title')
    product.content = request.POST.get('content')
    product.price = request.POST.get('price')
    product.stock = request.POST.get('stock')
    product.category = models.Category.objects.get(id=request.POST.get('category'))
    product.save()

    return redirect('manage_products')

def manage_product_delete (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    product = models.Product.objects.get(id=parametr)
    product.delete()

    return redirect('manage_products')

def manage_new_product (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    if request.method =="POST":
        productform = forms.ProductForm(request.POST,request.FILES)
        if productform.is_valid():
            product_f = productform.save(commit= False)
            product_f.save()

            return redirect('manage_products')
    else:
        productform = forms.ProductForm()

    return render(
        request,
        'manage/new_product.html',
        {
           'form':productform,
           'title': 'Добавить новый продукт',
           'year':datetime.now().year,
           'categories': models.Category.objects.all()
        }
    )

def manage_courses (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    courses = models.Course.objects.all()

    for course in courses:
        course.price = int(course.price)
        course.full_course_price = int(course.full_course_price)

    return render(
        request,
        'manage/courses.html',
        {
            'title':'Управление курсами',
            'year':datetime.now().year,
            'courses': courses
        }
    )

def manage_course_change (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    course = models.Course.objects.get(id=parametr)
    course.title = request.POST.get('title')
    course.content = request.POST.get('content')
    course.price = request.POST.get('price')
    course.full_course_price = request.POST.get('full_course_price')
    course.lessons_count = request.POST.get('lessons_count')
    course.start_date = request.POST.get('start_date')
    course.fdate_date = request.POST.get('fdate_date')
    course.save()

    return redirect('manage_courses')

def manage_course_delete (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    course = models.Course.objects.get(id=parametr)
    course.delete()

    return redirect('manage_courses')

def manage_new_course (request):
    assert isinstance(request, HttpRequest)

    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    if request.method =="POST":
        courseform = forms.CourseForm(request.POST,request.FILES)
        if courseform.is_valid():
            course_f = courseform.save(commit= False)
            course_f.save()

            return redirect('manage_courses')
    else:
        courseform = forms.CourseForm()

    return render(
        request,
        'manage/new_course.html',
        {
           'form':courseform,
           'title': 'Добавить новый курс',
           'year':datetime.now().year,
        }
    )


def newpost(request):
    assert isinstance(request,HttpRequest)

    if request.method =="POST":
        blogform = forms.BlogForm(request.POST,request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit= False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = forms.BlogForm()

    return render(
        request,
        'newpost.html',
        {
           'blogform':blogform,
           'title': 'Добавить статью блога',

           'year':datetime.now().year,

        }
    )

def missing_page (request):
    """Renders the 404 page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'error.html',
        {
            'year':datetime.now().year,
        }
    )
