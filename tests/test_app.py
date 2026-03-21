import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Should return all available activities"""
        # Arrange
        expected_activity_count = 9
        expected_activities = {"Chess Club", "Programming Class", "Gym Class"}
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == expected_activity_count
        assert expected_activities.issubset(data.keys())

    def test_get_activities_contains_required_fields(self, client):
        """Each activity should have required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity '{activity_name}' missing required fields"

    def test_get_activities_participants_is_list(self, client):
        """Participants should be a list for each activity"""
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Should successfully sign up a student"""
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert new_email in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Signing up should add participant to activity"""
        # Arrange
        activity_name = "Chess Club"
        new_email = "test@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert new_email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """Should return 404 for non-existent activity"""
        # Arrange
        fake_activity = "Nonexistent Club"
        test_email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup?email={test_email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student_returns_400(self, client):
        """Should return 400 if student already signed up"""
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={existing_email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_multiple_students_same_activity(self, client):
        """Should allow multiple different students to sign up for same activity"""
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup?email={email1}"
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup?email={email2}"
        )
        activities_response = client.get("/activities")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        participants = activities_response.json()[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants

    def test_signup_same_student_different_activities(self, client):
        """Should allow same student to sign up for different activities"""
        # Arrange
        test_email = "multiactivity@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        response1 = client.post(f"/activities/{activity1}/signup?email={test_email}")
        response2 = client.post(f"/activities/{activity2}/signup?email={test_email}")
        activities_response = client.get("/activities")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities = activities_response.json()
        assert test_email in activities[activity1]["participants"]
        assert test_email in activities[activity2]["participants"]


class TestUnregisterFromActivity:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client):
        """Should successfully unregister a student"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]

    def test_unregister_removes_participant_from_activity(self, client):
        """Unregistering should remove participant from activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/unregister?email={email}")
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Should return 404 for non-existent activity"""
        # Arrange
        fake_activity = "Nonexistent Club"
        test_email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{fake_activity}/unregister?email={test_email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_not_signed_up_student_returns_400(self, client):
        """Should return 400 if student not signed up"""
        # Arrange
        activity_name = "Chess Club"
        not_signed_up_email = "notasignup@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={not_signed_up_email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_then_resign_up(self, client):
        """Should allow student to resign up after unregistering"""
        # Arrange
        activity_name = "Chess Club"
        test_email = "test@mergington.edu"
        
        # Act - Sign up
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        response_after_signup = client.get("/activities")
        
        # Act - Unregister
        client.post(f"/activities/{activity_name}/unregister?email={test_email}")
        response_after_unregister = client.get("/activities")
        
        # Act - Sign up again
        signup_again_response = client.post(
            f"/activities/{activity_name}/signup?email={test_email}"
        )
        response_final = client.get("/activities")
        
        # Assert
        activities_after_signup = response_after_signup.json()
        activities_after_unregister = response_after_unregister.json()
        activities_final = response_final.json()
        
        assert test_email in activities_after_signup[activity_name]["participants"]
        assert test_email not in activities_after_unregister[activity_name]["participants"]
        assert test_email in activities_final[activity_name]["participants"]
        assert signup_again_response.status_code == 200

    def test_unregister_does_not_affect_other_activities(self, client):
        """Unregistering from one activity should not affect others"""
        # Arrange
        test_email = "student@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act - Sign up for both
        client.post(f"/activities/{activity1}/signup?email={test_email}")
        client.post(f"/activities/{activity2}/signup?email={test_email}")
        
        # Act - Unregister from activity1
        client.post(f"/activities/{activity1}/unregister?email={test_email}")
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert test_email not in activities[activity1]["participants"]
        assert test_email in activities[activity2]["participants"]
