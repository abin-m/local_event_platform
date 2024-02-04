from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, UserSerializer, EventSerializer
from .models import Event
from .tasks import  send_event_notification
from django.contrib.auth import authenticate
class UserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_200_OK)
class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token is None:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def event_list(request, pk=None):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save(creator=request.user)

        # Asynchronously send event notification email using Celery
        send_event_notification.apply_async(args=[event.id, 'POST'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        event = get_object_or_404(Event, pk=pk)
        
        # Check if the requesting user is the creator of the event
        if request.user == event.creator:
            event_details = {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "time": event.time,
                "location": event.location
            }

            event.delete()

            # Asynchronously send event notification email using Celery
            send_event_notification.apply_async(args=[event_details, 'DELETE'])

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You do not have permission to delete this event.'}, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':
        event = get_object_or_404(Event, pk=pk)
        
        # Check if the requesting user is the creator of the event
        if request.user == event.creator:
            serializer = EventSerializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Asynchronously send event notification email using Celery
            send_event_notification.apply_async(args=[pk, 'PUT'])

            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to update this event.'}, status=status.HTTP_403_FORBIDDEN)