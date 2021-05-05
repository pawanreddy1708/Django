from rest_framework import routers
from snippets.api.viewsets import UserViewset

router  = routers.DefaultRouter()
router.register('employee',UserViewset)