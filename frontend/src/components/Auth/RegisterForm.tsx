import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { Button } from '../../ui/Button';
import { Input } from '../../ui/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/Card';
import { useAuthStore } from '../../stores/authStore';

const registerSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  password_confirm: z.string(),
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  phone: z.string().optional(),
}).refine((data) => data.password === data.password_confirm, {
  message: "Passwords don't match",
  path: ["password_confirm"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

interface RegisterFormProps {
  onSuccess?: () => void;
  onSwitchToLogin?: () => void;
}

export function RegisterForm({ onSuccess, onSwitchToLogin }: RegisterFormProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const { register: registerUser, isLoading, error, clearError } = useAuthStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      clearError();
      const { password_confirm, ...userData } = data;
      await registerUser(userData);
      onSuccess?.();
    } catch (error) {
      // Error is handled by the store
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl font-bold">Create account</CardTitle>
        <CardDescription>
          Join Shared Finance to manage your group expenses
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {error && (
            <div className="p-3 text-sm text-error-600 bg-error-50 border border-error-200 rounded-md">
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <Input
              {...register('first_name')}
              label="First Name"
              placeholder="John"
              error={errors.first_name?.message}
              autoComplete="given-name"
            />
            <Input
              {...register('last_name')}
              label="Last Name"
              placeholder="Doe"
              error={errors.last_name?.message}
              autoComplete="family-name"
            />
          </div>

          <Input
            {...register('username')}
            label="Username"
            placeholder="johndoe"
            error={errors.username?.message}
            autoComplete="username"
          />

          <Input
            {...register('email')}
            type="email"
            label="Email"
            placeholder="john@example.com"
            error={errors.email?.message}
            autoComplete="email"
          />

          <Input
            {...register('phone')}
            type="tel"
            label="Phone (Optional)"
            placeholder="+1 (555) 123-4567"
            error={errors.phone?.message}
            autoComplete="tel"
          />

          <div className="relative">
            <Input
              {...register('password')}
              type={showPassword ? 'text' : 'password'}
              label="Password"
              placeholder="Create a strong password"
              error={errors.password?.message}
              autoComplete="new-password"
            />
            <button
              type="button"
              className="absolute right-3 top-8 text-secondary-400 hover:text-secondary-600"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <EyeSlashIcon className="h-4 w-4" />
              ) : (
                <EyeIcon className="h-4 w-4" />
              )}
            </button>
          </div>

          <div className="relative">
            <Input
              {...register('password_confirm')}
              type={showConfirmPassword ? 'text' : 'password'}
              label="Confirm Password"
              placeholder="Confirm your password"
              error={errors.password_confirm?.message}
              autoComplete="new-password"
            />
            <button
              type="button"
              className="absolute right-3 top-8 text-secondary-400 hover:text-secondary-600"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? (
                <EyeSlashIcon className="h-4 w-4" />
              ) : (
                <EyeIcon className="h-4 w-4" />
              )}
            </button>
          </div>

          <Button
            type="submit"
            className="w-full"
            loading={isLoading}
            disabled={isLoading}
          >
            Create Account
          </Button>

          {onSwitchToLogin && (
            <div className="text-center text-sm text-secondary-600">
              Already have an account?{' '}
              <button
                type="button"
                onClick={onSwitchToLogin}
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                Sign in
              </button>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}