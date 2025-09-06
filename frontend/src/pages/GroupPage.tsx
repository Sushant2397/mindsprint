import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeftIcon } from '@heroicons/react/24/outline';
import { Button } from '../ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/Card';
import { apiService } from '../services/api';
import { LoadingSpinner } from '../components/LoadingSpinner';

export function GroupPage() {
  const { groupId } = useParams<{ groupId: string }>();

  const { data: group, isLoading, error } = useQuery({
    queryKey: ['group', groupId],
    queryFn: () => apiService.getGroup(Number(groupId)),
    enabled: !!groupId,
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error || !group) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-error-600 mb-4">Group Not Found</h2>
          <p className="text-secondary-600 mb-4">The group you're looking for doesn't exist.</p>
          <Button onClick={() => window.history.back()}>
            <ArrowLeftIcon className="h-4 w-4 mr-2" />
            Go Back
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center h-16">
            <Button
              variant="ghost"
              onClick={() => window.history.back()}
              className="mr-4"
            >
              <ArrowLeftIcon className="h-4 w-4" />
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{group.name}</h1>
              <p className="text-gray-600">{group.description}</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Group Info */}
          <Card>
            <CardHeader>
              <CardTitle>Group Information</CardTitle>
              <CardDescription>Basic details about this group</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-secondary-600">Group Type</label>
                  <p className="text-sm text-secondary-900 capitalize">{group.group_type}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-600">Currency</label>
                  <p className="text-sm text-secondary-900">{group.currency}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-600">Billing Cycle</label>
                  <p className="text-sm text-secondary-900 capitalize">{group.billing_cycle}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-600">GST Mode</label>
                  <p className="text-sm text-secondary-900">{group.gst_mode ? 'Enabled' : 'Disabled'}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-600">Members</label>
                  <p className="text-sm text-secondary-900">{group.member_count || 0}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-secondary-600">Status</label>
                  <p className="text-sm text-secondary-900">{group.is_active ? 'Active' : 'Inactive'}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Placeholder for other sections */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Recent Expenses</CardTitle>
                <CardDescription>Latest expenses in this group</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-secondary-500 text-sm">No expenses yet. Add some expenses to get started!</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Settlement Status</CardTitle>
                <CardDescription>Current settlement information</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-secondary-500 text-sm">No pending settlements. All expenses are settled!</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}