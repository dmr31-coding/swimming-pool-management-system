from django.shortcuts import render, redirect

from django.template.loader import get_template

from . import models

from . import forms

from django.db.models import Count

from django.core import serializers

from django.http import JsonResponse

from datetime import timedelta

import json

import requests

import uuid

# Create your views here.


# Home page
def home(request):
    id = uuid.uuid4()
    banners = models.Banners.objects.all()
    services = models.Service.objects.all()[:3]
    gimgs = models.GalleryImage.objects.all().order_by("-id")[:9]
    return render(
        request,
        "bootstrap/home.html",
        {"banners": banners, "services": services, "gimgs": gimgs, "uuid": id},
    )


# ServiceDetail
def service_detail(request, id):
    service = models.Service.objects.get(id=id)
    return render(
        request, "bootstrap/service_detailpage.html", {"service_details": service}
    )


# PageDetail
def page_detail(request, id):
    page = models.Page.objects.get(id=id)
    return render(request, "bootstrap/page.html", {"page": page})


# FAQ
def faq_list(request):
    faq = models.Faq.objects.all()
    return render(request, "bootstrap/faq.html", {"faqs": faq})


# Contact
def contact_page(request):
    return render(request, "user/contact.html")


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

    # Notification
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

    return render(
        request,
        "user/dashboard.html",
        {
            "current_plan": current_plan,
            "my_trainer": my_trainer,
            "total_unread": totalUnread,
            "enddate": enddate,
        },
    )


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
    del request.session["tranerLogin"]
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


# Trainer subscriber
def trainer_subscribers(request):
    trainer = models.Trainer.objects.get(pk=request.session["tranerid"])
    trainer_subs = models.AssignSubscriber.objects.filter(trainer=trainer).order_by(
        "-id"
    )
    return render(
        request, "trainer/trainer_subscribers.html", {"trainer_subs": trainer_subs}
    )


# Trainer Payments
def trainer_payments(request):
    trainer = models.Trainer.objects.get(pk=request.session["tranerid"])
    trainer_pays = models.TrainerSalary.objects.filter(trainer=trainer).order_by("-id")
    return render(
        request, "trainer/trainer_payments.html", {"trainer_pays": trainer_pays}
    )


# Trainer Change Password
def trainer_changepassword(request):
    msg = None
    if request.method == "POST":
        new_password = request.POST["new_password"]
        updateRes = models.Trainer.objects.filter(
            pk=request.session["tranerid"]
        ).update(pwd=new_password)
        if updateRes:
            del request.session["tranerLogin"]
            return redirect("/trainerlogin")
        else:
            msg = "Something is wrong!!"
    form = forms.TrainerChangePassword
    return render(request, "trainer/trainer_changepassword.html", {"form": form})


# Trainer Notifications
def trainer_notifs(request):
    data = models.TrainerNotification.objects.all().order_by("-id")
    trainer = models.Trainer.objects.get(id=request.session["tranerid"])
    jsonData = []
    totalUnread = 0
    for d in data:
        try:
            notifStatusData = models.NotifTrainerStatus.objects.get(
                trainer=trainer, notif=d
            )
            if notifStatusData:
                notifStatus = True
        except models.NotifTrainerStatus.DoesNotExist:
            notifStatus = False
        if not notifStatus:
            totalUnread = totalUnread + 1
        jsonData.append(
            {"pk": d.id, "notify_detail": d.notif_msg, "notifStatus": notifStatus}
        )
    return render(
        request, "trainer/notifs.html", {"notifs": jsonData, "totalUnread": totalUnread}
    )


# Mark Read By trainer
def mark_read_trainer_notif(request):
    notif = request.GET["notif"]
    notif = models.TrainerNotification.objects.get(pk=notif)
    trainer = models.Trainer.objects.get(id=request.session["tranerid"])
    models.NotifTrainerStatus.objects.create(notif=notif, trainer=trainer, status=True)

    # Count Unread
    totalUnread = 0
    data = models.TrainerNotification.objects.all().order_by("-id")
    for d in data:
        try:
            notifStatusData = models.NotifTrainerStatus.objects.get(
                trainer=trainer, notif=d
            )
            if notifStatusData:
                notifStatus = True
        except models.NotifTrainerStatus.DoesNotExist:
            notifStatus = False
        if not notifStatus:
            totalUnread = totalUnread + 1

    return JsonResponse({"bool": True, "totalUnread": totalUnread})


# Trainer Messages
def trainer_msgs(request):
    data = models.TrainerMsg.objects.all().order_by("-id")
    return render(request, "trainer/msgs.html", {"msgs": data})


# Report for user
def report_for_user(request):
    trainer = models.Trainer.objects.get(id=request.session["tranerid"])
    msg = ""
    if request.method == "POST":
        form = forms.ReportForUserForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.report_from_trainer = trainer
            new_form.save()
            msg = "Data has been saved"
        else:
            msg = "Invalid Response!!"
    form = forms.ReportForUserForm
    return render(request, "report_for_user.html", {"form": form, "msg": msg})


# Report for trainer
def report_for_trainer(request):
    user = request.user
    msg = ""
    if request.method == "POST":
        form = forms.ReportForTrainerForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.report_from_user = user
            new_form.save()
            msg = "Data has been saved"
        else:
            msg = "Invalid Response!!"
    form = forms.ReportForTrainerForm
    return render(request, "report_for_trainer.html", {"form": form, "msg": msg})


# khalti
def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get("return_url")
    website_url = request.POST.get("return_url")
    amount = request.POST.get("amount")
    purchase_order_id = request.POST.get("purchase_order_id")

    print("url", url)
    print("return_url", return_url)
    print("web_url", website_url)
    print("amount", amount)
    print("purchase_order_id", purchase_order_id)
    payload = json.dumps(
        {
            "return_url": return_url,
            "website_url": "http://127.0.0.1:8000",
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": "Raju Magar",
                "email": "rm3671323@gmail.com",
                "phone": "9800000001",
            },
        }
    )

    # put your own live secet for admin
    headers = {
        "Authorization": "key f2e9f5b533b3495e970bf159a052d5d8",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(json.loads(response.text))

    print(response.text)
    new_res = json.loads(response.text)
    # print(new_res['payment_url'])
    print(type(new_res))
    return redirect(new_res["payment_url"])
    return redirect("home")


def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == "GET":
        headers = {
            "Authorization": "key b885cd9d8dc04eebb59e6f12190ae017",
            "Content-Type": "application/json",
        }
        pidx = request.GET.get("pidx")
        data = json.dumps({"pidx": pidx})
        res = requests.request("POST", url, headers=headers, data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)

        if new_res["status"] == "Completed":
            # user = request.user
            # user.has_verified_dairy = True
            # user.save()
            # perform your db interaction logic
            pass

        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        return redirect("home")
