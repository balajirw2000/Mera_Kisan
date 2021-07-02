from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns = [
    path('ShopNow', views.ShopNow, name='Shop-page'),
    path('add1', views.add1, name='add1'),
    path('checkout', views.checkout, name='checkout'),
    path('tracker', views.tracker, name='tracker'),
    path('viewDetail/<int:myid>', views.viewDetail, name='view-Detail'),
    path('postComment', views.postComment, name="postComment"),
    path('replyComment', views.replyComment, name="replyComment"),
    #APIS To Post a Comment
   # path('Comments',views.Comments,name='Comments'),
]
