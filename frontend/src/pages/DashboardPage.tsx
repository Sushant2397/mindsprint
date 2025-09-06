import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { PlusIcon, UserGroupIcon, CurrencyDollarIcon, ChartBarIcon, ArrowLeftOnRectangleIcon, UserCircleIcon, BellIcon } from '@heroicons/react/24/outline';
import { Button } from '../ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { apiService } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import { useAppStore } from '../stores/appStore';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { GroupCreateModal } from '../components/GroupCreateModal';

export function DashboardPage() {
  const { user, logout } = useAuthStore();
  const { addNotification } = useAppStore();
  const [isCreatingGroup, setIsCreatingGroup] = useState(false);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: groups, isLoading, error, refetch } = useQuery({
    queryKey: ['groups'],
    queryFn: () => apiService.getGroups(),
  });

  const createGroupMutation = useMutation({
    mutationFn: apiService.createGroup,
    onSuccess: (newGroup) => {
      queryClient.invalidateQueries({ queryKey: ['groups'] });
      addNotification({
        type: 'success',
        title: 'Group Created',
        message: `"${newGroup.name}" has been created successfully!`,
        read: false,
      });
      setIsCreatingGroup(false);
    },
    onError: (error: any) => {
      addNotification({
        type: 'error',
        title: 'Failed to Create Group',
        message: error.response?.data?.error || 'Could not create group. Please try again.',
        read: false,
      });
    },
  });

  const handleSeedDemo = async () => {
    try {
      await apiService.seedDemoData();
      addNotification({
        type: 'success',
        title: 'Demo Data Loaded',
        message: 'Sample groups and expenses have been created for you to explore.',
        read: false,
      });
      refetch();
    } catch (error) {
      addNotification({
        type: 'error',
        title: 'Error',
        message: 'Failed to load demo data. Please try again.',
        read: false,
      });
    }
  };

  const handleLogout = () => {
    logout();
    addNotification({
      type: 'info',
      title: 'Logged Out',
      message: 'You have been successfully logged out.',
      read: false,
    });
  };

  const handleGroupCreated = (group: any) => {
    createGroupMutation.mutate(group);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-error-600 mb-4">Error Loading Dashboard</h2>
          <p className="text-secondary-600 mb-4">Failed to load your groups.</p>
          <Button onClick={() => refetch()}>Try Again</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-2 border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
              <p className="text-lg text-gray-600">Welcome back, {user?.first_name}!</p>
            </div>
            <div className="flex items-center space-x-4">
              {/* User Info */}
              <div className="flex items-center space-x-3 bg-gray-100 rounded-lg px-4 py-2">
                <UserCircleIcon className="h-8 w-8 text-gray-600" />
                <div>
                  <p className="text-sm font-medium text-gray-900">{user?.first_name || user?.username}</p>
                  <p className="text-xs text-gray-500">{user?.email}</p>
                </div>
              </div>

              {/* Action Buttons */}
              <Button
                variant="outline"
                onClick={handleSeedDemo}
                className="px-4 py-2 text-sm font-semibold border-2 border-blue-600 text-blue-600 hover:bg-blue-50"
              >
                Load Demo Data
              </Button>
              <Button
                onClick={() => setIsCreatingGroup(true)}
                className="flex items-center space-x-2 px-4 py-2 text-sm font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
              >
                <PlusIcon className="h-4 w-4" />
                <span>Create Group</span>
              </Button>
              
              {/* Logout Button */}
              <Button
                variant="ghost"
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100"
              >
                <ArrowLeftOnRectangleIcon className="h-4 w-4" />
                <span>Logout</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!groups || groups.length === 0 ? (
        <div className="text-center py-16">
          <UserGroupIcon className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No groups yet</h3>
          <p className="text-lg text-gray-500 mb-8">
            Get started by creating a new group or loading demo data.
          </p>
            <div className="flex justify-center space-x-4">
              <Button 
                onClick={() => setIsCreatingGroup(true)}
                className="px-8 py-4 text-lg font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
              >
                Create Group
              </Button>
              <Button 
                variant="outline" 
                onClick={handleSeedDemo}
                className="px-8 py-4 text-lg font-semibold border-2 border-blue-600 text-blue-600 hover:bg-blue-50 rounded-lg"
              >
                Load Demo Data
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Groups</CardTitle>
                  <UserGroupIcon className="h-4 w-4 text-gray-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{groups.length}</div>
                  <p className="text-xs text-gray-600">
                    Active groups you're part of
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Expenses</CardTitle>
                  <CurrencyDollarIcon className="h-4 w-4 text-gray-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {groups.reduce((sum, group) => sum + (group.total_expenses || 0), 0)}
                  </div>
                  <p className="text-xs text-gray-600">
                    Across all groups
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Pending Settlements</CardTitle>
                  <ChartBarIcon className="h-4 w-4 text-gray-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {groups.reduce((sum, group) => sum + (group.pending_settlements || 0), 0)}
                  </div>
                  <p className="text-xs text-gray-600">
                    Awaiting settlement
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Groups List */}
            <div className="space-y-4">
              <h2 className="text-lg font-semibold text-gray-900">Your Groups</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {groups.map((group) => (
                  <Card 
                    key={group.id} 
                    className="hover:shadow-md transition-shadow cursor-pointer"
                    onClick={() => navigate(`/group/${group.id}`)}
                  >
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div>
                          <CardTitle className="text-lg">{group.name}</CardTitle>
                          <CardDescription className="mt-1">
                            {group.description}
                          </CardDescription>
                        </div>
                        <Badge variant="secondary">
                          {group.group_type}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-600">Members</span>
                          <span className="font-medium">{group.member_count || 0}</span>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-600">Currency</span>
                          <span className="font-medium">{group.currency}</span>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-600">Status</span>
                          <Badge variant={group.is_active ? 'success' : 'error'}>
                            {group.is_active ? 'Active' : 'Inactive'}
                          </Badge>
                        </div>
                      </div>
                      <Button 
                        className="w-full mt-4" 
                        variant="outline"
                        onClick={() => navigate(`/group/${group.id}`)}
                      >
                        View Group
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Group Creation Modal */}
      <GroupCreateModal
        isOpen={isCreatingGroup}
        onClose={() => setIsCreatingGroup(false)}
        onSuccess={handleGroupCreated}
      />
    </div>
  );
}