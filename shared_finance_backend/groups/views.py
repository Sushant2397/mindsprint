from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Group, GroupMember, FairnessPolicy
from .serializers import GroupSerializer, GroupMemberSerializer, FairnessPolicySerializer, GroupCreateSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """ViewSet for Group model"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Group.objects.filter(
            members__user=self.request.user,
            members__is_active=True
        ).distinct().prefetch_related('members__user', 'owner')
    
    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        # Add owner as a member
        GroupMember.objects.create(
            group=group,
            user=self.request.user,
            role='owner'
        )
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the group"""
        group = self.get_object()
        
        # Check if user is owner or treasurer
        member = group.members.filter(user=request.user).first()
        if not member or member.role not in ['owner', 'treasurer']:
            return Response(
                {'error': 'Only owners and treasurers can add members'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'member')
        share_factor = request.data.get('share_factor', 1.00)
        income_bracket = request.data.get('income_bracket', 'medium')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is already a member
        if group.members.filter(user_id=user_id).exists():
            return Response(
                {'error': 'User is already a member of this group'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            member = GroupMember.objects.create(
                group=group,
                user_id=user_id,
                role=role,
                share_factor=share_factor,
                income_bracket=income_bracket
            )
            serializer = GroupMemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'Error adding member: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the group"""
        group = self.get_object()
        member_id = request.data.get('member_id')
        
        if not member_id:
            return Response(
                {'error': 'member_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is owner or treasurer
        current_member = group.members.filter(user=request.user).first()
        if not current_member or current_member.role not in ['owner', 'treasurer']:
            return Response(
                {'error': 'Only owners and treasurers can remove members'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            member = get_object_or_404(GroupMember, id=member_id, group=group)
            
            # Cannot remove owner
            if member.role == 'owner':
                return Response(
                    {'error': 'Cannot remove group owner'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            member.is_active = False
            member.save()
            
            return Response({'message': 'Member removed successfully'})
        except Exception as e:
            return Response(
                {'error': f'Error removing member: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class GroupMemberViewSet(viewsets.ModelViewSet):
    """ViewSet for GroupMember model"""
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GroupMember.objects.filter(
            group__members__user=self.request.user,
            group__members__is_active=True
        ).select_related('user', 'group')


class FairnessPolicyViewSet(viewsets.ModelViewSet):
    """ViewSet for FairnessPolicy model"""
    queryset = FairnessPolicy.objects.all()
    serializer_class = FairnessPolicySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FairnessPolicy.objects.filter(
            group__members__user=self.request.user,
            group__members__is_active=True
        ).select_related('group', 'created_by')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)