from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pagedetail/<int:id>", views.page_detail, name="pagedetail"),
    path("faq", views.faq_list, name="faq"),
    path("enquiry", views.enquiry, name="enquiry"),
    path("gallery", views.gallery, name="gallery"),
    path("gallerydetail/<int:id>", views.gallery_detail, name="gallerydetail"),
    path("pricing", views.pricing, name="pricing"),
    path("signup", views.signup, name="signup"),
    path("checkout/<int:plan_id>", views.checkout, name="checkout"),
    # User dashboard section start
    path("user-dashboard", views.user_dashboard, name="user_dashboard"),
    path("update-profile", views.update_profile, name="update_profile"),
    # Trainer login
    path("trainerlogin", views.trainerlogin, name="trainerlogin"),
    path("trainerlogout", views.trainerlogout, name="trainerlogout"),
    # Notification
    path("notifs", views.notifs, name="notifs"),
    path('get_notifs',views.get_notifs,name='get_notifs'),
	path('mark_read_notif',views.mark_read_notif,name='mark_read_notif'),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
