from django.contrib import admin

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    #khalti
    path('initiate',views.initkhalti,name="initiate"),
    path('verify',views.verifyKhalti,name="verify"),
    
    path("pagedetail/<int:id>", views.page_detail, name="pagedetail"),
    path("service_details/<int:id>", views.service_detail, name="service_details"),
    path("faq", views.faq_list, name="faq"),
    path("enquiry", views.enquiry, name="enquiry"),
    path('contact',views.contact_page,name='contact_page'),
    path("gallery", views.gallery, name="gallery"),
    path("gallerydetail/<int:id>", views.gallery_detail, name="gallerydetail"),
    path("pricing", views.pricing, name="pricing"),
    path("signup", views.signup, name="signup"),
    path("checkout/<int:plan_id>", views.checkout, name="checkout"),
    # User dashboard section start
    path("user_dashboard", views.user_dashboard, name="user_dashboard"),
    path("update_profile", views.update_profile, name="update_profile"),
    # Trainer login
    path("trainerlogin", views.trainerlogin, name="trainerlogin"),
    path("trainerlogout", views.trainerlogout, name="trainerlogout"),
    path("trainer_dashboard", views.trainer_dashboard, name="trainer_dashboard"),
    path("trainer_profile", views.trainer_profile, name="trainer_profile"),
    path("trainer_subscribers", views.trainer_subscribers, name="trainer_subscribers"),
    path("trainer_payments", views.trainer_payments, name="trainer_payments"),
    path(
        "trainer_changepassword",
        views.trainer_changepassword,
        name="trainer_changepassword",
    ),
    path("trainer_notifs", views.trainer_notifs, name="trainer_notifs"),
    # Notification
    path("notifs", views.notifs, name="notifs"),
    path("get_notifs", views.get_notifs, name="get_notifs"),
    path("mark_read_notif", views.mark_read_notif, name="mark_read_notif"),
    # Messages
    path("messages", views.trainer_msgs, name="messages"),
    path(
        "mark_read_trainer_notif",
        views.mark_read_trainer_notif,
        name="mark_read_trainer_notif",
    ),
    path("report_for_user", views.report_for_user, name="report_for_user"),
    path("report_for_trainer", views.report_for_trainer, name="report_for_trainer"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
