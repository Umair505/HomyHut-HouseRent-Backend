from rest_framework import viewsets, permissions
from rest_framework import filters
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly  

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()  # Show all reviews to everyone
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Updated
    filter_backends = [filters.SearchFilter]
    search_fields = ['ad__title', 'comment']

    def perform_create(self, serializer):
        # Automatically assign the current user as the review owner
        serializer.save(user=self.request.user)