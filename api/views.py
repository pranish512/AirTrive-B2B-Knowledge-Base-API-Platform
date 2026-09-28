from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.db.models import Q, Count
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Company, KBEntry, QueryLog
from .permissions import IsAdminUser

def access_token(user): return str(RefreshToken.for_user(user).access_token)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    username=(request.data.get('username') or '').strip(); password=request.data.get('password') or ''; company_name=(request.data.get('company_name') or '').strip(); email=(request.data.get('email') or '').strip()
    if not all([username,password,company_name,email]): return Response({'error':'username, password, company_name and email are required.'},status=400)
    if User.objects.filter(username=username).exists(): return Response({'error':'Username already exists.'},status=400)
    try:
        with transaction.atomic():
            user=User.objects.create_user(username=username,password=password,email=email)
            company=user.company
            company.company_name=company_name
            company.save(update_fields=['company_name'])
    except IntegrityError:
        return Response({'error':'Unable to register user.'},status=400)
    return Response({'username':user.username,'company_name':company.company_name,'api_key':company.api_key,'access':access_token(user)},status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    username=(request.data.get('username') or '').strip(); password=request.data.get('password') or ''
    user=authenticate(request,username=username,password=password)
    if user is None: return Response({'error':'Invalid username or password.'},status=status.HTTP_401_UNAUTHORIZED)
    if not hasattr(user,'company'): return Response({'error':'Company profile not found.'},status=400)
    return Response({'access':access_token(user),'company_name':user.company.company_name,'api_key':user.company.api_key})

@api_view(['POST'])
def query_kb(request):
    breakpoint()
    search_term=(request.data.get('search') or '').strip()
    if not search_term: return Response({'error':'search field is required and cannot be blank.'},status=400)
    if not hasattr(request.user,'company'): return Response({'error':'Company profile not found.'},status=403)
    company=request.user.company
    with transaction.atomic():
        qs=KBEntry.objects.filter(Q(question__icontains=search_term)|Q(answer__icontains=search_term)).order_by('id')
        results=list(qs.values('id','question','answer','category'))
        count=len(results)
        QueryLog.objects.create(company=company,search_term=search_term,results_count=count)
    return Response({'search':search_term,'count':count,'results':results})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def usage_summary(request):
    total=QueryLog.objects.aggregate(total=Count('id'))['total'] or 0
    active=QueryLog.objects.values('company').distinct().count()
    top=list(QueryLog.objects.values('search_term').annotate(count=Count('id')).order_by('-count','search_term')[:5])
    return Response({'total_queries':total,'active_companies':active,'top_search_terms':top})
