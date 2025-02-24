from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import RentAdvertisement, RentRequest
from .serializers import RentAdvertisementSerializer, RentRequestSerializer
from .permissions import IsAdminOrReadOnly

class RentAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = RentAdvertisement.objects.all()
    serializer_class = RentAdvertisementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['title', 'location', 'price', 'description']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsAdminOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return RentAdvertisement.objects.filter(status='approved')
        return RentAdvertisement.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        ad = self.get_object()
        ad.status = "approved"
        ad.is_available = True  # Ensure ad becomes available when approved
        ad.save()
        return Response({"message": "Advertisement approved successfully"})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        ad = self.get_object()
        ad.status = "rejected"
        ad.save()
        return Response({"message": "Advertisement rejected"})

class RentRequestViewSet(viewsets.ModelViewSet):
    serializer_class = RentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return RentRequest.objects.filter(
            Q(user=self.request.user) | 
            Q(ad__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only allow ad owners to update status
        if instance.ad.user != request.user:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')
        if new_status not in ['accepted', 'rejected']:
            return Response(
                {"detail": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle status change
        if new_status == 'accepted':
            if not instance.ad.is_available:
                return Response(
                    {"detail": "Advertisement is already rented"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Update advertisement availability
            instance.ad.is_available = False
            instance.ad.save()
            
            # Reject other requests
            RentRequest.objects.filter(ad=instance.ad).exclude(pk=instance.pk).update(status='rejected')

        instance.status = new_status
        instance.save()
        return Response(self.get_serializer(instance).data)