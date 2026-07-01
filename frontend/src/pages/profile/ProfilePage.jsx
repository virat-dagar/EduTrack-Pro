import { Card } from "../../components/common/Card";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { studentService } from "../../services/studentService";
import { ROLES } from "../../utils/constants";

export default function ProfilePage() {
  const { user } = useAuth();
  const profile = useApi(() => (user?.role === ROLES.STUDENT ? studentService.me() : Promise.resolve({ data: user })), [user?.id]);

  if (profile.isLoading) return <LoadingState label="Loading profile" />;
  if (profile.error) return <ErrorState message={profile.error.message} />;

  return (
    <>
      <PageHeader title="Profile" description="Account and academic profile information." />
      <Card>
        <dl className="detail-grid">
          {Object.entries(profile.data || {}).map(([key, value]) => (
            <div key={key}>
              <dt>{key.replaceAll("_", " ")}</dt>
              <dd>{String(value ?? "-")}</dd>
            </div>
          ))}
        </dl>
      </Card>
    </>
  );
}
