import { Link } from "react-router-dom";
import { Card } from "../../components/common/Card";

export default function ForbiddenPage() {
  return (
    <Card className="error-page">
      <h1>Forbidden</h1>
      <p>You do not have permission to access this page.</p>
      <Link className="btn btn-primary btn-md" to="/login">Return to sign in</Link>
    </Card>
  );
}
