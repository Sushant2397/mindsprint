import { useAppStore } from '../stores/appStore';
import { XMarkIcon, CheckCircleIcon, ExclamationTriangleIcon, InformationCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { Button } from '../ui/Button';
import { cn } from '../utils/cn';

const iconMap = {
  success: CheckCircleIcon,
  error: XCircleIcon,
  warning: ExclamationTriangleIcon,
  info: InformationCircleIcon,
};

export function NotificationContainer() {
  const { notifications, removeNotification } = useAppStore();

  if (notifications.length === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map((notification) => {
        const Icon = iconMap[notification.type];
        
        return (
          <div
            key={notification.id}
            className={cn(
              'flex items-start p-4 rounded-lg shadow-lg max-w-sm bg-white border-l-4',
              {
                'border-success-500': notification.type === 'success',
                'border-error-500': notification.type === 'error',
                'border-warning-500': notification.type === 'warning',
                'border-primary-500': notification.type === 'info',
              }
            )}
          >
            <Icon
              className={cn('h-5 w-5 mt-0.5 mr-3', {
                'text-success-500': notification.type === 'success',
                'text-error-500': notification.type === 'error',
                'text-warning-500': notification.type === 'warning',
                'text-primary-500': notification.type === 'info',
              })}
            />
            
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-secondary-900">
                {notification.title}
              </p>
              <p className="text-sm text-secondary-600 mt-1">
                {notification.message}
              </p>
            </div>
            
            <Button
              variant="ghost"
              size="icon"
              className="h-6 w-6 p-0 ml-2"
              onClick={() => removeNotification(notification.id)}
            >
              <XMarkIcon className="h-4 w-4" />
            </Button>
          </div>
        );
      })}
    </div>
  );
}