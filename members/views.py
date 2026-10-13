
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Member
from .serializers import MemberSerializer


class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all().order_by("-created_at")
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
