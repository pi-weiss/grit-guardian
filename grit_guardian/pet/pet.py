from enum import Enum
from typing import List, Dict


class PetMood(Enum):
    """Enum representing different mood states of the pet."""

    ECSTATIC = "ecstatic"
    HAPPY = "happy"
    CONTENT = "content"
    SAD = "sad"
    WORRIED = "worried"


class Pet:
    """Represents the Grit Guardian pet that reflects user's habit performance."""

    def __init__(self, name: str = "Guardian", species: str = "Dragon"):
        """Initializes a new pet.

        Args:
        name: The pet's name (default: "Guardian")
        species: The pet's species (default: "Dragon")
        """
        self.name = name
        self.specias = species
        self.current_mood = PetMood.CONTENT

    def calculate_mood(self, habits_data: List[Dict]) -> PetMood:
        """Calculates mood based on habit completion data.

        Args:
            habits_data: List of dictionaries containing habit analytics
                        Each dict should have 'completion_rate' and 'current_streak' keys

        Returns:
            PetMood enum value representing the calculated mood
        """
        pass

    def get_ascii_art(self) -> str:
        """Returns ASCII art based on current mood.

        Returns:
            String containing ASCII art representation of the pet
        """
        pass

    def get_mood_message(self) -> str:
        """Gets a message based on the pet's current mood.

        Returns:
            String with mood-appropriate message
        """
        pass
