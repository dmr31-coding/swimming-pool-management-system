from django.shortcuts import render, redirect

from django.template.loader import get_template

from . import models

from . import forms

from django.db.models import Count

from django.core import serializers

from django.http import JsonResponse

from datetime import timedelta

# Create your views here.


# Home page
def home(request):
    banners = models.Banners.objects.all()
    services = models.Service.objects.all()[:3]
    gimgs = models.GalleryImage.objects.all().order_by("-id")[:9]
    return render(
        request,
        "bootstrap/home.html",
        {"banners": banners, "services": services, "gimgs": gimgs},
    )


# PageDetail
def page_detail(request, id):
    page = models.Page.objects.get(id=id)
    return render(request, "bootstrap/page.html", {"page": page})


# FAQ
def faq_list(request):
    faq = models.Faq.objects.all()
    return render(request, "bootstrap/faq.html", {"faqs": faq})


# Enquiry
def enquiry(request):
    msg = ""
    if request.method == "POST":
        form = forms.EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Data has been saved."
    form = forms.EnquiryForm
    return render(request, "bootstrap/enquiry.html", {"form": form, "msg": msg})


# Show galleries
def gallery(request):
    gallery = models.Gallery.objects.all().order_by("-id")
    return render(request, "bootstrap/gallery.html", {"galleries": gallery})


# Show gallery photos
def gallery_detail(request, id):
    gallery = models.Gallery.objects.get(id=id)
    gallery_imgs = models.GalleryImage.objects.filter(gallery=gallery).order_by("-id")
    return render(
        request,
        "bootstrap/gallery_img.html",
        {"gallery_imgs": gallery_imgs, "gallery": gallery},
    )


# Subcription plan
def pricing(request):
    pricing = (
        models.SubPlan.objects.annotate(total_members=Count("subscription__id"))
        .all()
        .order_by("price")
    )
    dfeatures = models.SubPlanFeature.objects.all()

    return render(
        request, "bootstrap/pricing.html", {"plans": pricing, "dfeatures": dfeatures}
    )


# SignUp
def signup(request):
    msg = None
    if request.method == "POST":
        form = forms.SignUp(request.POST)
        if form.is_valid():
            form.save()
            msg = "Thank you for register."
    form = forms.SignUp
    return render(request, "registration/signup.html", {"form": form, "msg": msg})


# Checkout
def checkout(request, plan_id):
    planDetail = models.SubPlan.objects.get(pk=plan_id)
    return render(request, "bootstrap/checkout.html", {"plan": planDetail})


# User Dashboard Section Start
def user_dashboard(request):
    current_plan = models.Subscription.objects.get(user=request.user)
    my_trainer = models.AssignSubscriber.objects.get(user=request.user)
    enddate = current_plan.reg_date + timedelta(days=current_plan.plan.validity_days)
    return redirect("home")


# Edit Form
def update_profile(request):
    msg = None
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = "Data has been saved"
    form = forms.ProfileForm(instance=request.user)
    return render(request, "user/update_profile.html", {"form": form, "msg": msg})


# Trainer Login
def trainerlogin(request):
    msg = ""
    if request.method == "POST":
        username = request.POST["username"]
        pwd = request.POST["pwd"]
        trainer = models.Trainer.objects.filter(username=username, pwd=pwd).count()
        if trainer > 0:
            trainer = models.Trainer.objects.filter(username=username, pwd=pwd).first()
            request.session["tranerLogin"] = True
            request.session["tranerid"] = trainer.id
            return redirect("/trainer_dashboard")
        else:
            msg = "Invalid!!"
    form = forms.TrainerLoginForm
    return render(request, "trainer/trainerlogin.html", {"form": form, "msg": msg})


# Trainer Logout
def trainerlogout(request):
    del request.session["trainerLogin"]
    return redirect("/trainerlogin")


# Trainer Dashboard
def trainer_dashboard(request):
    return render(request, "trainer/dashboard.html")


# Trainer Profile
def trainer_profile(request):
    t_id = request.session["tranerid"]
    trainer = models.Trainer.objects.get(pk=t_id)
    msg = None
    if request.method == "POST":
        form = forms.TrainerProfileForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            msg = "Profile has been updated."

    form = forms.TrainerProfileForm(instance=trainer)
    return render(request, "trainer/profile.html", {"form": form, "msg": msg})


# Notifications
def notifs(request):
    data = models.Notify.objects.all().order_by("-id")
    return render(request, "user/notif.html")


# Get All Notifications
def get_notifs(request):
    data = models.Notify.objects.all().order_by("-id")
    notifStatus = False
    jsonData = []
    totalUnread = 0
    for d in data:
        try:
            notifStatusData = models.NotifUserStatus.objects.get(
                user=request.user, notif=d
            )
            if notifStatusData:
                notifStatus = True
        except models.NotifUserStatus.DoesNotExist:
            notifStatus = False
        if not notifStatus:
            totalUnread = totalUnread + 1
        jsonData.append(
            {"pk": d.id, "notify_detail": d.notify_detail, "notifStatus": notifStatus}
        )
    # jsonData=serializers.serialize('json', data)
    return JsonResponse({"data": jsonData, "totalUnread": totalUnread})


# Mark Read By user
def mark_read_notif(request):
    notif = request.GET["notif"]
    notif = models.Notify.objects.get(pk=notif)
    user = request.user
    models.NotifUserStatus.objects.create(notif=notif, user=user, status=True)
    return JsonResponse({"bool": True})
