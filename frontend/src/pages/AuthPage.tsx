import { useState } from 'react';
import { LoginForm } from '../components/Auth/LoginForm';
import { RegisterForm } from '../components/Auth/RegisterForm';

export function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  const handleSuccess = () => {
    // Redirect will be handled by the router
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Shared Finance OS
          </h1>
          <p className="text-gray-600">
            Smart expense splitting for modern groups
          </p>
        </div>

        {isLogin ? (
          <LoginForm
            onSuccess={handleSuccess}
            onSwitchToRegister={() => setIsLogin(false)}
          />
        ) : (
          <RegisterForm
            onSuccess={handleSuccess}
            onSwitchToLogin={() => setIsLogin(true)}
          />
        )}

        <div className="text-center text-sm text-gray-500">
          <p>Demo Mode: Use any credentials to explore the app</p>
        </div>
      </div>
    </div>
  );
}