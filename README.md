## [Django] Auth 정복하기(1)_Signup (회원가입)



#### **📄 유저 시나리오**

1. 회원가입 버튼을 누른다.

2. 회원가입 폼이 담긴 페이지가 나온다.

3. 회원가입 폼을 작성하여 제출 버튼을 누른다.

4. 회원가입이 정상적으로 완료되면 바로 로그인이 되고 메인페이지가 나온다.



#### **🔨 기능 구현하기**

**1) urls** 

: accounts 앱에 signup이라는 이름의 주소 생성

```python
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
```





**2) views**



- GET: 회원가입 폼이 담긴 페이지를 응답
- POST: 회원가입 정보를 받아서 "유효성 검사" 후 회원가입 진행
  - 유효성 검사를 통과하지 못한 경우 에러 메세지를 담아서 출력

(단, 로그인이 된 상태에서 signup 함수를 실행하려한다면 바로 메인페이지로 이동)

```python
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```



**① request.user.is_authenticated**

: 사용자가 인증되었는지 확인하는 함수.
User에 항상 True이며, AnonymousUser에 대해서만 항상 False.



**② UserCreationForm**

: 새로운 유저를 생성해주는 내장 폼



**③ auth_login** (원래 login)

: 유저 정보를 세션에 생성 및 저장하는 역할을 하는 Django 내장 함수





**3) templates**

: 회원가입 폼이 담긴 페이지

```html
{% extends 'base.html' %}

{% block content %}
  <h1>Signup</h1>
  <form action="{% url 'accounts:signup' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```





\* 만약 UsercreationFrom을 수정하고 싶다면!



**4) forms**

```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# User 모델을 불러오는 2가지 방법 
from django.contrib.auth.models import User # Django 내장 User 모델
from django.conf import settings # => settings.AUTH_USER_MODEL


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        # fields = ('username', 'password1', 'password2', 'email')
        fields = UserCreationForm.Meta.fields + ('email',)
```





## [Django] Auth 정복하기(2)_Login & Logout



#### **📄 유저 시나리오**

**- 로그인**

1. 로그인 버튼을 누른다.

2. 로그인 폼이 담긴 페이지가 나온다.

3. 로그인 폼을 작성하여 제출 버튼을 누른다.

4. 로그인이 정상적으로 완료되면 메인페이지가 나온다.



**- 로그아웃**

1. 로그아웃 버튼을 누른다.

2. 로그아웃이 되고 메인페이지가 나온다.



#### **🔨 기능 구현하기**

**1) urls**

: accounts 앱에 login, logout이라는 이름의 주소 생성



```python
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
```





**2) views**



**- Login**

- GET: 로그인 폼이 담긴 페이지를 응답

- POST: 사용자 정보 받아서 유효성 검사 후 

  **로그인**

  - **로그인 == 세션 생성 후 DB에 저장**
  - 유효성 검사 실패 시 에러 메세지 출력

(단, 로그인이 된 상태에서 login 함수를 실행하려한다면 바로 메인페이지로 이동)

```python
from django.contrib.auth.forms import AuthenticationForm

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```



**① AuthenticationForm**

: 유저가 존재하는지를 검증하는 Django 내장 모델 폼





**- Logout**

- POST: 세션 제거

(단, 로그인이 되지 않은 상태에서 logout 함수를 실행하려한다면 바로 로그인 페이지로 이동)



```python
def logout(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    auth_logout(request) # 세션 제거 & requset.user 값 초기화
    return redirect('/articles/')
```



**① auth_logout** (원래 logout)

: 현재 요청에 대한 db의 세션 데이터를 삭제하고 클라이언트 쿠키에서도 sessionid를 삭제하는 함수





**3) templates**



**- login**

: 로그인 폼이 담긴 페이지

```html
{% extends 'base.html' %}

{% block content %}
  <h1>Login</h1>
  <form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```



## [Django] Auth 정복하기(3)_Update & Delete

#### **📄 유저 시나리오**

**- Update (회원정보수정)**

\1. 회원정보 수정 버튼을 누른다.

\2. 기존의 데이터와 함께 회원정보 수정 폼이 담긴 update 페이지가 나온다.

\3. 정보를 수정하고 체줄 버튼을 누른다.

\4. 정상적으로 수정이 완료되면 메인 페이지로 이동한다.



**- delete (회원탈퇴)**

\1. 회원 탈퇴 버튼을 누른다.

\2. 로그아웃 된채로 메인페이지로 이동한다.



#### **🔨 기능 구현하기**

**1) urls**

: accounts앱에 update, delete라는 이름의 주소 생성

```python
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
]
```





**2) views**



**- Update**

- GET: 정보 수정 폼이 담긴 페이지를 응답
- POST: 사용자 정보 받아서 유효성 검사 후 정보수정

```python
from django.contrib.auth.forms import UserChangeForm, 

def update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)
```



**① UserChangeForm**

: 유저의 정보를 수정하는 장고 내장 폼





**- Delete**

- POST: 유저 정보 제거, 세션 제거

```python
@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('articles:index')
```





**3) templates**



**- Update**

: 정보 수정 폼이 담긴 페이지

```html
{% extends 'base.html' %}

{% block content %}
  <h1>회원정보수정</h1>
  <form action="{% url 'accounts:update' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```





**4) forms**

: UserChangeForm을 수정한 CustomUserChangeForm 생성

```python
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)
```

