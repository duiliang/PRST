from django.urls import path
from businessApp.views import *

urlpatterns = [
    path('<slug:kind>/', home, name="business"),
    path('Employee/timecard/', timecard_home, name="timecard_home"),
    path('Employee/timecard/create_timecard/', create_timecard, name="create_timecard"),
    path('Employee/purchaseorder', purchaseorder_home, name="purchaseorder_home"),
    path('Employee/purchaseorder/create_purchaseorder', create_purchaseorder, name="create_purchaseorder"),
    path('Employee/purchaseorder/view_order_detail/<int:order_id>', view_order_detail, name="view_order_detail"),
    path('Employee/purchaseorder/update_order/<int:order_id>', update_order, name="update_purchaseorder"),
    path('Employee/purchaseorder/delete_order/<int:order_id>', delete_purchaseorder, name="delete_purchaseorder"),
]
