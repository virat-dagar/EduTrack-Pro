import { Link } from "react-router-dom";
import { Card } from "../../components/common/Card";

export default function NotFoundPage() {
  return (
    <Card className="error-page">
      <h1>Page Not Found</h1>
      <p>The page you requested does not exist.</p>
      <Link className="btn btn-primary btn-md" to="/login">Go home</Link>
    </Card>
  );
}
