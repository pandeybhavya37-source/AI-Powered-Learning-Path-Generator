from learning_path_generator import LearningPathGenerator


def test_generator_excludes_existing_skills() -> None:
    generator = LearningPathGenerator(
        goals=["become data scientist"],
        current_skills=["python"],
        recommended_technologies=[],
    )

    result = generator.generate()
    names = [module["name"].lower() for module in result["learning_modules"]]

    assert all("python" not in name for name in names)
    assert result["total_estimated_hours"] > 0


def test_generator_includes_fallback_for_unknown_technology() -> None:
    generator = LearningPathGenerator(
        goals=[],
        current_skills=[],
        recommended_technologies=["langchain"],
    )

    result = generator.generate()
    assert result["learning_modules"][0]["name"] == "Langchain Essentials"
