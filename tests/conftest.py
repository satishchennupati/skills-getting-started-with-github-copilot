import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for inter-school matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Volleyball Club": {
            "description": "Recreational and competitive volleyball",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["laura@mergington.edu", "alex@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions and acting techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture workshops",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ryan@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific experiments and research projects",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 22,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        }
    }
    
    # Clear and repopulate the activities dict
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    
    yield
