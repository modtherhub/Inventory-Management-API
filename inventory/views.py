from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import InventoryItem, InventoryChangeLog
from .serializers import InventoryItemSerializer, InventoryChangeLogSerializer, UserSerializer, UserRegisterSerializer
from .permissions import IsOwner
from .filters import InventoryItemFilter
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound

User = get_user_model()

# Inventory Item Management
# handles CRUD operations for inventory items
# only authenticated users can access, and users see only their own items
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner] # Ensure users can only access their items
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = InventoryItemFilter
    ordering_fields = ['name', 'quantity', 'price', 'last_updated']
    search_fields = ['name', 'description', 'category']

    def get_queryset(self):
        # only displays items owned by the current user.
        return InventoryItem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        item = serializer.save(owner=self.request.user)
        InventoryChangeLog.objects.create(
            item=item,
            changed_by=self.request.user,
            old_quantity=0,
            new_quantity=item.quantity,
            change_type="restock"
        )

    def perform_update(self, serializer):
        old_item = self.get_object()
        old_qty = old_item.quantity
        if serializer.validated_data.get("quantity", None) is not None and serializer.validated_data["quantity"] < 0:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"quantity": "Quantity cannot be negative"})
        
        # save update
        item = serializer.save()
        
        # define change
        if item.quantity > old_qty:
            change_type = "restock"
        elif item.quantity < old_qty:
            change_type = "sale"
        else:
            change_type = "adjustment"
        
        # Save change
        InventoryChangeLog.objects.create(
            item=item,
            changed_by=self.request.user,
            old_quantity=old_qty,
            new_quantity=item.quantity,
            change_type=change_type
        )

    # PermissionDenied when user tries modeify or delete item not owned  
    def get_object(self):
        try:
            obj = InventoryItem.objects.get(pk=self.kwargs["pk"], owner=self.request.user)
        except InventoryItem.DoesNotExist:
            raise NotFound(detail="Item not found.")
        return obj

# Inventory Change Log
# read-only view of all inventory changes, for auditing purposes
# accessible only by authenticated users
class InventoryChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = InventoryChangeLog.objects.all()
        # allow filtering by item
        item_id = self.request.query_params.get("item")
        if item_id:
            queryset = queryset.filter(item__id=item_id)
        # show only changes related to items owned by the current user
        return queryset.filter(item__owner=self.request.user)

# Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Only administrators can manage users.
    permission_classes = [permissions.IsAdminUser]

# Login Endpoint
# handles user authentication and returns a token for API access
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
             # generate or retrieve token for the user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        # return error for invalid credentials
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            #Delete the current user's token
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Token not found or already deleted"}, status=status.HTTP_400_BAD_REQUEST)
    
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class InventoryLevelViewSet(viewsets.ReadOnlyModelViewSet):

    # List-only endpoint that returns the current user's inventory items (with quantities).    
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = InventoryItemFilter
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['price', 'quantity', 'last_updated']

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user).order_by('-last_updated')