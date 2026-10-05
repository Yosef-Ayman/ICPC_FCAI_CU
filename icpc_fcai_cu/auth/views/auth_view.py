from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


def login_view(request):
    if request.user.is_authenticated:
        return redirect("app:home-index")

    next_url = request.GET.get("next") or request.POST.get("next") or "/"

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )

        if user is None:
            messages.error(request, "Invalid username or password")
        elif not user.is_active:
            messages.error(request, "Your account is inactive")
        else:
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("/")

    return render(request, "pages/auth/login.html", {"next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")