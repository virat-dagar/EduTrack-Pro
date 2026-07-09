import { LogIn } from "lucide-react";
import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { useAuth } from "../../hooks/useAuth";
import { getDashboardPath } from "../../utils/helpers";
import { validateLogin } from "../../utils/validators";

export default function LoginPage() {
  const [values, setValues] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const nextErrors = validateLogin(values);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;
    setIsSubmitting(true);
    try {
      const user = await login(values);
      toast.success("Login successful.");
      navigate(location.state?.from?.pathname || getDashboardPath(user), { replace: true });
    } catch (error) {
      toast.error(error.message || "Invalid email or password.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="auth-card">
      <div className="auth-card-header">
        <h2>Sign in</h2>
        <p>Use your teacher or student account.</p>
      </div>
      <form className="form-stack" onSubmit={handleSubmit}>
        <Input
          label="Email"
          name="email"
          type="email"
          autoComplete="email"
          value={values.email}
          error={errors.email}
          onChange={(event) => setValues({ ...values, email: event.target.value })}
        />
        <Input
          label="Password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={values.password}
          error={errors.password}
          onChange={(event) => setValues({ ...values, password: event.target.value })}
        />
        <Button type="submit" icon={LogIn} isLoading={isSubmitting}>
          Sign in
        </Button>
      </form>
    </Card>
  );
}
