from rest_framework import routers

from .viewsets import CertificateViewSet, NonceViewSet, SyncSessionViewSet, TransferSessionViewSet, BufferViewSet

router = routers.SimpleRouter()
router.register(r'certificates', CertificateViewSet, base_name="certificates")
router.register(r'nonces', NonceViewSet, base_name="nonces")
router.register(r'syncsessions', SyncSessionViewSet, base_name="syncsessions")
router.register(r'transfersessions', TransferSessionViewSet, base_name="transfersessions")
router.register(r'buffers', BufferViewSet, base_name="buffers")
urlpatterns = router.urls
