import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from '../ui/Modal';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { apiService } from '../services/api';

const groupTypes = [
  { value: 'roommates', label: 'Roommates', description: 'Share expenses with housemates' },
  { value: 'society', label: 'Society Committee', description: 'Manage society expenses' },
  { value: 'club', label: 'Club/Organization', description: 'Club or organization expenses' },
  { value: 'family', label: 'Family', description: 'Family expense sharing' },
  { value: 'friends', label: 'Friends', description: 'Split bills with friends' },
  { value: 'business', label: 'Business', description: 'Business expense management' },
  { value: 'other', label: 'Other', description: 'Other type of group' },
];

const currencies = [
  { value: 'INR', label: 'Indian Rupee (₹)' },
  { value: 'USD', label: 'US Dollar ($)' },
  { value: 'EUR', label: 'Euro (€)' },
  { value: 'GBP', label: 'British Pound (£)' },
];

const billingCycles = [
  { value: 'monthly', label: 'Monthly' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'daily', label: 'Daily' },
  { value: 'on_demand', label: 'On Demand' },
];

const schema = z.object({
  name: z.string().min(1, 'Group name is required').max(200, 'Name too long'),
  description: z.string().max(500, 'Description too long').optional(),
  group_type: z.string().min(1, 'Group type is required'),
  currency: z.string().default('INR'),
  billing_cycle: z.string().default('monthly'),
  gst_mode: z.boolean().default(false),
});

type FormData = z.infer<typeof schema>;

interface GroupCreateModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (group: any) => void;
}

export function GroupCreateModal({ isOpen, onClose, onSuccess }: GroupCreateModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedType, setSelectedType] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch,
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      currency: 'INR',
      billing_cycle: 'monthly',
      gst_mode: false,
    },
  });

  const gstMode = watch('gst_mode');

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true);
    try {
      const group = await apiService.createGroup(data);
      onSuccess(group);
      reset();
      onClose();
    } catch (error) {
      console.error('Error creating group:', error);
      // Error handling is done in the parent component
      throw error;
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    reset();
    setSelectedType('');
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} size="lg" title="Create New Group">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Group Name */}
        <div>
          <Input
            label="Group Name"
            placeholder="Enter group name"
            {...register('name')}
            error={errors.name?.message}
            required
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description (Optional)
          </label>
          <textarea
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
            placeholder="Describe your group..."
            {...register('description')}
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
          )}
        </div>

        {/* Group Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Group Type
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {groupTypes.map((type) => (
              <Card
                key={type.value}
                className={`cursor-pointer transition-all ${
                  selectedType === type.value
                    ? 'ring-2 ring-blue-500 bg-blue-50'
                    : 'hover:shadow-md'
                }`}
                onClick={() => {
                  setSelectedType(type.value);
                  setValue('group_type', type.value);
                }}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">{type.label}</h3>
                      <p className="text-sm text-gray-500 mt-1">{type.description}</p>
                    </div>
                    {selectedType === type.value && (
                      <Badge variant="default">Selected</Badge>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          {errors.group_type && (
            <p className="mt-1 text-sm text-red-600">{errors.group_type.message}</p>
          )}
        </div>

        {/* Currency and Billing Cycle */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Currency
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register('currency')}
            >
              {currencies.map((currency) => (
                <option key={currency.value} value={currency.value}>
                  {currency.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Billing Cycle
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register('billing_cycle')}
            >
              {billingCycles.map((cycle) => (
                <option key={cycle.value} value={cycle.value}>
                  {cycle.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* GST Mode */}
        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="gst_mode"
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            {...register('gst_mode')}
          />
          <label htmlFor="gst_mode" className="text-sm font-medium text-gray-700">
            Enable GST mode for this group
          </label>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <Button
            type="button"
            variant="outline"
            onClick={handleClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={isSubmitting || !selectedType}
            className="px-6"
          >
            {isSubmitting ? 'Creating...' : 'Create Group'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}