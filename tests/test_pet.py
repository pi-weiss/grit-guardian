import pytest
from grit_guardian.pet.pet import Pet, PetMood


class TestPetMood:
    """Tests the PetMood enum."""

    def test_mood_values(self):
        """Test that all mood values are properly defined."""
        assert PetMood.ECSTATIC.value == "ecstatic"
        assert PetMood.HAPPY.value == "happy"
        assert PetMood.CONTENT.value == "content"
        assert PetMood.SAD.value == "sad"
        assert PetMood.WORRIED.value == "worried"


class TestPet:
    """Tests the Pet class."""

    def test_pet_initialization(self):
        """Tests pet initialization with default values."""
        pet = Pet()
        assert pet.name == "Guardian"
        assert pet.species == "Dragon"
        assert pet.current_mood == PetMood.CONTENT

    def test_pet_custom_initialization(self):
        """Tests pet initialization with custom values."""
        pet = Pet(name="Adelheid", species="Phoenix")
        assert pet.name == "Adelheid"
        assert pet.species == "Phoenix"
        assert pet.current_mood == PetMood.CONTENT

    def test_calculate_mood_no_habits(self):
        """Tests mood calculation with no habits."""
        pet = Pet()
        mood = pet.calculate_mood([])
        assert mood == PetMood.WORRIED
        assert pet.current_mood == PetMood.WORRIED

    def test_calculate_mood_ecstatic(self):
        """Tests mood calculation for ecstatic mood."""
        pet = Pet()
        habits_data = [
            {"completion_rate": 95.0, "current_streak": 10},
            {"completion_rate": 92.0, "current_streak": 5},
            {"completion_rate": 100.0, "current_streak": 15},
        ]
        mood = pet.calculate_mood(habits_data)
        assert mood == PetMood.ECSTATIC
        assert pet.current_mood == PetMood.ECSTATIC

    def test_calculate_mood_happy(self):
        """Tests mood calculation for happy mood."""
        pet = Pet()
        habits_data = [
            {"completion_rate": 75.0, "current_streak": 5},
            {"completion_rate": 80.0, "current_streak": 0},
            {"completion_rate": 70.0, "current_streak": 3},
        ]
        mood = pet.calculate_mood(habits_data)
        assert mood == PetMood.HAPPY
        assert pet.current_mood == PetMood.HAPPY

    def test_calculate_mood_content(self):
        """Tests mood calculation for content mood."""
        pet = Pet()
        habits_data = [
            {"completion_rate": 60.0, "current_streak": 2},
            {"completion_rate": 55.0, "current_streak": 0},
            {"completion_rate": 50.0, "current_streak": 1},
        ]
        mood = pet.calculate_mood(habits_data)
        assert mood == PetMood.CONTENT
        assert pet.current_mood == PetMood.CONTENT

    def test_calculate_mood_sad(self):
        """Tests mood calculation for sad mood."""
        pet = Pet()
        habits_data = [
            {"completion_rate": 35.0, "current_streak": 0},
            {"completion_rate": 40.0, "current_streak": 0},
            {"completion_rate": 30.0, "current_streak": 1},
        ]
        mood = pet.calculate_mood(habits_data)
        assert mood == PetMood.SAD
        assert pet.current_mood == PetMood.SAD

    def test_calculate_mood_worried(self):
        """Tests mood calculation for worried mood."""
        pet = Pet()
        habits_data = [
            {"completion_rate": 20.0, "current_streak": 0},
            {"completion_rate": 15.0, "current_streak": 0},
            {"completion_rate": 25.0, "current_streak": 0},
        ]
        mood = pet.calculate_mood(habits_data)
        assert mood == PetMood.WORRIED
        assert pet.current_mood == PetMood.WORRIED

    def test_calculate_mood_edge_cases(self):
        """Tests mood calculation edge cases."""
        pet = Pet()

        # Exactly 90% with all streaks for ecstatic
        habits_data = [
            {"completion_rate": 90.0, "current_streak": 1},
            {"completion_rate": 90.0, "current_streak": 2},
        ]
        mood = pet.calculate_mood(habits_data)
        assert mood == PetMood.ECSTATIC

        # High completion but not all streaks active - should be happy
        habits_data = [
            {"completion_rate": 95.0, "current_streak": 10},
            {"completion_rate": 95.0, "current_streak": 0},
        ]
        mood = pet.calculate_mood(habits_data)
        assert mood == PetMood.HAPPY

    def test_get_ascii_art(self):
        """Tests ASCII art retrieval for each mood."""
        pet = Pet()

        # Test each mood's ASCII art
        for mood in PetMood:
            pet.current_mood = mood
            art = pet.get_ascii_art()
            assert isinstance(art, str)
            assert len(art) > 0
            assert "/\\" in art  # Check for dragon ears
            assert "___" in art  # Check for mouth

    def test_get_mood_message(self):
        """Tests mood message retrieval."""
        pet = Pet(name="TestPet")

        # Test each mood's message
        mood_keywords = {
            PetMood.ECSTATIC: "thrilled",
            PetMood.HAPPY: "happy",
            PetMood.CONTENT: "content",
            PetMood.SAD: "sad",
            PetMood.WORRIED: "worried",
        }

        for mood, keyword in mood_keywords.items():
            pet.current_mood = mood
            message = pet.get_mood_message()
            assert isinstance(message, str)
            assert pet.name in message
            assert keyword in message.lower()

    def test_str_representation(self):
        """Tests string representation of pet."""
        pet = Pet(name="Wolfgang", species="Griffin")
        pet.current_mood = PetMood.HAPPY

        str_repr = str(pet)
        assert "Griffin" in str_repr
        assert "Wolfgang" in str_repr
        assert "happy" in str_repr

    def test_mood_persistence(self):
        """Tests that mood persists between calculations."""
        pet = Pet()

        # Set to happy mood
        habits_data = [{"completion_rate": 75.0, "current_streak": 5}]
        pet.calculate_mood(habits_data)
        assert pet.current_mood == PetMood.HAPPY

        # Mood should still be happy before next calculation
        assert pet.current_mood == PetMood.HAPPY

        # Update to sad mood
        habits_data = [{"completion_rate": 35.0, "current_streak": 0}]
        pet.calculate_mood(habits_data)
        assert pet.current_mood == PetMood.SAD
