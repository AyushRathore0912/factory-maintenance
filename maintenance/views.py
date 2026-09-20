from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import (
    Category,
    Breakdown,
    BreakdownHistory,
    Machine,
)


# =========================================================
# LOGIN
# =========================================================

class UserLoginView(LoginView):
    template_name = "maintenance/login.html"
    redirect_authenticated_user = True


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # ---------------------------------------------
        # REQUIRED FIELD CHECK
        # ---------------------------------------------

        if not username:
            messages.error(request, "Username is required.")
            return render(
                request,
                "maintenance/register.html"
            )

        if not password:
            messages.error(request, "Password is required.")
            return render(
                request,
                "maintenance/register.html"
            )

        if not confirm_password:
            messages.error(
                request,
                "Please confirm your password."
            )
            return render(
                request,
                "maintenance/register.html"
            )


        # ---------------------------------------------
        # USERNAME CHECK
        # ---------------------------------------------

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "This username is already registered."
            )

            return render(
                request,
                "maintenance/register.html"
            )


        # ---------------------------------------------
        # PASSWORD MATCH CHECK
        # ---------------------------------------------

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "maintenance/register.html"
            )


        # ---------------------------------------------
        # CREATE USER
        # ---------------------------------------------

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )


        # ---------------------------------------------
        # SUCCESS
        # ---------------------------------------------

        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect("login")


    # GET REQUEST

    return render(
        request,
        "maintenance/register.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    return redirect("login")


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    categories = Category.objects.prefetch_related(
        "sections__machines"
    )

    return render(
        request,
        "maintenance/dashboard.html",
        {
            "categories": categories
        }
    )


# =========================================================
# REPORT BREAKDOWN
# =========================================================

@login_required
def report_breakdown(request):

    categories = Category.objects.prefetch_related(
        "sections__machines"
    )


    if request.method == "POST":

        machine_id = request.POST.get("machine")

        start_date = request.POST.get("start_date")

        start_time = request.POST.get("start_time")

        problem = request.POST.get(
            "problem",
            ""
        ).strip()

        solution = request.POST.get(
            "solution",
            ""
        ).strip()


        # ---------------------------------------------
        # MACHINE CHECK
        # ---------------------------------------------

        if not machine_id:

            messages.error(
                request,
                "Please select a machine."
            )

            return render(
                request,
                "maintenance/breakdown.html",
                {
                    "categories": categories
                }
            )


        # ---------------------------------------------
        # DATE/TIME CHECK
        # ---------------------------------------------

        if not start_date or not start_time:

            messages.error(
                request,
                "Please enter breakdown date and time."
            )

            return render(
                request,
                "maintenance/breakdown.html",
                {
                    "categories": categories
                }
            )


        # ---------------------------------------------
        # PROBLEM CHECK
        # ---------------------------------------------

        if not problem:

            messages.error(
                request,
                "Please describe the problem."
            )

            return render(
                request,
                "maintenance/breakdown.html",
                {
                    "categories": categories
                }
            )


        # ---------------------------------------------
        # GET MACHINE
        # ---------------------------------------------

        try:

            machine = Machine.objects.get(
                id=machine_id,
                is_active=True
            )

        except Machine.DoesNotExist:

            messages.error(
                request,
                "Selected machine was not found."
            )

            return render(
                request,
                "maintenance/breakdown.html",
                {
                    "categories": categories
                }
            )


        # ---------------------------------------------
        # DATETIME
        # ---------------------------------------------

        from datetime import datetime

        start_datetime = datetime.strptime(
            f"{start_date} {start_time}",
            "%Y-%m-%d %H:%M"
        )


        # ---------------------------------------------
        # CREATE BREAKDOWN
        # ---------------------------------------------

        breakdown = Breakdown.objects.create(

            machine=machine,

            reported_by=request.user,

            problem=problem,

            solution=solution,

            status="OPEN",

            start_time=start_datetime

        )


        # ---------------------------------------------
        # CREATE HISTORY
        # ---------------------------------------------

        BreakdownHistory.objects.create(

            breakdown=breakdown,

            action="BREAKDOWN_REPORTED",

            remarks="Breakdown reported by user.",

            performed_by=request.user

        )


        # ---------------------------------------------
        # SUCCESS MESSAGE
        # ---------------------------------------------

        messages.success(
            request,
            f"Breakdown reported successfully for {machine.name}."
        )


        return redirect("dashboard")


    # GET REQUEST

    return render(
        request,
        "maintenance/breakdown.html",
        {
            "categories": categories
        }
    )

# =========================================================
# ACTIVE BREAKDOWNS
# =========================================================

@login_required
def active_breakdowns(request):

    breakdowns = Breakdown.objects.filter(

        status__in=[
            "OPEN",
            "IN_PROGRESS"
        ]

    ).select_related(

        "machine",
        "machine__section",
        "machine__section__category",
        "reported_by",

    ).order_by(
        "-start_time"
    )

    return render(

        request,

        "maintenance/active_breakdowns.html",

        {
            "breakdowns": breakdowns
        }

    )


# =========================================================
# RESOLVE BREAKDOWN
# =========================================================

@login_required
def resolve_breakdown(request, breakdown_id):

    if request.method != "POST":
        return redirect("active_breakdowns")

    try:
        breakdown = Breakdown.objects.get(
            id=breakdown_id,
            status__in=[
                "OPEN",
                "IN_PROGRESS"
            ]
        )

    except Breakdown.DoesNotExist:

        messages.error(
            request,
            "Breakdown not found or already resolved."
        )

        return redirect("active_breakdowns")

    breakdown.status = "RESOLVED"
    breakdown.end_time = timezone.now()

    breakdown.save(
        update_fields=[
            "status",
            "end_time",
            "updated_at"
        ]
    )

    BreakdownHistory.objects.create(
        breakdown=breakdown,
        action="BREAKDOWN_RESOLVED",
        remarks="Machine repaired and breakdown resolved.",
        performed_by=request.user
    )

    messages.success(
        request,
        f"{breakdown.machine.name} breakdown resolved successfully."
    )

    return redirect("active_breakdowns")